from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./resume_screening.db"
    app_env: str = "development"
    secret_key: str = "change-this-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    upload_root: str = "../uploads"
    export_root: str = "../exports"
    max_resume_upload_count: int = 20
    max_upload_size_mb: int = 10
    sentence_transformer_model: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
