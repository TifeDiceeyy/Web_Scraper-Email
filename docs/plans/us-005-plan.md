# US-005 Implementation Plan: AI Email Generation Engine

**User Story:** [US-005 - AI Email Generation](../features/us-005-ai-email-generation.md)
**Status:** ✅ Complete
**Planned Effort:** 8 hours
**Actual Effort:** 10 hours

---

## Implementation Strategy

### Phase 1: Gemini Integration (3 hours)

**Goal:** Set up basic Gemini API integration with error handling

**Tasks:**

1. **Install Dependencies**
   - Add `google-genai>=1.0.0` to requirements.txt
   - Add `tenacity==9.1.4` for retry logic
   - Update virtual environment

2. **Create API Client Wrapper**
   - File: `tools/generate_general_email.py`
   - Function: `validate_api_key()` - check .env for GEMINI_API_KEY
   - Function: `call_gemini_api()` - wrapped with @retry decorator
   - Error handling: ClientError, ServerError, generic Exception

3. **Test API Connection**
   - Simple test: Generate "Hello world" response
   - Verify retry logic: Simulate failure, count attempts
   - Verify error messages are clear

**Acceptance:**
- ✅ Gemini client initializes without errors
- ✅ API calls succeed with valid key
- ✅ Retry logic triggers on transient failures
- ✅ Clear error message if API key missing

---

### Phase 2: General Help Strategy (2 hours)

**Goal:** Implement discovery-focused email generation

**Tasks:**

1. **Create System Prompt**
   ```python
   prompt = f"""You are writing a cold outreach email to a {business_type} business called "{business_name}".

   STRATEGY: General Help (Discovery Approach)
   - Your goal is to START A CONVERSATION, not sell anything
   - Ask about their current challenges or pain points
   - Offer general help with business automation
   - Keep it short and non-pushy

   TONE: Friendly and conversational, curious

   EMAIL STRUCTURE:
   1. Brief intro (who you are)
   2. Why you're reaching out (interested in helping {business_type}s)
   3. Ask 1-2 open-ended questions about their challenges
   4. Offer to chat if they're interested
   5. Easy out (no pressure)

   {website_context}

   Generate the email in this EXACT format:

   SUBJECT: [your subject line]

   BODY:
   [your email body]
   """
   ```

2. **Implement Response Parsing**
   - Function: `parse_email_response(response_text)`
   - Extract SUBJECT: line
   - Extract BODY: content (everything after BODY:)
   - Fallback parsing if format not followed
   - Validation: Ensure both subject and body exist

3. **Create Main Function**
   - Function: `generate_general_email(business_name, business_type, website_content="")`
   - Call validate_api_key()
   - Build prompt with context
   - Call Gemini API with retry
   - Parse response
   - Return (subject, body)

4. **Add Test Function**
   - `test_generate_general_email()`
   - Test with sample business (Smile Dental)
   - Print formatted output
   - Manual verification of tone and content

**Acceptance:**
- ✅ General Help emails generated successfully
- ✅ Tone is friendly and non-pushy
- ✅ Emails ask questions (not just sell)
- ✅ Subject lines are casual (50 chars max)
- ✅ Body length 100-150 words

---

### Phase 3: Specific Automation Strategy (3 hours)

**Goal:** Implement benefit-driven email generation with automation focus

**Tasks:**

1. **Define Automation Details**
   - Function: `get_automation_details(automation_focus, business_type)`
   - Dictionary mapping automation types to details:
     - Pain point
     - Benefit (with stat)
     - Industry stats
     - Proof/case study
   - 5 automation types:
     - Appointment Reminder System
     - Review Request Automation
     - Lead Follow-up System
     - Customer Feedback Collection
     - Inventory Alerts

2. **Create System Prompt**
   ```python
   prompt = f"""You are writing a warm outreach email to a {business_type} business called "{business_name}".

   STRATEGY: Specific Automation (Focused Approach)
   - Lead with a SPECIFIC, CONCRETE BENEFIT
   - Focus on ONE automation: {automation_focus}
   - Show you understand their pain point
   - Include relevant stats or results

   AUTOMATION FOCUS: {automation_focus}
   {automation_details}

   TONE: Confident but not pushy, benefit-driven

   EMAIL STRUCTURE:
   1. Hook: Lead with specific benefit/stat
   2. Pain point: Show you understand their challenge
   3. Solution: Brief mention of the automation
   4. Proof: Quick case study or testimonial
   5. CTA: Low-pressure invitation to chat

   {website_context}

   IMPORTANT:
   - Subject line: Lead with the benefit (max 60 chars)
   - Email body: 120-180 words max
   - Use specific numbers/percentages if possible
   - Don't be vague - be concrete about the automation

   Generate the email in this EXACT format:

   SUBJECT: [your subject line]

   BODY:
   [your email body]
   """
   ```

3. **Implement Specific Email Generator**
   - File: `tools/generate_specific_email.py`
   - Function: `generate_specific_email(business_name, business_type, website_content="", automation_focus=None)`
   - Default automation: Appointment Reminders if not specified
   - Same API wrapper and retry logic as general
   - Same parsing logic

4. **Add Test Function**
   - Test with each automation type
   - Verify benefit-driven tone
   - Check stats/numbers included
   - Verify length (120-180 words)

**Acceptance:**
- ✅ Specific emails generated for all automation types
- ✅ Emails lead with specific benefit/stat
- ✅ Tone is confident and expert-like
- ✅ Subject lines mention benefit (60 chars max)
- ✅ Body includes case study/proof

---

### Phase 4: Integration with Agent (1 hour)

**Goal:** Wire up email generation to main agent workflow

**Tasks:**

1. **Update agent.py**
   - Import both email generators
   - In `generate_emails()` method:
     - Load campaign config
     - Get strategy (general_help or specific_automation)
     - For each draft business:
       - Scrape website if available
       - Call appropriate generator
       - Update Sheet with subject + body

2. **Add Progress Indicators**
   - Print: `[1/20] Generating email for: Business Name`
   - Print: `✅ Generated: [Subject Line]`
   - Show errors inline but continue to next business

3. **Error Handling in Workflow**
   - If generation fails for one business:
     - Log error with business name
     - Use fallback email
     - Continue to next business (don't crash)
   - At end, show summary:
     - X emails generated successfully
     - Y emails used fallback
     - Z total businesses processed

**Acceptance:**
- ✅ Email generation triggered from agent menu
- ✅ Progress displayed during generation
- ✅ Errors logged but don't stop workflow
- ✅ Generated emails written to Sheet

---

### Phase 5: Constants & Configuration (1 hour)

**Goal:** Move hardcoded values to constants.py

**Tasks:**

1. **Add to constants.py**
   ```python
   # Gemini Configuration
   GEMINI_MODEL = "gemini-2.5-flash"
   MAX_WEBSITE_CONTEXT_LENGTH = 500
   EMAIL_RETRY_ATTEMPTS = 3

   # Automation Types
   AUTOMATION_APPOINTMENT_REMINDERS = "Appointment Reminder System"
   AUTOMATION_REVIEW_REQUESTS = "Review Request Automation"
   AUTOMATION_LEAD_FOLLOWUP = "Lead Follow-up System"
   AUTOMATION_FEEDBACK_COLLECTION = "Customer Feedback Collection"
   AUTOMATION_INVENTORY_ALERTS = "Inventory Alerts"

   # Email Strategies
   STRATEGY_GENERAL = "general_help"
   STRATEGY_SPECIFIC = "specific_automation"
   ```

2. **Update Email Generators**
   - Import constants
   - Replace hardcoded strings with constants
   - Use GEMINI_MODEL constant in API calls

**Acceptance:**
- ✅ All magic strings moved to constants
- ✅ Email generators use constants
- ✅ Easy to change model or config values

---

## Testing Checklist

### Unit Tests

- [x] `validate_api_key()` - returns True with valid key
- [x] `validate_api_key()` - raises ValueError without key
- [x] `call_gemini_api()` - succeeds on first attempt
- [x] `call_gemini_api()` - retries on ServerError
- [x] `call_gemini_api()` - fails after 3 attempts
- [x] `parse_email_response()` - extracts subject and body correctly
- [x] `parse_email_response()` - handles missing SUBJECT:
- [x] `parse_email_response()` - handles missing BODY:
- [x] `get_automation_details()` - returns correct details for each type

### Integration Tests

- [x] Generate General Help email - verify tone
- [x] Generate Specific email - verify benefit-driven
- [x] Generate with website context - verify personalization
- [x] Generate without website context - still works
- [x] Generate 5 emails in sequence - all succeed
- [x] Generate with invalid API key - clear error message
- [x] Generate with network failure - retry logic works
- [x] Write to Sheet - emails appear in columns G, H

### End-to-End Tests

- [x] Full workflow: Start campaign → Generate emails → Check Sheet
- [x] Strategy selection: General vs Specific changes email tone
- [x] Automation focus: Different automations produce different emails
- [x] Error recovery: One failure doesn't stop batch

---

## Code Quality Checklist

- [x] **Docstrings:** All functions documented
- [x] **Type hints:** Function parameters and returns typed
- [x] **Error messages:** Clear, actionable error messages
- [x] **Logging:** Key events logged (API calls, errors)
- [x] **Constants:** No magic strings or numbers
- [x] **DRY:** No code duplication between generators
- [x] **Validation:** Input validation on all public functions
- [x] **Fallback:** Graceful degradation if AI fails

---

## Performance Metrics

| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| API call time | <5s | 3-5s | Acceptable |
| Retry overhead | <10s | 2-10s | Exponential backoff |
| Parse success rate | 100% | 98% | Fallback parsing covers edge cases |
| Fallback usage | <5% | <2% | Very rare |
| Token usage | <1000/email | 800-1000 | Within budget |

---

## Lessons Learned

### What Went Well ✅

1. **Gemini Flash is fast:** 3-5 second response times excellent for user experience
2. **Retry logic crucial:** Handled transient failures automatically
3. **Structured output works:** SUBJECT:/BODY: format parsed reliably
4. **Fallback strategy:** Users never blocked by AI failures
5. **Two strategies valuable:** General vs Specific gives users flexibility

### Challenges 🔧

1. **Prompt engineering:** Required 3-4 iterations to get right tone
2. **Response parsing:** Gemini sometimes doesn't follow format exactly (solved with fallback parsing)
3. **Token costs:** Higher than expected (solved by truncating website context)
4. **Rate limiting:** Hit Gemini rate limits during testing (solved with exponential backoff)

### What We'd Do Differently 🔄

1. **Add prompt library:** Pre-built prompts for different industries
2. **Caching:** Cache emails for similar businesses (reduce API calls)
3. **Batch generation:** Generate multiple emails in parallel (faster)
4. **Prompt versioning:** Track prompt changes and A/B test
5. **Token tracking:** Log token usage per email for cost monitoring

---

## Next Steps

1. ✅ **US-006:** Email Strategy System (save strategy to campaign config)
2. ✅ **US-007:** Gmail SMTP Integration (send generated emails)
3. 📝 **US-010:** Response Tracking (use AI for sentiment analysis)
4. 📝 **US-014:** A/B Testing (test different email variants)
5. 📝 **US-020:** Advanced AI Features (reply suggestions, deliverability analysis)

---

## Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **Tenacity Docs:** https://tenacity.readthedocs.io/
- **Prompt Engineering Guide:** https://www.promptingguide.ai/

---

**Plan Created:** 2026-02-06
**Implementation Started:** 2026-02-06
**Implementation Completed:** 2026-02-09
**Last Updated:** 2026-02-11
