#!/bin/bash

# Deploy all backends to Vercel
# Prerequisites: Vercel CLI installed and logged in

set -e

APPS=(
  "ai-resume-builder"
  "contract-generator"
  "finance-coach"
  "landlord-utility-optimizer"
  "teacher-assistant"
  "tax-optimizer"
  "bookkeeping-automator"
  "insurance-claims-autofill"
  "doctor-note-summarizer"
  "micro-course-creator"
)

BASE_DIR="/root/git-repos/app-factory/apps"

echo "🚀 Deploying all backends to Vercel..."
echo "========================================"
echo ""

for app in "${APPS[@]}"; do
  echo "📦 Deploying: $app"
  backend_dir="$BASE_DIR/$app/backend"

  if [ ! -d "$backend_dir" ]; then
    echo "❌ Backend directory not found: $backend_dir"
    continue
  fi

  cd "$backend_dir"

  # Check if vercel.json exists
  if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found in $backend_dir"
    continue
  fi

  # Deploy to Vercel
  echo "  → Deploying..."
  if vercel --prod --yes; then
    echo "  ✅ Deployed $app successfully"
    # Get the deployed URL
    # Vercel CLI prints the URL, but we could also use vercel ls to get it
  else
    echo "  ❌ Failed to deploy $app"
  fi

  echo ""
done

echo "✅ Deployment process completed!"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables in Vercel dashboard for each deployment:"
echo "   - ANTHROPIC_API_KEY"
echo "   - STRIPE_SECRET_KEY"
echo "   - STRIPE_PUBLISHABLE_KEY"
echo "   - STRIPE_PRICE_ID"
echo "   - STRIPE_WEBHOOK_SECRET"
echo "   - SUPABASE_URL"
echo "   - SUPABASE_ANON_KEY"
echo "   - SECRET_KEY"
echo ""
echo "2. Configure Stripe webhook to point to: https://your-app.vercel.app/api/webhook"
echo "3. Update iOS app API endpoints with deployed backend URLs"
echo ""
