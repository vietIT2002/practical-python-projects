"""Environment-based configuration.

The application runs locally with safe defaults and no secrets. Override any
value with an environment variable prefixed ``URLSHORTENER_`` or an ``.env``
file (see ``.env.example``).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="URLSHORTENER_",
        env_file=".env",
        extra="ignore",
    )

    database_url: str = "sqlite:///./url_shortener.db"
    base_url: str = "http://localhost:8000"
    log_level: str = "INFO"
    code_length: int = Field(default=7, ge=4, le=32)


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
