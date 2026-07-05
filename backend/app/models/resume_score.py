from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Float, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class ResumeScore(Base):
    __tablename__ = "resume_scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    job_description_id: Mapped[int] = mapped_column(
        ForeignKey("job_descriptions.id"),
        nullable=False,
    )
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True)
    nlp_similarity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    skill_match: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    experience_match: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    education_match: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    matching_skills: Mapped[str] = mapped_column(Text, nullable=True)
    missing_skills: Mapped[str] = mapped_column(Text, nullable=True)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    candidate = relationship("Candidate", back_populates="resume_scores")
    job_description = relationship("JobDescription", back_populates="resume_scores")
