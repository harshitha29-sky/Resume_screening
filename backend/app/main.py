from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import candidates_router, dashboard_router, export_router, uploads_router
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Resume Screening Agent API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://192.168.32.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads_router)
app.include_router(candidates_router)
app.include_router(dashboard_router)
app.include_router(export_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Resume Screening Agent API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
