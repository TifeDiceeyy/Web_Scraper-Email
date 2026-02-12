# US-001: Business Outreach Automation System

## User Story

As a **business development professional**,
I want **an automated system that scrapes business data, generates personalized emails using AI, and tracks responses**,
So that **I can scale my outreach efforts without manual email writing and follow-up tracking**.

## Context

This implements the WAT Framework (Workflows, Agents, Tools) for business outreach automation:
- **Workflows** = Instructions (markdown SOPs in `workflows/`)
- **Agent** = Decision-maker (orchestrates tool execution in `agent.py`)
- **Tools** = Execution layer (Python scripts in `tools/`)

The system has ONE CRITICAL DECISION POINT: General Help (discovery-focused) vs Specific Automation (benefit-driven), which determines the entire email generation strategy.

## Acceptance Criteria

### Phase 1: Campaign Setup
- [ ] User can start a new campaign and specify business type
- [ ] System asks for outreach strategy (General Help OR Specific Automation)
- [ ] If Specific Automation chosen, user selects which automation to focus on
- [ ] Campaign configuration is saved to `.tmp/campaign_config.json`
- [ ] User can choose data source: Google Maps scraping, JSON file, or manual entry

### Phase 2: Data Collection
- [ ] System can scrape businesses from Google Maps (using external service)
- [ ] System can load businesses from JSON file
- [ ] System allows manual entry of business information
- [ ] All businesses are uploaded to Google Sheets with Status = "Draft"
- [ ] Sheet has columns: Business Name, Location, Email, Phone, Website, Contact Person, Generated Subject, Generated Body, Notes, Status, Date Approved, Date Sent, Last Response, Response Details

### Phase 3: Email Generation
- [ ] System reads campaign configuration to determine strategy
- [ ] For "General Help" strategy: Calls `tools/generate_general_email.py`
- [ ] For "Specific Automation" strategy: Calls `tools/generate_specific_email.py`
- [ ] System scrapes business website for context (if URL available)
- [ ] Gemini API generates personalized subject and body for each business
- [ ] Generated emails are written to Google Sheet (Subject and Body columns)
- [ ] Businesses remain at Status = "Draft" after generation

### Phase 4: Review & Approval
- [ ] User can open Google Sheet to review all generated emails
- [ ] User can edit emails directly in the sheet
- [ ] User changes Status from "Draft" to "Approved" for emails to send

### Phase 5: Email Sending
- [ ] System finds all businesses with Status = "Approved"
- [ ] Emails are sent via Gmail API
- [ ] System updates Status to "Sent" after successful send
- [ ] Date Sent timestamp is recorded
- [ ] System waits 5 seconds between sends to respect rate limits

### Phase 6: Response Tracking
- [ ] System monitors Gmail inbox for replies
- [ ] When reply detected, Status updates to "Replied"
- [ ] Last Response timestamp is recorded
- [ ] Response details/preview is saved to sheet
- [ ] User receives notification via Telegram or Email

### Phase 7: Error Handling & Limits
- [ ] System respects Gmail sending limits (500/day for free, 2000/day for Workspace)
- [ ] System handles API rate limits gracefully
- [ ] Failed emails are logged with error messages
- [ ] System can retry failed operations

## Technical Notes

**API Requirements:**
- Google Gemini API for email generation
- Google Sheets API for data storage
- Gmail API for sending and tracking emails
- Telegram Bot API (optional) for notifications

**Email Strategies:**

**Strategy 1: General Help**
- Subject: "Quick question about [Business Name]"
- Body: Asks about problems, offers general help
- Tone: Curious, non-sales-y, discovery-focused
- Use case: Cold outreach, building relationships

**Strategy 2: Specific Automation**
- Subject: "Reduce [problem] by X% at [Business Name]"
- Body: Leads with benefit, focuses on one automation
- Tone: Confident, benefit-driven, solution-focused
- Use case: Warm leads, focused solution

**Google Sheets Structure:**
Columns in order:
1. Business Name
2. Location
3. Email
4. Phone
5. Website
6. Contact Person
7. Generated Subject
8. Generated Body
9. Your Notes
10. Status (Draft → Approved → Sent → Replied)
11. Date Approved
12. Date Sent
13. Last Response
14. Response Details

## Edge Cases

- [ ] Empty website: Skip scraping, generate email without context
- [ ] Invalid email address: Mark as "Invalid" status, skip sending
- [ ] Gmail authentication expires: Re-authenticate with OAuth flow
- [ ] Claude API timeout: Retry with exponential backoff
- [ ] Duplicate businesses: Check before adding to sheet
- [ ] No approved emails: Show message, don't attempt to send
- [ ] Reply detection false positive: Log for manual review
- [ ] Network error during scraping: Continue with remaining businesses

## Out of Scope

- Custom email templates beyond the two strategies
- CRM integration (Salesforce, HubSpot, etc.)
- Advanced A/B testing (future enhancement)
- Automated follow-up sequences (future enhancement)
- Multi-language support (English only for MVP)
- Email open tracking (requires additional infrastructure)

## UI/UX Notes

**Agent Menu Structure:**
```
🚀 BUSINESS OUTREACH AUTOMATION SYSTEM
1. 📋 Start New Campaign
2. ✉️  Generate Emails
3. 📊 Manage Google Sheet
4. 📤 Send Approved Emails
5. 📥 Track Responses
6. 🚪 Exit
```

**Critical Decision Flow:**
```
Business Type? → Dentists
Outreach Strategy?
  1. General Help (discovery-focused)
  2. Specific Automation (benefit-driven)
→ If option 2: Which automation?
  1. Appointment Scheduling
  2. Customer Follow-up
  3. Review Management
  (etc.)
```

## Testing Notes

**Test Scenarios:**
1. **Happy Path**: Complete flow with 3 test businesses
2. **General Help Email**: Verify tone is discovery-focused
3. **Specific Automation Email**: Verify benefit-driven messaging
4. **Rate Limiting**: Test with 10+ businesses to verify delays
5. **Failed Scrape**: Test with invalid URL
6. **Gmail Auth**: Test OAuth flow on first run
7. **Response Detection**: Send test reply and verify tracking

**Test Data:**
Create sample businesses JSON with:
- Valid websites
- Invalid websites
- Missing emails
- Different business types

## Dependencies

**External Services:**
- Google Cloud Console (Sheets API + Gmail API enabled)
- Anthropic API account with credits
- Gmail account with App Password (for sending)
- Telegram Bot (optional, for notifications)

**Python Packages:**
- `anthropic` - Claude API client
- `google-auth-oauthlib` - Google OAuth
- `google-api-python-client` - Google APIs
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `python-dotenv` - Environment variables
- `schedule` or `APScheduler` - Task scheduling (optional)

## Success Metrics

- ✅ Campaign setup completes in < 2 minutes
- ✅ Email generation: 90%+ success rate
- ✅ Emails are personalized (mention business name, context from website)
- ✅ General Help vs Specific Automation emails are clearly different in tone
- ✅ Email sending: 100% success for approved emails (with retries)
- ✅ Response tracking: < 5 minute delay in detecting replies
- ✅ System handles 50+ businesses without manual intervention

---

**Created:** 2026-02-12
**Status:** 📝 Planned
