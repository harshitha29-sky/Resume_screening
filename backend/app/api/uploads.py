from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.deps import get_db
from app.models.user import User
from app.schemas.upload import JobDescriptionUploadResponse, ResumeUploadResponse, UploadRead
from app.services.uploads import UploadService
from app.utils.json_store import loads

router = APIRouter(prefix="/upload", tags=["uploads"])


def get_upload_service() -> UploadService:
    return UploadService()


@router.post("/resumes", response_model=ResumeUploadResponse)
async def upload_resumes(
    files: Annotated[list[UploadFile], File(...)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UploadService, Depends(get_upload_service)],
) -> ResumeUploadResponse:
    uploads = await service.upload_resumes(db, files, current_user)
    return ResumeUploadResponse(
        uploaded_count=len(uploads),
        uploads=[UploadRead.model_validate(upload) for upload in uploads],
    )


@router.post("/job-description", response_model=JobDescriptionUploadResponse)
async def upload_job_description(
    file: Annotated[UploadFile, File(...)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UploadService, Depends(get_upload_service)],
) -> JobDescriptionUploadResponse:
    job, upload = await service.upload_job_description(db, file, current_user)
    return JobDescriptionUploadResponse(
        job_description_id=job.id,
        filename=upload.filename,
        file_path=upload.file_path,
        required_skills=loads(job.required_skills),
        preferred_skills=loads(job.preferred_skills),
        required_experience=job.required_experience,
        education=loads(job.education),
        keywords=loads(job.keywords),
    )
