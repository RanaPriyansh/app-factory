"""Prompt catalog used by the generated backend."""

PROMPTS = {
    "resume_builder": {
        "system": "You are an expert resume writer who produces concise, ATS-friendly resumes tailored to job descriptions.",
        "template": """Create a professional resume draft based on the following job description.

Include:
- a short summary
- relevant experience bullet points
- education
- skills

Job Description:
{input}
""",
    },
    "contract_generator": {
        "system": "You are a practical contract drafting assistant for freelancers and small businesses.",
        "template": """Draft a plain-language freelance contract from the project details below.

Include:
- parties
- scope of work
- payment terms
- timeline
- termination
- IP/confidentiality

Project Details:
{input}
""",
    },
    "finance_coach": {
        "system": "You are a cautious financial education assistant. Give general planning guidance, not regulated advice.",
        "template": """Review the financial situation below and provide practical next steps.

Include:
- top priorities
- risks to watch
- 30-day action plan
- questions to ask a licensed professional if needed

Financial Situation:
{input}
""",
    },
    "teacher_assistant": {
        "system": "You are a helpful K-12 teaching assistant who creates usable classroom materials.",
        "template": """Create a lesson-plan draft from the topic below.

Include:
- objectives
- materials
- lesson flow
- differentiation ideas
- assessment
- extension or homework

Topic:
{input}
""",
    },
    "landlord_utility": {
        "system": "You help small landlords review utility usage and identify likely issues or savings opportunities.",
        "template": """Analyze the utility information below.

Include:
- possible anomalies
- likely causes
- savings opportunities
- follow-up actions

Utility Information:
{input}
""",
    },
    "default": {
        "system": "You are a practical AI assistant that turns rough user input into a structured first draft.",
        "template": """Turn the following request into a useful first draft with clear headings and actionable content.

Request:
{input}
""",
    },
}


def get_prompt(app_type: str):
    prompt_data = PROMPTS.get(app_type, PROMPTS["default"])
    return prompt_data["system"], prompt_data["template"]
