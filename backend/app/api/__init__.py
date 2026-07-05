from app.api.candidates import router as candidates_router
from app.api.dashboard import router as dashboard_router
from app.api.export import router as export_router
from app.api.uploads import router as uploads_router

__all__ = [
    "candidates_router",
    "dashboard_router",
    "export_router",
    "uploads_router",
]
