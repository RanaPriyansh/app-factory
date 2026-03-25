"""Optional payment endpoints.

These are intentionally non-production-ready. In local-first mode they return a
clear stub response instead of pretending a commercial stack is configured.
"""

from fastapi import APIRouter, HTTPException, Request

from config import settings
from models import CheckoutSessionRequest, CheckoutSessionResponse
from services.stripe import StripeService

router = APIRouter()
stripe_service = StripeService()


@router.get("/payments/status")
async def payment_status():
    return {
        "enabled": settings.PAYMENTS_ENABLED,
        "provider": "stripe" if settings.PAYMENTS_ENABLED else "disabled",
        "production_ready": False,
    }


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(payload: CheckoutSessionRequest):
    if not settings.PAYMENTS_ENABLED:
        return CheckoutSessionResponse(
            enabled=False,
            message="Payments are disabled in local-first mode.",
        )

    try:
        session = stripe_service.create_checkout_session(
            email=str(payload.email),
            success_url=payload.success_url or f"{settings.APP_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=payload.cancel_url or f"{settings.APP_URL}/cancel",
        )
        return CheckoutSessionResponse(enabled=True, message="Checkout session created.", url=session.url)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    if not settings.PAYMENTS_ENABLED:
        return {"status": "ignored", "detail": "Payments disabled in local-first mode."}

    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    event = stripe_service.construct_event(payload=payload, signature=signature)
    return {"status": "received", "type": event.get("type")}
