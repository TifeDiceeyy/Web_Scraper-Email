# Workflow: Generate Emails

## Purpose
Generate personalized emails using Claude API based on campaign strategy.

## CRITICAL: Two Paths

This workflow has TWO DISTINCT PATHS based on `campaign_config.json`:

### Path A: General Help Strategy
**When**: `outreach_type` = "general_help"

**Tool**: `generate_general_email.py`

**Claude Prompt Style**:
```
Subject: Discovery-focused, non-pushy
Body:
  - Ask about their current challenges
  - Offer general help with automation
  - Focus on understanding their needs
  - Broad value proposition
  - No specific solution mentioned
```

**Example Output**:
- Subject: "Quick question about [Business Name]'s operations"
- Body: Asks what problems they face, offers to chat

### Path B: Specific Automation Strategy
**When**: `outreach_type` = "specific_automation"

**Tool**: `generate_specific_email.py`

**Claude Prompt Style**:
```
Subject: Benefit-driven, specific value
Body:
  - Lead with concrete benefit (e.g., "reduce no-shows by 30%")
  - Focus on ONE automation (from automation_focus)
  - Show you understand their specific pain point
  - Include brief case study or stat
  - Clear call-to-action
```

**Example Output**:
- Subject: "Reduce no-shows by 30% at [Business Name]"
- Body: Specific benefit, focused solution, clear CTA

## Steps

### 1. Load Campaign Config
Read `.tmp/campaign_config.json` to determine strategy

### 2. Get Draft Businesses
Call `get_draft_businesses.py` to fetch all businesses with Status = "Draft"

### 3. For Each Business:

#### 3.1 Scrape Website (if available)
- Call `scrape_website.py`
- Extract key info:
  - Services offered
  - Current pain points mentioned
  - Contact information
  - Business tone/style

#### 3.2 Choose Email Generation Tool
```python
if config['outreach_type'] == "general_help":
    use generate_general_email.py
else:
    use generate_specific_email.py
```

#### 3.3 Generate Email
Pass to Claude API:
- Business name
- Business type
- Website content (if scraped)
- Automation focus (if specific strategy)

Receive:
- Subject line
- Email body

#### 3.4 Update Google Sheet
Call `update_sheet_emails.py`:
- Update "Generated Subject" column
- Update "Generated Body" column
- Keep Status = "Draft"

### 4. Review Prompt
Tell user to:
1. Open Google Sheet
2. Review all generated emails
3. Edit any that need changes
4. Change Status to "Approved" for emails to send

## Success Criteria
- All Draft businesses have generated emails
- Emails match campaign strategy
- User knows to review and approve
- Google Sheet updated

## Next Workflow
→ User manually reviews and approves
→ `send_emails.md` when ready

## Important Notes

**DO NOT mix strategies!**
- General Help emails should NOT mention specific automations
- Specific Automation emails should NOT ask discovery questions
- The strategy is locked in campaign_config.json
- Each campaign uses ONE strategy consistently
