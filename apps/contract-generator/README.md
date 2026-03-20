# AI Contract Generator for Freelancers

A functional MVP for generating AI-powered freelance contracts.

## Features

- **AI-Powered Generation**: Uses Claude API to create tailored contracts
- **Comprehensive Clauses**: Covers scope, payment, IP, confidentiality, termination
- **PDF Export**: Download professional PDF contracts
- **Freemium Model**: 1 free generation, then $12/month subscription
- **Stripe Integration**: Secure payment processing

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file from `.env.example` and fill in your API keys:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY`: Stripe API keys
   - `STRIPE_PRICE_ID`: Stripe Price ID for $12/month subscription
   - `SECRET_KEY`: Flask secret key

3. Run the app:
   ```bash
   python app.py
   ```

4. Open http://localhost:5001 in your browser.

## Deployment

### Using Gunicorn (production):
```bash
gunicorn -w 4 -b 0.0.0.0:8001 app:app
```

### Environment Variables (production):
Set all environment variables in your hosting platform.

## GTM Playbook

1. **Community Seeding** – Post in r/freelance, r/forhire, Indie Hackers
2. **Integration Partnerships** – Upwork/Fiverr marketplace listings
3. **Content Marketing** – "Freelancer Contract Checklist" lead magnet
4. **Referral Program** – "Invite a freelancer, both get 1 month free"
5. **Product Hunt Launch** – Target "Tools for Freelancers" category

## Next Steps

- [ ] Add user authentication
- [ ] Store contracts in database
- [ ] Add e-signature integration (Dropbox Sign API)
- [ ] Implement contract templates library
- [ ] Add milestone payment tracking
