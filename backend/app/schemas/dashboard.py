from pydantic import BaseModel


class DistributionItem(BaseModel):
    label: str
    count: int


class DashboardStats(BaseModel):
    total_candidates: int
    total_resumes: int
    average_score: float
    highest_score: float
    lowest_score: float
    top_candidate: str | None
    skill_distribution: list[DistributionItem]
    experience_distribution: list[DistributionItem]
    score_distribution: list[DistributionItem]
