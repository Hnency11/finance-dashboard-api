from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """
    API_TITLE: str = "Finance Dashboard API"
    APP_NAME: str = "Finance Dashboard"
    ENV: str = "development"
    DATABASE_URL: str = Field(..., min_length=1)
    SECRET_KEY: str = Field(..., min_length=32)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    """
    return Settings()
