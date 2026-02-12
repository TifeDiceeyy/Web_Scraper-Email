"""
Constants for Business Outreach Automation System
"""

# Outreach Strategies
STRATEGY_GENERAL = "general_help"
STRATEGY_SPECIFIC = "specific_automation"

# Business Status Values
STATUS_DRAFT = "Draft"
STATUS_APPROVED = "Approved"
STATUS_SENT = "Sent"
STATUS_REPLIED = "Replied"
STATUS_BOUNCED = "Bounced"
STATUS_AUTO_REPLY = "Auto-Reply"

# Data Sources
DATA_SOURCE_GOOGLE_MAPS = "google_maps"
DATA_SOURCE_JSON = "json_file"
DATA_SOURCE_MANUAL = "manual"

# Email Configuration
MAX_WEBSITE_CONTEXT_LENGTH = 500  # characters
RATE_LIMIT_DELAY = 5  # seconds between emails
EMAIL_RETRY_ATTEMPTS = 3
EMAIL_RETRY_DELAY = 2  # seconds

# API Configuration
GEMINI_MODEL = "gemini-2.5-flash"
MAX_TOKENS = 1000
API_TIMEOUT = 30  # seconds

# Google Sheets Configuration
SHEET_RANGE = "A2:N"  # Data range (excluding header)
HEADER_RANGE = "A1:N1"  # Header row

# Column Indices (0-based)
COL_BUSINESS_NAME = 0
COL_LOCATION = 1
COL_EMAIL = 2
COL_PHONE = 3
COL_WEBSITE = 4
COL_CONTACT_PERSON = 5
COL_GENERATED_SUBJECT = 6
COL_GENERATED_BODY = 7
COL_NOTES = 8
COL_STATUS = 9
COL_DATE_APPROVED = 10
COL_DATE_SENT = 11
COL_LAST_RESPONSE = 12
COL_RESPONSE_DETAILS = 13

# Validation Limits
MAX_BUSINESS_TYPE_LENGTH = 50
MAX_AUTOMATION_NAME_LENGTH = 100
MIN_EMAIL_LENGTH = 5
MAX_EMAIL_LENGTH = 100

# Automation Types
AUTOMATION_APPOINTMENT_REMINDERS = "Appointment Reminder System"
AUTOMATION_REVIEW_REQUESTS = "Review Request Automation"
AUTOMATION_LEAD_FOLLOWUP = "Lead Follow-up System"
AUTOMATION_FEEDBACK_COLLECTION = "Customer Feedback Collection"
AUTOMATION_INVENTORY_ALERTS = "Inventory Alerts"

# File Paths
CONFIG_FILENAME = "campaign_config.json"
LOG_FILENAME = "outreach.log"
