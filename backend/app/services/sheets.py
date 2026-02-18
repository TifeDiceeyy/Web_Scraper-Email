"""Google Sheets service wrapper for multi-user campaigns."""
import os
import sys
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from tools.upload_to_sheets import upload_businesses
from tools.get_draft_businesses import get_draft_businesses as get_draft
from tools.update_sheet_emails import update_email
from app.models import Campaign, UserSettings
from app.core.security import decrypt_value


class SheetsService:
    """Service for Google Sheets operations per campaign."""

    def __init__(self, db: Session):
        self.db = db

    def create_campaign_sheet(self, campaign: Campaign, user_settings: UserSettings) -> str:
        """
        Create a new Google Sheet for a campaign.

        Args:
            campaign: Campaign object
            user_settings: User settings with credentials

        Returns:
            Sheet ID

        Note:
            This will need to be implemented with Google Sheets API
            to create a new sheet programmatically.
        """
        # TODO: Implement sheet creation using Google Sheets API
        # For now, user will need to create sheet manually and provide ID
        pass

    def upload_businesses(
        self,
        campaign: Campaign,
        businesses: List[Dict[str, Any]],
        user_settings: UserSettings
    ) -> bool:
        """
        Upload businesses to campaign's Google Sheet.

        Args:
            campaign: Campaign object
            businesses: List of business dictionaries
            user_settings: User settings with credentials

        Returns:
            True if successful
        """
        if not campaign.google_sheet_id:
            raise ValueError("Campaign does not have a Google Sheet ID")

        # Set environment variable temporarily for the tool
        # (In production, refactor tools to accept credentials as parameters)
        original_sheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
        os.environ["GOOGLE_SPREADSHEET_ID"] = campaign.google_sheet_id

        try:
            upload_businesses(businesses)

            # Update campaign total_businesses count
            campaign.total_businesses = len(businesses)
            self.db.commit()

            return True
        finally:
            # Restore original env var
            if original_sheet_id:
                os.environ["GOOGLE_SPREADSHEET_ID"] = original_sheet_id
            else:
                os.environ.pop("GOOGLE_SPREADSHEET_ID", None)

    def get_draft_businesses(
        self,
        campaign: Campaign,
        user_settings: UserSettings
    ) -> List[Dict[str, Any]]:
        """
        Get businesses with 'Draft' status from campaign sheet.

        Args:
            campaign: Campaign object
            user_settings: User settings with credentials

        Returns:
            List of draft businesses
        """
        if not campaign.google_sheet_id:
            raise ValueError("Campaign does not have a Google Sheet ID")

        original_sheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
        os.environ["GOOGLE_SPREADSHEET_ID"] = campaign.google_sheet_id

        try:
            draft_businesses = get_draft()
            return draft_businesses
        finally:
            if original_sheet_id:
                os.environ["GOOGLE_SPREADSHEET_ID"] = original_sheet_id
            else:
                os.environ.pop("GOOGLE_SPREADSHEET_ID", None)

    def update_emails(
        self,
        campaign: Campaign,
        emails: List[Dict[str, Any]],
        user_settings: UserSettings
    ) -> bool:
        """
        Update generated emails in campaign sheet.

        Args:
            campaign: Campaign object
            emails: List of email dictionaries with row, subject, body
            user_settings: User settings with credentials

        Returns:
            True if successful
        """
        if not campaign.google_sheet_id:
            raise ValueError("Campaign does not have a Google Sheet ID")

        original_sheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
        os.environ["GOOGLE_SPREADSHEET_ID"] = campaign.google_sheet_id

        try:
            # Update each email individually
            for email in emails:
                update_email(email['row'], email['subject'], email['body'])
            return True
        finally:
            if original_sheet_id:
                os.environ["GOOGLE_SPREADSHEET_ID"] = original_sheet_id
            else:
                os.environ.pop("GOOGLE_SPREADSHEET_ID", None)

    def get_all_businesses(
        self,
        campaign: Campaign,
        user_settings: UserSettings
    ) -> List[Dict[str, Any]]:
        """
        Get all businesses from campaign sheet.

        Args:
            campaign: Campaign object
            user_settings: User settings with credentials

        Returns:
            List of all businesses
        """
        # TODO: Implement fetching all businesses from sheet
        # This requires reading all rows from the Google Sheet
        pass
