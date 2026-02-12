"""Web scraping service wrapper for campaigns."""
import os
import sys
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from tools.scrape_google_maps import scrape_google_maps
from tools.scrape_website import scrape_website
from app.models import Campaign, UserSettings


class ScraperService:
    """Service for web scraping operations."""

    def __init__(self, db: Session):
        self.db = db

    def scrape_google_maps_for_campaign(
        self,
        campaign: Campaign,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Scrape Google Maps for businesses matching campaign criteria.

        Args:
            campaign: Campaign object
            max_results: Maximum number of results to scrape

        Returns:
            List of business dictionaries

        Note:
            This is a wrapper around the CLI scraper tool.
            In a web context, we might want to:
            1. Run scraping asynchronously
            2. Provide progress updates via WebSocket
            3. Store results immediately in the campaign's Google Sheet
        """
        businesses = scrape_google_maps(
            business_type=campaign.business_type,
            location="",  # TODO: Add location field to Campaign model
            max_results=max_results
        )

        return businesses

    def scrape_website_for_context(self, url: str) -> str:
        """
        Scrape a website for context to personalize emails.

        Args:
            url: Website URL to scrape

        Returns:
            Scraped content as string
        """
        content = scrape_website(url)
        return content

    async def scrape_async(
        self,
        campaign: Campaign,
        max_results: int = 20,
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Asynchronous scraping with progress updates.

        Args:
            campaign: Campaign object
            max_results: Maximum number of results
            progress_callback: Optional callback for progress updates

        Returns:
            List of business dictionaries

        Note:
            This is a placeholder for async scraping implementation.
            Would use asyncio and provide real-time updates via WebSocket.
        """
        # TODO: Implement async scraping with progress updates
        # For now, just call the sync version
        businesses = self.scrape_google_maps_for_campaign(campaign, max_results)
        return businesses
