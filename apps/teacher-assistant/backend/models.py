"""Pydantic models for the local-first backend template."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GenerateRequest(BaseModel):
    email: Optional[str] = None
    app_type: str = "teacher_assistant"
    input: str = Field(..., min_length=3, description="User input for generation")
    options: Dict[str, Any] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    success: bool = True
    provider: str
    app_type: str
    output: str
    generation_id: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    ai_provider: str
    database_provider: str
    payments_enabled: bool


class CheckoutSessionRequest(BaseModel):
    email: str
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutSessionResponse(BaseModel):
    enabled: bool
    message: str
    url: Optional[str] = None


class UserRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    email: str
    generations_used: int = 0


class GenerationRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    user_id: Optional[str] = None
    app_type: str
    input_text: str
    output_text: str
