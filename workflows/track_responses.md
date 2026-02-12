# Workflow: Track Responses

## Purpose
Monitor Gmail for replies and automatically update Google Sheet + notify user.

## How It Works
This can run as:
1. **One-time check**: Check now and report
2. **Continuous monitoring**: Run in background, check every 30 minutes
3. **Scheduled**: Run via cron job

## Steps

### 1. Connect to Gmail
- Authenticate with Gmail API
- Access inbox with read permissions

### 2. Search for Replies
Query emails where:
- In inbox (not spam)
- From: Any business email address in sheet
- Received after: Date we sent our email
- Not already processed

### 3. For Each Reply Found

#### 3.1 Extract Reply Info
- From email address
- Subject line
- Body content
- Timestamp received

#### 3.2 Match to Business
- Look up email address in Google Sheet
- Find matching row

#### 3.3 Update Google Sheet
Update row:
- Status = "Replied"
- Last Response = Timestamp
- Response Details = Email body (first 500 chars)

#### 3.4 Notify User
Send notification via chosen method:

**Telegram**:
```
🎉 NEW REPLY RECEIVED

Business: [Name]
Response: [First 100 chars...]
Full details in Google Sheet
```

**Email**:
```
Subject: New Reply from [Business Name]

You received a reply from [Business Name]!

Response preview:
[First 200 chars...]

View full details:
[Link to Google Sheet]
```

### 4. Summary Report
After checking all:
```
📊 Response Check Complete

New Replies: 3
Total Replied: 8 / 25 (32%)

Businesses that replied:
1. Business Name A
2. Business Name B
3. Business Name C
```

### 5. Continuous Mode (Optional)
If running continuously:
```python
while True:
    check_for_replies()
    update_sheet()
    notify_user()
    wait(30 minutes)
```

## Success Criteria
- All new replies detected
- Google Sheet updated correctly
- User notified of new responses
- No false positives (spam filtered)

## Edge Cases

### Out-of-Office Replies
- Detect auto-reply patterns
- Mark as "Auto-Reply" not "Replied"
- Don't notify user

### Bounce Backs
- Detect delivery failure
- Update Status to "Bounced"
- Remove from active list

### Multiple Replies
- Update "Last Response" to most recent
- Keep count of total replies
- Show all in Response Details

### Spam Folder Replies
- Also check spam folder
- Mark differently in notes
- Still notify user

## Notification Setup

### Telegram Bot
1. Create bot via @BotFather
2. Get bot token
3. Get chat ID
4. Set in `.env`:
```
NOTIFICATION_METHOD=telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### Email Notifications
Set in `.env`:
```
NOTIFICATION_METHOD=email
NOTIFICATION_EMAIL=your@email.com
```

## Advanced Features

### Sentiment Analysis
- Run reply through Claude API
- Classify: Positive / Neutral / Negative
- Add to Google Sheet column

### Auto-Response Suggestions
- Use Claude to suggest reply
- Store in sheet for user review
- User can approve and send

### Lead Scoring
- Score reply quality (1-10)
- Flag hot leads
- Prioritize follow-up

## Running Modes

### Command Line
```bash
python agent.py
# Choose option 5: Track Responses
```

### Background Service
```bash
python tools/track_responses.py --continuous
```

### Cron Job (Linux/Mac)
```bash
# Check every 30 minutes
*/30 * * * * cd /path/to/project && python tools/track_responses.py
```

## Next Workflow
→ Manual follow-up based on responses
→ Or set up auto-reply system (future enhancement)
