"""Bot configuration module."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    BOT_TOKEN: str
    GEMINI_API_KEY: str = ""
    DB_URL: str = "sqlite+aiosqlite:///hisobchi.db"
    DEFAULT_LANG: str = "uz_lat"
    TIMEZONE: str = "Asia/Tashkent"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
