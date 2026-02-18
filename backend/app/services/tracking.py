"""Email response tracking service."""
import os
import sys
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from tools.track_responses import track_email_responses
from app.models import Campaign, UserSettings
from app.core.security import decrypt_value


class TrackingService:
    """Service for tracking email responses."""

    def __init__(self, db: Session):
        self.db = db

    def track_campaign_responses(
        self,
        campaign: Campaign,
        user_settings: UserSettings
    ) -> Dict[str, Any]:
        """
        Track responses for a campaign.

        Args:
            campaign: Campaign object
            user_settings: User settings with Gmail credentials

        Returns:
            Dictionary with tracking results
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
            # Run tracking
            track_email_responses()

            # TODO: Return detailed tracking results
            return {
                "status": "success",
                "message": "Response tracking completed"
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

    def get_responses(
        self,
        campaign: Campaign,
        user_settings: UserSettings
    ) -> List[Dict[str, Any]]:
        """
        Get all responses for a campaign.

        Args:
            campaign: Campaign object
            user_settings: User settings

        Returns:
            List of response dictionaries

        Note:
            This would read from the Google Sheet to get all
            businesses with "Replied" status and their response details.
        """
        # TODO: Implement reading responses from sheet
        pass
