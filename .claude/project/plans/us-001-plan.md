# Implementation Plan: US-001 Business Outreach Automation System

**Status:** ✅ Approved → In Progress
**User Story:** [US-001: Business Outreach Automation System](../features/us-001-business-outreach-automation.md)
**Created:** 2026-02-12

---

## 1. Requirements Summary

**User Story:** As a business development professional, I want an automated system that scrapes business data, generates personalized emails using AI, and tracks responses, so that I can scale my outreach efforts without manual email writing and follow-up tracking.

**Acceptance Criteria Summary:**
- ✅ Campaign setup with strategy selection (General Help vs Specific Automation)
- ✅ Multi-source data collection (Google Maps, JSON, manual)
- ✅ AI-powered email generation with two distinct strategies
- ✅ Google Sheets integration for data storage and review
- ✅ Gmail sending with rate limiting
- ✅ Automated response tracking with notifications
- ✅ Comprehensive error handling

**Scope:**

**In Scope:**
- WAT Framework architecture (Workflows, Agents, Tools)
- Two email generation strategies with different tones
- Google Sheets for data storage and manual review
- Gmail API for sending and tracking
- Website scraping for context
- Telegram/Email notifications
- Campaign configuration persistence

**Out of Scope:**
- CRM integration
- A/B testing analytics
- Automated follow-up sequences
- Custom email templates beyond two strategies
- Multi-language support

---

## 2. Technical Approach

**Solution Overview:**

The system implements the WAT (Workflows, Agents, Tools) Framework:

1. **Workflows** (Markdown files in `workflows/`): Define WHAT to do
   - SOPs for each phase (campaign setup, email generation, sending, tracking)
   - Two distinct email generation workflows based on strategy

2. **Agent** (`agent.py`): Decides HOW to execute
   - Main orchestrator with menu system
   - Contains critical decision logic (`ask_outreach_type()`)
   - Saves decisions to `campaign_config.json`
   - Calls appropriate tools based on workflow

3. **Tools** (Python scripts in `tools/`): Execute tasks
   - Separate tools for general vs specific email generation
   - Modular, reusable components
   - Each tool can be tested independently

**Key Decisions:**

| Decision | Rationale |
|----------|-----------|
| Google Sheets instead of SQLite | User can easily review/edit emails in familiar interface; no need for custom UI |
| Two separate email generation tools | Cleaner separation of concerns; easier to maintain different prompts |
| Campaign config in JSON file | Persists decision across sessions; easy to read/modify |
| Gmail API over SMTP | Better integration with Google Sheets; unified OAuth; reply tracking built-in |
| Google Gemini API | Free tier available; high-quality email generation; unified Google ecosystem; good at personalization |
| BeautifulSoup for scraping | Lightweight; sufficient for most websites; easy to use |

**Dependencies:**

- Python 3.11+
- Google Gemini API (email generation)
- Google Cloud APIs (Sheets + Gmail)
- Telegram Bot API (optional notifications)
- External Google Maps scraper (Outscraper or Apify)

---

## 3. Database Changes

**Google Sheets Structure:**

Since we're using Google Sheets instead of a traditional database, here's the schema:

**Sheet Name:** `Outreach Campaign - [Business Type]`

**Columns:**

| Column | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| Business Name | Text | Yes | - | Name of the business |
| Location | Text | No | - | City/address |
| Email | Email | Yes | - | Contact email address |
| Phone | Text | No | - | Phone number |
| Website | URL | No | - | Business website |
| Contact Person | Text | No | - | Name of contact |
| Generated Subject | Text | No | - | AI-generated email subject |
| Generated Body | Long Text | No | - | AI-generated email body |
| Your Notes | Long Text | No | - | User's manual notes |
| Status | Enum | Yes | "Draft" | Draft/Approved/Sent/Replied/Invalid |
| Date Approved | Timestamp | No | - | When user approved email |
| Date Sent | Timestamp | No | - | When email was sent |
| Last Response | Timestamp | No | - | When reply was received |
| Response Details | Long Text | No | - | Preview of reply content |

**Status Values:**
- `Draft` - Initial state after data collection or email generation
- `Approved` - User has reviewed and approved for sending
- `Sent` - Email has been sent successfully
- `Replied` - Business has replied to the email
- `Invalid` - Invalid email address or other issues

**Sheet Setup:**
```python
# Create header row
headers = [
    "Business Name", "Location", "Email", "Phone", "Website",
    "Contact Person", "Generated Subject", "Generated Body",
    "Your Notes", "Status", "Date Approved", "Date Sent",
    "Last Response", "Response Details"
]

# Format header row
# - Bold text
# - Background color
# - Freeze first row
# - Set column widths
```

**No migrations needed** - Google Sheets API creates the structure programmatically.

---

## 4. API Layer

**API Integrations:**

### 4.1 Google Gemini API

**Model:** `gemini-1.5-flash` or `gemini-1.5-pro`

**Request Structure:**
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content(
    prompt,
    generation_config={
        'temperature': 0.7,
        'max_output_tokens': 1024,
    }
)
```

**Response Structure:**
```python
{
    "text": '{"subject": "...", "body": "..."}'
}
```

**Two Different Prompts:**

**General Help Strategy:**
```python
prompt = f"""
Generate a discovery-focused email for {business_name}.

Business Type: {business_type}
Website Context: {website_data}

Requirements:
- Subject: Friendly question about their business
- Body: Ask about problems, offer general help
- Tone: Curious, non-sales-y
- Length: 3-4 short paragraphs
- End with: Would you have 15 minutes for a call?

IMPORTANT: Return ONLY valid JSON in this exact format:
{{"subject": "your subject here", "body": "your email body here"}}
"""
```

**Specific Automation Strategy:**
```python
prompt = f"""
Generate a benefit-driven email for {business_name}.

Business Type: {business_type}
Automation Focus: {automation_focus}
Website Context: {website_data}

Requirements:
- Subject: Lead with specific benefit (e.g., "Reduce no-shows by 30%")
- Body: Focus on ONE automation benefit
- Tone: Confident, solution-focused
- Include: Specific metric or time savings
- Length: 2-3 paragraphs
- End with: 15-minute conversation offer

IMPORTANT: Return ONLY valid JSON in this exact format:
{{"subject": "your subject here", "body": "your email body here"}}
"""
```

### 4.2 Google Sheets API

**Endpoints:**
- `spreadsheets.values.append()` - Add businesses to sheet
- `spreadsheets.values.get()` - Read businesses from sheet
- `spreadsheets.values.update()` - Update email content, status, timestamps
- `spreadsheets.batchUpdate()` - Format header row

**Example Operations:**
```python
# Read all businesses with Status = "Draft"
def get_draft_businesses():
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range='A2:N1000'  # Skip header row
    ).execute()
    rows = result.get('values', [])
    return [row for row in rows if row[9] == 'Draft']  # Column 9 = Status

# Update email content
def update_email(row_number, subject, body):
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f'G{row_number}:H{row_number}',  # Subject and Body columns
        valueInputOption='RAW',
        body={'values': [[subject, body]]}
    ).execute()
```

### 4.3 Gmail API

**Endpoints:**
- `POST /gmail/v1/users/me/messages/send` - Send email
- `GET /gmail/v1/users/me/messages` - List messages (for tracking)
- `GET /gmail/v1/users/me/messages/{id}` - Get message details

**Send Email:**
```python
from email.mime.text import MIMEText
import base64

def send_email(to_email, subject, body):
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
```

### 4.4 Website Scraping

**Library:** BeautifulSoup4

**Function:**
```python
def scrape_website(url):
    """
    Extracts key information from business website.

    Returns:
    {
        "title": str,
        "description": str,
        "services": List[str],
        "about_text": str
    }
    """
```

**Extracted Data:**
- Page title
- Meta description
- Services/offerings (from headings, lists)
- About section text
- Contact information

---

## 5. Component Architecture

**Project Structure:**

```
Web_Scraper&Email/
├── agent.py                          # Main orchestrator
├── .env                              # API keys and configuration
├── .env.example                      # Template for environment variables
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── workflows/                        # Workflow instructions (markdown)
│   ├── start_campaign.md             # Campaign initialization workflow
│   ├── generate_emails.md            # Email generation (2 strategies)
│   ├── send_emails.md                # Email sending workflow
│   ├── track_responses.md            # Response tracking workflow
│   └── manage_sheet.md               # Google Sheets management
│
├── tools/                            # Execution layer (Python scripts)
│   ├── __init__.py
│   ├── generate_general_email.py     # Strategy 1: General Help
│   ├── generate_specific_email.py    # Strategy 2: Specific Automation
│   ├── scrape_website.py             # Website content scraper
│   ├── upload_to_sheets.py           # Add businesses to Google Sheets
│   ├── get_draft_businesses.py       # Get Draft status businesses
│   ├── update_sheet_emails.py        # Update email content in sheet
│   ├── send_emails.py                # Send via Gmail API
│   ├── track_responses.py            # Monitor Gmail for replies
│   ├── notify.py                     # Send Telegram/email notifications
│   ├── load_json.py                  # Load businesses from JSON
│   ├── scrape_google_maps.py         # Google Maps integration
│   └── config_manager.py             # Read/write campaign config
│
├── .tmp/                             # Temporary files (in .gitignore)
│   ├── campaign_config.json          # Current campaign settings
│   ├── website_cache.json            # Cached website scrape results
│   └── credentials_token.pickle      # Google OAuth token
│
├── data/                             # Sample/test data
│   └── sample_businesses.json        # Test data
│
└── tests/                            # Unit tests
    ├── test_email_generation.py
    ├── test_scraping.py
    └── test_sheets_integration.py
```

**Key Components:**

### agent.py (Main Orchestrator)

```python
class OutreachAgent:
    def __init__(self):
        self.load_config()

    def main_menu(self):
        """
        Display menu:
        1. Start New Campaign
        2. Generate Emails
        3. Manage Google Sheet
        4. Send Approved Emails
        5. Track Responses
        6. Exit
        """

    def ask_outreach_type(self):
        """
        CRITICAL DECISION POINT

        Returns: "general_help" or "specific_automation"
        Saves to campaign_config.json
        """

    def start_campaign(self):
        """
        Workflow:
        1. Ask business type
        2. Ask outreach strategy → ask_outreach_type()
        3. If specific: Ask which automation
        4. Ask data source
        5. Save config
        6. Upload businesses to sheet
        """

    def generate_emails(self):
        """
        Workflow:
        1. Read campaign_config.json
        2. Get all Draft businesses from sheet
        3. For each business:
           - Scrape website (if URL present)
           - Call appropriate tool based on strategy
           - Update sheet with subject/body
        """

    def send_approved_emails(self):
        """
        Workflow:
        1. Get all Approved businesses
        2. For each:
           - Send via Gmail API
           - Wait 5 seconds
           - Update status to Sent
           - Record timestamp
        """
```

### tools/generate_general_email.py

```python
import google.generativeai as genai
import json
import os

def generate_general_help_email(business_name, business_type, website_context=""):
    """
    Calls Gemini API with discovery-focused prompt.

    Args:
        business_name: str
        business_type: str
        website_context: str (optional)

    Returns:
        {
            "subject": str,
            "body": str
        }
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Generate a discovery-focused outreach email...
    [Full prompt as defined in section 4.1]
    """

    response = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.7,
            'max_output_tokens': 1024,
        }
    )

    # Parse JSON from response
    # Clean response text (remove markdown code blocks if present)
    text = response.text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:].strip()

    result = json.loads(text)
    return result
```

### tools/generate_specific_email.py

```python
import google.generativeai as genai
import json
import os

def generate_specific_automation_email(business_name, business_type, automation_focus, website_context=""):
    """
    Calls Gemini API with benefit-driven prompt.

    Args:
        business_name: str
        business_type: str
        automation_focus: str (e.g., "Appointment Scheduling")
        website_context: str (optional)

    Returns:
        {
            "subject": str,
            "body": str
        }
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Generate a benefit-driven outreach email...
    [Full prompt as defined in section 4.1]
    """

    response = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.7,
            'max_output_tokens': 1024,
        }
    )

    # Parse JSON from response with cleanup
    text = response.text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:].strip()

    result = json.loads(text)
    return result
```

---

## 6. State Management

**Configuration Files:**

### .tmp/campaign_config.json

```json
{
  "business_type": "Dentists",
  "outreach_type": "specific_automation",
  "automation_focus": "Appointment Scheduling",
  "data_source": "google_maps",
  "created_at": "2026-02-12T10:30:00Z",
  "sheet_id": "abc123..."
}
```

**Purpose:** Persists the critical decision (outreach strategy) across sessions.

**Usage:**
- Written by `agent.py` during campaign setup
- Read by email generation tools to determine which prompt to use
- Updated when new campaign starts

### .env File

```bash
# Google Gemini API
GOOGLE_API_KEY=AIzaSy...

# Google APIs (Sheets + Gmail)
GOOGLE_SPREADSHEET_ID=1abc...
GOOGLE_CREDENTIALS_FILE=credentials.json

# Gmail (for sending)
GMAIL_ADDRESS=your-email@gmail.com

# Notifications
NOTIFICATION_METHOD=telegram  # or "email"
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789
```

**State Flow:**

```
User Decision
    ↓
agent.py → ask_outreach_type()
    ↓
Save to campaign_config.json
    ↓
Later: generate_emails() reads config
    ↓
Calls correct tool (general or specific)
    ↓
Email generated with appropriate strategy
```

---

## 7. Edge Cases & Error Handling

**Identified Edge Cases:**

### Data Collection
- [ ] **Empty/missing website URL**: Skip scraping, generate email without context
- [ ] **Invalid website URL**: Log error, continue with next business
- [ ] **Website scraping timeout**: Set 10-second timeout, continue without context
- [ ] **Website blocks scraping**: Handle 403/429 errors gracefully

### Email Generation
- [ ] **Gemini API timeout**: Retry with exponential backoff (3 attempts)
- [ ] **Gemini returns invalid JSON**: Parse with fallback cleanup (remove markdown code blocks), or mark for manual review
- [ ] **API rate limit hit**: Wait and retry based on rate limit headers
- [ ] **Empty email generated**: Log error, keep status as Draft

### Google Sheets
- [ ] **Duplicate businesses**: Check Business Name + Email before adding
- [ ] **Sheet not found**: Create new sheet with proper headers
- [ ] **OAuth token expired**: Re-authenticate user
- [ ] **Quota exceeded**: Log error, pause operations

### Email Sending
- [ ] **Invalid email address**: Validate format before sending, mark as "Invalid"
- [ ] **Gmail sending limit reached**: Track count, stop at 450/day (buffer), notify user
- [ ] **Email bounce**: Log but continue (can't detect immediately via API)
- [ ] **Network error during send**: Retry once, then mark as failed

### Response Tracking
- [ ] **False positive reply detection**: Filter out automated responses (out-of-office, etc.)
- [ ] **Multiple replies from same business**: Update with latest response
- [ ] **Reply to different email thread**: Log but don't match to campaign

**Error Handling Strategy:**

```python
# API calls with retry logic
def call_gemini_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(...)
            return response
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise

# Validation
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outreach.log'),
        logging.StreamHandler()
    ]
)
```

---

## 8. Testing Strategy

**Test Types:**

### Unit Tests
- [ ] `test_email_generation.py` - Test both email generation strategies
- [ ] `test_scraping.py` - Test website scraper with mock HTML
- [ ] `test_config_manager.py` - Test reading/writing campaign config
- [ ] `test_validation.py` - Test email validation, duplicate detection

### Integration Tests
- [ ] Google Sheets API - Create test sheet, add/update/read rows
- [ ] Gemini API - Generate emails with real API
- [ ] Gmail API - Send test email to self

### End-to-End Test
- [ ] Complete flow with 3 sample businesses:
  1. Start campaign (General Help strategy)
  2. Add 3 businesses manually
  3. Generate emails
  4. Review in Google Sheet
  5. Approve one email
  6. Send approved email
  7. Verify email received

**Key Test Cases:**

1. **General Help Email Generation**
   - Input: Business name, type, website context
   - Expected: Discovery-focused tone, question format, non-sales-y
   - Verify: Subject mentions business, body asks about problems

2. **Specific Automation Email Generation**
   - Input: Business name, type, automation focus, website context
   - Expected: Benefit-driven tone, specific metric, focused
   - Verify: Subject includes benefit, body focuses on one automation

3. **Strategy Decision Persistence**
   - Start campaign with "General Help"
   - Check campaign_config.json has `"outreach_type": "general_help"`
   - Generate email
   - Verify `generate_general_email.py` was called

4. **Rate Limiting**
   - Queue 10 approved emails
   - Send all
   - Verify 5-second delay between each send
   - Check total time is ~50 seconds

5. **Error Recovery**
   - Mock Claude API to return invalid JSON
   - Verify system logs error and continues
   - Check business status remains "Draft"

**Coverage Target:** 80%+

**Testing Tools:**
- `pytest` - Test runner
- `pytest-mock` - Mocking
- `pytest-cov` - Coverage reporting
- `responses` - Mock HTTP requests

---

## 9. Implementation Checklist

### Phase 1: Project Setup (2 hours)
- [ ] Create virtual environment
- [ ] Install dependencies (`requirements.txt`)
- [ ] Set up `.env` file with API keys
- [ ] Create project structure (folders: workflows, tools, .tmp, data, tests)
- [ ] Set up `.gitignore` (ignore `.env`, `.tmp/*`, `*.pickle`)
- [ ] Initialize git repository

### Phase 2: Google APIs Setup (1 hour)
- [ ] Create Google Cloud project
- [ ] Enable Google Sheets API
- [ ] Enable Gmail API
- [ ] Create OAuth 2.0 credentials (Desktop app)
- [ ] Download `credentials.json`
- [ ] Test OAuth flow with simple script

### Phase 3: Core Agent Structure (3 hours)
- [ ] Create `agent.py` with menu system
- [ ] Implement `ask_outreach_type()` - THE CRITICAL DECISION
- [ ] Create `tools/config_manager.py` (read/write campaign config)
- [ ] Test: Start campaign, save config, verify JSON file

### Phase 4: Google Sheets Integration (4 hours)
- [ ] Create `tools/upload_to_sheets.py`
  - [ ] Create sheet with proper headers
  - [ ] Format header row (bold, freeze, colors)
  - [ ] Add businesses with Status = "Draft"
- [ ] Create `tools/get_draft_businesses.py`
  - [ ] Read all rows with Status = "Draft"
  - [ ] Return as list of dictionaries
- [ ] Create `tools/update_sheet_emails.py`
  - [ ] Update Subject and Body columns
  - [ ] Update Status column
  - [ ] Update timestamp columns
- [ ] Test: Add 3 businesses, read them back, update one

### Phase 5: Website Scraping (3 hours)
- [ ] Create `tools/scrape_website.py`
  - [ ] Fetch page with requests
  - [ ] Parse with BeautifulSoup
  - [ ] Extract: title, description, services, about text
  - [ ] Handle timeouts and errors
  - [ ] Cache results in `.tmp/website_cache.json`
- [ ] Test with 5 different websites

### Phase 6: Email Generation - General Help (4 hours)
- [ ] Create `tools/generate_general_email.py`
  - [ ] Build discovery-focused prompt
  - [ ] Call Claude API
  - [ ] Parse JSON response
  - [ ] Handle errors (retry logic)
- [ ] Create workflow: `workflows/generate_emails.md` (Path A section)
- [ ] Test: Generate 5 general help emails, verify tone

### Phase 7: Email Generation - Specific Automation (4 hours)
- [ ] Create `tools/generate_specific_email.py`
  - [ ] Build benefit-driven prompt
  - [ ] Call Claude API
  - [ ] Parse JSON response
  - [ ] Handle errors
- [ ] Update workflow: `workflows/generate_emails.md` (Path B section)
- [ ] Test: Generate 5 specific emails, verify different tone

### Phase 8: Campaign Workflow Integration (3 hours)
- [ ] Implement `agent.start_campaign()`
  - [ ] Ask business type
  - [ ] Call `ask_outreach_type()` → CRITICAL DECISION
  - [ ] If specific: ask which automation
  - [ ] Ask data source
  - [ ] Save to campaign_config.json
- [ ] Implement `agent.generate_emails()`
  - [ ] Read campaign_config.json
  - [ ] Get Draft businesses from sheet
  - [ ] For each business:
    - [ ] Scrape website
    - [ ] Call correct tool based on outreach_type
    - [ ] Update sheet with email content
- [ ] Create `workflows/start_campaign.md`
- [ ] Test: Full campaign setup → email generation flow

### Phase 9: Email Sending (4 hours)
- [ ] Create `tools/send_emails.py`
  - [ ] Get Approved businesses from sheet
  - [ ] Send via Gmail API
  - [ ] Wait 5 seconds between sends
  - [ ] Update Status to "Sent"
  - [ ] Record Date Sent timestamp
  - [ ] Handle sending errors
- [ ] Implement `agent.send_approved_emails()`
- [ ] Create `workflows/send_emails.md`
- [ ] Test: Send 3 emails to self, verify timing

### Phase 10: Response Tracking (5 hours)
- [ ] Create `tools/track_responses.py`
  - [ ] Query Gmail API for messages since last check
  - [ ] Match replies to sent emails
  - [ ] Filter out auto-responses
  - [ ] Update sheet: Status = "Replied", timestamps, preview
- [ ] Create `tools/notify.py`
  - [ ] Send Telegram notification
  - [ ] OR send email notification
  - [ ] Include: business name, reply preview
- [ ] Implement `agent.track_responses()`
- [ ] Create `workflows/track_responses.md`
- [ ] Test: Send email to self, reply, verify detection

### Phase 11: Data Loading Options (3 hours)
- [ ] Create `tools/load_json.py`
  - [ ] Load businesses from JSON file
  - [ ] Validate structure
  - [ ] Upload to sheet
- [ ] Create `tools/scrape_google_maps.py`
  - [ ] Integration with Outscraper/Apify API
  - [ ] OR instructions for manual export
- [ ] Create `data/sample_businesses.json` for testing
- [ ] Test: Load businesses from JSON

### Phase 12: Workflows Documentation (2 hours)
- [ ] Write `workflows/start_campaign.md` (complete)
- [ ] Write `workflows/generate_emails.md` (both paths)
- [ ] Write `workflows/send_emails.md`
- [ ] Write `workflows/track_responses.md`
- [ ] Write `workflows/manage_sheet.md`

### Phase 13: Error Handling & Logging (3 hours)
- [ ] Add logging to all tools
- [ ] Implement retry logic for API calls
- [ ] Add email validation
- [ ] Add duplicate business detection
- [ ] Handle quota limits gracefully
- [ ] Create user-friendly error messages

### Phase 14: Testing (4 hours)
- [ ] Write unit tests for each tool
- [ ] Write integration tests for APIs
- [ ] Run end-to-end test with sample data
- [ ] Test both email strategies
- [ ] Test error scenarios
- [ ] Verify rate limiting works

### Phase 15: Documentation & Polish (2 hours)
- [ ] Create `README.md` with setup instructions
- [ ] Create `.env.example` template
- [ ] Add code comments
- [ ] Test setup flow from scratch
- [ ] Create sample data files

---

## 10. Effort & Risks

**Complexity:** High

**Total Estimated Time:** 47 hours (~6 days full-time, ~2 weeks part-time)

**Breakdown:**
- Setup & APIs: 6 hours
- Core implementation: 25 hours
- Testing: 4 hours
- Documentation: 4 hours
- Polish & debugging: 8 hours

**Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Google Maps scraping requires paid service | High | Medium | Provide JSON import option + manual entry; recommend Outscraper free tier |
| Claude API costs exceed budget | Medium | High | Track API usage; implement caching for website context; use smaller model for testing |
| Gmail sending limits block scaling | Medium | Medium | Document limits clearly; add counter to prevent hitting limit; suggest Google Workspace upgrade |
| Google OAuth setup confusing for users | Medium | Medium | Create detailed setup guide with screenshots; provide troubleshooting section |
| Email generation quality inconsistent | Low | High | Test extensively; refine prompts; add examples to prompt; implement quality checks |
| Reply detection has false positives | Medium | Low | Filter out common auto-responses; add manual review option; log all detections |
| Website scraping blocked by sites | High | Low | Handle gracefully; generate emails without context; don't block on scraping failures |

**Critical Path:**
1. Google APIs setup (blocker for everything)
2. Campaign config system (needed for strategy decision)
3. Email generation tools (core value)
4. Google Sheets integration (data layer)

**Notes:**

- **The critical decision point** (`ask_outreach_type()`) is the heart of this system - everything else flows from it
- Start with manual data entry and JSON import; add Google Maps scraping later
- Test both email strategies extensively to ensure clear differentiation in tone
- Consider starting with just one strategy (General Help) for MVP, add Specific Automation in v2
- Gmail API quota is generous but track usage to avoid surprises
- Website scraping is "nice to have" - system works without it

---

**Plan Status:** ✅ Ready for Review

**Next Steps After Approval:**
1. Set up development environment
2. Begin Phase 1: Project Setup
3. Implement in order of checklist (dependencies respected)

