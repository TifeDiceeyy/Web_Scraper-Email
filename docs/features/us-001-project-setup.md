# US-001: Project Setup & Configuration

**Status:** ✅ Complete
**Priority:** P0 (Critical)
**Estimated Effort:** 4 hours
**Actual Effort:** 4 hours

---

## User Story

**As a** developer setting up the outreach system
**I want** a complete project environment with all dependencies and configuration
**So that** I can start building and running the outreach automation

---

## Acceptance Criteria

1. ✅ Python virtual environment created with Python 3.11+
2. ✅ All required dependencies installed from `requirements.txt`
3. ✅ `.env` file configured with all required API keys:
   - GEMINI_API_KEY
   - GOOGLE_SPREADSHEET_ID
   - GOOGLE_CREDENTIALS_FILE
   - GMAIL_ADDRESS
   - GMAIL_PASSWORD
4. ✅ Project structure organized with clear separation:
   - `/tools/` - Individual tool scripts
   - `/workflows/` - Workflow documentation
   - `agent.py` - Main orchestrator
5. ✅ Google Sheets API credentials configured (OAuth2)
6. ✅ Gmail SMTP credentials configured (App Password)
7. ✅ Test run successful (can import all modules)

---

## Technical Requirements

### Dependencies

```txt
google-genai>=1.0.0              # Google Gemini AI
google-auth-oauthlib==1.2.0      # Google OAuth2
google-auth-httplib2==0.2.0      # Google Auth HTTP
google-api-python-client==2.100.0 # Google Sheets API
python-dotenv==1.0.0             # Environment variables
requests==2.31.0                 # HTTP requests
beautifulsoup4==4.12.0           # Web scraping
tenacity==9.1.4                  # Retry logic
```

### Environment Variables

```bash
# Required for Phase 1
GEMINI_API_KEY=AIzaSy...
GOOGLE_SPREADSHEET_ID=1lt1ykDA13Pa...
GOOGLE_CREDENTIALS_FILE=credentials.json
GMAIL_ADDRESS=yourname@gmail.com
GMAIL_PASSWORD=app_password_16chars
```

### File Structure

```
Web_Scraper&Email/
├── tools/
├── workflows/
├── agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Implementation Notes

### Virtual Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Google Sheets API Setup

1. Go to Google Cloud Console
2. Create new project or select existing
3. Enable Google Sheets API
4. Create OAuth2 credentials (Desktop app)
5. Download credentials JSON
6. Place in project root as `credentials.json`

### Gmail App Password Setup

1. Enable 2-factor authentication on Google account
2. Go to Security → 2-Step Verification → App passwords
3. Generate new app password (select "Mail" and "Other")
4. Copy 16-character password
5. Add to `.env` as `GMAIL_PASSWORD`

---

## Testing

**Test 1: Dependencies**
```bash
python3 -c "import google.genai, google.auth, dotenv; print('✅ All dependencies installed')"
```

**Test 2: Environment Variables**
```bash
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ .env loaded')"
```

**Test 3: Module Imports**
```bash
python3 -c "import agent; print('✅ Agent module loads successfully')"
```

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing Python 3.11+ | High | Check version: `python3 --version` |
| Google API credentials invalid | High | Test OAuth2 flow manually |
| Gmail app password wrong | Medium | Regenerate and test |
| Dependency conflicts | Medium | Use virtual environment isolation |

---

## Related Stories

- **Blocks:** US-002 (Google Sheets Integration)
- **Blocks:** US-005 (AI Email Generation)

---

## Definition of Done

- [x] Virtual environment active and dependencies installed
- [x] `.env` file exists with all required keys
- [x] Google Sheets API credentials valid (tested)
- [x] Gmail SMTP credentials valid (tested)
- [x] All modules can be imported without errors
- [x] `.gitignore` configured to exclude `.env`, credentials, logs
- [x] README.md exists with setup instructions

---

**Created:** 2026-02-01
**Completed:** 2026-02-05
**Last Updated:** 2026-02-11
