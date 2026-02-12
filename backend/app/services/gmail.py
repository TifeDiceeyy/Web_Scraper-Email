"""Gmail service wrapper for sending emails."""
import os
import sys
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from tools.send_emails import send_emails
from app.models import Campaign, UserSettings
from app.core.security import decrypt_value


class GmailService:
    """Service for sending emails via Gmail."""

    def __init__(self, db: Session):
        self.db = db

    def send_approved_emails(
        self,
        campaign: Campaign,
        user_settings: UserSettings,
        approved_businesses: List[Dict[str, Any]],
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Send emails to approved businesses.

        Args:
            campaign: Campaign object
            user_settings: User settings with Gmail credentials
            approved_businesses: List of businesses with Approved status
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with send statistics

        Raises:
            ValueError: If Gmail credentials not configured
        """
        if not user_settings.gmail_address or not user_settings.gmail_app_password:
            raise ValueError("Gmail credentials not configured for user")

        # Decrypt credentials and set env vars temporarily
        gmail_password = decrypt_value(user_settings.gmail_app_password)

        original_email = os.environ.get("GMAIL_ADDRESS")
        original_password = os.environ.get("GMAIL_APP_PASSWORD")
        original_sheet = os.environ.get("GOOGLE_SPREADSHEET_ID")

        os.environ["GMAIL_ADDRESS"] = user_settings.gmail_address
        os.environ["GMAIL_APP_PASSWORD"] = gmail_password
        os.environ["GOOGLE_SPREADSHEET_ID"] = campaign.google_sheet_id or ""

        try:
            # The send_emails tool will read from sheet and send
            # TODO: Refactor send_emails to accept businesses list directly
            send_emails()

            return {
                "sent": len(approved_businesses),
                "status": "success"
            }

        finally:
            # Restore original env vars
            if original_email:
                os.environ["GMAIL_ADDRESS"] = original_email
            else:
                os.environ.pop("GMAIL_ADDRESS", None)

            if original_password:
                os.environ["GMAIL_APP_PASSWORD"] = original_password
            else:
                os.environ.pop("GMAIL_APP_PASSWORD", None)

            if original_sheet:
                os.environ["GOOGLE_SPREADSHEET_ID"] = original_sheet
            else:
                os.environ.pop("GOOGLE_SPREADSHEET_ID", None)

    async def send_emails_async(
        self,
        campaign: Campaign,
        user_settings: UserSettings,
        approved_businesses: List[Dict[str, Any]],
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Asynchronously send emails with progress updates.

        Args:
            campaign: Campaign object
            user_settings: User settings
            approved_businesses: List of approved businesses
            progress_callback: Callback for WebSocket updates

        Returns:
            Send statistics

        Note:
            Placeholder for async implementation.
        """
        # TODO: Implement async email sending
        return self.send_approved_emails(
            campaign=campaign,
            user_settings=user_settings,
            approved_businesses=approved_businesses,
            progress_callback=progress_callback
        )
