# Workflow: Send Emails

## Purpose
Send all approved emails via Gmail and track sending status.

## Prerequisites
- Gmail credentials configured in `.env`
- Businesses have Status = "Approved"
- Generated Subject and Body exist

## Steps

### 1. Get Approved Businesses
Query Google Sheet for all rows where:
- Status = "Approved"
- Generated Subject is not empty
- Generated Body is not empty
- Email address is valid

### 2. Confirmation
Show user:
- Number of emails to send
- List of business names
- Ask for final confirmation

### 3. Send Each Email

For each approved business:

#### 3.1 Connect to Gmail
- Use Gmail API or SMTP
- Authenticate with credentials from `.env`

#### 3.2 Compose Email
- To: Business email
- From: Your Gmail address
- Subject: Generated Subject
- Body: Generated Body
- Format: HTML or plain text

#### 3.3 Send Email
Try to send, handle errors:
- Success: Continue
- Failure: Log error, continue to next

#### 3.4 Update Google Sheet
On success:
- Status = "Sent"
- Date Sent = Current timestamp
- Record in notes

On failure:
- Keep Status = "Approved"
- Add error to notes

#### 3.5 Rate Limiting
- Wait 5-10 seconds between sends
- Avoid Gmail rate limits
- Show progress to user

### 4. Summary Report
After all sends:
```
✅ Sent: 23 emails
❌ Failed: 2 emails
📊 Total: 25 emails

Failed businesses:
- Business Name 1 (invalid email)
- Business Name 2 (connection error)
```

### 5. Next Steps Prompt
Tell user:
- Emails sent successfully
- Monitor responses in next 24-48 hours
- Use "Track Responses" to automate monitoring

## Success Criteria
- All approved emails attempted
- Google Sheet updated with results
- User has summary report
- Failed sends are logged

## Error Handling

**Invalid Email**:
- Skip, mark in notes
- Continue to next

**Gmail Connection Error**:
- Retry once
- If fails again, abort and report

**Rate Limit Hit**:
- Pause for 60 seconds
- Resume sending

## Next Workflow
→ `track_responses.md` (automated monitoring)

## Gmail Setup Notes

### Using Gmail API (Recommended)
- More reliable
- Higher send limits
- Better error handling

### Using SMTP (Alternative)
- Easier setup
- Lower send limits (500/day)
- Requires "App Password"

### Send Limits
- Gmail: 500 emails/day (free), 2000/day (workspace)
- Recommended: Send in batches, not all at once
- Wait 10 seconds between emails
