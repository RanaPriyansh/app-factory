# AI Finance Coach

[![GitHub](https://img.shields.io/badge/GitHub-000000?logo=github)](https://github.com/RanaPriyansh/finance-coach)
[![License](https://img.shields.io/github/license/RanaPriyansh/finance-coach)](https://github.com/RanaPriyansh/finance-coach/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/RanaPriyansh/finance-coach)](https://github.com/RanaPriyansh/finance-coach/commits/main)

AI-powered finance coach for iOS.

## Features
- AI generation using Claude API
- Stripe subscription payments ($12/month)
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
iOS app template: iOS/FinanceCoach/
Configure bundle ID: com.appfactory.financecoach
Set RevenueCat product: AI Finance Coach

## Revenue
- Freemium: 1 free generation
- Pro: $12/month
- Target: 100+ subscribers in first month = $1200/mo
