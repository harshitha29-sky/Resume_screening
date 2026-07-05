from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.dashboard import DashboardStats
from app.services.dashboard import get_dashboard_stats

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
def read_dashboard(
    db: Annotated[Session, Depends(get_db)],
) -> DashboardStats:
    return get_dashboard_stats(db)
