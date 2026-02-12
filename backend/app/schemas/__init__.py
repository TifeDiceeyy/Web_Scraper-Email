"""Pydantic schemas for API validation."""
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserSettingsCreate,
    UserSettingsUpdate,
    UserSettingsResponse,
    Token,
    TokenData,
)
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignStats,
)
from app.schemas.business import (
    BusinessCreate,
    BusinessUpdate,
    BusinessWithEmail,
    BusinessBulkUpload,
    EmailGenerationRequest,
    EmailApprovalRequest,
    SendEmailsRequest,
)

__all__ = [
    # User
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserSettingsCreate",
    "UserSettingsUpdate",
    "UserSettingsResponse",
    "Token",
    "TokenData",
    # Campaign
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CampaignStats",
    # Business
    "BusinessCreate",
    "BusinessUpdate",
    "BusinessWithEmail",
    "BusinessBulkUpload",
    "EmailGenerationRequest",
    "EmailApprovalRequest",
    "SendEmailsRequest",
]
