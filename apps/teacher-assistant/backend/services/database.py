"""Database service with a durable local JSON mode and optional Supabase mode."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from config import settings


class Database:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.DATABASE_PROVIDER
        self.client = None
        self._local_path = settings.local_data_file
        self._state: Dict[str, Any] = {"users": [], "generations": []}

    async def connect(self):
        if self.provider == "supabase":
            await self._connect_supabase()
            return
        self._load_local()

    async def disconnect(self):
        if self.provider == "local":
            self._save_local()
        self.client = None

    async def create_user(self, email: str, stripe_customer_id: Optional[str] = None) -> Dict[str, Any]:
        if self.provider == "supabase":
            data = {
                "email": email,
                "stripe_customer_id": stripe_customer_id,
                "subscription_status": "inactive",
                "generations_used": 0,
            }
            result = self.client.table("users").insert(data).execute()
            return result.data[0]

        user = {
            "id": str(uuid4()),
            "email": email,
            "stripe_customer_id": stripe_customer_id,
            "subscription_status": "inactive",
            "generations_used": 0,
        }
        self._state["users"].append(user)
        self._save_local()
        return user

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if self.provider == "supabase":
            result = self.client.table("users").select("*").eq("email", email).execute()
            return result.data[0] if result.data else None

        for user in self._state["users"]:
            if user["email"] == email:
                return user
        return None

    async def update_user_subscription(self, user_id: str, status: str, stripe_subscription_id: Optional[str] = None):
        if self.provider == "supabase":
            data = {"subscription_status": status}
            if stripe_subscription_id:
                data["stripe_subscription_id"] = stripe_subscription_id
            self.client.table("users").update(data).eq("id", user_id).execute()
            return

        for user in self._state["users"]:
            if user["id"] == user_id:
                user["subscription_status"] = status
                if stripe_subscription_id:
                    user["stripe_subscription_id"] = stripe_subscription_id
                self._save_local()
                return

    async def increment_generations(self, user_id: str):
        if self.provider == "supabase":
            self.client.rpc("increment_generations", {"user_id": user_id}).execute()
            return

        for user in self._state["users"]:
            if user["id"] == user_id:
                user["generations_used"] += 1
                self._save_local()
                return

    async def save_generation(self, user_id: Optional[str], input_text: str, output_text: str, app_type: str) -> Dict[str, Any]:
        if self.provider == "supabase":
            data = {
                "user_id": user_id,
                "input_text": input_text,
                "output_text": output_text,
                "app_type": app_type,
            }
            result = self.client.table("generations").insert(data).execute()
            return result.data[0] if result.data else data

        generation = {
            "id": str(uuid4()),
            "user_id": user_id,
            "input_text": input_text,
            "output_text": output_text,
            "app_type": app_type,
        }
        self._state["generations"].append(generation)
        self._save_local()
        return generation

    async def _connect_supabase(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError("DATABASE_PROVIDER=supabase requires SUPABASE_URL and SUPABASE_ANON_KEY")
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError("supabase package is not installed") from exc
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    def _load_local(self):
        path = Path(self._local_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self._state = json.loads(path.read_text())
        else:
            self._save_local()

    def _save_local(self):
        path = Path(self._local_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._state, indent=2))
