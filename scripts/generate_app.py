#!/usr/bin/env python3
"""
Thielon App Factory - Generate AI SaaS iOS apps from templates
Usage: python generate_app.py <app_name> <price> <prompt_key>
"""

import os
import sys
import shutil
from pathlib import Path

FACTORY_ROOT = Path(__file__).parent.parent
TEMPLATE_BACKEND = FACTORY_ROOT / 'templates' / 'backend'
TEMPLATE_IOS = FACTORY_ROOT / 'templates' / 'ios'

APPS = {
    'ai-resume-builder': {
        'price': 9,
        'prompt_key': 'resume_builder',
        'display': 'AI Resume Builder',
        'bundle_id': 'com.thielon.resumebuilder',
        'app_name': 'ResumeBuilder',
        'target': 'Gen Z job seekers'
    },
    'contract-generator': {
        'price': 12,
        'prompt_key': 'contract_generator',
        'display': 'AI Contract Generator',
        'bundle_id': 'com.thielon.contractgenerator',
        'app_name': 'ContractGenerator',
        'target': 'Freelancers'
    },
    'finance-coach': {
        'price': 12,
        'prompt_key': 'finance_coach',
        'display': 'AI Finance Coach',
        'bundle_id': 'com.thielon.financecoach',
        'app_name': 'FinanceCoach',
        'target': 'Baby Boomers'
    },
    'landlord-utility-optimizer': {
        'price': 29,
        'prompt_key': 'landlord_utility',
        'display': 'Landlord Utility Optimizer',
        'bundle_id': 'com.thielon.landlordutility',
        'app_name': 'LandlordUtility',
        'target': 'Property owners'
    },
    'teacher-assistant': {
        'price': 15,
        'prompt_key': 'teacher_assistant',
        'display': 'Teacher Assistant',
        'bundle_id': 'com.thielon.teacherassistant',
        'app_name': 'TeacherAssistant',
        'target': 'K-12 teachers'
    },
    'tax-optimizer': {
        'price': 15,
        'prompt_key': 'tax_optimizer',
        'display': 'AI Tax Optimizer',
        'bundle_id': 'com.thielon.taxoptimizer',
        'app_name': 'TaxOptimizer',
        'target': 'Freelancers & small businesses'
    },
    'bookkeeping-automator': {
        'price': 19,
        'prompt_key': 'bookkeeping_automator',
        'display': 'AI Bookkeeping Automator',
        'bundle_id': 'com.thielon.bookkeepingautomator',
        'app_name': 'BookkeepingAutomator',
        'target': 'Small business owners'
    },
    'insurance-claims-autofill': {
        'price': 12,
        'prompt_key': 'insurance_claims_autofill',
        'display': 'AI Insurance Claims Autofill',
        'bundle_id': 'com.thielon.insuranceclaimsautofill',
        'app_name': 'InsuranceClaimsAutofill',
        'target': 'Insurance policyholders'
    },
    'doctor-note-summarizer': {
        'price': 9,
        'prompt_key': 'doctor_note_summarizer',
        'display': 'AI Doctor Note Summarizer',
        'bundle_id': 'com.thielon.doctornotesummarizer',
        'app_name': 'DoctorNoteSummarizer',
        'target': 'Patients & caregivers'
    },
    'micro-course-creator': {
        'price': 29,
        'prompt_key': 'micro_course_creator',
        'display': 'AI Micro Course Creator',
        'bundle_id': 'com.thielon.microcoursecreator',
        'app_name': 'MicroCourseCreator',
        'target': 'Educators & content creators'
    }
}

def copy_template(src, dst, replacements=None):
    """Copy template file with optional replacements"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    content = src.read_text()
    if replacements:
        for key, value in replacements.items():
            content = content.replace(f'{{{key}}}', str(value))
    
    dst.write_text(content)
    print(f"  ✓ {src.name} -> {dst}")

def generate_app(app_key):
    """Generate complete app structure"""
    if app_key not in APPS:
        print(f"Error: Unknown app '{app_key}'")
        print(f"Available: {', '.join(APPS.keys())}")
        sys.exit(1)
    
    config = APPS[app_key]
    print(f"\nGenerating {config['display']}...")
    
    # App directory
    app_dir = FACTORY_ROOT / 'apps' / app_key
    if app_dir.exists():
        print(f"Warning: {app_dir} already exists. Skipping.")
        return
    
    app_dir.mkdir(parents=True)
    
    # 1. Backend
    print("  Backend...")
    backend_dir = app_dir / 'backend'
    shutil.copytree(TEMPLATE_BACKEND, backend_dir)
    
    # Customize backend files
    replacements = {
        'APP_NAME': config['display'],
        'APP_PRICE': str(config['price']),
        'BUNDLE_ID': config['bundle_id'],
        'APP_KEY': app_key
    }
    
    # Update config.py
    config_content = f'''from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_PRICE_ID: str
    STRIPE_WEBHOOK_SECRET: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SECRET_KEY: str
    APP_NAME: str = "{config['display']}"
    APP_ENV: str = "production"
    REDIS_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None
    class Config:
        env_file = ".env"
settings = Settings()
'''
    (backend_dir / 'config.py').write_text(config_content)
    
    # Update main.py title
    main_py = (backend_dir / 'main.py').read_text()
    main_py = main_py.replace('AI SaaS Backend', config['display'])
    (backend_dir / 'main.py').write_text(main_py)
    
    # Create app-specific README
    (app_dir / 'README.md').write_text(f'''# {config['display']}

AI-powered {app_key.replace('-', ' ')} for iOS.

## Features
- AI generation using Claude API
- Stripe subscription payments (${config['price']}/month)
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
iOS app template: iOS/{config['app_name']}/
Configure bundle ID: {config['bundle_id']}
Set RevenueCat product: {config['display']}

## Revenue
- Freemium: 1 free generation
- Pro: ${config['price']}/month
- Target: 100+ subscribers in first month = ${config['price']*100}/mo
''')
    
    # 2. iOS
    print("  iOS app...")
    ios_dir = app_dir / 'iOS'
    shutil.copytree(TEMPLATE_IOS, ios_dir)
    
    # Copy Xcode project template
    xcodeproj_src = TEMPLATE_IOS / 'ThielonApp.xcodeproj'
    xcodeproj_dst = ios_dir / f'{config["app_name"]}.xcodeproj'
    if xcodeproj_src.exists():
        shutil.copytree(xcodeproj_src, xcodeproj_dst)
        print(f"  ✓ Xcode project created: {xcodeproj_dst}")
    else:
        print(f"  ⚠ Warning: Xcode project template not found at {xcodeproj_src}")
    
    # Rename ThielonApp to actual app name
    src_app = ios_dir / 'ThielonApp'
    dst_app = ios_dir / config['app_name']
    if src_app.exists():
        src_app.rename(dst_app)
    
    # Update bundle ID and app name in Info.plist
    info_plist = (dst_app / 'Info.plist').read_text()
    info_plist = info_plist.replace('com.thielon.resumebuilder', config['bundle_id'])
    info_plist = info_plist.replace('AI Resume Builder', config['display'])
    info_plist = info_plist.replace('ThielonAI', config['app_name'])
    (dst_app / 'Info.plist').write_text(info_plist)
    
    # Update Xcode project with bundle ID and app name
    if xcodeproj_dst.exists():
        pbxproj_path = xcodeproj_dst / 'project.pbxproj'
        if pbxproj_path.exists():
            pbxproj = pbxproj_path.read_text()
            # Replace placeholders
            pbxproj = pbxproj.replace('com.thielon.template', config['bundle_id'])
            pbxproj = pbxproj.replace('PRODUCT_NAME = ThielonApp;', f'PRODUCT_NAME = {config["app_name"]};')
            pbxproj = pbxproj.replace('name = ThielonApp;', f'name = {config["app_name"]};')
            pbxproj = pbxproj.replace('path = ThielonApp;', f'path = {config["app_name"]};')
            pbxproj = pbxproj.replace('INFOPLIST_FILE = ThielonApp/Info.plist;', f'INFOPLIST_FILE = {config["app_name"]}/Info.plist;')
            pbxproj_path.write_text(pbxproj)
            print(f"  ✓ Updated Xcode project settings")
    
    # Clean up template .xcodeproj if it exists (from copytree)
    template_xcodeproj = ios_dir / 'ThielonApp.xcodeproj'
    if template_xcodeproj.exists() and template_xcodeproj != xcodeproj_dst:
        shutil.rmtree(template_xcodeproj)
        print(f"  ✓ Cleaned up template Xcode project")
    
    # Update ContentView
    content_view = (dst_app / 'Views' / 'ContentView.swift').read_text()
    content_view = content_view.replace('AI Resume Builder', config['display'])
    (dst_app / 'Views' / 'ContentView.swift').write_text(content_view)
    
    # Create deployment guide
    (app_dir / 'DEPLOYMENT.md').write_text(f'''# Deploying {config['display']}

## Backend (One-time)
1. Create Stripe product and price (${config['price']}/month)
2. Create Supabase database (users, generations tables)
3. Deploy backend to Vercel/Railway
4. Set webhook endpoint in Stripe dashboard

## iOS App
1. Open Xcode project in iOS/{config['app_name']}/
2. Set bundle identifier: {config['bundle_id']}
3. Add RevenueCat API key
4. Configure App Store Connect entry
5. Build and submit for review
6. Release to TestFlight first

## RevenueCat Setup
- Create entitlement: "premium"
- Create product: "{config['display']}" (${config['price']}/mo)
- Add to configurations in Xcode

## Database Schema
Run in Supabase SQL editor:

CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    stripe_customer_id TEXT,
    subscription_status TEXT DEFAULT 'inactive',
    generations_used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE generations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    input_text TEXT,
    output_text TEXT,
    app_type TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE FUNCTION increment_generations(user_id UUID)
RETURNS void AS $$
BEGIN
    UPDATE users SET generations_used = generations_used + 1 WHERE id = user_id;
END;
$$ LANGUAGE plpgsql;
''')
    
    print(f"✓ Generated {config['display']}")
    print(f"  Location: {app_dir}")
    print(f"  Backend: {backend_dir}")
    print(f"  iOS: {dst_app}")

def main():
    if len(sys.argv) < 2:
        print("Thielon App Factory")
        print("===================\n")
        print("Available apps:")
        for key, cfg in APPS.items():
            print(f"  {key:25s} - ${cfg['price']}/mo - {cfg['target']}")
        print("\nUsage: python generate_app.py <app_name>")
        print("Or: python generate_app.py all")
        sys.exit(0)
    
    if sys.argv[1] == 'all':
        for key in APPS.keys():
            generate_app(key)
        print("\n✅ All apps generated!")
    else:
        generate_app(sys.argv[1])

if __name__ == '__main__':
    main()
