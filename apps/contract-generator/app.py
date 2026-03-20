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

# In-memory store for demo
user_generations = {}

def get_user_generation_count():
    ip = request.remote_addr
    return user_generations.get(ip, 0)

def increment_generation_count():
    ip = request.remote_addr
    user_generations[ip] = user_generations.get(ip, 0) + 1

def generate_contract_with_claude(project_description, client_details, freelancer_details):
    """Use Claude API to generate contract content."""
    prompt = f"""You are an expert freelance contract writer. Generate a comprehensive freelance contract for the following project.

Project Description:
{project_description}

Client Details:
{client_details}

Freelancer Details:
{freelancer_details}

Please output the contract in the following JSON format:
{{
  "title": "Freelance Service Agreement",
  "parties": {{
    "client": "Client Name and Address",
    "freelancer": "Freelancer Name and Address"
  }},
  "project_scope": "Detailed description of the project scope and deliverables",
  "timeline": {{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "milestones": [
      {{
        "description": "Milestone description",
        "due_date": "YYYY-MM-DD",
        "payment_amount": "Amount"
      }}
    ]
  }},
  "payment_terms": {{
    "total_amount": "Total project amount",
    "payment_schedule": "Description of payment schedule",
    "late_fee": "Late payment fee percentage"
  }},
  "intellectual_property": "Who owns the final deliverables",
  "confidentiality": "Confidentiality terms",
  "termination": "Termination conditions",
  "liability": "Liability limitations",
  "general_terms": "Other standard contract terms"
}}

Ensure the contract is legally sound for freelance work and includes standard protections for both parties.
"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Claude API error: {e}")
        return {
            "title": "Freelance Service Agreement",
            "parties": {"client": "", "freelancer": ""},
            "project_scope": "",
            "timeline": {},
            "payment_terms": {},
            "intellectual_property": "",
            "confidentiality": "",
            "termination": "",
            "liability": "",
            "general_terms": ""
        }

def create_contract_pdf(contract_data):
    """Generate PDF from contract data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.HexColor('#2c3e50')
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph(contract_data.get('title', 'Freelance Service Agreement'), title_style))
    elements.append(Spacer(1, 20))
    
    # Parties
    elements.append(Paragraph("PARTIES", section_style))
    parties = contract_data.get('parties', {})
    elements.append(Paragraph(f"<b>Client:</b> {parties.get('client', '')}", normal_style))
    elements.append(Paragraph(f"<b>Freelancer:</b> {parties.get('freelancer', '')}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Project Scope
    elements.append(Paragraph("PROJECT SCOPE", section_style))
    elements.append(Paragraph(contract_data.get('project_scope', ''), normal_style))
    elements.append(Spacer(1, 12))
    
    # Timeline
    timeline = contract_data.get('timeline', {})
    if timeline:
        elements.append(Paragraph("TIMELINE", section_style))
        elements.append(Paragraph(f"<b>Start Date:</b> {timeline.get('start_date', '')}", normal_style))
        elements.append(Paragraph(f"<b>End Date:</b> {timeline.get('end_date', '')}", normal_style))
        milestones = timeline.get('milestones', [])
        if milestones:
            elements.append(Paragraph("<b>Milestones:</b>", normal_style))
            for i, milestone in enumerate(milestones, 1):
                elements.append(Paragraph(f"{i}. {milestone.get('description', '')} - Due: {milestone.get('due_date', '')} - ${milestone.get('payment_amount', '')}", normal_style))
        elements.append(Spacer(1, 12))
    
    # Payment Terms
    payment = contract_data.get('payment_terms', {})
    if payment:
        elements.append(Paragraph("PAYMENT TERMS", section_style))
        elements.append(Paragraph(f"<b>Total Amount:</b> ${payment.get('total_amount', '')}", normal_style))
        elements.append(Paragraph(f"<b>Payment Schedule:</b> {payment.get('payment_schedule', '')}", normal_style))
        elements.append(Paragraph(f"<b>Late Fee:</b> {payment.get('late_fee', '')}% per month", normal_style))
        elements.append(Spacer(1, 12))
    
    # Intellectual Property
    elements.append(Paragraph("INTELLECTUAL PROPERTY", section_style))
    elements.append(Paragraph(contract_data.get('intellectual_property', ''), normal_style))
    elements.append(Spacer(1, 12))
    
    # Confidentiality
    elements.append(Paragraph("CONFIDENTIALITY", section_style))
    elements.append(Paragraph(contract_data.get('confidentiality', ''), normal_style))
    elements.append(Spacer(1, 12))
    
    # Termination
    elements.append(Paragraph("TERMINATION", section_style))
    elements.append(Paragraph(contract_data.get('termination', ''), normal_style))
    elements.append(Spacer(1, 12))
    
    # Liability
    elements.append(Paragraph("LIABILITY", section_style))
    elements.append(Paragraph(contract_data.get('liability', ''), normal_style))
    elements.append(Spacer(1, 12))
    
    # General Terms
    elements.append(Paragraph("GENERAL TERMS", section_style))
    elements.append(Paragraph(contract_data.get('general_terms', ''), normal_style))
    
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
        flash("You've used your free generation. Subscribe for unlimited access.", "warning")
        return redirect(url_for('index'))
    
    project_description = request.form.get('project_description', '').strip()
    client_details = request.form.get('client_details', '').strip()
    freelancer_details = request.form.get('freelancer_details', '').strip()
    
    if not project_description:
        flash("Please enter a project description.", "error")
        return redirect(url_for('index'))
    
    # Generate contract
    contract_data = generate_contract_with_claude(project_description, client_details, freelancer_details)
    
    # Create PDF
    pdf_buffer = create_contract_pdf(contract_data)
    
    # Increment generation count
    increment_generation_count()
    
    # Return PDF as download
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mimetype='application/pdf'
    )

@app.route('/subscribe')
def subscribe():
    if not STRIPE_PRICE_ID:
        flash("Payment system not configured.", "error")
        return redirect(url_for('index'))
    
    try:
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
    flash("Subscription successful! You now have unlimited generations.", "success")
    return redirect(url_for('index'))

@app.route('/cancel')
def cancel():
    flash("Subscription cancelled.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
