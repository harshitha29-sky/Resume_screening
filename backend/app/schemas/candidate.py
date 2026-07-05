from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ScoreBreakdown(BaseModel):
    overall_score: float
    nlp_similarity: float
    skill_match: float
    experience_match: float
    education_match: float
    matching_skills: list[str]
    missing_skills: list[str]
    recommendation: str


class CandidateListItem(BaseModel):
    id: int
    full_name: str
    email: str | None
    phone: str | None
    skills: list[str]
    education: list[str]
    total_years_experience: float
    overall_score: float | None = None
    recommendation: str | None = None


class CandidateDetail(CandidateListItem):
    experience: list[str]
    projects: list[str]
    certifications: list[str]
    raw_text: str | None
    resume_url: str | None
    score_breakdown: ScoreBreakdown | None
    created_at: datetime


class RankingItem(BaseModel):
    rank: int
    candidate_id: int
    candidate_name: str
    overall_score: float
    skill_match: float
    experience_match: float
    education_match: float
    recommendation: str


class CandidateSearchParams(BaseModel):
    search: str | None = None
    min_score: float | None = None
    max_score: float | None = None
    sort_by: str = "score"
    sort_order: str = "desc"
    page: int = 1
    page_size: int = 10


class PaginatedCandidates(BaseModel):
    items: list[CandidateListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
