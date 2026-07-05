from collections import Counter
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.resume_score import ResumeScore
from app.models.upload import Upload
from app.schemas.dashboard import DashboardStats, DistributionItem
from app.utils.json_store import loads


def get_dashboard_stats(db: Session) -> DashboardStats:
    candidates = db.scalars(select(Candidate)).all()
    resume_uploads = db.scalars(select(Upload).where(Upload.upload_type == "resume")).all()
    scores = db.scalars(select(ResumeScore)).all()
    score_values = [float(score.score or Decimal("0")) for score in scores]

    top_score = max(scores, key=lambda item: float(item.score or 0), default=None)
    top_candidate = db.get(Candidate, top_score.candidate_id).full_name if top_score else None

    return DashboardStats(
        total_candidates=len(candidates),
        total_resumes=len(resume_uploads),
        average_score=round(sum(score_values) / len(score_values), 2) if score_values else 0.0,
        highest_score=round(max(score_values), 2) if score_values else 0.0,
        lowest_score=round(min(score_values), 2) if score_values else 0.0,
        top_candidate=top_candidate,
        skill_distribution=_skill_distribution(candidates),
        experience_distribution=_experience_distribution(candidates),
        score_distribution=_score_distribution(score_values),
    )


def _skill_distribution(candidates: list[Candidate]) -> list[DistributionItem]:
    counter: Counter[str] = Counter()
    for candidate in candidates:
        counter.update(loads(candidate.skills))
    return [DistributionItem(label=skill, count=count) for skill, count in counter.most_common(12)]


def _experience_distribution(candidates: list[Candidate]) -> list[DistributionItem]:
    buckets = Counter({"0-2": 0, "3-5": 0, "6-8": 0, "9+": 0})
    for candidate in candidates:
        years = candidate.total_years_experience or 0
        if years <= 2:
            buckets["0-2"] += 1
        elif years <= 5:
            buckets["3-5"] += 1
        elif years <= 8:
            buckets["6-8"] += 1
        else:
            buckets["9+"] += 1
    return [DistributionItem(label=label, count=count) for label, count in buckets.items()]


def _score_distribution(scores: list[float]) -> list[DistributionItem]:
    buckets = Counter({"0-49": 0, "50-69": 0, "70-85": 0, "86-100": 0})
    for score in scores:
        if score < 50:
            buckets["0-49"] += 1
        elif score < 70:
            buckets["50-69"] += 1
        elif score <= 85:
            buckets["70-85"] += 1
        else:
            buckets["86-100"] += 1
    return [DistributionItem(label=label, count=count) for label, count in buckets.items()]
