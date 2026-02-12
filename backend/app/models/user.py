"""User model for authentication and user management."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User model for multi-user authentication."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class UserSettings(Base):
    """User settings for API keys and credentials (encrypted)."""

    __tablename__ = "user_settings"

    user_id = Column(UUID(as_uuid=True), primary_key=True)

    # Encrypted API keys and credentials
    gemini_api_key = Column(Text, nullable=True)  # Encrypted
    gmail_address = Column(String(255), nullable=True)
    gmail_app_password = Column(Text, nullable=True)  # Encrypted
    telegram_bot_token = Column(Text, nullable=True)  # Encrypted
    telegram_chat_id = Column(String(255), nullable=True)

    # Preferences
    notification_method = Column(String(50), default="email", nullable=False)  # email | telegram

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="settings")

    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id})>"
