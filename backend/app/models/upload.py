from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=True)
    upload_type: Mapped[str] = mapped_column(String(50), nullable=False, default="resume")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="uploaded")
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=True)
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    candidate = relationship("Candidate", back_populates="uploads")
    job_description = relationship("JobDescription")
    user = relationship("User", back_populates="uploads")
