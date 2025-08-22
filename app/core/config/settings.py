from pydantic_settings import BaseSettings
from ...docs.content.headers_content import headers_content
from typing import Optional


class Settings(BaseSettings):

    """

    Server settings.

    
    Usage
    -----
    The class instance must be used.

    """

    # Project info
    PROJECT_NAME: str = "Insight Extractor AI Agent"
    PROJECT_DESCRIPTION: str = f"A backend service to extract structured insights from documents using any LLM agent. {headers_content}"
    VERSION: str = "0.1.0"

    # Logging
    HANDLER_LOG_LEVEL: str = "DEBUG"
    ROOT_LOG_LEVEL: str = "INFO"
    UVICORN_LOG_LEVEL: str = "INFO"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Docs
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # Rate Limits
    ## Global
    RATE_LIMITS: list[str] = ["1/minute", "60/hour", "100/day"]

    # Redis settings
    USE_REDIS: bool = False
    REDIS_URL: Optional[str] = None

    # Storage settings
    STORAGE_TYPE: str = "local" 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()