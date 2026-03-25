"""Generation endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from config import settings
from models import GenerateRequest, GenerateResponse
from services.claude import ClaudeService
from services.database import Database

router = APIRouter()
logger = logging.getLogger(__name__)

claude_service = ClaudeService()
db = Database()


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        user = None
        warnings = []

        if request.email:
            user = await db.get_user_by_email(str(request.email))
            if not user:
                user = await db.create_user(str(request.email))
        else:
            warnings.append("No email supplied; generation will not be associated with a named user.")

        output = await claude_service.generate_for_app(app_type=request.app_type, user_input=request.input)

        generation = await db.save_generation(
            user_id=user["id"] if user else None,
            input_text=request.input,
            output_text=output,
            app_type=request.app_type,
        )

        if user:
            await db.increment_generations(user["id"])

        return GenerateResponse(
            success=True,
            provider=settings.AI_PROVIDER,
            app_type=request.app_type,
            output=output,
            generation_id=generation.get("id"),
            warnings=warnings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Generation error")
        raise HTTPException(status_code=500, detail="Generation failed") from exc
