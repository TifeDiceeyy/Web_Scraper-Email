#!/usr/bin/env python3
"""
Generate GENERAL HELP emails using Google Gemini API
Strategy: Discovery-focused, ask about problems, offer broad help
"""

import os
import sys
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import GEMINI_MODEL, MAX_WEBSITE_CONTEXT_LENGTH

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
            subject = "Quick question about your business"
        if not body:
            raise ValueError("Failed to parse email body from AI response")

    except Exception as e:
        print(f"⚠️  Error parsing AI response: {e}")
        # Provide fallback
        subject = "Quick question about your business"
        body = response_text[:500] if response_text else "Email generation failed"

    return subject, body


def generate_general_email(business_name, business_type, website_content="", automation_focus=None):
    """
    Generate a discovery-focused email that asks about problems

    Args:
        business_name: Name of the business
        business_type: Type of business (e.g., "Dentist", "Restaurant")
        website_content: Scraped website content (optional)
        automation_focus: Not used in general strategy, but kept for consistency

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

    # Build context from website if available
    website_context = ""
    if website_content:
        website_context = f"\n\nWebsite info:\n{website_content[:MAX_WEBSITE_CONTEXT_LENGTH]}"

    # GENERAL HELP PROMPT - Discovery-focused
    prompt = f"""
You are writing a cold outreach email to a {business_type} business called "{business_name}".

STRATEGY: General Help (Discovery Approach)
- Your goal is to START A CONVERSATION, not sell anything
- Ask about their current challenges or pain points
- Offer general help with business automation
- Be genuinely curious about their operations
- Don't mention specific solutions yet
- Keep it short and non-pushy

TONE:
- Friendly and conversational
- Curious, not sales-y
- Personal, not template-like
- Respectful of their time

EMAIL STRUCTURE:
1. Brief intro (who you are)
2. Why you're reaching out (interested in helping {business_type}s)
3. Ask 1-2 open-ended questions about their challenges
4. Offer to chat if they're interested
5. Easy out (no pressure)

{website_context}

IMPORTANT:
- Subject line: Keep it casual and curiosity-driven (max 50 chars)
- Email body: 100-150 words max
- Don't mention specific automation tools
- Don't lead with benefits or stats
- Ask, don't tell

Generate the email in this EXACT format:

SUBJECT: [your subject line]

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
            f"Quick question about {business_name}",
            f"Hi {business_name} team,\n\nI help {business_type}s streamline their operations. "
            f"Would you be open to a brief chat about any challenges you're facing?\n\nBest regards"
        )

    # Parse response with error handling
    subject, body = parse_email_response(response_text)

    return subject, body


def test_generate_general_email():
    """Test function"""
    try:
        subject, body = generate_general_email(
            business_name="Smile Dental",
            business_type="Dentist",
            website_content="Family dentistry serving the community for 20 years. Services: cleanings, fillings, cosmetic dentistry."
        )

        print("="*60)
        print("GENERAL HELP EMAIL TEST (Gemini)")
        print("="*60)
        print(f"\nSubject: {subject}")
        print(f"\nBody:\n{body}")
        print("\n" + "="*60)
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_generate_general_email()
