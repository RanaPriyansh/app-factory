# Teacher Assistant

[![GitHub](https://img.shields.io/badge/GitHub-000000?logo=github)](https://github.com/RanaPriyansh/teacher-assistant)
[![License](https://img.shields.io/github/license/RanaPriyansh/teacher-assistant)](https://github.com/RanaPriyansh/teacher-assistant/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/RanaPriyansh/teacher-assistant)](https://github.com/RanaPriyansh/teacher-assistant/commits/main)

AI-powered teacher assistant for iOS.

## Features
- AI generation using Claude API
- Stripe subscription payments ($15/month)
- Freemium model: 1 free generation
- PDF export (coming soon)

## Setup
1. Copy `.env.example` to `.env` and fill in your API keys
2. Run: `pip install -r requirements.txt`
3. Run: `uvicorn main:app --reload`
4. Open http://localhost:8000/docs for API docs

## Deployment
Deploy to Vercel, Railway, or Heroku. Set all environment variables.

## App Store
iOS app template: iOS/TeacherAssistant/
Configure bundle ID: com.appfactory.teacherassistant
Set RevenueCat product: Teacher Assistant

## Revenue
- Freemium: 1 free generation
- Pro: $15/month
- Target: 100+ subscribers in first month = $1500/mo
