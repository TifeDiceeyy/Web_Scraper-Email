#!/usr/bin/env python3
"""
Environment Validation Script
Checks that all required environment variables are set correctly
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def check_env_var(name, required=True, validate_fn=None):
    """
    Check if environment variable exists and optionally validate it

    Args:
        name: str - Environment variable name
        required: bool - Whether this variable is required
        validate_fn: callable - Optional validation function

    Returns:
        tuple: (bool, str) - (is_valid, message)
    """
    value = os.getenv(name)

    if value is None or value == "":
        if required:
            return False, f"❌ {name}: NOT SET (required)"
        else:
            return True, f"⚠️  {name}: Not set (optional)"

    # Check if it's still the placeholder value
    placeholders = [
        "your-", "your_", "xxx", "example", "test", "placeholder",
        "here", "todo", "replace"
    ]
    if any(placeholder in value.lower() for placeholder in placeholders):
        if required:
            return False, f"❌ {name}: Still using placeholder value"
        else:
            return True, f"⚠️  {name}: Still using placeholder value (optional)"

    # Run custom validation if provided
    if validate_fn:
        is_valid, error_msg = validate_fn(value)
        if not is_valid:
            return False, f"❌ {name}: {error_msg}"

    return True, f"✅ {name}: Set correctly"


def validate_email(value):
    """Validate email format"""
    if '@' not in value or '.' not in value:
        return False, "Invalid email format"
    return True, ""


def validate_sheet_id(value):
    """Validate Google Sheets ID format"""
    if len(value) < 20:
        return False, "Sheet ID too short (should be ~44 characters)"
    if value.startswith("http"):
        return False, "Use Sheet ID only, not full URL"
    return True, ""


def validate_file_exists(value):
    """Check if file exists"""
    if not Path(value).exists():
        return False, f"File not found: {value}"
    return True, ""


def validate_notification_method(value):
    """Validate notification method"""
    valid_methods = ['telegram', 'email', '']
    if value.lower() not in valid_methods:
        return False, f"Must be 'telegram' or 'email', not '{value}'"
    return True, ""


def main():
    """Run all environment validations"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print("🔍 ENVIRONMENT VALIDATION")
    print(f"{'='*60}{Colors.RESET}\n")

    # Define all environment variables to check
    checks = [
        # Required for AI email generation
        ("GEMINI_API_KEY", True, lambda v: (len(v) > 20, "API key seems too short")),

        # Required for Google Sheets
        ("GOOGLE_SPREADSHEET_ID", True, validate_sheet_id),
        ("GOOGLE_CREDENTIALS_FILE", True, validate_file_exists),

        # Required for Gmail sending
        ("GMAIL_ADDRESS", True, validate_email),
        ("GMAIL_APP_PASSWORD", True, lambda v: (len(v) == 16, "App password should be 16 characters")),

        # Optional but recommended for notifications
        ("NOTIFICATION_METHOD", False, validate_notification_method),
        ("TELEGRAM_BOT_TOKEN", False, None),
        ("TELEGRAM_CHAT_ID", False, None),
        ("NOTIFICATION_EMAIL", False, validate_email),

        # Optional for Google Maps scraping
        ("OUTSCRAPER_API_KEY", False, None),
    ]

    results = []
    all_valid = True

    print(f"{Colors.BOLD}Required Variables:{Colors.RESET}\n")

    for name, required, validate_fn in checks:
        if required:
            is_valid, message = check_env_var(name, required, validate_fn)
            results.append((name, is_valid, message))
            if is_valid:
                print(f"  {Colors.GREEN}{message}{Colors.RESET}")
            else:
                print(f"  {Colors.RED}{message}{Colors.RESET}")
                all_valid = False

    print(f"\n{Colors.BOLD}Optional Variables:{Colors.RESET}\n")

    for name, required, validate_fn in checks:
        if not required:
            is_valid, message = check_env_var(name, required, validate_fn)
            results.append((name, is_valid, message))
            if is_valid:
                print(f"  {Colors.YELLOW}{message}{Colors.RESET}")
            else:
                print(f"  {Colors.YELLOW}{message}{Colors.RESET}")

    # Summary
    print(f"\n{Colors.BOLD}{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}{Colors.RESET}\n")

    required_count = sum(1 for _, req, _ in checks if req)
    valid_required = sum(1 for (_, req, _), (_, valid, _) in zip(checks, results) if req and valid)

    print(f"Required variables: {valid_required}/{required_count}")

    if all_valid:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All required environment variables are set correctly!{Colors.RESET}")
        print(f"\n{Colors.BLUE}You're ready to run:{Colors.RESET}")
        print(f"  {Colors.BOLD}python agent.py{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some required environment variables are missing or invalid.{Colors.RESET}")
        print(f"\n{Colors.YELLOW}To fix:{Colors.RESET}")
        print(f"  1. Copy .env.example to .env: {Colors.BOLD}cp .env.example .env{Colors.RESET}")
        print(f"  2. Edit .env and replace placeholder values")
        print(f"  3. Run this script again: {Colors.BOLD}python validate_env.py{Colors.RESET}\n")

        print(f"{Colors.YELLOW}Quick setup guide:{Colors.RESET}")
        print(f"  - GEMINI_API_KEY: Get from https://aistudio.google.com/apikey")
        print(f"  - GOOGLE_SPREADSHEET_ID: Create a Google Sheet, copy ID from URL")
        print(f"  - GOOGLE_CREDENTIALS_FILE: Download from Google Cloud Console")
        print(f"  - GMAIL_ADDRESS: Your Gmail address")
        print(f"  - GMAIL_APP_PASSWORD: Generate at https://myaccount.google.com/apppasswords")
        print()

        return 1


if __name__ == "__main__":
    sys.exit(main())
