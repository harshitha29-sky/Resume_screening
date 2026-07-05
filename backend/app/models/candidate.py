from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    skills: Mapped[str] = mapped_column(Text, nullable=True)
    education: Mapped[str] = mapped_column(Text, nullable=True)
    experience: Mapped[str] = mapped_column(Text, nullable=True)
    projects: Mapped[str] = mapped_column(Text, nullable=True)
    certifications: Mapped[str] = mapped_column(Text, nullable=True)
    total_years_experience: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    uploads = relationship("Upload", back_populates="candidate")
    resume_scores = relationship("ResumeScore", back_populates="candidate")
