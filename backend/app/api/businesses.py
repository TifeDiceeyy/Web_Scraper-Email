"""Business and email workflow API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import User, Campaign, UserSettings
from app.schemas import (
    BusinessBulkUpload,
    EmailGenerationRequest,
    SendEmailsRequest,
)
from app.dependencies import get_current_user
from app.services import (
    ScraperService,
    EmailGenerationService,
    SheetsService,
    GmailService,
    TrackingService,
)

router = APIRouter(prefix="/api/campaigns", tags=["businesses", "emails"])


@router.post("/{campaign_id}/scrape", status_code=status.HTTP_202_ACCEPTED)
async def scrape_businesses(
    campaign_id: UUID,
    max_results: int = 20,
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Scrape businesses from Google Maps for a campaign (Workflow 1).

    Args:
        campaign_id: Campaign UUID
        max_results: Maximum number of results to scrape
        background_tasks: Background task handler
        current_user: Current authenticated user
        db: Database session

    Returns:
        Task status message
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    # Initialize services
    scraper_service = ScraperService(db)
    sheets_service = SheetsService(db)

    # Scrape businesses
    # TODO: Run this as a background task with WebSocket updates
    businesses = scraper_service.scrape_google_maps_for_campaign(campaign, max_results)

    # Upload to Google Sheet
    sheets_service.upload_businesses(campaign, businesses, user_settings)

    return {
        "status": "completed",
        "campaign_id": str(campaign_id),
        "businesses_scraped": len(businesses),
        "message": f"Scraped and uploaded {len(businesses)} businesses"
    }


@router.post("/{campaign_id}/businesses/upload", status_code=status.HTTP_201_CREATED)
async def upload_businesses_json(
    campaign_id: UUID,
    upload_data: BusinessBulkUpload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload businesses from JSON file.

    Args:
        campaign_id: Campaign UUID
        upload_data: Bulk upload data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Upload status
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    # Convert Pydantic models to dicts
    businesses = [b.model_dump() for b in upload_data.businesses]

    # Upload to sheet
    sheets_service = SheetsService(db)
    sheets_service.upload_businesses(campaign, businesses, user_settings)

    return {
        "status": "success",
        "campaign_id": str(campaign_id),
        "businesses_uploaded": len(businesses)
    }


@router.post("/{campaign_id}/generate-emails", status_code=status.HTTP_202_ACCEPTED)
async def generate_emails(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate emails for all draft businesses in a campaign (Workflow 2).

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Generation status
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    if not user_settings or not user_settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gemini API key not configured. Please update settings."
        )

    # Initialize services
    sheets_service = SheetsService(db)
    email_service = EmailGenerationService(db)

    # Get draft businesses
    draft_businesses = sheets_service.get_draft_businesses(campaign, user_settings)

    if not draft_businesses:
        return {
            "status": "success",
            "campaign_id": str(campaign_id),
            "emails_generated": 0,
            "message": "No draft businesses found"
        }

    # Generate emails
    # TODO: Run as background task with WebSocket updates
    emails = email_service.generate_emails_for_drafts(
        campaign=campaign,
        user_settings=user_settings,
        draft_businesses=draft_businesses
    )

    # Update sheet with generated emails
    sheets_service.update_emails(campaign, emails, user_settings)

    return {
        "status": "completed",
        "campaign_id": str(campaign_id),
        "emails_generated": len(emails),
        "message": f"Generated {len(emails)} emails"
    }


@router.post("/{campaign_id}/send-approved", status_code=status.HTTP_202_ACCEPTED)
async def send_approved_emails(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send all approved emails for a campaign (Workflow 4).

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Send status
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    if not user_settings or not user_settings.gmail_address or not user_settings.gmail_app_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gmail credentials not configured. Please update settings."
        )

    # Initialize services
    gmail_service = GmailService(db)

    # Send emails
    # TODO: Get approved businesses from sheet first
    # TODO: Run as background task with WebSocket updates
    result = gmail_service.send_approved_emails(
        campaign=campaign,
        user_settings=user_settings,
        approved_businesses=[],  # Will be fetched from sheet by send_emails tool
    )

    return {
        "status": "completed",
        "campaign_id": str(campaign_id),
        **result
    }


@router.post("/{campaign_id}/track-responses", status_code=status.HTTP_202_ACCEPTED)
async def track_responses(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Track email responses for a campaign (Workflow 5).

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Tracking status
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    if not user_settings or not user_settings.gmail_address or not user_settings.gmail_app_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gmail credentials not configured. Please update settings."
        )

    # Initialize service
    tracking_service = TrackingService(db)

    # Track responses
    result = tracking_service.track_campaign_responses(campaign, user_settings)

    return {
        "status": "completed",
        "campaign_id": str(campaign_id),
        **result
    }


@router.get("/{campaign_id}/responses")
async def get_campaign_responses(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all responses for a campaign.

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of responses
    """
    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Get user settings
    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    # Get responses
    tracking_service = TrackingService(db)
    responses = tracking_service.get_responses(campaign, user_settings)

    return {
        "campaign_id": str(campaign_id),
        "responses": responses or []
    }
