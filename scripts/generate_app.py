#!/usr/bin/env python3
"""
 App Factory - Generate AI SaaS iOS apps from templates
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
        'bundle_id': 'com.appfactory.resumebuilder',
        'app_name': 'ResumeBuilder',
        'target': 'Gen Z job seekers'
    },
    'contract-generator': {
        'price': 12,
        'prompt_key': 'contract_generator',
        'display': 'AI Contract Generator',
        'bundle_id': 'com.appfactory.contractgenerator',
        'app_name': 'ContractGenerator',
        'target': 'Freelancers'
    },
    'finance-coach': {
        'price': 12,
        'prompt_key': 'finance_coach',
        'display': 'AI Finance Coach',
        'bundle_id': 'com.appfactory.financecoach',
        'app_name': 'FinanceCoach',
        'target': 'Baby Boomers'
    },
    'landlord-utility-optimizer': {
        'price': 29,
        'prompt_key': 'landlord_utility',
        'display': 'Landlord Utility Optimizer',
        'bundle_id': 'com.appfactory.landlordutility',
        'app_name': 'LandlordUtility',
        'target': 'Property owners'
    },
    'teacher-assistant': {
        'price': 15,
        'prompt_key': 'teacher_assistant',
        'display': 'Teacher Assistant',
        'bundle_id': 'com.appfactory.teacherassistant',
        'app_name': 'TeacherAssistant',
        'target': 'K-12 teachers'
    },
    'tax-optimizer': {
        'price': 15,
        'prompt_key': 'tax_optimizer',
        'display': 'AI Tax Optimizer',
        'bundle_id': 'com.appfactory.taxoptimizer',
        'app_name': 'TaxOptimizer',
        'target': 'Freelancers & small businesses'
    },
    'bookkeeping-automator': {
        'price': 19,
        'prompt_key': 'bookkeeping_automator',
        'display': 'AI Bookkeeping Automator',
        'bundle_id': 'com.appfactory.bookkeepingautomator',
        'app_name': 'BookkeepingAutomator',
        'target': 'Small business owners'
    },
    'insurance-claims-autofill': {
        'price': 12,
        'prompt_key': 'insurance_claims_autofill',
        'display': 'AI Insurance Claims Autofill',
        'bundle_id': 'com.appfactory.insuranceclaimsautofill',
        'app_name': 'InsuranceClaimsAutofill',
        'target': 'Insurance policyholders'
    },
    'doctor-note-summarizer': {
        'price': 9,
        'prompt_key': 'doctor_note_summarizer',
        'display': 'AI Doctor Note Summarizer',
        'bundle_id': 'com.appfactory.doctornotesummarizer',
        'app_name': 'DoctorNoteSummarizer',
        'target': 'Patients & caregivers'
    },
    'micro-course-creator': {
        'price': 29,
        'prompt_key': 'micro_course_creator',
        'display': 'AI Micro Course Creator',
        'bundle_id': 'com.appfactory.microcoursecreator',
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
    
    # Customize backend files for the generated app
    config_py = (backend_dir / 'config.py').read_text()
    config_py = config_py.replace('APP_NAME: str = "AI SaaS Backend"', f'APP_NAME: str = "{config["display"]}"')
    (backend_dir / 'config.py').write_text(config_py)

    env_example = (backend_dir / '.env.example').read_text()
    env_example = env_example.replace('APP_NAME="AI SaaS Backend"', f'APP_NAME="{config["display"]}"')
    env_example = env_example.replace('DEFAULT_APP_TYPE=resume_builder', f'DEFAULT_APP_TYPE={config["prompt_key"]}')
    (backend_dir / '.env.example').write_text(env_example)
    
    # Create app-specific README
    (app_dir / 'README.md').write_text(f'''# {config['display']}

Generated from App Factory as a local-first MVP.

## Current backend path

The backend is designed to run locally without paid services.

### Local setup
1. `cd backend`
2. `cp .env.example .env`
3. Leave `AI_PROVIDER=local`
4. Leave `DATABASE_PROVIDER=local`
5. `pip install -r requirements.txt`
6. `uvicorn main:app --reload`

### Example request
`curl -X POST http://localhost:8000/api/v1/generate -H 'Content-Type: application/json' -d '{{"app_type":"{config['prompt_key']}","input":"Create a first draft for {config['display']}","email":"demo@example.com"}}'`

## Notes
- Anthropic is optional, not required
- Stripe and Supabase are optional scaffolding
- iOS template work still needs follow-up before production use

## App metadata
- Bundle ID: {config['bundle_id']}
- Suggested price if you later commercialize it: ${config['price']}/month
''')
    
    # 2. iOS
    print("  iOS app...")
    ios_dir = app_dir / 'iOS'
    shutil.copytree(TEMPLATE_IOS, ios_dir)
    
    # Copy Xcode project template
    xcodeproj_src = TEMPLATE_IOS / 'App.xcodeproj'
    xcodeproj_dst = ios_dir / f'{config["app_name"]}.xcodeproj'
    if xcodeproj_src.exists():
        shutil.copytree(xcodeproj_src, xcodeproj_dst)
        print(f"  ✓ Xcode project created: {xcodeproj_dst}")
    else:
        print(f"  ⚠ Warning: Xcode project template not found at {xcodeproj_src}")
    
    # Rename App to actual app name
    src_app = ios_dir / 'App'
    dst_app = ios_dir / config['app_name']
    if src_app.exists():
        src_app.rename(dst_app)
    
    # Update bundle ID and app name in Info.plist
    info_plist = (dst_app / 'Info.plist').read_text()
    info_plist = info_plist.replace('com.appfactory.resumebuilder', config['bundle_id'])
    info_plist = info_plist.replace('AI Resume Builder', config['display'])
    info_plist = info_plist.replace('AI', config['app_name'])
    (dst_app / 'Info.plist').write_text(info_plist)
    
    # Update Xcode project with bundle ID and app name
    if xcodeproj_dst.exists():
        pbxproj_path = xcodeproj_dst / 'project.pbxproj'
        if pbxproj_path.exists():
            pbxproj = pbxproj_path.read_text()
            # Replace placeholders
            pbxproj = pbxproj.replace('com.appfactory.template', config['bundle_id'])
            pbxproj = pbxproj.replace('PRODUCT_NAME = App;', f'PRODUCT_NAME = {config["app_name"]};')
            pbxproj = pbxproj.replace('name = App;', f'name = {config["app_name"]};')
            pbxproj = pbxproj.replace('path = App;', f'path = {config["app_name"]};')
            pbxproj = pbxproj.replace('INFOPLIST_FILE = App/Info.plist;', f'INFOPLIST_FILE = {config["app_name"]}/Info.plist;')
            pbxproj_path.write_text(pbxproj)
            print(f"  ✓ Updated Xcode project settings")
    
    # Clean up template .xcodeproj if it exists (from copytree)
    template_xcodeproj = ios_dir / 'App.xcodeproj'
    if template_xcodeproj.exists() and template_xcodeproj != xcodeproj_dst:
        shutil.rmtree(template_xcodeproj)
        print(f"  ✓ Cleaned up template Xcode project")
    
    # Update ContentView
    content_view = (dst_app / 'Views' / 'ContentView.swift').read_text()
    content_view = content_view.replace('AI Resume Builder', config['display'])
    (dst_app / 'Views' / 'ContentView.swift').write_text(content_view)
    
    # Create deployment guide
    (app_dir / 'DEPLOYMENT.md').write_text(f'''# Deploying {config['display']}

## Recommended MVP path

Start local first.

### Backend
1. `cd backend`
2. `cp .env.example .env`
3. Keep `AI_PROVIDER=local`
4. Keep `DATABASE_PROVIDER=local`
5. `pip install -r requirements.txt`
6. `uvicorn main:app --reload`

This gives you a working demo backend without Stripe, Supabase, or Anthropic.

## Optional upgrades later

- Anthropic: set `AI_PROVIDER=anthropic` and add `ANTHROPIC_API_KEY`
- Supabase: set `DATABASE_PROVIDER=supabase` and add credentials
- Stripe: set `PAYMENTS_ENABLED=true` and add Stripe keys

## Important

Commercial integrations in this repo are scaffolding only. They are not production-ready billing or app-store workflows.

## iOS

The generated iOS project exists under `iOS/{config['app_name']}/`, but backend rescue was prioritized over full iOS productization.
''')
    
    print(f"✓ Generated {config['display']}")
    print(f"  Location: {app_dir}")
    print(f"  Backend: {backend_dir}")
    print(f"  iOS: {dst_app}")

def main():
    if len(sys.argv) < 2:
        print(" App Factory")
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
