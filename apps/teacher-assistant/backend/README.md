# Teacher Assistant backend

This backend is aligned to the rescued local-first app-factory MVP path.

What works now:
- FastAPI backend that compiles cleanly
- `/health` endpoint
- `/api/v1/generate` in local mode without paid APIs
- local JSON persistence for users and generations
- `teacher_assistant` prompt path for lesson-plan style drafts
- optional Anthropic, Stripe, and Supabase scaffolding

What is intentionally not production-ready:
- Stripe subscription flows
- Supabase schema management
- App Store / RevenueCat automation
- commercial billing and multi-tenant auth

## Quick start

1. `cd backend`
2. `cp .env.example .env`
3. Leave `AI_PROVIDER=local`
4. Leave `DATABASE_PROVIDER=local`
5. `pip install -r requirements.txt`
6. `uvicorn main:app --reload`

Docs will be available at `http://localhost:8000/docs`.

## Local demo request

`curl -X POST http://localhost:8000/api/v1/generate -H 'Content-Type: application/json' -d '{"app_type":"teacher_assistant","email":"demo@example.com","input":"Create a 5th grade lesson plan on fractions with a short warm-up, guided practice, differentiation ideas, and an exit ticket."}'`

The local provider returns a deterministic teacher-assistant draft so the app can demo without Anthropic, Stripe, or Supabase.

## Optional providers

Anthropic:
- set `AI_PROVIDER=anthropic`
- add `ANTHROPIC_API_KEY`

Supabase:
- set `DATABASE_PROVIDER=supabase`
- add `SUPABASE_URL` and `SUPABASE_ANON_KEY`

Stripe:
- set `PAYMENTS_ENABLED=true`
- add Stripe environment variables
- treat this as scaffolding, not a production billing system

## File guide

- `main.py`: FastAPI app and lifecycle wiring
- `routes/generate.py`: generation endpoint
- `routes/payments.py`: payment stubs
- `services/claude.py`: local-first AI service with Anthropic fallback
- `services/database.py`: local JSON persistence with optional Supabase mode
- `utils/prompts.py`: prompt catalog including `teacher_assistant`
