# Teacher Assistant

Generated from App Factory as a local-first MVP.

## Current backend path

The backend is aligned to run locally without paid services.

### Local setup
1. `cd backend`
2. `cp .env.example .env`
3. Leave `AI_PROVIDER=local`
4. Leave `DATABASE_PROVIDER=local`
5. `pip install -r requirements.txt`
6. `uvicorn main:app --reload`

### Example request
`curl -X POST http://localhost:8000/api/v1/generate -H 'Content-Type: application/json' -d '{"app_type":"teacher_assistant","input":"Create a 4th grade reading comprehension lesson plan about identifying main idea with guided practice and an exit ticket.","email":"demo@example.com"}'`

## Notes
- Anthropic is optional, not required
- Stripe and Supabase are optional scaffolding
- iOS template work still needs follow-up before production use

## App metadata
- Bundle ID: com.appfactory.teacherassistant
- Suggested price if you later commercialize it: $15/month
