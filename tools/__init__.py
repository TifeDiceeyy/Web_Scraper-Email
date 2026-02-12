"""
Business Outreach Automation Tools

This package contains all execution tools for the WAT framework.
"""

__version__ = "1.0.0"

# Email Generation
from .generate_general_email import generate_general_email
from .generate_specific_email import generate_specific_email

# Data Collection
from .scrape_google_maps import scrape_google_maps
from .scrape_website import scrape_website
from .load_json import load_businesses_from_json
from .scrape_social_media import (
    scrape_instagram_profiles,
    scrape_facebook_pages,
    scrape_tiktok_users,
    scrape_multi_platform
)
from .enrich_contacts import enrich_business_contacts
from .verify_emails import verify_email, verify_email_list, verify_businesses

# Google Sheets Operations
from .upload_to_sheets import upload_businesses
from .get_draft_businesses import get_draft_businesses
from .update_sheet_emails import update_email

# Email Operations
from .send_emails import send_approved_emails

# Response Tracking
from .track_responses import track_email_responses

# Utilities
from .config_manager import ConfigManager
from .notify import (
    send_telegram_notification,
    send_email_notification,
    notify_reply_received,
    notify_campaign_complete
)

__all__ = [
    # Email Generation
    'generate_general_email',
    'generate_specific_email',

    # Data Collection
    'scrape_google_maps',
    'scrape_website',
    'load_businesses_from_json',
    'scrape_instagram_profiles',
    'scrape_facebook_pages',
    'scrape_tiktok_users',
    'scrape_multi_platform',
    'enrich_business_contacts',
    'verify_email',
    'verify_email_list',
    'verify_businesses',

    # Sheets Operations
    'upload_businesses',
    'get_draft_businesses',
    'update_email',

    # Email Operations
    'send_approved_emails',

    # Tracking
    'track_email_responses',

    # Utilities
    'ConfigManager',
    'send_telegram_notification',
    'send_email_notification',
    'notify_reply_received',
    'notify_campaign_complete',
]
