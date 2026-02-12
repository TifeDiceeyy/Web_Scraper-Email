#!/usr/bin/env python3
"""
Verify email addresses before sending
Uses multiple validation techniques:
1. Syntax validation (RFC 5322)
2. Domain validation (DNS MX records)
3. Disposable email detection
"""

import re
import dns.resolver
from email_validator import validate_email, EmailNotValidError


# Common disposable email domains
DISPOSABLE_DOMAINS = {
    'tempmail.com', 'guerrillamail.com', 'mailinator.com',
    '10minutemail.com', 'throwaway.email', 'temp-mail.org'
}


def is_valid_syntax(email):
    """
    Check if email has valid syntax

    Args:
        email: Email address string

    Returns:
        bool: True if syntax is valid
    """

    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def has_mx_record(domain):
    """
    Check if domain has valid MX (mail exchange) records

    Args:
        domain: Domain name (e.g., 'gmail.com')

    Returns:
        bool: True if MX records exist
    """

    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return False


def is_disposable(email):
    """
    Check if email is from a disposable email service

    Args:
        email: Email address string

    Returns:
        bool: True if disposable
    """

    domain = email.split('@')[-1].lower()
    return domain in DISPOSABLE_DOMAINS


def verify_email(email, check_dns=True):
    """
    Comprehensive email verification

    Args:
        email: Email address to verify
        check_dns: Whether to check DNS MX records (slower but more thorough)

    Returns:
        dict: Verification result with status and details
    """

    result = {
        'email': email,
        'valid': False,
        'reason': '',
        'checks': {
            'syntax': False,
            'dns': False,
            'disposable': False,
        }
    }

    # Skip empty emails
    if not email or not email.strip():
        result['reason'] = 'Empty email address'
        return result

    email = email.strip().lower()

    # 1. Syntax validation
    if not is_valid_syntax(email):
        result['reason'] = 'Invalid email syntax'
        return result

    result['checks']['syntax'] = True

    # 2. Check for disposable email
    if is_disposable(email):
        result['reason'] = 'Disposable email address'
        result['checks']['disposable'] = True
        return result

    # 3. DNS validation (optional)
    if check_dns:
        domain = email.split('@')[-1]
        if not has_mx_record(domain):
            result['reason'] = 'No MX records found for domain'
            return result
        result['checks']['dns'] = True

    # All checks passed
    result['valid'] = True
    result['reason'] = 'Valid email address'

    return result


def verify_email_list(emails, check_dns=True, show_progress=True):
    """
    Verify a list of email addresses

    Args:
        emails: List of email addresses
        check_dns: Whether to check DNS (slower)
        show_progress: Whether to print progress

    Returns:
        dict: Results with valid/invalid counts and details
    """

    if show_progress:
        print("\n✉️  EMAIL VERIFICATION")
        print("=" * 60)
        print(f"📊 Verifying {len(emails)} email addresses...")
        if check_dns:
            print("⏳ DNS validation enabled (this may take a moment)...")

    results = {
        'valid': [],
        'invalid': [],
        'total': len(emails),
        'valid_count': 0,
        'invalid_count': 0,
    }

    for i, email in enumerate(emails, 1):
        if show_progress and i % 10 == 0:
            print(f"   Processed {i}/{len(emails)}...")

        verification = verify_email(email, check_dns=check_dns)

        if verification['valid']:
            results['valid'].append(email)
            results['valid_count'] += 1
        else:
            results['invalid'].append({
                'email': email,
                'reason': verification['reason']
            })
            results['invalid_count'] += 1

    if show_progress:
        print("\n" + "=" * 60)
        print(f"✅ Valid emails: {results['valid_count']}")
        print(f"❌ Invalid emails: {results['invalid_count']}")
        print(f"📊 Success rate: {results['valid_count']/results['total']*100:.1f}%")

        if results['invalid']:
            print(f"\n⚠️  Invalid emails:")
            for item in results['invalid'][:5]:  # Show first 5
                print(f"   • {item['email']}: {item['reason']}")
            if len(results['invalid']) > 5:
                print(f"   ... and {len(results['invalid']) - 5} more")

    return results


def verify_businesses(businesses, check_dns=True):
    """
    Verify emails in a list of business dictionaries

    Args:
        businesses: List of business dicts with 'email' field
        check_dns: Whether to check DNS

    Returns:
        list: Businesses with verified emails only
    """

    print("\n🔍 BUSINESS EMAIL VERIFICATION")
    print("=" * 60)

    businesses_with_email = [
        b for b in businesses
        if b.get('email') and b['email'].strip()
    ]

    if not businesses_with_email:
        print("⚠️  No businesses with email addresses to verify")
        return businesses

    print(f"📊 Verifying {len(businesses_with_email)} business emails...")

    verified_businesses = []
    invalid_businesses = []

    for business in businesses_with_email:
        email = business.get('email', '').strip()
        verification = verify_email(email, check_dns=check_dns)

        if verification['valid']:
            business['email_verified'] = True
            business['email_status'] = 'valid'
            verified_businesses.append(business)
        else:
            business['email_verified'] = False
            business['email_status'] = verification['reason']
            invalid_businesses.append(business)

    # Add businesses without emails (not verified)
    businesses_without_email = [
        b for b in businesses
        if not b.get('email') or not b['email'].strip()
    ]

    print("\n" + "=" * 60)
    print(f"✅ Valid: {len(verified_businesses)}")
    print(f"❌ Invalid: {len(invalid_businesses)}")
    print(f"⚠️  No email: {len(businesses_without_email)}")

    if invalid_businesses:
        print(f"\n❌ Invalid emails found:")
        for b in invalid_businesses[:3]:
            print(f"   • {b['name']}: {b['email']} ({b['email_status']})")

    # Return all businesses, but mark verification status
    return verified_businesses + invalid_businesses + businesses_without_email


def test_email_verification():
    """Test function"""

    test_emails = [
        'valid@gmail.com',
        'invalid-email',
        'test@tempmail.com',
        'business@nonexistentdomain12345.com',
        '',
    ]

    print("Testing individual emails:")
    for email in test_emails:
        result = verify_email(email, check_dns=False)
        status = "✅" if result['valid'] else "❌"
        print(f"{status} {email or '(empty)'}: {result['reason']}")

    print("\n" + "=" * 60)

    # Test with business list
    test_businesses = [
        {'name': 'Valid Business', 'email': 'contact@example.com'},
        {'name': 'Invalid Business', 'email': 'bad-email'},
        {'name': 'No Email Business', 'email': ''},
    ]

    verified = verify_businesses(test_businesses, check_dns=False)


if __name__ == "__main__":
    # Note: Requires installation of dependencies
    try:
        test_email_verification()
    except ImportError as e:
        print(f"⚠️  Missing dependency: {e}")
        print("Install with: pip install dnspython email-validator")
