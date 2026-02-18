# 🧪 End-to-End Testing Plan

**Date:** 2026-02-12
**Purpose:** Validate all Week 1 features work together
**Duration:** ~15-20 minutes

---

## 📋 Test Sequence

We'll test the complete workflow:
1. ✅ **Instagram Scraping** → Get profiles
2. ✅ **Contact Enrichment** → Get emails/phones from websites
3. ✅ **Email Verification** → Validate email addresses
4. ✅ **Google Sheet Updates** → Verify data persistence

---

## 🎯 Test 1: Instagram Profile Scraping

### What We're Testing:
- Instagram hashtag search functionality
- Profile data extraction
- Google Sheet upload

### Steps:
```bash
python agent.py
# Choose: 6 (Scrape Social Media)
# Choose: 1 (Instagram)
# Hashtag: coffee
# Max results: 5
```

### Expected Results:
✅ Found 5 unique Instagram profiles
✅ Data includes: username, name, profile_url
✅ Uploaded to Google Sheet

### What to Check:
- [ ] No errors during scraping
- [ ] Profile usernames displayed
- [ ] Google Sheet has new rows
- [ ] Profile URLs are valid (format: https://instagram.com/username)

---

## 🎯 Test 2: Contact Enrichment

### What We're Testing:
- Website scraping for contact info
- Email/phone extraction
- Handling of blocked websites

### Prerequisites:
- Instagram profiles from Test 1 (need website URLs)
- OR manually add some business websites to Google Sheet

### Steps:
```bash
python agent.py
# Choose: 7 (Enrich Contact Info)
# Confirm: yes
```

### Expected Results:
✅ Scrapes business websites
⚠️ 40-60% success rate (some will be blocked)
✅ Adds emails/phones where found
✅ Updates Google Sheet

### What to Check:
- [ ] No crash on blocked websites
- [ ] Enriched count matches expectations
- [ ] Helpful error messages if low success rate
- [ ] Google Sheet updated with new emails/phones

### Known Limitations:
- Corporate sites (Starbucks, Blue Bottle) → Likely blocked
- Small local businesses → Higher success rate
- 40-60% success is NORMAL

---

## 🎯 Test 3: Email Verification

### What We're Testing:
- Email syntax validation
- DNS MX record checking
- Results display and feedback

### Prerequisites:
- Businesses with emails from Test 2
- OR manually add some test emails

### Test 3A: Quick Verification (Syntax Only)
```bash
python agent.py
# Choose: 8 (Verify Email Addresses)
# Choose: 1 (Quick - syntax only)
# Confirm: yes
```

### Expected Results:
✅ Fast validation (~1 second)
✅ Catches format errors (@@, missing @, etc.)
✅ Shows valid/invalid breakdown
✅ Lists invalid emails with reasons

### Test 3B: Full Verification (DNS Check)
```bash
python agent.py
# Choose: 8 (Verify Email Addresses)
# Choose: 2 (Full - syntax + DNS)
# Confirm: yes
```

### Expected Results:
✅ Slower validation (~1-2 minutes)
✅ Checks DNS MX records
✅ Detects disposable emails
✅ Shows detailed reasons for failures

### What to Check:
- [ ] Both verification modes work
- [ ] Results show percentages
- [ ] Invalid emails explained clearly
- [ ] No crashes on network issues

---

## 🎯 Test 4: Google Sheet Integration

### What We're Testing:
- Data persistence
- Column mapping
- No duplicate rows

### Steps:
1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1lt1ykDA13Pa4S-tj8wEiKYXSxHS2wQgLIcaX5YGse4U/edit
2. Check for new data from Tests 1-3

### Expected Columns:
- Name
- Location
- Category
- Website
- Email
- Phone
- Platform (instagram, google_maps, etc.)
- Profile URL
- Notes

### What to Check:
- [ ] All scraped profiles appear
- [ ] Enriched data filled in
- [ ] No duplicate rows
- [ ] Data is readable and formatted correctly

---

## 📊 Success Criteria

### Minimum Requirements (Must Pass):
- ✅ Instagram scraper returns 5 profiles
- ✅ No crashes or unhandled exceptions
- ✅ Data appears in Google Sheet
- ✅ Email verification runs without errors

### Nice to Have (Bonus):
- ✅ 40%+ contact enrichment success rate
- ✅ 80%+ email validation rate
- ✅ Clear error messages for failures
- ✅ Fast performance (<2 min per test)

---

## 🐛 Known Issues to Watch For

### Issue 1: Instagram Rate Limiting
**Symptom:** "Too many requests" error
**Cause:** Apify free tier limit hit
**Solution:** Wait 5 minutes, try again with fewer results

### Issue 2: Contact Enrichment Low Success
**Symptom:** 0-20% enrichment rate
**Cause:** Corporate websites blocking scraper
**Solution:** This is NORMAL - don't panic!

### Issue 3: DNS Verification Timeout
**Symptom:** Verification hangs or times out
**Cause:** Slow DNS servers or network issues
**Solution:** Use Quick mode (syntax only) instead

### Issue 4: Google Sheet Permission Error
**Symptom:** "Permission denied" when uploading
**Cause:** credentials.json expired or invalid
**Solution:** Re-authenticate Google API

---

## 📝 Test Results Template

Copy this and fill in as you test:

```
## TEST RESULTS - [Your Name]
Date: 2026-02-12

### Test 1: Instagram Scraping
Status: [ ] Pass [ ] Fail
Profiles found: ___ / 5
Notes: ___________________

### Test 2: Contact Enrichment
Status: [ ] Pass [ ] Fail
Success rate: ____%
Enriched: ___ / ___
Notes: ___________________

### Test 3: Email Verification
Status: [ ] Pass [ ] Fail
Quick mode: [ ] Pass [ ] Fail
Full mode: [ ] Pass [ ] Fail
Valid rate: ____%
Notes: ___________________

### Test 4: Google Sheet
Status: [ ] Pass [ ] Fail
Data visible: [ ] Yes [ ] No
Columns correct: [ ] Yes [ ] No
Notes: ___________________

### Overall Status:
[ ] All tests passed - Ready for production!
[ ] Some issues - Need fixes (details above)
[ ] Major problems - Needs debugging
```

---

## 🚀 After Testing

### If All Tests Pass:
1. ✅ Document success
2. ✅ Move to Week 2 (Testing Infrastructure)
3. ✅ Consider Week 3 (Documentation)

### If Tests Fail:
1. 🐛 Document errors with details
2. 🔍 Debug issues together
3. 🔧 Fix and re-test

---

## 💡 Testing Tips

1. **Start fresh:** Clear Google Sheet or use test tab
2. **One test at a time:** Don't rush through
3. **Copy error messages:** If something fails, copy full output
4. **Check logs:** Look at console output for clues
5. **Screenshot results:** Especially Google Sheet state

---

Ready to start testing! 🎯
