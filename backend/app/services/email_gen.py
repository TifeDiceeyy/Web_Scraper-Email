"""Email generation service wrapper using Gemini AI."""
import os
import sys
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from tools.generate_general_email import generate_general_email
from tools.generate_specific_email import generate_specific_email
from app.models import Campaign, UserSettings, OutreachType
from app.core.security import decrypt_value


class EmailGenerationService:
    """Service for generating personalized emails using AI."""

    def __init__(self, db: Session):
        self.db = db

    def generate_email_for_business(
        self,
        campaign: Campaign,
        user_settings: UserSettings,
        business: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Generate email subject and body for a single business.

        Args:
            campaign: Campaign object
            user_settings: User settings with Gemini API key
            business: Business dictionary

        Returns:
            Tuple of (subject, body)
        """
        # Decrypt and set Gemini API key temporarily
        if not user_settings.gemini_api_key:
            raise ValueError("Gemini API key not configured for user")

        gemini_key = decrypt_value(user_settings.gemini_api_key)
        original_key = os.environ.get("GEMINI_API_KEY")
        os.environ["GEMINI_API_KEY"] = gemini_key

        try:
            if campaign.outreach_type == OutreachType.GENERAL_HELP:
                subject, body = generate_general_email(
                    business_name=business.get("name", ""),
                    business_type=campaign.business_type,
                    location=business.get("location", ""),
                    website=business.get("website", ""),
                    website_context=business.get("website_context", "")
                )
            else:  # SPECIFIC_AUTOMATION
                subject, body = generate_specific_email(
                    business_name=business.get("name", ""),
                    business_type=campaign.business_type,
                    automation_focus=campaign.automation_focus or "",
                    location=business.get("location", ""),
                    website=business.get("website", ""),
                    website_context=business.get("website_context", "")
                )

            return subject, body

        finally:
            # Restore original env var
            if original_key:
                os.environ["GEMINI_API_KEY"] = original_key
            else:
                os.environ.pop("GEMINI_API_KEY", None)

    def generate_emails_for_drafts(
        self,
        campaign: Campaign,
        user_settings: UserSettings,
        draft_businesses: List[Dict[str, Any]],
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Generate emails for all draft businesses.

        Args:
            campaign: Campaign object
            user_settings: User settings with API key
            draft_businesses: List of businesses with Draft status
            progress_callback: Optional callback for progress updates

        Returns:
            List of email dictionaries with row, subject, body
        """
        emails = []

        for idx, business in enumerate(draft_businesses):
            try:
                subject, body = self.generate_email_for_business(
                    campaign=campaign,
                    user_settings=user_settings,
                    business=business
                )

                emails.append({
                    "row": business.get("row", idx + 2),  # +2 for header row
                    "subject": subject,
                    "body": body
                })

                # Progress callback
                if progress_callback:
                    progress = (idx + 1) / len(draft_businesses) * 100
                    progress_callback(progress, f"Generated {idx + 1}/{len(draft_businesses)} emails")

            except Exception as e:
                print(f"Error generating email for {business.get('name')}: {e}")
                # Continue with next business
                continue

        return emails

    async def generate_emails_async(
        self,
        campaign: Campaign,
        user_settings: UserSettings,
        draft_businesses: List[Dict[str, Any]],
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously generate emails with progress updates.

        Args:
            campaign: Campaign object
            user_settings: User settings
            draft_businesses: List of draft businesses
            progress_callback: Callback for WebSocket updates

        Returns:
            List of email dictionaries

        Note:
            This is a placeholder for async implementation.
            Would use asyncio for concurrent generation.
        """
        # TODO: Implement async email generation
        # For now, use sync version
        return self.generate_emails_for_drafts(
            campaign=campaign,
            user_settings=user_settings,
            draft_businesses=draft_businesses,
            progress_callback=progress_callback
        )
