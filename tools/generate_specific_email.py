#!/usr/bin/env python3
"""
Generate SPECIFIC AUTOMATION emails using Google Gemini API
Strategy: Benefit-driven, lead with value, focus on one solution
"""

import os
import sys
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (
    GEMINI_MODEL, MAX_WEBSITE_CONTEXT_LENGTH,
    AUTOMATION_APPOINTMENT_REMINDERS, AUTOMATION_REVIEW_REQUESTS,
    AUTOMATION_LEAD_FOLLOWUP, AUTOMATION_FEEDBACK_COLLECTION,
    AUTOMATION_INVENTORY_ALERTS
)

load_dotenv()


def validate_api_key():
    """Validate that Gemini API key exists"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    return api_key


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((google_exceptions.GoogleAPIError, Exception))
)
def call_gemini_api(client, prompt):
    """
    Call Gemini API with retry logic

    Args:
        client: Gemini client instance
        prompt: The prompt to send

    Returns:
        API response object

    Raises:
        errors.ClientError: If API request fails after retries
    """
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response
    except google_exceptions.GoogleAPIError as e:
        print(f"⚠️  Gemini API Error (retrying...): {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error calling Gemini API: {e}")
        raise


def parse_email_response(response_text):
    """
    Parse email response from AI with robust error handling

    Args:
        response_text: Raw text from AI response

    Returns:
        tuple: (subject, body)
    """
    subject = ""
    body = ""

    try:
        lines = response_text.strip().split('\n')

        for i, line in enumerate(lines):
            if line.startswith("SUBJECT:"):
                subject = line.replace("SUBJECT:", "").strip()
            elif line.startswith("BODY:"):
                # Everything after BODY: is the body
                body = '\n'.join(lines[i+1:]).strip()
                break

        # Fallback parsing if standard format not found
        if not subject or not body:
            parts = response_text.split("BODY:")
            if len(parts) == 2:
                subject_part = parts[0].replace("SUBJECT:", "").strip()
                subject = subject_part
                body = parts[1].strip()
            else:
                # Last resort: use first line as subject, rest as body
                lines = response_text.strip().split('\n', 1)
                subject = lines[0].replace("SUBJECT:", "").strip()
                body = lines[1].strip() if len(lines) > 1 else response_text

        # Validate that we got both parts
        if not subject:
            subject = "Improve your business operations"
        if not body:
            raise ValueError("Failed to parse email body from AI response")

    except Exception as e:
        print(f"⚠️  Error parsing AI response: {e}")
        # Provide fallback
        subject = "Improve your business operations"
        body = response_text[:500] if response_text else "Email generation failed"

    return subject, body


def get_automation_details(automation_focus, business_type):
    """
    Get specific details about each automation type
    This helps Gemini generate more targeted emails
    """

    automations = {
        AUTOMATION_APPOINTMENT_REMINDERS: f"""
        PAIN POINT: {business_type}s lose revenue from no-shows and late cancellations
        BENEFIT: Reduce no-shows by 30-40% with automated SMS/email reminders
        STATS: Average {business_type} loses $150-300 per no-show
        PROOF: "Dr. Smith reduced no-shows from 15% to 6% in 60 days"
        """,

        AUTOMATION_REVIEW_REQUESTS: f"""
        PAIN POINT: {business_type}s struggle to get consistent 5-star reviews
        BENEFIT: Increase Google reviews by 300% with automated follow-ups
        STATS: 88% of customers will leave a review if asked at the right time
        PROOF: "{business_type} went from 12 reviews to 80+ in 6 months"
        """,

        AUTOMATION_LEAD_FOLLOWUP: f"""
        PAIN POINT: {business_type}s miss potential customers who inquire online
        BENEFIT: Never miss a lead with instant automated follow-up
        STATS: 78% of customers choose the business that responds first
        PROOF: "{business_type} increased conversions by 45% with instant follow-up"
        """,

        AUTOMATION_FEEDBACK_COLLECTION: f"""
        PAIN POINT: {business_type}s don't know what customers really think
        BENEFIT: Get actionable feedback automatically after every appointment
        STATS: Businesses that collect feedback see 25% higher retention
        PROOF: "{business_type} improved service quality score from 3.8 to 4.7"
        """,

        AUTOMATION_INVENTORY_ALERTS: f"""
        PAIN POINT: {business_type}s run out of stock or over-order supplies
        BENEFIT: Never run out of critical supplies with smart alerts
        STATS: Reduces supply costs by 15-20% through better forecasting
        PROOF: "{business_type} cut supply waste by $800/month"
        """
    }

    return automations.get(automation_focus, f"Focus on {automation_focus} benefits for {business_type}s")


def generate_specific_email(business_name, business_type, website_content="", automation_focus=None):
    """
    Generate a benefit-driven email focused on a specific automation

    Args:
        business_name: Name of the business
        business_type: Type of business (e.g., "Dentist", "Restaurant")
        website_content: Scraped website content (optional)
        automation_focus: The specific automation to highlight

    Returns:
        tuple: (subject, body)

    Raises:
        ValueError: If API key is missing
        errors.ClientError: If API call fails after retries
    """

    # Validate API key exists
    api_key = validate_api_key()

    # Configure Gemini
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini client: {e}")

    # Default to appointment reminders if not specified
    if not automation_focus:
        automation_focus = AUTOMATION_APPOINTMENT_REMINDERS

    # Build context from website if available
    website_context = ""
    if website_content:
        website_context = f"\n\nWebsite info:\n{website_content[:MAX_WEBSITE_CONTEXT_LENGTH]}"

    # Get automation-specific details
    automation_details = get_automation_details(automation_focus, business_type)

    # SPECIFIC AUTOMATION PROMPT - Benefit-driven
    prompt = f"""
You are writing a warm outreach email to a {business_type} business called "{business_name}".

STRATEGY: Specific Automation (Focused Approach)
- Lead with a SPECIFIC, CONCRETE BENEFIT
- Focus on ONE automation: {automation_focus}
- Show you understand their pain point
- Include relevant stats or results
- Clear value proposition upfront
- Call-to-action to chat

AUTOMATION FOCUS: {automation_focus}
{automation_details}

TONE:
- Confident but not pushy
- Benefit-driven, not feature-driven
- Show expertise in {business_type} automation
- Personalized to {business_name}

EMAIL STRUCTURE:
1. Hook: Lead with specific benefit/stat
2. Pain point: Show you understand their challenge
3. Solution: Brief mention of the automation
4. Proof: Quick case study or testimonial
5. CTA: Low-pressure invitation to chat

{website_context}

IMPORTANT:
- Subject line: Lead with the benefit (max 60 chars)
- Email body: 120-180 words max
- Use specific numbers/percentages if possible
- Don't be vague - be concrete about the automation
- Focus ONLY on {automation_focus}, don't mention other solutions

Generate the email in this EXACT format:

SUBJECT: [your subject line - must include specific benefit]

BODY:
[your email body]

Start now:
"""

    # Call API with error handling and retry logic
    try:
        response = call_gemini_api(client, prompt)
        response_text = response.text
    except Exception as e:
        print(f"❌ Failed to generate email after retries: {e}")
        # Return a fallback email
        return (
            f"Boost {business_name}'s Efficiency",
            f"Hi {business_name} team,\n\nWe help {business_type}s with {automation_focus}. "
            f"Would you like to learn how we can help improve your operations?\n\nBest regards"
        )

    # Parse response with error handling
    subject, body = parse_email_response(response_text)

    return subject, body


def test_generate_specific_email():
    """Test function"""
    try:
        subject, body = generate_specific_email(
            business_name="Smile Dental",
            business_type="Dentist",
            website_content="Family dentistry serving the community for 20 years. Services: cleanings, fillings, cosmetic dentistry.",
            automation_focus=AUTOMATION_APPOINTMENT_REMINDERS
        )

        print("="*60)
        print("SPECIFIC AUTOMATION EMAIL TEST (Gemini)")
        print("="*60)
        print(f"\nSubject: {subject}")
        print(f"\nBody:\n{body}")
        print("\n" + "="*60)
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_generate_specific_email()
