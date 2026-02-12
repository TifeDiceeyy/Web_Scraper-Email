"""Pydantic schemas for campaign-related operations."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.campaign import OutreachType, DataSource, CampaignStatus


class CampaignBase(BaseModel):
    """Base campaign schema."""
    name: str
    business_type: str
    outreach_type: OutreachType
    automation_focus: Optional[str] = None
    data_source: DataSource


class CampaignCreate(CampaignBase):
    """Schema for creating a campaign."""
    pass


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign (partial)."""
    name: Optional[str] = None
    status: Optional[CampaignStatus] = None
    automation_focus: Optional[str] = None


class CampaignResponse(CampaignBase):
    """Schema for campaign response."""
    id: UUID
    user_id: UUID
    google_sheet_id: Optional[str] = None
    status: CampaignStatus
    total_businesses: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignStats(BaseModel):
    """Campaign statistics."""
    total_campaigns: int
    active_campaigns: int
    total_businesses: int
    emails_sent: int
    response_rate: float
