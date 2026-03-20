# Technical Architecture - AI Resume Builder MVP

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐    ┌──────────┐│
│  │  Landing  │────▶│   Job    │────▶│   User   │───▶│  Resume  ││
│  │   Page    │     │  Input   │     │  Details  │    │ Generate ││
│  └──────────┘     └──────────┘     └──────────┘    └──────────┘│
│       │                                              │          │
│       │              ┌───────────────────────────────┘          │
│       ▼              ▼                                          │
│  ┌──────────┐  ┌──────────┐     ┌──────────┐    ┌──────────┐  │
│  │  Sign Up │  │  Resume  │────▶│   Edit   │───▶│   PDF    │  │
│  │  /Login  │  │ Preview  │     │  Resume  │    │  Export  │  │
│  └──────────┘  └──────────┘     └──────────┘    └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      TECH STACK                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    BUBBLE.IO (Frontend + Backend)            ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ││
│  │  │    Pages    │  │  Workflows  │  │    API      │         ││
│  │  │   (React)   │  │   (Logic)   │  │  Connector  │         ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    EXTERNAL SERVICES                         ││
│  │                                                             ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ││
│  │  │  Supabase   │  │ Claude API  │  │   Stripe    │         ││
│  │  │  (DB+Auth)  │  │   (AI)      │  │ (Payments)  │         ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Bubble.io)
**Responsibilities:**
- User interface rendering
- Form inputs and validation
- Resume preview display
- PDF generation trigger
- Authentication UI

**Key Pages:**
- Landing/Marketing page
- Sign Up / Login
- Job Description Input
- Resume Builder/Editor
- Resume Preview
- User Dashboard
- Pricing/Upgrade
- Account Settings

### 2. Backend (Bubble.io API Workflows)
**Responsibilities:**
- API endpoint management
- Business logic execution
- External API orchestration
- Usage tracking
- Paywall enforcement

**Key Workflows:**
- `generate-resume`: Send job desc to Claude, process response
- `extract-keywords`: Parse job description for ATS keywords
- `create-pdf`: Convert resume data to PDF
- `check-subscription`: Verify user's subscription status
- `track-usage`: Log resume generation for rate limiting

### 3. Database (Supabase/PostgreSQL)

**Tables:**

#### users (extends Supabase auth.users)
```sql
id UUID PRIMARY KEY (references auth.users)
full_name TEXT
phone TEXT
created_at TIMESTAMP
updated_at TIMESTAMP
subscription_status TEXT DEFAULT 'free'
stripe_customer_id TEXT
free_resumes_used INTEGER DEFAULT 0
```

#### resumes
```sql
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
user_id UUID REFERENCES users(id)
title TEXT
job_description TEXT
resume_data JSONB
pdf_url TEXT
created_at TIMESTAMP
updated_at TIMESTAMP
is_archived BOOLEAN DEFAULT false
```

#### resume_sections
```sql
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
resume_id UUID REFERENCES resumes(id)
section_type TEXT (summary, experience, education, skills, projects)
content JSONB
sort_order INTEGER
created_at TIMESTAMP
```

#### experience_entries
```sql
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
resume_id UUID REFERENCES resumes(id)
company_name TEXT
job_title TEXT
start_date DATE
end_date DATE
is_current BOOLEAN
description TEXT
achievements JSONB
sort_order INTEGER
```

#### subscriptions
```sql
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
user_id UUID REFERENCES users(id)
stripe_subscription_id TEXT
plan TEXT (free, pro)
status TEXT (active, canceled, past_due)
current_period_start TIMESTAMP
current_period_end TIMESTAMP
created_at TIMESTAMP
```

### 4. AI Integration (Claude API)

**Endpoint:** `POST https://api.anthropic.com/v1/messages`

**Request Flow:**
1. User submits job description
2. Bubble sends to Claude API with structured prompt
3. Claude returns JSON-formatted resume content
4. Bubble parses and displays in editor
5. User edits if needed
6. PDF generated from final data

**Prompt Strategy:**
- System prompt with resume best practices
- Job description as user input
- Structured JSON output format
- ATS optimization instructions

### 5. Payment Integration (Stripe)

**Products:**
- Free Tier: 1 resume/month
- Pro Plan: $9/month - unlimited resumes

**Webhook Events:**
- `checkout.session.completed` → Activate subscription
- `customer.subscription.updated` → Update status
- `customer.subscription.deleted` → Downgrade to free
- `invoice.payment_failed` → Handle failed payment

## Data Flow

### Resume Generation Flow
```
1. User Input (Job Description)
   ↓
2. Bubble API Workflow triggered
   ↓
3. Check user subscription/resume count
   ↓
4. If limit reached → Show upgrade modal
   ↓
5. If allowed → Send to Claude API
   ↓
6. Parse Claude response (JSON)
   ↓
7. Store in Supabase (resumes table)
   ↓
8. Display editable preview
   ↓
9. User edits (optional)
   ↓
10. Generate PDF via Bubble plugin
   ↓
11. Store PDF URL in Supabase
   ↓
12. Increment user's resume count
```

### Authentication Flow
```
1. User signs up (email/password or Google OAuth)
   ↓
2. Supabase Auth creates user record
   ↓
3. Bubble creates user profile in users table
   ↓
4. Session token stored in Bubble
   ↓
5. Protected routes check auth status
```

## Security Considerations

1. **API Keys**: Store Claude API key in Bubble environment variables
2. **Row Level Security**: Enable RLS on all Supabase tables
3. **Stripe Webhooks**: Verify webhook signatures
4. **Rate Limiting**: Implement per-user rate limits on AI calls
5. **Data Validation**: Validate all inputs before processing

## Performance Targets

| Metric | Target |
|--------|--------|
| Page Load | < 2 seconds |
| Resume Generation | < 15 seconds |
| PDF Export | < 5 seconds |
| Database Query | < 200ms |
| API Response | < 500ms |

## Scalability Notes

- Bubble can handle ~10,000 concurrent users on Professional plan
- Supabase free tier: 500MB database, 1GB storage, 50K monthly active users
- Claude API: Rate limits based on tier (recommend starting with Tier 1)
- Consider caching common job descriptions to reduce API calls

---
*Architecture Version: 1.0 | Last updated: March 17, 2026*
