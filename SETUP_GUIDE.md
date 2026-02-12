# Business Outreach Automation - Setup Guide

## 🎉 PROJECT COMPLETE!

Your business outreach automation system is fully built using the WAT Framework (Workflows, Agents, Tools).

## 📁 What Was Built

### ✅ Core Files
- `agent.py` - Main orchestrator with menu system and critical decision logic
- `requirements.txt` - All Python dependencies
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

### ✅ Workflows (Instruction Files)
- `workflows/start_campaign.md` - Campaign initialization workflow
- `workflows/generate_emails.md` - Email generation (2 strategies)
- `workflows/send_emails.md` - Email sending workflow
- `workflows/track_responses.md` - Response tracking workflow

### ✅ Tools (Implementation Scripts)
- `tools/generate_general_email.py` - General help strategy emails
- `tools/generate_specific_email.py` - Specific automation emails
- `tools/scrape_website.py` - Website content scraper
- `tools/upload_to_sheets.py` - Google Sheets uploader
- `tools/scrape_google_maps.py` - Google Maps scraper
- `tools/load_json.py` - JSON file loader
- `tools/get_draft_businesses.py` - Get draft businesses
- `tools/update_sheet_emails.py` - Update sheet with emails
- `tools/send_emails.py` - Send emails via Gmail
- `tools/track_responses.py` - Track email responses

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable **Google Sheets API**
4. Enable **Gmail API** (for sending/tracking)
5. Create OAuth 2.0 credentials:
   - Application type: Desktop app
   - Download credentials as `credentials.json`
6. Place `credentials.json` in project root

### Step 3: Create a Google Sheet

1. Create a new Google Sheet
2. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```
3. Keep it handy for `.env` file

### Step 4: Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account / sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

### Step 5: Set Up Gmail (for sending emails)

1. Enable 2-Factor Authentication on your Gmail
2. Generate an **App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Create app password for "Mail"
   - Copy the 16-character password

### Step 6: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use any text editor
```

Fill in:
```
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_SPREADSHEET_ID=your-sheet-id
GOOGLE_CREDENTIALS_FILE=credentials.json
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_PASSWORD=your-16-char-app-password
```

### Step 7: (Optional) Set Up Notifications

**For Telegram notifications:**
1. Talk to [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token
4. Get your Chat ID:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find your chat_id in the response

Add to `.env`:
```
NOTIFICATION_METHOD=telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

---

## 🎯 HOW TO USE

### First Run

```bash
python agent.py
```

You'll see the main menu:
```
🚀 BUSINESS OUTREACH AUTOMATION SYSTEM
1. 📋 Start New Campaign
2. ✉️  Generate Emails
3. 📊 Manage Google Sheet
4. 📤 Send Approved Emails
5. 📥 Track Responses
6. 🚪 Exit
```

### Typical Workflow

#### 1️⃣ Start Campaign
- Choose business type (e.g., "Dentists")
- **CRITICAL DECISION:** Choose strategy:
  - **General Help**: Discovery emails asking about problems
  - **Specific Automation**: Benefit-driven, focused on one solution
- If specific: Choose which automation (e.g., "Appointment Reminders")
- Choose data source (Google Maps / JSON / Manual)
- Businesses uploaded to Google Sheet with Status = "Draft"

#### 2️⃣ Generate Emails
- System reads your campaign strategy from config
- For each Draft business:
  - Scrapes website (if available)
  - Calls appropriate Claude API:
    - **General Help** → Discovery-focused email
    - **Specific Automation** → Benefit-driven email
  - Updates Google Sheet with subject and body

#### 3️⃣ Review in Google Sheet
- Open your Google Sheet
- Review all generated emails
- Edit any that need changes
- Change Status from "Draft" to "Approved" for emails you want to send

#### 4️⃣ Send Emails
- System finds all "Approved" businesses
- Sends emails via Gmail
- Updates Status to "Sent"
- Records timestamp

#### 5️⃣ Track Responses
- System monitors Gmail for replies
- Updates Google Sheet when replies received
- Changes Status to "Replied"
- Sends notification (Telegram or Email)

---

## 🔑 KEY FEATURE: TWO EMAIL STRATEGIES

### Strategy 1: General Help
**When to use:** Cold outreach, building relationships, broad appeal

**Email style:**
- Subject: "Quick question about [Business Name]"
- Body: Asks about problems, offers general help
- Tone: Curious, non-sales-y, discovery-focused

**Generated by:** `tools/generate_general_email.py`

### Strategy 2: Specific Automation
**When to use:** Warm leads, focused solution, target problem

**Email style:**
- Subject: "Reduce no-shows by 30% at [Business Name]"
- Body: Leads with benefit, focuses on one automation
- Tone: Confident, benefit-driven, solution-focused

**Generated by:** `tools/generate_specific_email.py`

**The decision is saved in `.tmp/campaign_config.json` and determines all email generation.**

---

## 🧪 TESTING

### Test Email Generation (without sending)

```bash
# Test General Help strategy
python tools/generate_general_email.py

# Test Specific Automation strategy
python tools/generate_specific_email.py
```

### Test Individual Tools

```bash
# Test website scraper
python tools/scrape_website.py

# Test JSON loader
python tools/load_json.py
```

---

## 📊 GOOGLE SHEET STRUCTURE

Your sheet will have these columns:
1. Business Name
2. Location
3. Email
4. Phone
5. Website
6. Contact Person
7. Generated Subject
8. Generated Body
9. Your Notes
10. **Status** (Draft → Approved → Sent → Replied)
11. Date Approved
12. Date Sent
13. Last Response
14. Response Details

---

## ⚠️ IMPORTANT NOTES

### Gmail Sending Limits
- Free Gmail: 500 emails/day
- Google Workspace: 2000 emails/day
- System waits 5 seconds between sends
- Recommend: Send in batches

### Google Maps Scraping
- The included scraper provides structure but needs external service
- Options:
  - Outscraper API (paid, reliable) - https://outscraper.com/
  - Apify Google Maps Scraper (paid) - https://apify.com/
  - Manual export + JSON file
  - Sample data for testing

### First-Time OAuth
- When you first run, a browser will open for Google OAuth
- Approve access to Sheets and Gmail
- Tokens are saved for future runs

### Rate Limits
- Gmail API: Check your quota in Google Cloud Console
- Anthropic API: Check your tier limits
- System includes delays to respect limits

---

## 🐛 TROUBLESHOOTING

### "GOOGLE_SPREADSHEET_ID not set"
- Check your `.env` file
- Make sure the Sheet ID is correct
- Restart terminal after editing `.env`

### "credentials.json not found"
- Download from Google Cloud Console
- Place in project root directory

### "Invalid API key"
- Check Anthropic API key in `.env`
- Make sure there are no extra spaces

### Gmail authentication fails
- Make sure 2FA is enabled
- Use App Password, not regular password
- Check for typos in `.env`

### No emails generated
- Check that businesses have Status = "Draft"
- Verify campaign_config.json exists in `.tmp/`
- Check terminal for error messages

---

## 🎓 HOW IT WORKS (WAT Framework)

### Workflows
Markdown files that define WHAT to do:
- `start_campaign.md` - Campaign initialization steps
- `generate_emails.md` - Email generation process
- `send_emails.md` - Email sending process
- `track_responses.md` - Response tracking process

### Agent
`agent.py` orchestrates HOW to decide:
- Shows menu
- Asks questions
- Makes the critical strategy decision
- Calls appropriate tools
- Manages workflow execution

### Tools
Python scripts that know HOW to execute:
- `generate_general_email.py` - Claude API call for general strategy
- `generate_specific_email.py` - Claude API call for specific strategy
- `scrape_website.py` - Web scraping
- `upload_to_sheets.py` - Google Sheets integration
- And more...

---

## 🚀 NEXT STEPS

1. ✅ Complete setup (follow steps above)
2. ✅ Test with sample data first
3. ✅ Run a small campaign (5-10 businesses)
4. ✅ Review results
5. ✅ Scale up!

---

## 📚 RESOURCES

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Gmail API](https://developers.google.com/gmail/api)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 🆘 NEED HELP?

Check the code comments in each file - they explain what each function does.

All tool files have test functions at the bottom - run them individually to debug.

---

**Happy Automating! 🚀**
