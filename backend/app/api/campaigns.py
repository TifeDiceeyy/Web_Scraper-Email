"""Campaign API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import User, Campaign, CampaignStatus
from app.schemas import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignStats
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new campaign.

    Args:
        campaign_data: Campaign creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created campaign object
    """
    # Validate automation_focus is provided for specific_automation
    if campaign_data.outreach_type == "specific_automation" and not campaign_data.automation_focus:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="automation_focus is required for specific_automation outreach type"
        )

    # Create campaign
    campaign = Campaign(
        user_id=current_user.id,
        name=campaign_data.name,
        business_type=campaign_data.business_type,
        outreach_type=campaign_data.outreach_type,
        automation_focus=campaign_data.automation_focus,
        data_source=campaign_data.data_source,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    # TODO: Create Google Sheet for this campaign (will be done in service layer)

    return campaign


@router.get("", response_model=List[CampaignResponse])
async def list_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: CampaignStatus = None
):
    """
    List all campaigns for the current user.

    Args:
        current_user: Current authenticated user
        db: Database session
        status_filter: Optional status filter

    Returns:
        List of campaigns
    """
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)

    if status_filter:
        query = query.filter(Campaign.status == status_filter)

    campaigns = query.order_by(Campaign.created_at.desc()).all()
    return campaigns


@router.get("/stats", response_model=CampaignStats)
async def get_campaign_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get campaign statistics for the current user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Campaign statistics
    """
    all_campaigns = db.query(Campaign).filter(Campaign.user_id == current_user.id).all()

    total_campaigns = len(all_campaigns)
    active_campaigns = len([c for c in all_campaigns if c.status == CampaignStatus.ACTIVE])
    total_businesses = sum(c.total_businesses for c in all_campaigns)

    # TODO: Get emails_sent and response_rate from Google Sheets
    emails_sent = 0
    response_rate = 0.0

    return CampaignStats(
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        total_businesses=total_businesses,
        emails_sent=emails_sent,
        response_rate=response_rate,
    )


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific campaign by ID.

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Campaign object

    Raises:
        HTTPException: If campaign not found or access denied
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: UUID,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a campaign.

    Args:
        campaign_id: Campaign UUID
        campaign_data: Campaign update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated campaign object

    Raises:
        HTTPException: If campaign not found or access denied
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Update fields
    update_data = campaign_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)

    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a campaign.

    Args:
        campaign_id: Campaign UUID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If campaign not found or access denied
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    db.delete(campaign)
    db.commit()

    # TODO: Delete associated Google Sheet
