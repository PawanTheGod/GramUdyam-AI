from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "GramUdyam AI"
    APP_VERSION: str = "1.0.0-mvp"
    DATABASE_URL: str = "sqlite:///./gramudyam.db"
    SECRET_KEY: str = "gramudyam-mvp-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours for demo
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
