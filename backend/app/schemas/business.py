"""Pydantic schemas for business-related operations."""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from uuid import UUID


class BusinessBase(BaseModel):
    """Base business schema."""
    name: str
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None


class BusinessCreate(BusinessBase):
    """Schema for creating/adding a business."""
    pass


class BusinessUpdate(BaseModel):
    """Schema for updating a business (partial)."""
    name: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None


class BusinessWithEmail(BusinessBase):
    """Business with generated email content."""
    generated_subject: Optional[str] = None
    generated_body: Optional[str] = None
    status: str  # Draft, Approved, Sent, Replied

    model_config = ConfigDict(from_attributes=True)


class BusinessBulkUpload(BaseModel):
    """Schema for bulk uploading businesses from JSON."""
    businesses: List[BusinessCreate]


class EmailGenerationRequest(BaseModel):
    """Request to generate emails for a campaign."""
    campaign_id: UUID


class EmailApprovalRequest(BaseModel):
    """Request to approve an email."""
    business_id: str  # Row ID in Google Sheet


class SendEmailsRequest(BaseModel):
    """Request to send approved emails."""
    campaign_id: UUID
