"""Pydantic schemas for user-related operations."""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for user update."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# User settings schemas
class UserSettingsBase(BaseModel):
    """Base user settings schema."""
    gemini_api_key: Optional[str] = None
    gmail_address: Optional[str] = None
    gmail_app_password: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    notification_method: str = "email"


class UserSettingsCreate(UserSettingsBase):
    """Schema for creating user settings."""
    pass


class UserSettingsUpdate(BaseModel):
    """Schema for updating user settings (partial)."""
    gemini_api_key: Optional[str] = None
    gmail_address: Optional[str] = None
    gmail_app_password: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    notification_method: Optional[str] = None


class UserSettingsResponse(BaseModel):
    """Schema for user settings response (without sensitive data)."""
    user_id: UUID
    gmail_address: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    notification_method: str
    has_gemini_api_key: bool
    has_gmail_app_password: bool
    has_telegram_bot_token: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Token schemas
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[UUID] = None
