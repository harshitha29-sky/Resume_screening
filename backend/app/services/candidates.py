import math
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.resume_score import ResumeScore
from app.models.upload import Upload
from app.schemas.candidate import (
    CandidateDetail,
    CandidateListItem,
    CandidateSearchParams,
    PaginatedCandidates,
    RankingItem,
    ScoreBreakdown,
)
from app.services.scoring import recommendation_for_score
from app.utils.json_store import loads


def list_candidates(db: Session, params: CandidateSearchParams) -> PaginatedCandidates:
    rows = _candidate_score_rows(db)
    items = [_to_list_item(candidate, score) for candidate, score in rows]
    items = _filter_items(items, params)
    items = _sort_items(items, params.sort_by, params.sort_order)

    total = len(items)
    start = (params.page - 1) * params.page_size
    end = start + params.page_size
    return PaginatedCandidates(
        items=items[start:end],
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=max(1, math.ceil(total / params.page_size)) if total else 0,
    )


def get_candidate_detail(db: Session, candidate_id: int) -> CandidateDetail | None:
    candidate = db.get(Candidate, candidate_id)
    if candidate is None:
        return None
    score = _latest_score(db, candidate.id)
    upload = db.scalar(select(Upload).where(Upload.candidate_id == candidate.id).order_by(Upload.id.desc()))
    breakdown = None
    if score is not None:
        overall = float(score.score or Decimal("0"))
        breakdown = ScoreBreakdown(
            overall_score=overall,
            nlp_similarity=score.nlp_similarity,
            skill_match=score.skill_match,
            experience_match=score.experience_match,
            education_match=score.education_match,
            matching_skills=loads(score.matching_skills),
            missing_skills=loads(score.missing_skills),
            recommendation=score.recommendation or recommendation_for_score(overall),
        )

    item = _to_list_item(candidate, score)
    return CandidateDetail(
        **item.model_dump(),
        experience=loads(candidate.experience),
        projects=loads(candidate.projects),
        certifications=loads(candidate.certifications),
        raw_text=candidate.raw_text,
        resume_url=f"/candidate/{candidate.id}/resume" if upload else None,
        score_breakdown=breakdown,
        created_at=candidate.created_at,
    )


def ranking(db: Session) -> list[RankingItem]:
    rows = _candidate_score_rows(db)
    scored = [
        (candidate, score)
        for candidate, score in rows
        if score is not None and score.score is not None
    ]
    scored.sort(key=lambda row: float(row[1].score), reverse=True)
    return [
        RankingItem(
            rank=index + 1,
            candidate_id=candidate.id,
            candidate_name=candidate.full_name,
            overall_score=float(score.score),
            skill_match=score.skill_match,
            experience_match=score.experience_match,
            education_match=score.education_match,
            recommendation=score.recommendation or recommendation_for_score(float(score.score)),
        )
        for index, (candidate, score) in enumerate(scored)
    ]


def get_resume_upload(db: Session, candidate_id: int) -> Upload | None:
    return db.scalar(select(Upload).where(Upload.candidate_id == candidate_id).order_by(Upload.id.desc()))


def _candidate_score_rows(db: Session) -> list[tuple[Candidate, ResumeScore | None]]:
    candidates = db.scalars(select(Candidate)).all()
    return [(candidate, _latest_score(db, candidate.id)) for candidate in candidates]


def _latest_score(db: Session, candidate_id: int) -> ResumeScore | None:
    return db.scalar(
        select(ResumeScore)
        .where(ResumeScore.candidate_id == candidate_id)
        .order_by(ResumeScore.created_at.desc(), ResumeScore.id.desc())
    )


def _to_list_item(candidate: Candidate, score: ResumeScore | None) -> CandidateListItem:
    overall = float(score.score) if score is not None and score.score is not None else None
    return CandidateListItem(
        id=candidate.id,
        full_name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,
        skills=loads(candidate.skills),
        education=loads(candidate.education),
        total_years_experience=candidate.total_years_experience or 0.0,
        overall_score=overall,
        recommendation=(score.recommendation if score else None),
    )


def _filter_items(items: list[CandidateListItem], params: CandidateSearchParams) -> list[CandidateListItem]:
    filtered = items
    if params.search:
        needle = params.search.lower()
        filtered = [
            item
            for item in filtered
            if needle in item.full_name.lower()
            or (item.email and needle in item.email.lower())
            or any(needle in skill.lower() for skill in item.skills)
        ]
    if params.min_score is not None:
        filtered = [item for item in filtered if (item.overall_score or 0) >= params.min_score]
    if params.max_score is not None:
        filtered = [item for item in filtered if (item.overall_score or 0) <= params.max_score]
    return filtered


def _sort_items(items: list[CandidateListItem], sort_by: str, sort_order: str) -> list[CandidateListItem]:
    reverse = sort_order.lower() != "asc"
    key_map = {
        "name": lambda item: item.full_name.lower(),
        "experience": lambda item: item.total_years_experience,
        "education": lambda item: " ".join(item.education).lower(),
        "score": lambda item: item.overall_score or 0,
    }
    return sorted(items, key=key_map.get(sort_by, key_map["score"]), reverse=reverse)
