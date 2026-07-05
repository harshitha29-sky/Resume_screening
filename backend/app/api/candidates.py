from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.deps import get_db
from app.models.user import User
from app.schemas.candidate import CandidateDetail, CandidateSearchParams, PaginatedCandidates, RankingItem
from app.services.candidates import get_candidate_detail, get_resume_upload, list_candidates, ranking

router = APIRouter(tags=["candidates"])


@router.get("/candidates", response_model=PaginatedCandidates)
def read_candidates(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
    search: str | None = None,
    min_score: float | None = Query(default=None, ge=0, le=100),
    max_score: float | None = Query(default=None, ge=0, le=100),
    sort_by: str = Query(default="score", pattern="^(score|name|experience|education)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> PaginatedCandidates:
    params = CandidateSearchParams(
        search=search,
        min_score=min_score,
        max_score=max_score,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return list_candidates(db, params)


@router.get("/candidate/{candidate_id}", response_model=CandidateDetail)
def read_candidate(
    candidate_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> CandidateDetail:
    candidate = get_candidate_detail(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.get("/candidate/{candidate_id}/resume")
def preview_resume(
    candidate_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> FileResponse:
    upload = get_resume_upload(db, candidate_id)
    if upload is None or not Path(upload.file_path).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found")
    return FileResponse(path=upload.file_path, filename=upload.filename, media_type=upload.content_type)


@router.get("/ranking", response_model=list[RankingItem])
def read_ranking(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> list[RankingItem]:
    return ranking(db)
