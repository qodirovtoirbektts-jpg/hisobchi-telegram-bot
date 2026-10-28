"""Bot configuration module."""
from pathlib import Path
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    GEMINI_API_KEY: str = ""
    DB_URL: str = "sqlite+aiosqlite:///hisobchi.db"
    DEFAULT_LANG: str = "uz_lat"
    TIMEZONE: str = "Asia/Tashkent"

    @field_validator("BOT_TOKEN", "GEMINI_API_KEY", mode="before")
    @classmethod
    def clean_secrets(cls, v: Any) -> str:
        if isinstance(v, str):
            return v.strip().strip("'\"")
        return str(v or "")

    model_config = SettingsConfigDict(
        env_file=(str(BASE_DIR / ".env"), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
