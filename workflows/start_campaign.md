# Workflow: Start Campaign

## Purpose
Initialize a new business outreach campaign with the correct strategy.

## Steps

### 1. Ask Business Type
- Prompt user for target business type
- Examples: Dentists, Restaurants, Plumbers, Hair Salons
- Store in `campaign_config.json`

### 2. Ask Outreach Strategy (CRITICAL DECISION)
This determines everything downstream:

**Option A: General Help**
- Discovery-focused
- Asks about problems
- Offers general automation help
- Broader appeal, lower initial conversion

**Option B: Specific Automation**
- Benefit-driven
- Leads with specific value proposition
- Focuses on one automation
- Higher conversion for target problem

**Storage**: Save as `outreach_type` = "general_help" or "specific_automation"

### 3. If Specific Automation: Ask Focus
- Only if Step 2 = "specific_automation"
- Prompt for which automation to highlight
- Examples:
  - Appointment Reminder System
  - Review Request Automation
  - Lead Follow-up System
  - Customer Feedback Collection
- Store in `campaign_config.json` as `automation_focus`

### 4. Ask Data Source
Options:
- Google Maps scraping
- JSON file upload
- Manual entry

### 5. Collect Businesses
Based on data source:
- **Google Maps**: Call `scrape_google_maps.py`
- **JSON**: Call `load_json.py`
- **Manual**: Interactive entry

### 6. Upload to Google Sheets
- Call `upload_to_sheets.py`
- Set all Status = "Draft"
- Create columns if sheet is new

### 7. Save Configuration
Write to `.tmp/campaign_config.json`:
```json
{
  "business_type": "Dentists",
  "outreach_type": "specific_automation",
  "automation_focus": "Appointment Reminder System",
  "data_source": "google_maps",
  "total_businesses": 25
}
```

## Success Criteria
- Configuration saved
- Businesses uploaded to sheet
- All businesses have Status = "Draft"
- User knows next step (generate emails)

## Next Workflow
→ `generate_emails.md`
