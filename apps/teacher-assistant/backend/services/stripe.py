"""Optional Stripe helpers used only when payments are explicitly enabled."""
from __future__ import annotations

from typing import Optional

from config import settings


class StripeService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.STRIPE_SECRET_KEY

    def is_configured(self) -> bool:
        return bool(settings.PAYMENTS_ENABLED and self.api_key and settings.STRIPE_PRICE_ID)

    def _require_client(self):
        if not self.is_configured():
            raise ValueError("Stripe is not enabled or fully configured")
        try:
            import stripe
        except ImportError as exc:
            raise RuntimeError("stripe package is not installed") from exc
        stripe.api_key = self.api_key
        return stripe

    def create_checkout_session(self, email: str, success_url: str, cancel_url: str):
        stripe = self._require_client()
        return stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=["card"],
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )

    def construct_event(self, payload: bytes, signature: str):
        stripe = self._require_client()
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise ValueError("STRIPE_WEBHOOK_SECRET is required for webhook verification")
        return stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
