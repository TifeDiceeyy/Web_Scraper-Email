# ✅ Setup Checklist - Action Items for You

**Priority: CRITICAL** - Complete these steps before running the application

---

## 🔥 Step 1: Get Gemini API Key (5 minutes)

### Instructions:
1. Visit **https://aistudio.google.com/**
2. Click "Get API Key" or "Create API Key"
3. Copy the API key (starts with `AIzaSy...`)
4. Add to your `.env` file:
   ```env
   GEMINI_API_KEY=AIzaSy_your_actual_key_here
   ```

**Why:** Required for AI email generation (core feature)

---

## 📊 Step 2: Set Up Google Sheets (15 minutes)

### Part A: Create OAuth Credentials
1. Go to **https://console.cloud.google.com/**
2. Create a new project (or select existing)
3. Click "APIs & Services" → "Enable APIs and Services"
4. Search for "Google Sheets API" → Enable it
5. Search for "Google Drive API" → Enable it
6. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
7. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: "Business Outreach Automation"
   - User support email: Your email
   - Developer contact: Your email
   - Save and continue through all steps
8. Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Business Outreach Desktop"
   - Click "Create"
9. Download the JSON file
10. Save it as **`credentials.json`** in your project root:
    ```bash
    /Users/tifediceeyy/All projects/Agentic Workflows/Web_Scraper&Email/credentials.json
    ```

### Part B: Create Google Sheet
1. Go to **https://sheets.google.com/**
2. Create a new blank spreadsheet
3. Name it "Business Outreach - [Your Name]"
4. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit
                                             ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
   Example: 1lt1ykDA13Pa4S-tj8wEiKYXSxHS2wQgLIcaX5YGse4U
   ```
5. Add to your `.env` file:
   ```env
   GOOGLE_SPREADSHEET_ID=1lt1ykDA13Pa4S-tj8wEiKYXSxHS2wQgLIcaX5YGse4U
   GOOGLE_CREDENTIALS_FILE=credentials.json
   ```

**Why:** Google Sheets is your database for businesses and emails

---

## 📧 Step 3: Set Up Gmail App Password (10 minutes)

### Prerequisites:
- Gmail account
- 2-factor authentication enabled

### Instructions:

#### Enable 2FA (if not already enabled):
1. Go to **https://myaccount.google.com/security**
2. Click "2-Step Verification"
3. Follow the setup wizard
4. Verify your phone number

#### Create App Password:
1. Go to **https://myaccount.google.com/apppasswords**
   - (Or: Google Account → Security → 2-Step Verification → App passwords)
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: "Business Outreach"
5. Click "Generate"
6. **Copy the 16-character password** (shown once!)
   - Example: `abcd efgh ijkl mnop` (remove spaces)
7. Add to your `.env` file:
   ```env
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   ```

**Why:** Required for sending emails via Gmail SMTP

---

## 🔧 Step 4: Complete .env File

### Current State:
Your `.env` file only has 3 variables. You need to add more.

### Action Required:
Open `.env` file and add the missing variables:

```env
# ============================================
# Your Current .env (Keep these)
# ============================================
JWT_SECRET_KEY=dev-jwt-secret-key-for-testing-purposes-change-in-production
ENCRYPTION_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=
APIFY_TOKEN=your_apify_token_here

# ============================================
# ADD THESE (from Steps 1-3 above)
# ============================================

# Google Gemini API (from Step 1)
GEMINI_API_KEY=AIzaSy_your_actual_key_here

# Google Sheets (from Step 2)
GOOGLE_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS_FILE=credentials.json

# Gmail (from Step 3)
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_password_here

# ============================================
# OPTIONAL (Notifications)
# ============================================

# Notification Method (choose one)
NOTIFICATION_METHOD=telegram
# or
# NOTIFICATION_METHOD=email

# Telegram Notifications (optional)
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_CHAT_ID=your-chat-id-here

# Email Notifications (optional)
NOTIFICATION_EMAIL=your-notification-email@gmail.com
```

**Save the file after editing.**

---

## 📁 Step 5: Create Missing Directories

Run these commands in your terminal:

```bash
cd "/Users/tifediceeyy/All projects/Agentic Workflows/Web_Scraper&Email"

mkdir -p data
mkdir -p logs
mkdir -p .tmp

# Verify directories created
ls -la | grep -E "data|logs|.tmp"
```

---

## ✅ Step 6: Verify Installation

Run these tests:

### Test 1: Python Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Check Python version
python --version
# Expected: Python 3.11 or higher

# Check dependencies
pip list | grep -E "google-genai|beautifulsoup4|apify-client"
# Expected: All should be installed
```

### Test 2: Import Test
```bash
python -c "
from tools.scrape_google_maps import scrape_google_maps
from tools.generate_general_email import generate_general_email
from tools.send_emails import send_approved_emails
print('✅ All imports successful!')
"
```

### Test 3: Configuration Check
```bash
python validate_env.py
```

**Expected output:**
```
✅ GEMINI_API_KEY is set
✅ GOOGLE_SPREADSHEET_ID is set
✅ GOOGLE_CREDENTIALS_FILE exists
✅ GMAIL_ADDRESS is set
✅ GMAIL_APP_PASSWORD is set
✅ All required configurations present
```

---

## 🚀 Step 7: Test the Application

### First Run:
```bash
# Make sure you're in the project directory
cd "/Users/tifediceeyy/All projects/Agentic Workflows/Web_Scraper&Email"

# Activate virtual environment
source venv/bin/activate

# Run the application
python agent.py
```

### Expected Output:
```
============================================================
🚀 BUSINESS OUTREACH AUTOMATION SYSTEM
============================================================

1. 📋 Start New Campaign
2. ✉️  Generate Emails
3. 📊 Manage Google Sheet
4. 📤 Send Approved Emails
5. 📥 Track Responses
6. 🚪 Exit

============================================================

Enter your choice (1-6):
```

### Quick Test Campaign:
1. Choose option **1** (Start New Campaign)
2. Enter business type: **Coffee Shops**
3. Choose strategy: **2** (Specific Automation)
4. Choose automation: **1** (Appointment Reminder System)
5. Choose data source: **1** (Google Maps)
6. Enter location: **San Francisco, CA**
7. Enter number of businesses: **5** (small test)

**Expected:** Scrapes 5 coffee shops, uploads to Google Sheet

---

## 🔍 Step 8: Verify Google Sheet

1. Open your Google Sheet (from Step 2)
2. Check that businesses were added
3. Verify columns:
   - Name
   - Email
   - Phone
   - Website
   - Location
   - Status (should be "Draft")

---

## 📊 Completion Checklist

Use this to track your progress:

- [ ] ✅ Got Gemini API key from Google AI Studio
- [ ] ✅ Created Google Cloud project
- [ ] ✅ Enabled Google Sheets API and Google Drive API
- [ ] ✅ Created OAuth credentials (Desktop app)
- [ ] ✅ Downloaded credentials.json file
- [ ] ✅ Placed credentials.json in project root
- [ ] ✅ Created Google Sheet and copied Sheet ID
- [ ] ✅ Enabled 2FA on Gmail account
- [ ] ✅ Generated Gmail App Password
- [ ] ✅ Updated .env file with all required variables
- [ ] ✅ Created data/, logs/, .tmp/ directories
- [ ] ✅ Verified Python environment
- [ ] ✅ Ran import test successfully
- [ ] ✅ Ran configuration validation
- [ ] ✅ Launched agent.py successfully
- [ ] ✅ Completed test campaign (5 businesses)
- [ ] ✅ Verified data in Google Sheet

---

## 🆘 Troubleshooting

### Problem: "Module not found" errors
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "GEMINI_API_KEY not found"
**Solution:** Check your `.env` file is in the project root and has the correct variable name (no typos)

### Problem: "credentials.json not found"
**Solution:**
1. Verify file is in project root directory
2. Check filename is exactly `credentials.json` (no extra extensions)
3. Verify `.env` has `GOOGLE_CREDENTIALS_FILE=credentials.json`

### Problem: Gmail authentication failed
**Solution:**
1. Verify 2FA is enabled on your Gmail account
2. Verify App Password is 16 characters (no spaces)
3. Try regenerating the App Password

### Problem: Google Sheets permission denied
**Solution:**
1. First run will open browser for OAuth consent
2. Click "Allow" to grant permissions
3. This creates `token.json` file (one-time setup)

---

## 📞 Need Help?

Check these resources:
1. **Main README:** `README.md`
2. **Comprehensive Review:** `COMPREHENSIVE_REVIEW.md`
3. **Setup Guide:** `SETUP_GUIDE.md`
4. **Quick Start:** `QUICK_START.md`
5. **Logs:** Check `outreach.log` for error details

---

**Once all checklist items are complete, you're ready to run production campaigns!** 🎉
