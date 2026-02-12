#!/usr/bin/env python3
"""
Input validation utilities for the outreach system
"""

import re
from pathlib import Path
from logger import logger


def validate_business_type(business_type):
    """
    Validate business type input

    Args:
        business_type: User input for business type

    Returns:
        tuple: (is_valid, error_message)
    """
    if not business_type:
        return False, "Business type cannot be empty"

    if len(business_type) < 1:
        return False, "Business type must be at least 1 character"

    if len(business_type) > 50:
        return False, "Business type must be 50 characters or less"

    # Check for reasonable characters (letters, spaces, hyphens)
    if not re.match(r'^[a-zA-Z\s\-&]+$', business_type):
        return False, "Business type can only contain letters, spaces, hyphens, and ampersands"

    return True, None


def validate_email(email):
    """
    Validate email address format

    Args:
        email: Email address to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False, "Invalid email format. Expected: user@domain.com"

    if len(email) > 254:  # RFC 5321
        return False, "Email address is too long (max 254 characters)"

    return True, None


def validate_file_path(file_path, must_exist=True):
    """
    Validate file path

    Args:
        file_path: Path to validate
        must_exist: Whether file must already exist

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file_path:
        return False, "File path cannot be empty"

    path = Path(file_path)

    if must_exist and not path.exists():
        return False, f"File not found: {file_path}"

    if must_exist and not path.is_file():
        return False, f"Path is not a file: {file_path}"

    return True, None


def validate_integer(value, min_val=None, max_val=None):
    """
    Validate integer input

    Args:
        value: Value to validate
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)

    Returns:
        tuple: (is_valid, error_message, parsed_value)
    """
    try:
        parsed = int(value)

        if min_val is not None and parsed < min_val:
            return False, f"Value must be at least {min_val}", None

        if max_val is not None and parsed > max_val:
            return False, f"Value must be at most {max_val}", None

        return True, None, parsed

    except ValueError:
        return False, f"Invalid number: {value}", None


def validate_choice(choice, valid_choices):
    """
    Validate user menu choice

    Args:
        choice: User's choice
        valid_choices: List of valid options (e.g., ["1", "2", "3"])

    Returns:
        tuple: (is_valid, error_message)
    """
    if choice not in valid_choices:
        return False, f"Invalid choice. Please select from: {', '.join(valid_choices)}"

    return True, None


def validate_location(location):
    """
    Validate location input

    Args:
        location: Location string (e.g., "San Francisco, CA")

    Returns:
        tuple: (is_valid, error_message)
    """
    if not location:
        return False, "Location cannot be empty"

    if len(location) < 2:
        return False, "Location must be at least 2 characters"

    if len(location) > 100:
        return False, "Location must be 100 characters or less"

    return True, None


def get_validated_input(prompt, validator, **validator_kwargs):
    """
    Get user input with validation loop

    Args:
        prompt: Prompt to display to user
        validator: Validation function to use
        **validator_kwargs: Additional arguments for validator

    Returns:
        Validated input value
    """
    while True:
        value = input(prompt).strip()

        result = validator(value, **validator_kwargs)

        # Handle different return formats
        if len(result) == 2:  # (is_valid, error_message)
            is_valid, error_message = result
            parsed_value = value
        elif len(result) == 3:  # (is_valid, error_message, parsed_value)
            is_valid, error_message, parsed_value = result
        else:
            raise ValueError(f"Validator returned unexpected format: {result}")

        if is_valid:
            return parsed_value
        else:
            logger.warning(f"❌ {error_message}")
            print(f"❌ {error_message}")
