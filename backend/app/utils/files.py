from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_upload_file(file: UploadFile) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {suffix or 'unknown'}",
        )
    return suffix


def unique_export_name(prefix: str, suffix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}{suffix}"
