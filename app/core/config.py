# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI RAG Basic Starter Kit"
    API_V1_STR: str = "/api/v1"
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Chunking Configurations
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # RAG Configurations
    RETRIEVER_K: int = 3  # Number of documents to retrieve

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()