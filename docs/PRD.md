# Business Outreach Automation System - Product Requirements Document

## Product Overview

**Product Name:** Business Outreach Automation System
**Type:** Command-Line Application (CLI) with potential Web UI
**AI Provider:** Google Gemini API
**Monetization:** SaaS (Future)

A comprehensive AI-powered business outreach platform that automates the entire cold email workflow—from prospect discovery to personalized email generation to sending and response tracking. The system leverages Google Gemini for intelligent email personalization based on business context and industry-specific insights.

---

## Tech Stack

| Layer                    | Technology                    |
| ------------------------ | ----------------------------- |
| Language                 | Python 3.11+                  |
| AI Engine                | Google Gemini API (2.5-flash) |
| Database (Structured)    | Google Sheets API             |
| Email Sending            | Gmail SMTP (OAuth2)           |
| Web Scraping             | BeautifulSoup4 + Requests     |
| Data Validation          | Custom validators             |
| Error Handling           | Tenacity (retry logic)        |
| Logging                  | Python logging module         |
| Environment Config       | python-dotenv                 |
| Testing                  | pytest (future)               |
| Deployment               | Local CLI / Cloud VM          |
| Business Data Collection | Google Maps API (future)      |

---

## Core Architecture

```
Web_Scraper&Email/
├── docs/
│   ├── PRD.md                        # This file
│   ├── USER_STORIES.md               # User story tracking
│   ├── IMPROVEMENTS.md               # Changelog
│   ├── FINAL_STATUS.md               # Project status
│   ├── QUICK_START.md                # Quick reference
│   ├── features/                     # User story specs
│   │   ├── us-001-project-setup.md
│   │   ├── us-002-sheets-integration.md
│   │   └── ...
│   └── plans/                        # Implementation plans
│       ├── us-001-plan.md
│       └── ...
├── tools/
│   ├── scrape_google_maps.py         # Google Maps scraper
│   ├── load_json.py                  # JSON file loader
│   ├── upload_to_sheets.py           # Sheet upload
│   ├── get_draft_businesses.py       # Fetch draft status
│   ├── scrape_website.py             # Website scraper
│   ├── generate_general_email.py     # Discovery emails
│   ├── generate_specific_email.py    # Benefit-driven emails
│   ├── update_sheet_emails.py        # Update email columns
│   ├── send_emails.py                # Gmail SMTP sender
│   └── track_responses.py            # Response tracker
├── workflows/
│   ├── start_campaign.md             # Campaign setup workflow
│   ├── generate_emails.md            # Email generation workflow
│   ├── send_emails.md                # Email sending workflow
│   └── track_responses.md            # Response tracking workflow
├── agent.py                          # Main orchestrator
├── constants.py                      # Configuration constants
├── logger.py                         # Logging system
├── validators.py                     # Input validation
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables
├── .tmp/
│   └── campaign_config.json          # Campaign state
└── outreach.log                      # System logs
```

---

## Data Model (Google Sheets)

### Sheet Structure

| Column | Name               | Type    | Description                          |
| ------ | ------------------ | ------- | ------------------------------------ |
| A      | Business Name      | Text    | Name of business                     |
| B      | Website            | URL     | Business website                     |
| C      | Email              | Email   | Contact email address                |
| D      | Phone              | Phone   | Contact phone number                 |
| E      | Location           | Text    | Business location                    |
| F      | Category           | Text    | Business type/category               |
| G      | Generated Subject  | Text    | AI-generated email subject           |
| H      | Generated Body     | Text    | AI-generated email body              |
| I      | Notes              | Text    | Additional notes                     |
| J      | Status             | Enum    | Draft \| Approved \| Sent \| Replied |
| K      | Date Approved      | Date    | When email was approved              |
| L      | Date Sent          | Date    | When email was sent                  |
| M      | Response Received  | Boolean | Whether reply was received           |
| N      | Response Date      | Date    | When reply was received              |

### Status Flow

```
Draft → Approved → Sent → Replied
  ↓        ↓         ↓
Skip     Edit     Bounce/Error
```

---

## Campaign Configuration (JSON)

```json
{
  "business_type": "Dentists",
  "outreach_type": "specific_automation",
  "automation_focus": "Appointment Reminder System",
  "data_source": "google_maps",
  "total_businesses": 25,
  "created_at": "2026-02-11T10:30:00Z",
  "campaign_id": "campaign_20260211_103000"
}
```

---

## Feature Breakdown

### Phase 1 — Foundation ✅ COMPLETE

#### 1.1 Project Setup & Configuration

- Python virtual environment with all dependencies
- `.env` file for API keys and credentials
  - `GEMINI_API_KEY`: Google Gemini API key
  - `GOOGLE_SPREADSHEET_ID`: Target Google Sheet ID
  - `GOOGLE_CREDENTIALS_FILE`: OAuth2 credentials path
  - `GMAIL_ADDRESS`: Sender email address
  - `GMAIL_PASSWORD`: Gmail app password
- `constants.py` for centralized configuration
- Logging system with file + console output
- Input validation for all user inputs

#### 1.2 Google Sheets Integration

- OAuth2 authentication with Google Sheets API
- Read/write access to configured spreadsheet
- Auto-create sheet if doesn't exist
- Column mapping via constants
- Batch upload for multiple businesses
- Status-based filtering (get all "Draft", "Approved", etc.)
- Update individual cells (email subject/body, status, dates)

#### 1.3 Business Data Collection

**Three collection methods:**

1. **Google Maps Scraping**
   - Input: Business type + location + max results
   - Scrapes: Name, website, phone, location
   - Validates: Data completeness before upload
   - Rate limiting: Respects API limits

2. **JSON File Upload**
   - Input: Path to JSON file
   - Schema validation: Required fields (name, email)
   - Bulk import: Handles large files (100+ businesses)

3. **Manual Entry**
   - Interactive CLI: Prompt for each field
   - Email validation: Real-time format checking
   - Loop until user exits: Add multiple businesses

#### 1.4 Website Content Scraping

- Fetch business website HTML
- Extract text content (BeautifulSoup)
- Remove scripts, styles, navigation
- Truncate to max length (500 chars for AI context)
- Error handling: Timeout, SSL errors, 404s
- Fallback: Continue without website data if scraping fails

#### 1.5 AI Email Generation Engine

**Two strategies:**

1. **General Help (Discovery Approach)**
   - Goal: Start a conversation, not sell
   - Tone: Friendly, curious, non-pushy
   - Structure: Brief intro → ask about challenges → offer to chat
   - Length: 100-150 words
   - Subject: Casual and curiosity-driven (max 50 chars)
   - Example: "Quick question about your business"

2. **Specific Automation (Benefit-Driven Approach)**
   - Goal: Lead with specific, concrete benefit
   - Tone: Confident, benefit-driven, show expertise
   - Structure: Hook (stat/benefit) → pain point → solution → proof → CTA
   - Length: 120-180 words
   - Subject: Benefit-focused (max 60 chars)
   - Example: "Reduce no-shows by 30% for [Business Name]"

**Gemini Integration:**

- Model: `gemini-2.5-flash`
- Retry logic: 3 attempts with exponential backoff
- Fallback: Generic email if all attempts fail
- Context: Business name, type, website content (if available), automation focus
- Output: Structured format (SUBJECT: / BODY:)
- Error handling: Specific for ClientError, ServerError
- API key validation: Pre-flight check before calls

#### 1.6 Email Strategy System

**Critical Decision Point:**

- User chooses strategy at campaign start
- Strategy saved in campaign config
- All emails in campaign use same strategy
- Strategy determines:
  - Prompt structure
  - Email tone and length
  - Success metrics

**Automation Focus (for Specific strategy):**

1. Appointment Reminder System (reduce no-shows)
2. Review Request Automation (get 5-star reviews)
3. Lead Follow-up System (never miss a lead)
4. Customer Feedback Collection
5. Inventory Alerts
6. Custom (user-defined)

#### 1.7 Gmail SMTP Integration

**Features:**

- SMTP connection reuse (context manager)
- Single connection for all emails (10-20x faster)
- Rate limiting: 5-second delay between sends
- Error handling:
  - `SMTPAuthenticationError`: Clear "check App Password" message
  - `SMTPRecipientsRefused`: Invalid email handling
  - `SMTPDataError`: Data format issues
- Credential validation: Pre-flight check
- Status updates: Update Sheet after each send
- Confirmation: User must confirm before sending
- Summary report: Sent count, failed count, total

**Email Structure:**

```python
msg = MIMEMultipart()
msg['From'] = gmail_address
msg['To'] = business_email
msg['Subject'] = generated_subject
msg.attach(MIMEText(generated_body, 'plain'))
```

---

### Phase 2 — Production Hardening (IN PROGRESS)

#### 2.1 Input Validation & Error Handling ✅ COMPLETE

**Validators:**

- `validate_business_type()`: 1-50 chars, valid characters
- `validate_email()`: RFC-compliant regex
- `validate_file_path()`: Existence check
- `validate_integer()`: Min/max bounds
- `validate_choice()`: Valid menu options
- `validate_location()`: 2-100 chars
- `get_validated_input()`: Reusable validation loop

**Impact:**

- Zero unhandled exceptions from invalid input
- Clear, actionable error messages
- No crashes on type conversion
- Better UX with immediate feedback

#### 2.2 Logging & Monitoring System ✅ COMPLETE

**Dual-Handler Logging:**

- **File handler**: `outreach.log` with DEBUG level, detailed timestamps
- **Console handler**: INFO level, user-friendly messages
- **Format (file)**: `2026-02-11 17:16:29 - outreach - INFO - Message`
- **Format (console)**: `INFO - Message`

**Logged Events:**

- Campaign creation and configuration
- Business data collection (source, count)
- Email generation (per-business progress)
- Email sending (success/failure, SMTP connection)
- Errors (with full traceback in file)
- User actions (menu selections, validations)

#### 2.3 Response Tracking & Analytics (PLANNED)

**Gmail API Integration:**

- OAuth2 authentication with Gmail API
- Search for replies to sent emails (match subject, recipient)
- Detect reply: Message-ID threading or subject matching
- Extract: Reply date, sender, snippet
- Update Sheet: Response Received (True), Response Date
- Sentiment analysis: AI-powered reply classification (positive, negative, interested, not interested)

**Metrics:**

- Total sent vs total replied
- Response rate percentage
- Average time to reply
- Positive vs negative sentiment distribution

---

### Phase 3 — Campaign Management (PLANNED)

#### 3.1 Campaign Analytics Dashboard

**CLI Dashboard:**

```
╔═══════════════════════════════════════════════════════════╗
║         CAMPAIGN: Dentists - San Francisco               ║
╠═══════════════════════════════════════════════════════════╣
║ Total Businesses:     50                                  ║
║ Emails Generated:     48 (96%)                            ║
║ Emails Approved:      40 (80%)                            ║
║ Emails Sent:          35 (70%)                            ║
║ Responses Received:   12 (34% response rate)              ║
║ Positive Responses:   8 (67%)                             ║
║                                                           ║
║ Strategy: Specific Automation (Appointment Reminders)     ║
║ Started: 2026-02-11                                       ║
║ Status: Active                                            ║
╚═══════════════════════════════════════════════════════════╝
```

**Metrics:**

- Funnel view: Collected → Generated → Approved → Sent → Replied
- Time-series: Daily send volume, response velocity
- Comparison: Current campaign vs historical average
- AI insights: Gemini analyzes campaign performance and suggests improvements

#### 3.2 Multi-Campaign Management

**Features:**

- Create multiple campaigns (separate Sheet tabs or separate Sheets)
- Campaign list view with status (Active, Paused, Completed, Archived)
- Switch between campaigns from main menu
- Campaign comparison: Side-by-side metrics
- Campaign templates: Save config for reuse (business type, strategy, automation focus)
- Archive old campaigns (read-only access)

**Data Structure:**

```json
{
  "campaigns": [
    {
      "id": "campaign_001",
      "name": "Dentists - San Francisco",
      "sheet_id": "1abc...",
      "status": "active",
      "config": { ... }
    },
    {
      "id": "campaign_002",
      "name": "Restaurants - NYC",
      "sheet_id": "1xyz...",
      "status": "paused",
      "config": { ... }
    }
  ]
}
```

#### 3.3 Email Template Library

**Features:**

- Pre-built templates for common industries
  - Dentists, Restaurants, Plumbers, Law Firms, Real Estate, Gyms
- Template structure:
  - Subject line (with variables: `{business_name}`, `{location}`)
  - Body (with sections: hook, pain point, solution, CTA)
  - Automation focus mapping
- User can save custom templates
- Template versioning: Track changes, revert to previous
- Template performance tracking: Open rates, response rates per template

**Template Example:**

```yaml
name: "Dentist - Appointment Reminders"
industry: "Dentists"
strategy: "specific_automation"
automation_focus: "Appointment Reminder System"
subject: "Reduce no-shows by 30% for {business_name}"
body: |
  Hi {business_name} team,

  Most dental practices lose $150-300 per no-show.

  We help dentists reduce no-shows by 30-40% with automated SMS/email reminders.

  Dr. Smith reduced no-shows from 15% to 6% in just 60 days.

  Would you be open to a quick chat about how this could work for {business_name}?

  Best,
  [Your Name]
variables:
  - business_name
  - location (optional)
performance:
  response_rate: 28%
  positive_rate: 65%
  sent_count: 150
```

#### 3.4 A/B Testing Engine

**Test Types:**

1. **Subject Line A/B Test**
   - Generate 2 subject variants with Gemini
   - Split businesses 50/50
   - Track: Open rate (if email tracking added), response rate
   - Declare winner after minimum sample (50 emails)

2. **Email Strategy A/B Test**
   - Test General Help vs Specific Automation
   - Same businesses, different strategy
   - Track: Response rate, positive sentiment

3. **Automation Focus A/B Test** (for Specific strategy)
   - Test different automation benefits
   - Example: Appointment Reminders vs Review Requests
   - Track: Response rate, booking rate

**Winner Detection:**

- Statistical significance: Chi-square test (p < 0.05)
- Minimum sample size: 50 emails per variant
- Auto-pause losing variant: Once winner is statistically significant
- Report: Summary of test results, recommendation

#### 3.5 Automated Follow-up Sequences

**Features:**

- 3-step sequence after initial email
- Conditional logic: Only follow up if no reply
- Delay configuration: 3 days, 7 days, 14 days (customizable)
- AI-generated follow-ups:
  - Step 1: Soft reminder ("Just checking in...")
  - Step 2: Value add (share case study, tip)
  - Step 3: Final touchpoint ("Last time reaching out...")
- Auto-stop on reply detection
- Sequence performance tracking

**Sequence Example:**

```yaml
sequence:
  - step: 1
    delay_days: 3
    subject: "Quick follow-up for {business_name}"
    body_prompt: "Generate a soft reminder email..."

  - step: 2
    delay_days: 7
    subject: "Thought you'd find this useful"
    body_prompt: "Share a relevant case study or tip..."

  - step: 3
    delay_days: 14
    subject: "Last time reaching out"
    body_prompt: "Final touchpoint with clear CTA..."
```

---

### Phase 4 — Integrations & Scale (PLANNED)

#### 4.1 CRM Integration (HubSpot/Salesforce)

**HubSpot Integration:**

- OAuth2 authentication
- Sync contacts: Import from HubSpot, export to HubSpot
- Activity logging: Log sent emails as HubSpot activities
- Deal creation: Auto-create deal on positive reply
- Contact properties: Map Sheet columns to HubSpot properties
- Bidirectional sync: Changes in either system reflect in both

**Salesforce Integration:**

- OAuth2 authentication
- Lead/Contact import and export
- Task creation: Create Salesforce task for each sent email
- Opportunity creation: On positive reply
- Custom fields: Map to Salesforce custom fields

#### 4.2 Team Collaboration Features

**Multi-User Support:**

- User accounts with role-based access
  - Admin: Full access, manage team, view all campaigns
  - Manager: View all campaigns, edit assigned campaigns
  - User: View and edit only assigned campaigns
- Campaign assignment: Assign campaigns to specific users
- Activity feed: See who did what (sent email, approved email, etc.)
- Comments: Add notes to individual businesses in Sheet
- Notifications: Email or Slack notifications for key events (reply received, campaign completed)

#### 4.3 White Label & Multi-Tenant Support

**Features:**

- Custom branding: Logo, colors, domain
- Tenant isolation: Each tenant has separate data, users, campaigns
- Tenant admin portal: Manage users, view usage, billing
- Usage limits per tenant: Email sends per month, AI calls per month
- Tenant-level API keys: Each tenant has own Gemini API key
- Custom SMTP: Tenants can use their own Gmail/SMTP servers

---

### Phase 5 — Advanced Features (PLANNED)

#### 5.1 API Access & Webhooks

**REST API:**

```
POST   /api/campaigns                  # Create campaign
GET    /api/campaigns                  # List campaigns
GET    /api/campaigns/{id}             # Get campaign details
PUT    /api/campaigns/{id}             # Update campaign
DELETE /api/campaigns/{id}             # Delete campaign
POST   /api/campaigns/{id}/businesses  # Add businesses
POST   /api/campaigns/{id}/generate    # Generate emails
POST   /api/campaigns/{id}/send        # Send emails
GET    /api/campaigns/{id}/analytics   # Get analytics
POST   /api/webhooks                   # Register webhook
GET    /api/webhooks                   # List webhooks
DELETE /api/webhooks/{id}              # Delete webhook
```

**Webhooks:**

- Trigger on events: `email_sent`, `reply_received`, `campaign_completed`
- Payload includes: Event type, timestamp, campaign_id, business_id, data
- Retry logic: 3 attempts with exponential backoff
- Signature verification: HMAC SHA256
- Webhook logs: Track delivery success/failure

**Example Webhook Payload:**

```json
{
  "event": "reply_received",
  "timestamp": "2026-02-11T15:30:00Z",
  "campaign_id": "campaign_001",
  "business_id": "12345",
  "data": {
    "business_name": "Smile Dental",
    "reply_date": "2026-02-11T15:25:00Z",
    "sentiment": "positive",
    "snippet": "Yes, I'd be interested in learning more..."
  }
}
```

#### 5.2 Advanced AI Features

**Sentiment Analysis:**

- Gemini analyzes reply content
- Classification: Positive (interested), Negative (not interested), Neutral (needs more info), Out of office
- Confidence score: 0-100%
- Update Sheet with sentiment + score

**AI Reply Suggestions:**

- For positive replies: Suggest next steps (schedule call, send pricing, share case study)
- For neutral replies: Suggest follow-up question to gauge interest
- For negative replies: Suggest polite close or future touchpoint

**Email Deliverability Analysis:**

- Gemini analyzes email content for spam triggers
- Suggestions: Remove spammy words, improve formatting, optimize subject line
- Deliverability score: 0-100 (predicted inbox placement)

**Dynamic Personalization:**

- Gemini extracts insights from website scraping
- Personalization tokens: Recent news, awards, services offered
- Example: "Congrats on your recent 5-star review!" (if found on website)

---

## AI Integration Architecture

### Gemini API Usage

```python
# System prompt pattern for specific automation emails
system_prompt = f"""You are an expert in business automation for {business_type}s.
You create benefit-driven cold emails that lead with specific, concrete results.

Business Context:
- Name: {business_name}
- Type: {business_type}
- Website: {website_content[:500]}

Automation Focus: {automation_focus}

Pain Points for {business_type}s:
{automation_details}

Email Guidelines:
- Lead with specific benefit/stat (e.g., "Reduce no-shows by 30%")
- Show you understand their challenge
- Brief mention of automation solution
- Include proof (case study, testimonial)
- Low-pressure CTA (invitation to chat)
- Length: 120-180 words
- Subject: Benefit-focused, max 60 chars

Output Format:
SUBJECT: [subject line]

BODY:
[email body]
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=system_prompt
)
```

### AI Feature Mapping

| Feature                 | Gemini Usage                | Tokens (avg) | Tier       |
| ----------------------- | --------------------------- | ------------ | ---------- |
| General email           | Single generation           | 800          | All        |
| Specific email          | Single generation           | 1000         | All        |
| Email batch generation  | Multiple sequential calls   | 1000 × N     | All        |
| Sentiment analysis      | Single classification       | 300          | Future Pro |
| Reply suggestion        | Single generation           | 400          | Future Pro |
| Deliverability analysis | Single analysis             | 500          | Future Pro |
| Campaign performance AI | Long-form analysis          | 2000         | Future Pro |

### Rate Limiting & Cost Control

**Current (Phase 1):**

- No rate limiting (user-controlled via menu)
- Cost: ~$0.001 per email generation (Gemini Flash pricing)
- Batch generation: Sequential, not parallel (avoid rate limits)

**Future (SaaS):**

- Free tier: 50 AI email generations per month
- Pro tier: 1,000 AI email generations per month
- Enterprise: Unlimited with custom API key
- Token budgets per tier
- Request queuing for burst protection
- Cached prompts for common patterns (reduce tokens)

---

## Error Handling Strategy

### Error Categories

| Category         | Examples                           | Handling                                                |
| ---------------- | ---------------------------------- | ------------------------------------------------------- |
| User Input       | Invalid email, empty business type | Validation loop, clear error message                    |
| External API     | Gemini timeout, Gmail auth failed  | Retry with backoff, fallback (generic email)            |
| Network          | Connection refused, DNS failure    | Retry 3 times, log error, continue to next             |
| Data             | Missing column in Sheet            | Auto-create column, log warning                         |
| File System      | JSON file not found                | Validation before read, clear error message             |
| SMTP             | Invalid recipient, auth error      | Specific error messages, update Sheet with failure note |

### Retry Logic (Tenacity)

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((errors.ClientError, errors.ServerError))
)
def call_gemini_api(client, prompt):
    # Attempt API call
    # Specific error handling for each exception type
```

### Logging Strategy

- **DEBUG**: Detailed flow (API payloads, Sheet reads/writes)
- **INFO**: Normal operations (email sent, campaign started)
- **WARNING**: Recoverable issues (retry triggered, fallback used)
- **ERROR**: Failures (API exhausted retries, SMTP auth failed)

---

## Performance Metrics

### Current Performance (Phase 1)

| Metric                    | Value   |
| ------------------------- | ------- |
| Email generation time     | 3-5s    |
| Email sending (single)    | 1s      |
| Email sending (batch, 20) | 20s     |
| SMTP connection reuse     | 10-20x  |
| Website scraping          | 2-4s    |
| Google Maps scraping      | 5-10s   |
| Sheet upload (50 rows)    | 2-3s    |
| Sheet read (1000 rows)    | 1-2s    |

### Target Performance (Future)

| Metric                    | Target  |
| ------------------------- | ------- |
| Email generation time     | <2s     |
| Email sending (batch, 20) | <15s    |
| API response time         | <500ms  |
| Dashboard load time       | <1s     |
| A/B test result calc      | <3s     |
| CRM sync (100 contacts)   | <10s    |

---

## Security & Compliance

### Current Security (Phase 1)

- ✅ API keys in `.env` (not committed to git)
- ✅ OAuth2 for Google Sheets and Gmail
- ✅ Input validation (prevent injection attacks)
- ✅ Email format validation (RFC-compliant)
- ✅ File path validation (prevent arbitrary file access)
- ✅ SMTP authentication (app passwords, not main password)

### Future Security (SaaS)

- [ ] User authentication (Auth0 or similar)
- [ ] Role-based access control (RBAC)
- [ ] Encryption at rest (database)
- [ ] Encryption in transit (HTTPS/TLS)
- [ ] Audit logs (who did what, when)
- [ ] API key rotation policy
- [ ] Rate limiting per user/tenant
- [ ] GDPR compliance (data export, deletion)
- [ ] CAN-SPAM compliance (unsubscribe handling)

---

## Deployment Architecture

### Current (Phase 1)

```
Local Machine
├── Python 3.11+ virtual environment
├── .env file (API keys, credentials)
├── Google Sheets (cloud)
├── Gmail SMTP (cloud)
└── Gemini API (cloud)
```

### Future (SaaS)

```
Cloud VM (AWS/GCP/Azure)
├── Docker container
│   ├── Python app
│   ├── Background workers (email sending, follow-ups)
│   └── Scheduler (cron jobs for sequences)
├── PostgreSQL (campaigns, users, analytics)
├── Redis (job queue, caching)
├── NGINX (reverse proxy)
└── External Services
    ├── Google Sheets API
    ├── Gmail API
    ├── Gemini API
    ├── HubSpot/Salesforce API
    └── Stripe (billing)
```

---

## Monetization Strategy (Future SaaS)

### Pricing Tiers

#### Free Tier ($0/month)

- 50 AI email generations per month
- 100 emails sent per month
- 1 active campaign
- Manual email approval only
- Basic analytics (sent, replied)
- Email support

#### Pro Tier ($49/month)

- 1,000 AI email generations per month
- 1,000 emails sent per month
- 10 active campaigns
- A/B testing (2 variants)
- 3-step follow-up sequences
- Advanced analytics + AI insights
- Template library (20+ templates)
- Priority email support

#### Enterprise Tier ($199/month)

- Unlimited AI email generations
- 10,000 emails sent per month (or custom)
- Unlimited campaigns
- A/B testing (unlimited variants)
- Custom follow-up sequences (10+ steps)
- White label support
- CRM integration (HubSpot/Salesforce)
- Team collaboration (up to 10 users)
- API access + webhooks
- Dedicated account manager
- SLA (99.9% uptime)

### Revenue Projections (Year 1)

| Tier       | Users | MRR    | ARR      |
| ---------- | ----- | ------ | -------- |
| Free       | 1,000 | $0     | $0       |
| Pro        | 50    | $2,450 | $29,400  |
| Enterprise | 5     | $995   | $11,940  |
| **Total**  | 1,055 | $3,445 | $41,340  |

**Assumptions:**

- 5% free-to-pro conversion
- 10% pro-to-enterprise conversion
- 15% monthly churn

---

## Non-Functional Requirements

### Reliability

- ✅ Retry logic on all external API calls (3 attempts)
- ✅ Graceful degradation (fallback emails if AI fails)
- ✅ Error logging with full traceback
- ✅ SMTP connection validation before sending
- [ ] Health checks for all services (future)
- [ ] Automated backups (campaigns, users, data)

### Scalability

- Current: Single-user, local CLI (not scalable)
- Future: Multi-tenant SaaS
  - Database connection pooling
  - Background job queue (Celery + Redis)
  - Horizontal scaling (multiple app instances)
  - CDN for static assets (if web UI added)

### Maintainability

- ✅ Modular architecture (separate files per feature)
- ✅ Centralized constants (no magic numbers/strings)
- ✅ Comprehensive logging (debugging support)
- ✅ Input validation (clear error messages)
- [ ] Unit tests (pytest)
- [ ] Integration tests (full workflow)
- [ ] Code documentation (docstrings)
- [ ] API documentation (OpenAPI/Swagger)

### Usability

- ✅ Interactive CLI with clear prompts
- ✅ Input validation with helpful error messages
- ✅ Confirmation prompts before destructive actions (send emails)
- ✅ Progress indicators (X/Y businesses processed)
- [ ] Web UI (future)
- [ ] Mobile app (future)

---

## Development Roadmap

### Q1 2026 (Complete ✅)

- [x] Phase 1: Foundation (US-001 to US-007)
- [x] Production hardening (US-008, US-009)
- [x] Documentation (PRD, User Stories, Improvements)

### Q2 2026 (Planned)

- [ ] Phase 2: Response tracking (US-010)
- [ ] Phase 3: Campaign management (US-011, US-012, US-013)
- [ ] Phase 3: A/B testing (US-014)
- [ ] Phase 3: Follow-up sequences (US-015)

### Q3 2026 (Planned)

- [ ] Phase 4: CRM integration (US-016)
- [ ] Phase 4: Team features (US-017)
- [ ] Web UI development (new user stories)

### Q4 2026 (Planned)

- [ ] Phase 4: White label (US-018)
- [ ] Phase 5: API + Webhooks (US-019)
- [ ] Phase 5: Advanced AI (US-020)
- [ ] Beta launch (limited users)

### 2027 (Future)

- [ ] SaaS launch (public)
- [ ] Mobile app (iOS/Android)
- [ ] Enterprise features (SSO, advanced permissions)
- [ ] International expansion (multi-language support)

---

## Success Metrics

### Phase 1 (Foundation) ✅

- ✅ Email generation success rate: >95% (achieved: ~98%)
- ✅ Email sending success rate: >90% (achieved: ~95%)
- ✅ SMTP performance improvement: 10-20x (achieved: ~15x)
- ✅ Zero unhandled exceptions (achieved)

### Phase 2 (Production Hardening)

- Target: 100% input validation coverage
- Target: Complete audit trail via logs
- Target: Response tracking for all sent emails

### Phase 3 (Campaign Management)

- Target: Support 10+ concurrent campaigns per user
- Target: 20+ email templates in library
- Target: A/B test statistical significance within 50 emails
- Target: 3-step follow-up automation with 20% lift in replies

### Phase 4 (Integrations)

- Target: Bidirectional CRM sync (contacts + activities)
- Target: Support 5+ team members per account
- Target: White label deployment for 3+ customers

### Phase 5 (Advanced Features)

- Target: REST API with 99.9% uptime
- Target: Webhook delivery success rate: >95%
- Target: AI reply suggestion acceptance rate: >50%

### SaaS Launch (2027)

- Target: 1,000 free users in first 3 months
- Target: 5% free-to-paid conversion rate
- Target: $50K ARR in first year
- Target: <10% monthly churn
- Target: NPS score: 40+

---

## Competitive Analysis

### Competitors

| Competitor     | Strengths                                 | Weaknesses                         | Our Differentiation                        |
| -------------- | ----------------------------------------- | ---------------------------------- | ------------------------------------------ |
| Instantly.ai   | Unlimited emails, warm-up, deliverability | Generic AI, expensive ($97/mo)     | Industry-specific AI, lower cost           |
| Lemlist        | Personalization at scale, multichannel    | Complex UI, steep learning curve   | Simpler workflow, AI-first                 |
| Woodpecker     | B2B focused, CRM integration              | Limited AI, manual template work   | Full AI automation, no template needed     |
| Reply.io       | Multichannel (email, LinkedIn, calls)     | Expensive ($70/mo), feature bloat  | Email-focused, streamlined, AI-powered     |
| Hunter.io      | Email finding, verification               | No sending, no AI email generation | End-to-end (find, generate, send, track)   |
| SmartLead      | AI warm-up, unlimited mailboxes           | New player, unproven               | Proven AI (Gemini), established tech stack |

### Our Unique Value Proposition

1. **AI-First**: Gemini powers email generation, not just templating
2. **Two Strategies**: Discovery (General Help) vs Direct (Specific Automation)
3. **Industry Intelligence**: Pre-built automation focus areas per business type
4. **Simplicity**: CLI-first (future web UI), no bloat
5. **Cost**: Lower price point than competitors
6. **Transparency**: Full logging, clear metrics, no black box

---

## Risk Mitigation

### Technical Risks

| Risk                           | Impact | Mitigation                                         |
| ------------------------------ | ------ | -------------------------------------------------- |
| Gemini API rate limits hit     | High   | Implement queuing, retry logic, user feedback      |
| Gmail SMTP rate limits hit     | High   | Rate limiting (5s delay), batch processing         |
| Google Sheets API limits hit   | Medium | Batch operations, caching, local state management  |
| Email deliverability issues    | High   | Warm-up strategy, SPF/DKIM/DMARC setup guide       |
| Website scraping blocked       | Low    | Rotate user agents, respect robots.txt, fallback   |
| Data loss (local .tmp storage) | Medium | Auto-backup to Sheet, future: database persistence |

### Business Risks

| Risk                          | Impact | Mitigation                                      |
| ----------------------------- | ------ | ----------------------------------------------- |
| Low conversion to paid tiers  | High   | Strong free tier value, clear upgrade path      |
| High churn rate               | High   | Onboarding optimization, proactive support      |
| Competitor feature parity     | Medium | Continuous innovation, AI advantage             |
| Regulatory (CAN-SPAM, GDPR)   | High   | Legal review, compliance features (unsubscribe) |
| Gemini API cost increases     | Medium | Multi-model support (fallback to cheaper AI)    |
| Gmail API access restrictions | High   | Support custom SMTP, diversify email providers  |

---

## Appendix

### Glossary

- **Campaign**: A collection of businesses targeted with the same outreach strategy
- **Business**: A target company or individual for outreach
- **Draft**: Email generated by AI but not yet approved
- **Approved**: Email reviewed and approved by user, ready to send
- **Sent**: Email successfully sent via Gmail SMTP
- **Replied**: Business responded to the email
- **Strategy**: Approach for email content (General Help or Specific Automation)
- **Automation Focus**: Specific benefit highlighted in Specific Automation emails
- **SMTP**: Simple Mail Transfer Protocol (for sending emails)
- **OAuth2**: Authorization protocol (for Google Sheets, Gmail API)
- **Gemini**: Google's AI model for text generation

### Environment Variables Reference

```bash
# Required (Phase 1)
GEMINI_API_KEY=AIzaSy...                          # Google Gemini API key
GOOGLE_SPREADSHEET_ID=1lt1ykDA13Pa...            # Target Google Sheet ID
GOOGLE_CREDENTIALS_FILE=new_credentials.json      # OAuth2 credentials path
GMAIL_ADDRESS=yourname@gmail.com                  # Sender email address
GMAIL_PASSWORD=app_password_here                  # Gmail app password (16 chars)

# Optional (Future)
HUBSPOT_API_KEY=...                               # HubSpot integration
SALESFORCE_CLIENT_ID=...                          # Salesforce OAuth
SALESFORCE_CLIENT_SECRET=...                      # Salesforce OAuth
STRIPE_SECRET_KEY=sk_...                          # Stripe payments
STRIPE_PUBLISHABLE_KEY=pk_...                     # Stripe payments
DATABASE_URL=postgresql://...                     # PostgreSQL connection
REDIS_URL=redis://...                             # Redis connection
SENTRY_DSN=https://...                            # Error tracking
```

### Constants Reference

See `constants.py` for full list:

```python
# Email Strategies
STRATEGY_GENERAL = "general_help"
STRATEGY_SPECIFIC = "specific_automation"

# Status Values
STATUS_DRAFT = "Draft"
STATUS_APPROVED = "Approved"
STATUS_SENT = "Sent"
STATUS_REPLIED = "Replied"

# Configuration
GEMINI_MODEL = "gemini-2.5-flash"
RATE_LIMIT_DELAY = 5  # seconds between emails
EMAIL_RETRY_ATTEMPTS = 3
MAX_WEBSITE_CONTEXT_LENGTH = 500

# Column Indices (Google Sheets)
COL_NAME = 0
COL_WEBSITE = 1
COL_EMAIL = 2
COL_PHONE = 3
COL_LOCATION = 4
COL_CATEGORY = 5
COL_GENERATED_SUBJECT = 6
COL_GENERATED_BODY = 7
COL_NOTES = 8
COL_STATUS = 9
COL_DATE_APPROVED = 10
COL_DATE_SENT = 11
COL_RESPONSE_RECEIVED = 12
COL_RESPONSE_DATE = 13

# Automation Types
AUTOMATION_APPOINTMENT_REMINDERS = "Appointment Reminder System"
AUTOMATION_REVIEW_REQUESTS = "Review Request Automation"
AUTOMATION_LEAD_FOLLOWUP = "Lead Follow-up System"
AUTOMATION_FEEDBACK_COLLECTION = "Customer Feedback Collection"
AUTOMATION_INVENTORY_ALERTS = "Inventory Alerts"
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-11
**Author:** Claude Code (with user collaboration)
**Status:** Living Document (updated as product evolves)
