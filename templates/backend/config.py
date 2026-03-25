from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "AI SaaS Backend"
    APP_ENV: str = "local"
    APP_URL: str = "http://localhost:8000"
    SECRET_KEY: str = "dev-secret-key"

    AI_PROVIDER: Literal["local", "anthropic"] = "local"
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.2

    DATABASE_PROVIDER: Literal["local", "supabase"] = "local"
    LOCAL_DATA_PATH: str = "./data/local_store.json"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None

    PAYMENTS_ENABLED: bool = False
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_PRICE_ID: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    DEFAULT_APP_TYPE: str = "resume_builder"

    @property
    def local_data_file(self) -> Path:
        return Path(self.LOCAL_DATA_PATH)


settings = Settings()
