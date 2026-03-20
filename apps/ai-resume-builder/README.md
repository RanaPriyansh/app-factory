# AI Resume Builder for Gen Z

A functional MVP for generating AI-powered resumes tailored to specific job descriptions.

## Features

- **AI-Powered Generation**: Uses Claude API to create tailored resumes
- **ATS Optimization**: Includes keywords from job descriptions
- **PDF Export**: Download professional PDF resumes
- **Freemium Model**: 1 free generation, then $9/month subscription
- **Stripe Integration**: Secure payment processing

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file from `.env.example` and fill in your API keys:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY`: Stripe API keys
   - `STRIPE_PRICE_ID`: Stripe Price ID for $9/month subscription
   - `SECRET_KEY`: Flask secret key

3. Run the app:
   ```bash
   python app.py
   ```

4. Open http://localhost:5000 in your browser.

## Deployment

### Using Gunicorn (production):
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables (production):
Set all environment variables in your hosting platform (Heroku, Railway, etc.)

## GTM Playbook

1. **Launch on Product Hunt** - Target "AI tools for students" segment
2. **TikTok Campaign** - "30-second resume hack" videos
3. **Campus Ambassadors** - 1 ambassador per 5k students
4. **Referral Program** - "Invite a friend, both get 1 extra free resume"

## Next Steps

- [ ] Add user authentication
- [ ] Store generations in database
- [ ] Add more resume templates
- [ ] Implement usage tracking per user
- [ ] Add cover letter generation
