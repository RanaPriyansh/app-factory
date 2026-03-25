# App Factory

App Factory is an app generator repo with a usable local-first MVP path.

Current reality:
- the backend template generates FastAPI backends
- generated backends can run in a simple local mode without Anthropic, Stripe, or Supabase
- commercial integrations remain optional scaffolding, not the core path
- the iOS side is still template-heavy and incomplete compared with the backend rescue work

## Recommended use

If you want a working baseline, focus on the generated backend first.

### Generate an app

From the repo root:

`python3 scripts/generate_app.py teacher-assistant`

or, if the directory already exists, inspect `templates/backend` and copy from there.

### Run a generated backend locally

Inside an app backend directory:

1. `cp .env.example .env`
2. leave `AI_PROVIDER=local`
3. leave `DATABASE_PROVIDER=local`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

Then call:

`curl -X POST http://localhost:8000/api/v1/generate -H 'Content-Type: application/json' -d '{"app_type":"teacher_assistant","input":"Create a 5th grade lesson plan about fractions","email":"demo@example.com"}'`

## What is working

- backend template compiles cleanly
- prompt catalog is fixed
- local JSON persistence is available
- generator copies the rescued backend template
- optional Anthropic / Supabase / Stripe hooks remain available for future work

## What is not solved here

- production billing
- robust auth
- complete iOS commercialization pipeline
- deployment automation across Vercel/App Store/RevenueCat

## Key files

- `templates/backend/` - rescued backend template
- `scripts/generate_app.py` - app generator
- `apps/` - generated example apps

This repo should now be treated as a local/open-source-compatible app generator first, not a fully wired commercial SaaS factory.
