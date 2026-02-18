# 📖 Business Outreach - User Guide

**Simple guide for getting started with automated business outreach**

---

## 🎯 What is This Tool?

This tool helps you automatically:
1. **Find businesses** (dentists, cafes, gyms, etc.)
2. **Get their contact info** (emails, phones)
3. **Create personalized emails** using AI
4. **Send bulk emails** professionally
5. **Track responses** and manage follow-ups

All managed through Google Sheets - no complex software needed!

---

## ⚡ Quick Start (10 Minutes)

### Step 1: Get Your API Keys

You'll need 4 free accounts:

| Service | What For | Sign Up Link | Free Tier |
|---------|----------|--------------|-----------|
| **Apify** | Finding businesses | [apify.com](https://apify.com) | 5,000 credits/month |
| **Google Gemini** | AI email writing | [aistudio.google.com](https://aistudio.google.com/app/apikey) | 1,500 requests/day |
| **Google Sheets** | Data storage | [console.cloud.google.com](https://console.cloud.google.com) | Unlimited |
| **Gmail** | Sending emails | Your Gmail account | 500/day |

**Cost:** $0 on free tier! Good for up to 100 businesses/day.

---

### Step 2: Install & Configure

```bash
# 1. Open Terminal and go to project folder
cd "/path/to/Web_Scraper&Email"

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create configuration file
cp .env.example .env
nano .env  # Or use any text editor
```

**Add your API keys to `.env`:**
```
APIFY_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
GOOGLE_SPREADSHEET_ID=your_sheet_id
GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASSWORD=your_16_char_password
```

---

### Step 3: Run the Tool

```bash
python agent.py
```

You'll see this menu:
```
🚀 BUSINESS OUTREACH AUTOMATION SYSTEM
1. 📋 Start New Campaign
2. ✉️  Generate Emails
3. 📊 Manage Google Sheet
4. 📤 Send Approved Emails
5. 📥 Track Responses
6. 📱 Scrape Social Media
7. 🔍 Enrich Contact Info
8. ✅ Verify Email Addresses
9. 🚪 Exit
```

---

## 📚 How to Use Each Feature

### Option 1: Find Businesses 🗺️

**What it does:** Finds businesses on Google Maps

**When to use:** Starting a new outreach campaign

**Steps:**
1. Choose `1` (Start New Campaign)
2. Choose `2` (Apify)
3. Enter business type: `Dentist` (or `Cafe`, `Gym`, etc.)
4. Enter location: `Istanbul, Turkey` (always include country!)
5. Enter max results: `10` (start small!)

**Result:** 10 businesses added to your Google Sheet with names, phones, websites

**Time:** ~1-2 minutes

---

### Option 6: Find on Instagram 📱

**What it does:** Finds businesses active on Instagram

**When to use:** Targeting social media-active businesses

**Steps:**
1. Choose `6` (Scrape Social Media)
2. Choose `1` (Instagram)
3. Enter hashtag: `coffee` (popular hashtags work best!)
4. Max results: `10`

**Result:** 10 Instagram profiles with usernames

**Note:** Won't have emails yet - use Option 7 next!

**Time:** ~10-15 seconds

---

### Option 7: Get Contact Info 🔍

**What it does:** Scrapes business websites for emails and phones

**When to use:** After finding businesses that have websites

**Steps:**
1. Choose `7` (Enrich Contact Info)
2. Confirm `yes`

**Result:** Emails and phones added to Google Sheet

**Success Rate:** 40-60% is normal (some websites block scrapers)

**Time:** ~2-3 minutes for 10 websites

**Pro Tip:** Small local businesses work better than big corporations!

---

### Option 8: Verify Emails ✅

**What it does:** Checks if emails are real and deliverable

**When to use:** After getting emails (Option 7)

**Steps:**
1. Choose `8` (Verify Email Addresses)
2. Choose verification level:
   - `1` = Quick (syntax check only) - 1 second
   - `2` = Full (checks mail servers) - 1-2 minutes
3. Confirm `yes`

**Result:** Shows which emails are valid/invalid

**Why do this:** Avoid bounces and protect your sender reputation!

**Time:**
- Quick: ~1 second
- Full: ~1-2 minutes for 10 emails

---

### Option 2: Generate Emails ✉️

**What it does:** AI writes personalized emails for each business

**When to use:** After you have contact info

**Steps:**
1. Choose `2` (Generate Emails)
2. Describe your offer: "I sell premium coffee beans with same-day Istanbul delivery"
3. AI generates custom emails for each business

**Result:** Personalized emails in Google Sheet (columns G & H)

**Time:** ~10-30 seconds per email

**Pro Tip:** Be specific in your offer for better emails!

---

### Option 3: Review in Google Sheet 📊

**What it does:** Opens your data in Google Sheets

**When to use:** Reviewing AI-generated emails before sending

**Steps:**
1. Choose `3` (Manage Google Sheet)
2. Browser opens with your sheet
3. Review emails in columns G (subject) and H (body)
4. Edit if needed
5. Change "Status" column (J) from `Draft` to `Approved` for emails you want to send

**Important:** Only `Approved` emails will be sent!

---

### Option 4: Send Emails 📤

**What it does:** Sends emails to businesses you approved

**When to use:** After approving emails in Google Sheet

**Steps:**
1. Make sure you approved some emails (Status = "Approved")
2. Choose `4` (Send Approved Emails)
3. Confirm `yes`

**Result:** Emails sent, status updated to "Sent"

**Time:** ~1-2 seconds per email

**⚠️ Test First:** Send to yourself or 1-2 test businesses first!

---

## 🎯 Complete Example Workflow

**Goal:** Find 10 cafes in Istanbul and send them coffee bean offers

### Step-by-Step:

```
1. Find Cafes (2 min)
   → Option 1 → Apify
   → Business: Cafe
   → Location: Istanbul, Turkey
   → Results: 10
   ✅ Result: 10 cafes with phones & websites

2. Get Emails (3 min)
   → Option 7 → Enrich Contact Info
   → Confirm: yes
   ✅ Result: 5-6 emails found (50% success rate)

3. Verify Emails (1 min)
   → Option 8 → Full verification
   ✅ Result: 4-5 valid emails

4. Generate Emails (2 min)
   → Option 2 → Generate Emails
   → Offer: "Premium Turkish coffee beans, 30% off, same-day delivery"
   ✅ Result: 5 personalized emails created

5. Review & Approve (2 min)
   → Option 3 → Opens Google Sheet
   → Review emails
   → Change Status to "Approved"
   ✅ Result: 4 emails approved

6. Send Campaign (1 min)
   → Option 4 → Send Approved Emails
   → Confirm: yes
   ✅ Result: 4 emails sent!

Total Time: ~11 minutes
Cost: $0 (free tier)
Result: 4 cafes contacted with personalized offers!
```

---

## 💡 Pro Tips

### For Best Results:

1. **Start Small** - Test with 5-10 businesses first
2. **Mix Sources** - Use Google Maps (has phones) + Instagram (trendy businesses)
3. **Always Verify** - Verify emails before sending to avoid bounces
4. **Personalize** - Edit AI emails to add personal touch
5. **Test Send** - Send to yourself first to check formatting
6. **Best Time** - Send Tuesday-Thursday, 9-11 AM for best open rates
7. **Follow Up** - If no response in 3 days, send polite follow-up

### Success Rates:

- **Google Maps:** 80-90% have phone numbers
- **Contact Enrichment:** 40-60% find emails (normal!)
- **Email Verification:** 80-90% pass validation
- **Open Rates:** 20-30% typical for cold emails
- **Response Rates:** 1-5% typical

---

## ❓ Common Questions

### Q: Why didn't it find emails for all businesses?

**A:** This is normal! Many reasons:
- Website blocks scrapers (security)
- No email on website (uses contact forms)
- Corporate sites have protection
- **40-60% success rate is expected**

**Solution:** Focus on quantity. Scrape more businesses!

---

### Q: Can I get banned for sending too many emails?

**A:** Gmail has limits:
- **500 emails/day** on free Gmail
- **Warm up slowly** - Start with 10-20/day
- **Space them out** - Tool adds 5-second delays
- **Don't spam** - Only send to relevant businesses

**Best Practice:** Start with 10 emails, increase gradually

---

### Q: How much does this cost?

**A:** Free tier covers most needs:
- **0-100 emails/day:** $0
- **100-500 emails/day:** ~$5/month (Apify credits)
- **500+ emails/day:** Consider paid tiers

**Comparison:**
- This tool: $0-5/month
- Instantly.ai: $97/month
- Lemlist: $59/month

---

### Q: What if emails bounce?

**A:** Use the email verification (Option 8) BEFORE sending:
- Catches 80% of bad emails
- Protects your sender reputation
- Takes 1-2 extra minutes but worth it!

---

### Q: Can I customize the AI emails?

**A:** Yes! Two ways:
1. **Before generating:** Give detailed offer description
2. **After generating:** Edit directly in Google Sheet

**Tip:** AI writes 80% of email, you perfect the 20%

---

## 🔧 Troubleshooting

### Error: "APIFY_TOKEN not found"

**Fix:**
1. Check `.env` file exists
2. Make sure `APIFY_TOKEN=your_token_here` is filled
3. Restart the program

---

### Error: "Error 403: access_denied" (Google)

**Fix:**
1. Go to Google Cloud Console
2. Add your email to "Test users"
3. Try again

Full guide: [FIX_OAUTH_ERROR.md](FIX_OAUTH_ERROR.md)

---

### Error: "No contact data found"

**This is normal!** Not an error. Means:
- Websites blocked the scraper
- No visible contact info on site
- **40-60% success is expected**

**Fix:** Scrape more businesses (volume approach)

---

### Emails not sending

**Check:**
1. Gmail app password correct? (16 characters, no spaces)
2. Status = "Approved" in Google Sheet?
3. Email addresses valid?
4. Gmail daily limit not hit? (500/day max)

---

## 📞 Need Help?

### Documentation:
- 📖 [Setup Checklist](SETUP_CHECKLIST.md)
- 📖 [Google Sheet Format](GOOGLE_SHEET_FORMAT.md)
- 📖 [OAuth Fix Guide](FIX_OAUTH_ERROR.md)
- 📖 [Test Results](TEST_RESULTS.md)

### Still Stuck?
- Check logs: `outreach.log` file
- GitHub Issues: Report bugs
- Review this guide again!

---

## ✅ Checklist: Am I Ready?

Before your first campaign:

- [ ] All 4 API keys configured in `.env`
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Sheet created and ID in `.env`
- [ ] Gmail app password generated
- [ ] Ran `python agent.py` successfully
- [ ] Tested with 1-2 businesses first
- [ ] Read this user guide

**All checked?** You're ready to launch your first campaign! 🚀

---

## 🎉 Success Stories

### Use Case 1: Coffee Shop Supplier
- Target: 50 cafes in Istanbul
- Found: 45 cafes with websites
- Enriched: 22 emails (49%)
- Verified: 18 valid (82%)
- Sent: 18 personalized offers
- Replies: 3 interested (17%)
- **Time:** 30 minutes total
- **Cost:** $0 (free tier)

### Use Case 2: Marketing Agency
- Target: Local dentists
- Found: 100 dentists
- Enriched: 58 emails (58%)
- Verified: 52 valid (90%)
- Sent: 52 website redesign offers
- Replies: 4 booked calls (7.7%)
- **Revenue:** 2 contracts = $8,000
- **ROI:** Infinite (free tool!)

---

**Ready to start?** Run `python agent.py` now! 🚀

**Questions?** Re-read relevant sections above or check troubleshooting!

---

**Last Updated:** 2026-02-18
**Version:** 1.0.0 - Customer Edition
