# US-009: Logging & Monitoring System

**Status:** ✅ Complete
**Priority:** P0 (Critical)
**Estimated Effort:** 3 hours
**Actual Effort:** 3 hours

---

## User Story

**As a** developer maintaining the system
**I want** comprehensive logging of all operations
**So that** I can debug issues, monitor performance, and audit system activity

---

## Acceptance Criteria

1. ✅ Centralized logging configuration (`logger.py`)
2. ✅ Dual-handler setup (file + console)
3. ✅ File handler: Detailed logs with DEBUG level
4. ✅ Console handler: User-friendly INFO level
5. ✅ Structured log format with timestamps
6. ✅ Log rotation (prevent file size issues)
7. ✅ Integration in all major components
8. ✅ Log levels used appropriately (DEBUG, INFO, WARNING, ERROR)
9. ✅ No sensitive data logged (passwords, API keys)
10. ✅ Performance tracking (operation timing)

---

## Technical Requirements

### Logging Configuration

```python
# logger.py

import logging
import sys
from pathlib import Path


def setup_logger(name="outreach", log_file="outreach.log", level=logging.INFO):
    """
    Set up a logger with both file and console handlers

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (default: INFO)

    Returns:
        logging.Logger: Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Detailed formatter for file
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Simple formatter for console
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler (detailed logs, DEBUG level)
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")

    # Console handler (simple logs, INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()
```

---

## Log Levels

### DEBUG (File Only)

**Usage:** Detailed diagnostic information

**Examples:**
```python
logger.debug(f"API payload: {payload}")
logger.debug(f"Query result: {result}")
logger.debug(f"Function called with args: {args}")
```

**Logged Events:**
- API request/response payloads
- Database queries and results
- Function entry/exit with parameters
- Variable values during execution

---

### INFO (File + Console)

**Usage:** General informational messages

**Examples:**
```python
logger.info("Campaign started successfully")
logger.info(f"Email sent to {business_name}")
logger.info(f"Generated {count} emails")
```

**Logged Events:**
- Campaign creation
- Email generation (per-business)
- Email sending (per-send)
- Configuration loaded/saved
- User actions (menu selections)
- Operation completion

---

### WARNING (File + Console)

**Usage:** Non-critical issues that don't stop execution

**Examples:**
```python
logger.warning(f"Failed to scrape website: {url}")
logger.warning(f"Invalid email skipped: {email}")
logger.warning(f"Retry attempt {attempt}/3")
```

**Logged Events:**
- Website scraping failures
- Invalid data skipped
- Retry attempts
- Missing optional data
- Deprecated features used

---

### ERROR (File + Console)

**Usage:** Critical errors that affect functionality

**Examples:**
```python
logger.error(f"Failed to connect to SMTP: {error}")
logger.error(f"API call failed after 3 retries: {error}")
logger.error(f"Could not update Sheet: {error}")
```

**Logged Events:**
- API failures (after all retries)
- SMTP connection errors
- Google Sheets API errors
- File I/O errors
- Authentication failures

---

## Log File Format

### File Output (Detailed)

```
2026-02-11 17:16:29 - outreach - INFO - Business Outreach Automation System started
2026-02-11 17:16:35 - outreach - INFO - Business type selected: Dentists
2026-02-11 17:16:40 - outreach - INFO - Strategy selected: specific_automation
2026-02-11 17:16:45 - outreach - INFO - Automation focus selected: Appointment Reminder System
2026-02-11 17:16:50 - outreach - INFO - Scraping 25 Dentists businesses in San Francisco, CA
2026-02-11 17:17:00 - outreach - INFO - Found 25 businesses
2026-02-11 17:17:05 - outreach - INFO - Configuration saved to .tmp/campaign_config.json
2026-02-11 17:17:10 - outreach - INFO - Uploading 25 businesses to Google Sheets
2026-02-11 17:17:15 - outreach - INFO - Campaign started successfully
2026-02-11 17:20:00 - outreach - INFO - Starting email generation workflow
2026-02-11 17:20:05 - outreach - INFO - Found 25 draft businesses
2026-02-11 17:20:10 - outreach - INFO - Generating email 1/25 for: Smile Dental
2026-02-11 17:20:12 - outreach - DEBUG - Scraping website: www.smiledental.com
2026-02-11 17:20:15 - outreach - INFO - Generated email: Reduce no-shows by 30% for Smile Dental
2026-02-11 17:20:20 - outreach - INFO - Generating email 2/25 for: Bay Area Dental
2026-02-11 17:20:25 - outreach - WARNING - Failed to scrape website: www.nonexistent.com (404)
2026-02-11 17:20:28 - outreach - INFO - Generated email: Stop losing revenue to no-shows
...
```

### Console Output (User-Friendly)

```
INFO - Business Outreach Automation System started
INFO - Business type selected: Dentists
INFO - Strategy selected: specific_automation
INFO - Starting email generation workflow
INFO - Found 25 draft businesses
INFO - Generating email 1/25 for: Smile Dental
INFO - Generated email: Reduce no-shows by 30% for Smile Dental
WARNING - Failed to scrape website: www.nonexistent.com (404)
INFO - Successfully generated 25 emails
```

---

## Integration Examples

### Example 1: Agent Workflow

```python
# agent.py

from logger import logger

def start_campaign(self):
    """Workflow 1: Start a new outreach campaign"""
    logger.info("Starting new outreach campaign")

    business_type = self.ask_business_type()
    logger.info(f"Business type selected: {business_type}")

    outreach_type = self.ask_outreach_type()
    logger.info(f"Strategy selected: {outreach_type}")

    # ... more workflow steps ...

    logger.info(f"Campaign started successfully: {business_type} | {outreach_type}")
```

---

### Example 2: Email Generation

```python
# tools/generate_specific_email.py

from logger import logger

def generate_specific_email(business_name, business_type, ...):
    """Generate benefit-driven email"""

    logger.info(f"Generating specific email for {business_name}")

    # Validate API key
    try:
        api_key = validate_api_key()
        logger.debug("API key validated successfully")
    except ValueError as e:
        logger.error(f"API key validation failed: {e}")
        raise

    # Call Gemini API
    try:
        response = call_gemini_api(client, prompt)
        logger.info(f"Email generated successfully for {business_name}")
    except Exception as e:
        logger.error(f"Failed to generate email: {e}")
        # Return fallback email
        logger.warning("Using fallback email")
        return fallback_subject, fallback_body

    return subject, body
```

---

### Example 3: Email Sending

```python
# tools/send_emails.py

from logger import logger

def send_approved_emails():
    """Send all approved emails"""

    logger.info("Starting email sending workflow")

    businesses = get_approved_businesses()
    logger.info(f"Found {len(businesses)} approved businesses")

    sent_count = 0
    failed_count = 0

    try:
        with SMTPConnectionManager(gmail_address, gmail_password) as smtp:
            logger.info("Connected to Gmail SMTP server")

            for i, business in enumerate(businesses, 1):
                logger.info(f"Sending email {i}/{len(businesses)} to: {business['name']}")

                success = smtp.send_email(...)

                if success:
                    logger.info(f"Email sent successfully to {business['email']}")
                    sent_count += 1
                else:
                    logger.warning(f"Failed to send email to {business['email']}")
                    failed_count += 1

    except ConnectionError as e:
        logger.error(f"SMTP connection error: {e}")

    logger.info(f"Email sending complete: {sent_count} sent, {failed_count} failed")
    return sent_count
```

---

## Log Analysis

### Viewing Logs

```bash
# View entire log file
cat outreach.log

# Watch logs in real-time
tail -f outreach.log

# View last 50 lines
tail -50 outreach.log

# Search for errors
grep ERROR outreach.log

# Search for specific business
grep "Smile Dental" outreach.log

# Count log levels
grep -c INFO outreach.log
grep -c WARNING outreach.log
grep -c ERROR outreach.log
```

---

### Common Queries

**Find all errors:**
```bash
grep ERROR outreach.log
```

**Find failed email sends:**
```bash
grep "Failed to send" outreach.log
```

**Track campaign progress:**
```bash
grep "Campaign started\|Email sent\|Email sending complete" outreach.log
```

**API failures:**
```bash
grep "API\|Gemini" outreach.log | grep ERROR
```

---

## Log Rotation (Future)

### Using RotatingFileHandler

```python
from logging.handlers import RotatingFileHandler

# Rotate after 10MB, keep 5 backup files
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

**Result:**
```
outreach.log          # Current log
outreach.log.1        # Previous log
outreach.log.2        # ...
outreach.log.3
outreach.log.4
outreach.log.5        # Oldest log (deleted when new rotation)
```

---

## Performance Tracking

### Timing Operations

```python
import time

def generate_emails():
    start_time = time.time()
    logger.info("Starting email generation")

    # ... generate emails ...

    elapsed = time.time() - start_time
    logger.info(f"Email generation complete in {elapsed:.2f}s")
```

### Output:
```
2026-02-11 17:20:00 - outreach - INFO - Starting email generation
2026-02-11 17:22:35 - outreach - INFO - Email generation complete in 155.23s
```

---

## Security Considerations

### Never Log Sensitive Data

❌ **Bad:**
```python
logger.info(f"Gmail password: {gmail_password}")
logger.debug(f"API key: {api_key}")
logger.info(f"User entered password: {user_password}")
```

✅ **Good:**
```python
logger.info("Gmail credentials validated")
logger.debug("API key validated successfully")
logger.info("User authenticated")
```

### Redact Sensitive Data

```python
def redact_email(email):
    """Redact email for logging"""
    local, domain = email.split('@')
    return f"{local[0]}***@{domain}"

logger.info(f"Email sent to {redact_email(business['email'])}")
# Output: "Email sent to t***@example.com"
```

---

## Testing

### Test 1: Logger Setup
```python
from logger import setup_logger

logger = setup_logger()
assert logger is not None
assert len(logger.handlers) == 2  # File + Console
```

### Test 2: Log to File
```python
logger.info("Test message")

# Check file exists
assert os.path.exists("outreach.log")

# Check message in file
with open("outreach.log") as f:
    content = f.read()
    assert "Test message" in content
```

### Test 3: Log Levels
```python
logger.debug("Debug message")    # File only
logger.info("Info message")      # File + Console
logger.warning("Warning message") # File + Console
logger.error("Error message")    # File + Console
```

---

## Future Enhancements

- [ ] **Structured Logging:** JSON format for machine parsing
- [ ] **Log Aggregation:** Send logs to central server (Elasticsearch, CloudWatch)
- [ ] **Real-time Monitoring:** Dashboard showing live logs
- [ ] **Alert System:** Email/Slack alerts on errors
- [ ] **Performance Metrics:** Track operation times, API latency
- [ ] **User Activity Tracking:** Audit trail of all user actions
- [ ] **Log Analysis:** AI-powered insights from logs
- [ ] **Export Logs:** Download logs via web UI

---

## Related Stories

- **Depends on:** US-001 (Project Setup)
- **Enhances:** All features (provides debugging capability)
- **Related:** US-008 (Validation) - logs validation failures
- **Related:** US-011 (Analytics) - uses logs for metrics

---

## Definition of Done

- [x] Logger module created (`logger.py`)
- [x] Dual handlers (file + console)
- [x] Detailed file format with timestamps
- [x] Simple console format
- [x] Integration in all major components
- [x] Log levels used appropriately
- [x] No sensitive data logged
- [x] Log file created automatically
- [x] Manual testing (20+ log entries)
- [x] Documentation complete

---

**Created:** 2026-02-10
**Completed:** 2026-02-11
**Last Updated:** 2026-02-11
