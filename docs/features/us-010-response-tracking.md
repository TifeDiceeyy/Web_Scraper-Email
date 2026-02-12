# US-010: Response Tracking & Analytics

**Status:** 📝 Planned
**Priority:** P0 (Critical)
**Estimated Effort:** 12 hours

---

## User Story

**As a** user who has sent outreach emails
**I want** to automatically track which businesses replied
**So that** I can follow up with interested prospects and measure campaign effectiveness

---

## Acceptance Criteria

1. [ ] Gmail API integration to fetch replies
2. [ ] Match replies to sent emails (by subject, recipient, Message-ID)
3. [ ] Extract reply metadata:
   - Reply date/time
   - Sender (confirm it's the business)
   - Email body snippet
4. [ ] Update Google Sheet with reply status:
   - Column M: Response Received (TRUE/FALSE)
   - Column N: Response Date
5. [ ] AI sentiment analysis on reply content:
   - Positive (interested)
   - Negative (not interested)
   - Neutral (needs more info)
   - Out of Office (auto-reply)
6. [ ] Response analytics displayed in dashboard:
   - Total sent vs total replied
   - Response rate percentage
   - Average time to reply
   - Sentiment distribution
7. [ ] Manual trigger: Check for responses on demand
8. [ ] Automated trigger: Check daily (future)

---

## Technical Requirements

### Gmail API Setup

**Scopes Required:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'  # for marking as read
]
```

**Authentication:**
- Same OAuth2 flow as Google Sheets
- Additional scope consent required
- Refresh token stored locally

### Reply Detection Logic

**Method 1: Message-ID Threading**
```python
# When sending email, save Message-ID
sent_message_id = msg['Message-ID']

# Later, search for replies
query = f"in:inbox to:me in-reply-to:{sent_message_id}"
messages = gmail_service.users().messages().list(userId='me', q=query).execute()
```

**Method 2: Subject Line Matching**
```python
# Search for emails with "Re: [Original Subject]"
query = f"in:inbox to:me subject:'Re: {original_subject}'"
```

**Method 3: Email Thread Detection**
```python
# Gmail automatically threads emails
# Get thread, check if it has >1 message
thread = gmail_service.users().threads().get(userId='me', id=thread_id).execute()
if len(thread['messages']) > 1:
    # Thread has replies
```

---

## Sentiment Analysis

### Gemini Prompt

```python
sentiment_prompt = f"""Analyze this email reply and classify the sentiment.

Original Email Subject: {sent_subject}
Reply Content:
{reply_body}

Classify into exactly ONE category:
1. POSITIVE - Interested, wants to learn more, open to call/meeting
2. NEGATIVE - Not interested, no thanks, unsubscribe request
3. NEUTRAL - Needs more information, asking questions, non-committal
4. OUT_OF_OFFICE - Automated out-of-office reply

Respond with ONLY the category name (POSITIVE, NEGATIVE, NEUTRAL, or OUT_OF_OFFICE).
"""
```

### Sentiment Confidence

```python
# If sentiment is unclear, mark as NEUTRAL
# Future: Add confidence score (0-100%)
{
    "sentiment": "POSITIVE",
    "confidence": 85,
    "keywords": ["interested", "schedule a call", "tell me more"]
}
```

---

## Data Flow

```
1. User clicks "Track Responses" in menu
2. System fetches all businesses with Status = "Sent"
3. For each sent business:
   a. Search Gmail for replies (by subject or Message-ID)
   b. If reply found:
      - Extract reply date, body snippet
      - Call Gemini for sentiment analysis
      - Update Sheet: Response Received = TRUE, Response Date, Sentiment
   c. If no reply found:
      - Skip (leave as-is)
4. Display summary:
   - X replies found
   - Y positive, Z neutral, W negative
   - Response rate: X/Total Sent
```

---

## Google Sheet Updates

### New Columns (Optional)

| Column | Name | Type | Description |
|--------|------|------|-------------|
| O | Sentiment | Text | POSITIVE, NEGATIVE, NEUTRAL, OUT_OF_OFFICE |
| P | Reply Snippet | Text | First 100 chars of reply |
| Q | Follow-up Status | Text | Pending, Scheduled, Completed, Not Needed |

### Update Logic

```python
def update_response_status(row_number, reply_date, sentiment, snippet):
    """Update Sheet with reply information"""
    range_name = f'M{row_number}:P{row_number}'
    values = [[
        'TRUE',                    # Response Received
        reply_date,                # Response Date
        sentiment,                 # Sentiment
        snippet[:100]              # Reply Snippet (truncated)
    ]]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
```

---

## Analytics Dashboard

### CLI Output

```
╔═══════════════════════════════════════════════════════════╗
║              RESPONSE TRACKING RESULTS                    ║
╠═══════════════════════════════════════════════════════════╣
║ Emails Sent:          35                                  ║
║ Responses Received:   12 (34.3% response rate)            ║
║                                                           ║
║ Sentiment Breakdown:                                      ║
║   ✅ Positive:        8 (66.7%)                           ║
║   ⚪ Neutral:         3 (25.0%)                           ║
║   ❌ Negative:        1 (8.3%)                            ║
║   📧 Out of Office:   0 (0.0%)                            ║
║                                                           ║
║ Average Time to Reply: 2.4 days                           ║
║ Fastest Reply:         4 hours                            ║
║ Slowest Reply:         7 days                             ║
╚═══════════════════════════════════════════════════════════╝

Next Steps:
  • 8 positive responses → Schedule follow-up calls
  • 3 neutral responses → Send additional info
  • 1 negative response → Mark as not interested
```

---

## Implementation Plan

### Phase 1: Basic Reply Detection (4 hours)

1. Add Gmail API scope to OAuth2 setup
2. Implement reply search by subject line
3. Update Sheet with Response Received + Date
4. Test with sample sent emails

### Phase 2: Sentiment Analysis (4 hours)

1. Create Gemini sentiment prompt
2. Implement sentiment classification
3. Add sentiment column to Sheet
4. Test with various reply types (positive, negative, neutral)

### Phase 3: Analytics Dashboard (4 hours)

1. Calculate response metrics (rate, avg time, etc.)
2. Create CLI dashboard view
3. Add sentiment distribution chart (ASCII art)
4. Export analytics to CSV (optional)

---

## Testing Strategy

### Test Cases

**Test 1: Positive Reply**
- Send email to test account
- Reply with: "Yes, I'm interested! Let's schedule a call."
- Expected: Sentiment = POSITIVE, Response Received = TRUE

**Test 2: Negative Reply**
- Send email to test account
- Reply with: "Not interested, please remove me."
- Expected: Sentiment = NEGATIVE

**Test 3: Neutral Reply**
- Send email to test account
- Reply with: "Can you send me more information?"
- Expected: Sentiment = NEUTRAL

**Test 4: Out of Office**
- Send email to test account
- Reply with auto-responder: "I'm out of office until..."
- Expected: Sentiment = OUT_OF_OFFICE

**Test 5: No Reply**
- Send email, don't reply
- Expected: Response Received = FALSE (unchanged)

---

## Performance Considerations

### API Quotas

- Gmail API: 1 billion quota units per day (generous)
- Each search query: ~5 quota units
- 100 emails checked: ~500 quota units (well within limits)

### Rate Limiting

- Batch search queries (search for multiple subjects at once)
- Cache results (don't re-check already processed replies)
- Implement exponential backoff for rate limit errors

### Optimization

```python
# Instead of individual searches
for email in sent_emails:
    query = f"subject:'Re: {email.subject}'"
    search(query)  # Slow: N API calls

# Batch search with OR operator
subjects = [email.subject for email in sent_emails]
query = " OR ".join([f"subject:'Re: {s}'" for s in subjects])
search(query)  # Fast: 1 API call
```

---

## Error Handling

| Error | Cause | Handling |
|-------|-------|----------|
| `HttpError 401` | Gmail auth expired | Re-authenticate user |
| `HttpError 403` | Insufficient permissions | Request additional scopes |
| `HttpError 429` | Rate limit exceeded | Exponential backoff, retry |
| `ParseError` | Malformed email | Skip, log warning |
| Sentiment API fail | Gemini down | Mark as NEUTRAL (fallback) |

---

## Future Enhancements

- [ ] **Real-time tracking:** Webhook notifications when reply received
- [ ] **Advanced sentiment:** Emotion detection (excited, frustrated, confused)
- [ ] **Reply scoring:** Score reply quality (hot lead, warm lead, cold)
- [ ] **Auto-follow-up:** Trigger follow-up sequence on NEUTRAL replies
- [ ] **Unsubscribe detection:** Automatically mark as "Do Not Contact"
- [ ] **Reply templates:** Suggest AI-generated reply based on sentiment
- [ ] **Time-series chart:** Response rate over time (daily/weekly)
- [ ] **A/B test integration:** Compare response rates between email variants

---

## Dependencies

- **Depends on:** US-007 (Gmail SMTP Integration) - need sent email tracking
- **Depends on:** US-002 (Google Sheets Integration) - for updating status
- **Depends on:** US-005 (AI Email Generation) - for sentiment analysis model
- **Blocks:** US-011 (Campaign Analytics Dashboard) - provides metrics
- **Blocks:** US-015 (Automated Follow-up Sequences) - triggers follow-ups

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gmail API access revoked | High | Support custom SMTP + IMAP for tracking |
| False sentiment classification | Medium | Add manual sentiment override in Sheet |
| Reply not detected (threading issue) | Medium | Use multiple detection methods (Message-ID + subject) |
| Out of office replies counted as responses | Low | Detect OOO pattern, mark separately |
| High API cost (Gemini sentiment) | Medium | Cache sentiment results, batch processing |

---

## Success Metrics

- **Target response tracking accuracy:** >95%
- **Target sentiment classification accuracy:** >85%
- **Target API response time:** <2s per email
- **Target false positive rate (OOO as real reply):** <5%

---

## Definition of Done

- [ ] Gmail API integrated and authenticated
- [ ] Reply detection working (3 methods tested)
- [ ] Sentiment analysis implemented
- [ ] Google Sheet updated with reply data
- [ ] Analytics dashboard displays metrics
- [ ] Error handling covers edge cases
- [ ] Manual testing with 20+ test emails
- [ ] Documentation complete (docstrings, user guide)

---

**Created:** 2026-02-11
**Target Completion:** 2026-02-25
**Last Updated:** 2026-02-11
