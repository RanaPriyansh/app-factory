#!/bin/bash

# Prepare all apps for Vercel deployment

APPS_DIR=~/git-repos/thielon-app-factory/apps

# Create vercel.json for each backend
for app in ai-resume-builder contract-generator finance-coach landlord-utility-optimizer teacher-assistant tax-optimizer bookkeeping-automator insurance-claims-autofill doctor-note-summarizer micro-course-creator; do
    backend_dir="$APPS_DIR/$app/backend"
    if [ -d "$backend_dir" ]; then
        echo "Creating vercel.json for $app..."
        cat > "$backend_dir/vercel.json" << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
EOF
    else
        echo "Backend directory not found: $backend_dir"
    fi
done

echo "✅ Created vercel.json for all backends"

# Initialize git repos and commit code
for app in ai-resume-builder contract-generator finance-coach landlord-utility-optimizer teacher-assistant tax-optimizer bookkeeping-automator insurance-claims-autofill doctor-note-summarizer micro-course-creator; do
    app_dir="$APPS_DIR/$app"
    if [ -d "$app_dir" ]; then
        echo "Initializing git repo in $app..."
        cd "$app_dir" && git init && git add . && git commit -m "Initial commit - generated app"
        echo "✓ Committed $app"
    fi
done

echo "✅ Initialized and committed all apps"
