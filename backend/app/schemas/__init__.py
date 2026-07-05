from app.schemas.auth import Token, TokenPayload, UserLogin, UserRead, UserRegister
from app.schemas.candidate import CandidateDetail, CandidateListItem, RankingItem
from app.schemas.dashboard import DashboardStats
from app.schemas.upload import JobDescriptionUploadResponse, ResumeUploadResponse, UploadRead

__all__ = [
    "CandidateDetail",
    "CandidateListItem",
    "DashboardStats",
    "JobDescriptionUploadResponse",
    "RankingItem",
    "ResumeUploadResponse",
    "Token",
    "TokenPayload",
    "UploadRead",
    "UserLogin",
    "UserRead",
    "UserRegister",
]
