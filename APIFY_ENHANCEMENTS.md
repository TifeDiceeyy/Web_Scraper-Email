# Apify Integration Enhancements

This document describes the three major enhancements integrated into your business outreach automation system using Apify.

---

## 🎯 Overview

Your system now has **three powerful enhancements**:

1. **Contact Enrichment** - Find emails and phone numbers from websites
2. **Multi-Platform Scraping** - Scrape leads from Instagram, Facebook, TikTok
3. **Email Verification** - Validate emails before sending campaigns

---

## 1. 📧 Contact Enrichment

**File:** `tools/enrich_contacts.py`

### What It Does

- Scrapes business websites to find email addresses and phone numbers
- Uses Apify's `vdrmota/contact-info-scraper` Actor
- Crawls up to 5 pages per domain
- Automatically enriches businesses that have websites but no emails

### How to Use

```python
from tools.enrich_contacts import enrich_business_contacts

# Your businesses with websites
businesses = [
    {
        'name': 'Coffee Shop',
        'website': 'https://example.com',
        'email': '',  # Empty - will be enriched
        'phone': ''
    }
]

# Enrich with contact data
enriched = enrich_business_contacts(businesses)

# Now businesses have:
# - email: Primary email found
# - phone: Primary phone found
# - all_emails: List of all emails found
# - all_phones: List of all phones found
```

### Example Output

```
🔍 CONTACT ENRICHMENT
============================================================
📊 Enriching 10 businesses with contact data...

⏳ Running Apify Contact Scraper (this may take 2-3 minutes)...
✅ Scraping complete! Processing contact data...

✅ Enriched 8 businesses with contact data!
```

---

## 2. 📱 Multi-Platform Scraping

**File:** `tools/scrape_social_media.py`

### What It Does

- Scrapes business profiles from Instagram, Facebook, and TikTok
- Extracts contact information (emails, phones, websites)
- Gets follower counts and engagement metrics
- Supports multiple platforms in one query

### Supported Platforms

| Platform  | Function                      | Actor Used                              |
| --------- | ----------------------------- | --------------------------------------- |
| Instagram | `scrape_instagram_profiles()` | `apify/instagram-profile-scraper`       |
| Facebook  | `scrape_facebook_pages()`     | `apify/facebook-pages-scraper`          |
| TikTok    | `scrape_tiktok_users()`       | `clockworks/tiktok-user-search-scraper` |

### How to Use

#### Single Platform

```python
from tools.scrape_social_media import scrape_instagram_profiles

# Scrape Instagram profiles
leads = scrape_instagram_profiles(
    search_query="coffee shop san francisco",
    max_results=20
)

# Each lead has:
# - name, username, bio
# - email (if business account)
# - phone (if provided)
# - website
# - followers
# - profile_url
```

#### Multiple Platforms

```python
from tools.scrape_social_media import scrape_multi_platform

# Scrape from multiple platforms at once
all_leads = scrape_multi_platform(
    business_type="coffee shop",
    location="San Francisco",
    platforms=['instagram', 'facebook', 'tiktok'],
    max_per_platform=10
)

# Returns combined list from all platforms
# Each lead is tagged with 'platform' field
```

### Example Output

```
🌐 MULTI-PLATFORM LEAD SCRAPER
============================================================
🔍 Business Type: coffee shop
📍 Location: San Francisco
📱 Platforms: instagram, facebook

📸 INSTAGRAM PROFILE SCRAPER
============================================================
⏳ Running Apify Instagram Scraper...
✅ Found 10 Instagram profiles!

📘 FACEBOOK PAGE SCRAPER
============================================================
⏳ Running Apify Facebook Scraper...
✅ Found 8 Facebook pages!

============================================================
✅ TOTAL LEADS FOUND: 18
============================================================
  Instagram: 10 leads
  Facebook: 8 leads
```

---

## 3. ✉️ Email Verification

**File:** `tools/verify_emails.py`

### What It Does

- Validates email syntax (RFC 5322 compliant)
- Checks DNS MX records to verify domain can receive emails
- Detects disposable/temporary email addresses
- Marks invalid emails before sending campaigns

### Validation Checks

1. **Syntax** - Valid email format (user@domain.com)
2. **DNS** - Domain has valid MX records
3. **Disposable** - Not from temporary email services

### How to Use

#### Verify Single Email

```python
from tools.verify_emails import verify_email

result = verify_email('contact@example.com', check_dns=True)

# Returns:
# {
#     'email': 'contact@example.com',
#     'valid': True,
#     'reason': 'Valid email address',
#     'checks': {
#         'syntax': True,
#         'dns': True,
#         'disposable': False
#     }
# }
```

#### Verify Business List

```python
from tools.verify_emails import verify_businesses

businesses = [
    {'name': 'Coffee Shop', 'email': 'hello@example.com'},
    {'name': 'Invalid Business', 'email': 'bad-email'},
]

verified = verify_businesses(businesses, check_dns=True)

# Each business now has:
# - email_verified: True/False
# - email_status: 'valid' or reason for failure
```

### Example Output

```
🔍 BUSINESS EMAIL VERIFICATION
============================================================
📊 Verifying 50 business emails...

============================================================
✅ Valid: 42
❌ Invalid: 5
⚠️  No email: 3

❌ Invalid emails found:
   • Business A: bad@email (Invalid email syntax)
   • Business B: test@tempmail.com (Disposable email address)
   • Business C: contact@nonexistent.xyz (No MX records found for domain)
```

---

## 🚀 Complete Workflow Example

Here's how to use all three enhancements together:

```python
from dotenv import load_dotenv
from tools.scrape_google_maps import scrape_with_apify
from tools.scrape_social_media import scrape_multi_platform
from tools.enrich_contacts import enrich_business_contacts
from tools.verify_emails import verify_businesses

load_dotenv()

# Step 1: Scrape Google Maps
businesses = scrape_with_apify(
    business_type="Coffee Shop",
    location="San Francisco, CA",
    max_results=20
)

# Step 2: Scrape Social Media (optional)
social_leads = scrape_multi_platform(
    business_type="Coffee Shop",
    location="San Francisco",
    platforms=['instagram', 'facebook'],
    max_per_platform=10
)

# Combine all leads
all_leads = businesses + social_leads

# Step 3: Enrich contacts (find missing emails)
enriched_leads = enrich_business_contacts(all_leads)

# Step 4: Verify all emails
verified_leads = verify_businesses(enriched_leads, check_dns=True)

# Filter to only valid, contactable leads
ready_to_contact = [
    lead for lead in verified_leads
    if lead.get('email_verified') and lead.get('email')
]

print(f"✅ {len(ready_to_contact)} leads ready for outreach!")
```

---

## 📊 Demo Script

Run the complete demo:

```bash
# Full demo (uses Apify credits)
python demo_apify_enhancements.py

# Quick test (no API calls, just email verification)
python demo_apify_enhancements.py quick
```

---

## 💰 Apify Credits Usage

| Enhancement         | Actor Used                        | Approx. Cost (per run) |
| ------------------- | --------------------------------- | ---------------------- |
| Google Maps Scraper | `compass/crawler-google-places`   | $0.50 per 100 results  |
| Contact Enrichment  | `vdrmota/contact-info-scraper`    | $1.00 per 100 URLs     |
| Instagram Scraper   | `apify/instagram-profile-scraper` | $0.20 per 100 profiles |
| Facebook Scraper    | `apify/facebook-pages-scraper`    | $0.30 per 100 pages    |
| TikTok Scraper      | `clockworks/tiktok-user-search`   | $0.25 per 100 users    |

**Note:** Apify offers a free tier with $5/month in credits for testing.

---

## ⚙️ Configuration

All enhancements use the same `APIFY_TOKEN` from your `.env` file:

```bash
# .env
APIFY_TOKEN=your_apify_token_here
```

---

## 🔧 Integration with Main Agent

To integrate with your main `agent.py`, add these options to your workflow:

### Option 1: Enhanced Google Maps Scraping

```python
# In agent.py, after scraping Google Maps:
from tools.enrich_contacts import enrich_business_contacts
from tools.verify_emails import verify_businesses

# Enrich and verify
businesses = enrich_business_contacts(businesses)
businesses = verify_businesses(businesses, check_dns=True)
```

### Option 2: Multi-Platform Campaign

```python
# In agent.py, add new menu option:
# "3. 📱 Scrape Social Media"

from tools.scrape_social_media import scrape_multi_platform

social_leads = scrape_multi_platform(
    business_type=business_type,
    location=location,
    platforms=['instagram', 'facebook'],
    max_per_platform=20
)
```

### Option 3: Auto-Verify Before Sending

```python
# In send_emails.py, before sending:
from tools.verify_emails import verify_businesses

# Verify approved emails
businesses = verify_businesses(businesses, check_dns=True)

# Only send to verified emails
businesses_to_send = [
    b for b in businesses
    if b.get('email_verified') and b['status'] == 'Approved'
]
```

---

## 🎯 Best Practices

1. **Contact Enrichment**
   - Run after Google Maps scraping to find missing emails
   - Only enrich businesses with websites
   - Check results before sending campaigns

2. **Social Media Scraping**
   - Use for B2C campaigns (influencers, creators)
   - Instagram works best for visual businesses (cafes, gyms, salons)
   - Facebook better for local businesses

3. **Email Verification**
   - Always verify before sending campaigns
   - Use `check_dns=False` for faster verification in development
   - Use `check_dns=True` for production campaigns

4. **Credit Management**
   - Start with small batches (10-20 results) for testing
   - Monitor your Apify dashboard for credit usage
   - Use the free tier ($5/month) for development

---

## 📚 Additional Resources

- [Apify Documentation](https://docs.apify.com/)
- [Google Maps Scraper Docs](https://apify.com/compass/crawler-google-places)
- [Instagram Scraper Docs](https://apify.com/apify/instagram-profile-scraper)
- [Contact Info Scraper Docs](https://apify.com/vdrmota/contact-info-scraper)

---

**Last Updated:** 2026-02-12
