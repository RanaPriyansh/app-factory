import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from anthropic import Anthropic
import stripe
from dotenv import load_dotenv
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")

# In-memory store for demo (use database in production)
user_generations = {}  # ip -> count

def get_user_generation_count():
    ip = request.remote_addr
    return user_generations.get(ip, 0)

def increment_generation_count():
    ip = request.remote_addr
    user_generations[ip] = user_generations.get(ip, 0) + 1

def generate_resume_with_claude(job_description, experience):
    """Use Claude API to generate resume content."""
    prompt = f"""You are an expert resume writer. Generate a professional resume tailored for the following job description.
    
Job Description:
{job_description}

Candidate Experience:
{experience}

Please output the resume in the following JSON format:
{{
  "summary": "A 2-3 sentence professional summary",
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "dates": "Date Range",
      "bullets": ["Achievement 1", "Achievement 2", "Achievement 3"]
    }}
  ],
  "education": [
    {{
      "degree": "Degree",
      "school": "School Name",
      "dates": "Date Range"
    }}
  ],
  "skills": ["Skill 1", "Skill 2", "Skill 3"]
}}

Ensure the resume is ATS-friendly and includes relevant keywords from the job description.
"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract JSON from response
        content = response.content[0].text
        # Find JSON in the response (it might be wrapped in ```json ... ```)
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Claude API error: {e}")
        # Fallback response
        return {
            "summary": "Professional with relevant experience.",
            "experience": [],
            "education": [],
            "skills": []
        }

def create_pdf(resume_data):
    """Generate PDF from resume data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50')
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4
    )
    
    elements = []
    
    # Summary
    if resume_data.get('summary'):
        elements.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        elements.append(Paragraph(resume_data['summary'], normal_style))
        elements.append(Spacer(1, 12))
    
    # Experience
    if resume_data.get('experience'):
        elements.append(Paragraph("EXPERIENCE", section_style))
        for exp in resume_data['experience']:
            elements.append(Paragraph(f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}", normal_style))
            elements.append(Paragraph(f"<i>{exp.get('dates', '')}</i>", normal_style))
            for bullet in exp.get('bullets', []):
                elements.append(Paragraph(f"• {bullet}", normal_style))
            elements.append(Spacer(1, 6))
    
    # Education
    if resume_data.get('education'):
        elements.append(Paragraph("EDUCATION", section_style))
        for edu in resume_data['education']:
            elements.append(Paragraph(f"<b>{edu.get('degree', '')}</b> - {edu.get('school', '')}", normal_style))
            elements.append(Paragraph(f"<i>{edu.get('dates', '')}</i>", normal_style))
            elements.append(Spacer(1, 6))
    
    # Skills
    if resume_data.get('skills'):
        elements.append(Paragraph("SKILLS", section_style))
        skills_text = ", ".join(resume_data['skills'])
        elements.append(Paragraph(skills_text, normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    generations = get_user_generation_count()
    return render_template('index.html', 
                         generations=generations,
                         stripe_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/generate', methods=['POST'])
def generate():
    generations = get_user_generation_count()
    if generations >= 1:
        # Check if user has subscription (simplified)
        # In production, check Stripe subscription status
        flash("You've used your free generation. Subscribe for unlimited access.", "warning")
        return redirect(url_for('index'))
    
    job_description = request.form.get('job_description', '').strip()
    experience = request.form.get('experience', '').strip()
    
    if not job_description:
        flash("Please enter a job description.", "error")
        return redirect(url_for('index'))
    
    # Generate resume
    resume_data = generate_resume_with_claude(job_description, experience)
    
    # Create PDF
    pdf_buffer = create_pdf(resume_data)
    
    # Increment generation count
    increment_generation_count()
    
    # Return PDF as download
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mimetype='application/pdf'
    )

@app.route('/subscribe')
def subscribe():
    if not STRIPE_PRICE_ID:
        flash("Payment system not configured.", "error")
        return redirect(url_for('index'))
    
    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + 'cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        logging.error(f"Stripe error: {e}")
        flash("Failed to create checkout session.", "error")
        return redirect(url_for('index'))

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    # In production, verify session and update user subscription status
    flash("Subscription successful! You now have unlimited generations.", "success")
    return redirect(url_for('index'))

@app.route('/cancel')
def cancel():
    flash("Subscription cancelled.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
