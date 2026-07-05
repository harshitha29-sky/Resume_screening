from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.models.upload import Upload
from app.models.user import User
from app.services.parser import JobDescriptionParser, ResumeParser
from app.services.scoring import ResumeMatcher
from app.utils.config import settings
from app.utils.files import ensure_directory, validate_upload_file
from app.utils.json_store import dumps


class UploadService:
    def __init__(self) -> None:
        self.resume_parser = ResumeParser()
        self.job_parser = JobDescriptionParser()
        self.matcher = ResumeMatcher()

    async def upload_resumes(self, db: Session, files: list[UploadFile], user: User) -> list[Upload]:
        if len(files) > settings.max_resume_upload_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum {settings.max_resume_upload_count} resumes are allowed per upload",
            )

        upload_dir = self._upload_dir("resumes")
        uploads: list[Upload] = []
        seen_names: set[str] = set()

        for file in files:
            filename = self._clean_filename(file.filename)
            if filename in seen_names or self._filename_exists(db, filename, "resume", upload_dir):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Duplicate filename rejected: {filename}",
                )
            seen_names.add(filename)
            validate_upload_file(file)
            path, size = await self._save_upload(file, upload_dir / filename)
            parsed = self.resume_parser.parse_file(str(path))
            candidate = Candidate(
                full_name=parsed.candidate_name,
                email=parsed.email,
                phone=parsed.phone,
                skills=dumps(parsed.skills),
                education=dumps(parsed.education),
                experience=dumps(parsed.experience),
                projects=dumps(parsed.projects),
                certifications=dumps(parsed.certifications),
                total_years_experience=parsed.total_years_experience,
                raw_text=parsed.raw_text,
            )
            db.add(candidate)
            db.flush()

            upload = Upload(
                filename=filename,
                file_path=str(path),
                content_type=file.content_type,
                upload_type="resume",
                status="parsed",
                file_size=size,
                candidate_id=candidate.id,
                user_id=user.id,
            )
            db.add(upload)
            uploads.append(upload)

            active_job = db.scalar(select(JobDescription).where(JobDescription.is_active.is_(True)))
            if active_job is not None:
                self.matcher.score_candidate(db, candidate, active_job)

        db.commit()
        for upload in uploads:
            db.refresh(upload)
        return uploads

    async def upload_job_description(self, db: Session, file: UploadFile, user: User) -> tuple[JobDescription, Upload]:
        filename = self._clean_filename(file.filename)
        validate_upload_file(file)
        upload_dir = self._upload_dir("job_description")
        if self._filename_exists(db, filename, "job_description", upload_dir):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Duplicate filename rejected: {filename}",
            )

        path, size = await self._save_upload(file, upload_dir / filename)
        parsed = self.job_parser.parse_file(str(path))

        db.execute(update(JobDescription).values(is_active=False))
        job = JobDescription(
            title=parsed.title,
            description=parsed.description,
            file_path=str(path),
            is_active=True,
            required_skills=dumps(parsed.required_skills),
            preferred_skills=dumps(parsed.preferred_skills),
            required_experience=parsed.required_experience,
            education=dumps(parsed.education),
            keywords=dumps(parsed.keywords),
            owner_id=user.id,
        )
        db.add(job)
        db.flush()

        upload = Upload(
            filename=filename,
            file_path=str(path),
            content_type=file.content_type,
            upload_type="job_description",
            status="parsed",
            file_size=size,
            job_description_id=job.id,
            user_id=user.id,
        )
        db.add(upload)
        db.commit()
        db.refresh(job)
        db.refresh(upload)
        self.matcher.score_all_for_active_job(db)
        return job, upload

    def _upload_dir(self, folder: str) -> Path:
        return ensure_directory(Path(settings.upload_root) / folder)

    def _clean_filename(self, filename: str | None) -> str:
        cleaned = Path(filename or "upload.txt").name
        if not cleaned:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required")
        return cleaned

    def _filename_exists(self, db: Session, filename: str, upload_type: str, upload_dir: Path) -> bool:
        database_match = db.scalar(
            select(Upload).where(Upload.filename == filename, Upload.upload_type == upload_type)
        )
        return database_match is not None or (upload_dir / filename).exists()

    async def _save_upload(self, file: UploadFile, destination: Path) -> tuple[Path, int]:
        max_size = settings.max_upload_size_mb * 1024 * 1024
        size = 0
        with destination.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > max_size:
                    buffer.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds {settings.max_upload_size_mb} MB limit",
                    )
                buffer.write(chunk)
        await file.close()
        return destination, size
