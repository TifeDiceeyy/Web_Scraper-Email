"""Campaign model for outreach campaigns."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class OutreachType(str, enum.Enum):
    """Outreach strategy types."""
    GENERAL_HELP = "general_help"
    SPECIFIC_AUTOMATION = "specific_automation"


class DataSource(str, enum.Enum):
    """Data source types for campaign businesses."""
    GOOGLE_MAPS = "google_maps"
    JSON_FILE = "json_file"
    MANUAL = "manual"


class CampaignStatus(str, enum.Enum):
    """Campaign status types."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class Campaign(Base):
    """Campaign model for managing outreach campaigns."""

    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Campaign details
    name = Column(String(255), nullable=False)
    business_type = Column(String(255), nullable=False)
    outreach_type = Column(SQLEnum(OutreachType), nullable=False)
    automation_focus = Column(String(255), nullable=True)  # Only for specific_automation
    data_source = Column(SQLEnum(DataSource), nullable=False)

    # Google Sheet integration
    google_sheet_id = Column(String(255), unique=True, nullable=True)  # Created automatically per campaign

    # Status and metrics
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.ACTIVE, nullable=False)
    total_businesses = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="campaigns")

    def __repr__(self):
        return f"<Campaign(id={self.id}, name={self.name}, user_id={self.user_id})>"
