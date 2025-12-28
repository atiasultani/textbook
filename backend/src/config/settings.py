from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Qdrant settings
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Cohere settings
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "")

    # Gemini settings
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "cohere")  # cohere or gemini

    # Authentication settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Application settings
    app_name: str = "Textbook RAG API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_v1_prefix: str = "/api/v1"

    #Auth settings
    VITE_NEON_AUTH_URL: str | None = os.getenv("VITE_NEON_AUTH_URL")
    DATABASE_URL: str=os.getenv("DATABASE_URL")
    JWT_SECRET: str=os.getenv("JWT_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()