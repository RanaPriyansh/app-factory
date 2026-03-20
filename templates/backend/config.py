from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Anthropic Claude
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_PRICE_ID: str
    STRIPE_WEBHOOK_SECRET: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    # App
    SECRET_KEY: str
    APP_NAME: str = "AI SaaS Backend"
    APP_ENV: str = "production"

    # Optional
    REDIS_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
