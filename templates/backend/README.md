# Backend Template

This backend template is now local-first and intended as a practical MVP.

What works now:
- FastAPI backend that compiles cleanly
- `/api/v1/generate` endpoint
- local AI mode that works without paid APIs
- local JSON persistence for users and generations
- optional Anthropic mode if you add `ANTHROPIC_API_KEY`
- optional Stripe/Supabase hooks, clearly marked as non-essential

What is intentionally not production-ready:
- Stripe subscription flows
- Supabase schema management
- App Store / RevenueCat automation
- multi-tenant auth and commercial billing workflows

## Quick start

1. Install dependencies:
   `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`
3. Leave `AI_PROVIDER=local` and `DATABASE_PROVIDER=local`
4. Run:
   `uvicorn main:app --reload`
5. Open docs at `http://localhost:8000/docs`

## Local demo request

Example:

`curl -X POST http://localhost:8000/api/v1/generate -H 'Content-Type: application/json' -d '{"app_type":"teacher_assistant","email":"demo@example.com","input":"5th grade lesson plan on fractions with group activity"}'`

The local provider returns a deterministic draft-like response so generated apps can run without Anthropic, Stripe, or Supabase.

## Optional providers

Anthropic:
- set `AI_PROVIDER=anthropic`
- add `ANTHROPIC_API_KEY`

Supabase:
- set `DATABASE_PROVIDER=supabase`
- add `SUPABASE_URL` and `SUPABASE_ANON_KEY`

Stripe:
- set `PAYMENTS_ENABLED=true`
- add the Stripe environment variables
- treat this as scaffolding, not a production billing setup

## Template structure

- `main.py`: FastAPI app and lifecycle wiring
- `routes/generate.py`: main generation endpoint
- `routes/payments.py`: optional payment stubs
- `services/claude.py`: local-first AI service with Anthropic fallback
- `services/database.py`: local JSON persistence with optional Supabase mode
- `utils/prompts.py`: prompt catalog by app type
