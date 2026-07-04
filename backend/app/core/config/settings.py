"""Application settings and configuration."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "File Conversion Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_STR: str = "/api/v1"
    API_TITLE: str = "File Conversion API"
    API_DESCRIPTION: str = "Professional file conversion platform"
    API_VERSION: str = "1.0.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 4

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    UPLOAD_DIR: Path = Path("app/uploads")
    OUTPUT_DIR: Path = Path("app/outputs")
    TEMP_DIR: Path = Path("app/temp")
    ALLOWED_IMAGE_FORMATS: tuple = ("jpg", "jpeg", "png", "webp", "gif", "bmp")
    ALLOWED_PDF_EXTENSIONS: tuple = ("pdf",)
    ALLOWED_ZIP_EXTENSIONS: tuple = ("zip",)

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds

    # Storage
    STORAGE_TYPE: str = "local"  # local, s3, gcs, azure
    STORAGE_PATH: str = "uploads"

    # Cleanup
    TEMP_FILE_TTL: int = 3600  # 1 hour in seconds
    AUTO_CLEANUP_ENABLED: bool = True
    AUTO_CLEANUP_INTERVAL: int = 300  # 5 minutes

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Database
    DATABASE_URL: Optional[str] = None
    SQLALCHEMY_ECHO: bool = False

    # Redis
    REDIS_URL: Optional[str] = None
    REDIS_ENABLED: bool = False

    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_ENABLED: bool = False

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()
