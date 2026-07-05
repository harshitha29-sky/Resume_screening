from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.services.exporter import export_rankings_csv, export_rankings_json

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/csv")
def export_csv(
    db: Annotated[Session, Depends(get_db)],
) -> FileResponse:
    path = export_rankings_csv(db)
    return FileResponse(path=path, filename=path.name, media_type="text/csv")


@router.get("/json")
def export_json(
    db: Annotated[Session, Depends(get_db)],
) -> FileResponse:
    path = export_rankings_json(db)
    return FileResponse(path=path, filename=path.name, media_type="application/json")
