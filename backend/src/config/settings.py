from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Qdrant settings
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # OpenAI settings
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "")

    # Application settings
    app_name: str = "Textbook RAG API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()