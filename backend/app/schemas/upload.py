from pydantic import BaseModel, ConfigDict


class UploadRead(BaseModel):
    id: int
    filename: str
    file_path: str
    content_type: str | None
    upload_type: str
    status: str
    file_size: int
    candidate_id: int | None = None
    job_description_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ResumeUploadResponse(BaseModel):
    uploaded_count: int
    uploads: list[UploadRead]


class JobDescriptionUploadResponse(BaseModel):
    job_description_id: int
    filename: str
    file_path: str
    required_skills: list[str]
    preferred_skills: list[str]
    required_experience: float
    education: list[str]
    keywords: list[str]
