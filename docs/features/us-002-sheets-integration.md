# US-002: Google Sheets Integration

**Status:** ✅ Complete
**Priority:** P0 (Critical)
**Estimated Effort:** 6 hours
**Actual Effort:** 6 hours

---

## User Story

**As a** user managing outreach campaigns
**I want** to store and manage all business data in Google Sheets
**So that** I can easily review, edit, and track campaign progress in a familiar spreadsheet interface

---

## Acceptance Criteria

1. ✅ OAuth2 authentication with Google Sheets API
2. ✅ Automatic sheet creation if doesn't exist
3. ✅ Structured columns with proper headers
4. ✅ Batch upload of businesses (upload_to_sheets)
5. ✅ Read businesses with status filtering (get_draft_businesses)
6. ✅ Update individual cells (update_sheet_emails)
7. ✅ Status-based filtering (Draft, Approved, Sent, Replied)
8. ✅ Handles missing columns gracefully
9. ✅ Connection reuse for multiple operations
10. ✅ Error handling for API failures

---

## Technical Requirements

### OAuth2 Setup

**Required Scopes:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]
```

**Authentication Flow:**
1. User runs app first time
2. Browser opens for Google account selection
3. User grants permissions
4. Token saved to `token.json` (auto-refresh)
5. Subsequent runs use saved token

### Sheet Structure

| Column | Header | Type | Description |
|--------|--------|------|-------------|
| A | Business Name | Text | Name of business |
| B | Website | URL | Business website |
| C | Email | Email | Contact email |
| D | Phone | Phone | Contact phone |
| E | Location | Text | Business location |
| F | Category | Text | Business type |
| G | Generated Subject | Text | AI-generated subject |
| H | Generated Body | Text | AI-generated body |
| I | Notes | Text | User notes |
| J | Status | Enum | Draft/Approved/Sent/Replied |
| K | Date Approved | Date | Approval timestamp |
| L | Date Sent | Date | Send timestamp |
| M | Response Received | Boolean | Reply detected |
| N | Response Date | Date | Reply timestamp |

### Constants Mapping

```python
# Column Indices (0-indexed)
COL_NAME = 0
COL_WEBSITE = 1
COL_EMAIL = 2
COL_PHONE = 3
COL_LOCATION = 4
COL_CATEGORY = 5
COL_GENERATED_SUBJECT = 6
COL_GENERATED_BODY = 7
COL_NOTES = 8
COL_STATUS = 9
COL_DATE_APPROVED = 10
COL_DATE_SENT = 11
COL_RESPONSE_RECEIVED = 12
COL_RESPONSE_DATE = 13

# Status Values
STATUS_DRAFT = "Draft"
STATUS_APPROVED = "Approved"
STATUS_SENT = "Sent"
STATUS_REPLIED = "Replied"
```

---

## Key Functions

### 1. `get_sheets_service()`

**Purpose:** Create authenticated Google Sheets service

**Returns:** `googleapiclient.discovery.Resource`

**Error Handling:**
- `FileNotFoundError`: credentials.json missing
- `RefreshError`: Token expired, re-authenticate
- `HttpError`: API access issues

**Implementation:**
```python
def get_sheets_service():
    """Get authenticated Google Sheets service"""
    creds = None

    # Load existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Refresh or authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)
```

---

### 2. `upload_businesses(businesses)`

**Purpose:** Bulk upload businesses to Sheet

**Parameters:**
- `businesses`: List of dicts with keys: name, website, email, phone, location

**Logic:**
1. Get sheets service
2. Prepare header row if sheet is empty
3. Convert business dicts to row arrays
4. Set initial status to "Draft"
5. Batch append to Sheet
6. Return count uploaded

**Performance:**
- Batch operation (single API call)
- Handles up to 100 businesses efficiently
- Rate limit: Respects Google API quotas

**Error Handling:**
- Empty businesses list: Log warning, return 0
- API failure: Retry once, then fail gracefully
- Invalid spreadsheet ID: Clear error message

---

### 3. `get_draft_businesses()`

**Purpose:** Fetch all businesses with Status = "Draft"

**Returns:** List of dicts with keys: row_number, name, email, website, status

**Logic:**
1. Read entire Sheet (range: A2:N)
2. Filter rows where column J = "Draft"
3. Build dict for each matching row
4. Include row_number for later updates
5. Return list

**Performance:**
- Single API call reads all data
- Client-side filtering (no query overhead)
- Typical time: <2s for 1000 rows

---

### 4. `update_email(row_number, subject, body)`

**Purpose:** Write AI-generated email to specific row

**Parameters:**
- `row_number`: Row index (1-indexed)
- `subject`: Email subject line
- `body`: Email body text

**Logic:**
1. Build range: `G{row_number}:H{row_number}`
2. Create values array: `[[subject, body]]`
3. Update Sheet with valueInputOption='RAW'
4. Return success boolean

**API Call:**
```python
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f'G{row_number}:H{row_number}',
    valueInputOption='RAW',
    body={'values': [[subject, body]]}
).execute()
```

---

### 5. `update_status(row_number, status, timestamp=None)`

**Purpose:** Update status and optional timestamp

**Parameters:**
- `row_number`: Row index
- `status`: New status value
- `timestamp`: Optional datetime string

**Logic:**
- Status only: Update column J
- Status + timestamp: Update columns J + K/L based on status
- "Sent" status: Update Date Sent (column L)
- "Approved" status: Update Date Approved (column K)

**Example:**
```python
# Mark as sent
update_status(5, "Sent", "2026-02-11 15:30:00")
# Updates J5="Sent", L5="2026-02-11 15:30:00"
```

---

## Error Handling

### API Errors

| Error Code | Description | Handling |
|------------|-------------|----------|
| 401 | Unauthorized | Re-authenticate user |
| 403 | Permission denied | Check Sheet sharing settings |
| 404 | Spreadsheet not found | Verify SPREADSHEET_ID in .env |
| 429 | Rate limit exceeded | Exponential backoff retry |
| 500 | Server error | Retry 3 times with delay |

### Data Validation Errors

| Error | Cause | Handling |
|-------|-------|----------|
| Missing columns | Sheet structure changed | Auto-add missing columns |
| Invalid row index | Row deleted manually | Skip, log warning |
| Empty spreadsheet | Fresh sheet | Initialize with headers |

---

## Testing

### Test 1: Initial Setup
```python
# First run - should trigger OAuth flow
service = get_sheets_service()
assert service is not None
assert os.path.exists('token.json')
```

### Test 2: Upload Businesses
```python
businesses = [
    {
        'name': 'Test Business 1',
        'email': 'test1@example.com',
        'website': 'https://test1.com',
        'phone': '555-1234',
        'location': 'San Francisco, CA'
    },
    # ... more businesses
]

count = upload_businesses(businesses)
assert count == len(businesses)
```

### Test 3: Get Draft Businesses
```python
drafts = get_draft_businesses()
assert len(drafts) > 0
assert all(b['status'] == 'Draft' for b in drafts)
```

### Test 4: Update Email
```python
success = update_email(2, "Test Subject", "Test Body")
assert success == True

# Verify in Sheet
drafts = get_draft_businesses()
business = next(b for b in drafts if b['row_number'] == 2)
assert business['subject'] == "Test Subject"
```

---

## Performance Metrics

| Operation | API Calls | Time | Notes |
|-----------|-----------|------|-------|
| Upload 50 businesses | 1 | ~1s | Batch append |
| Get draft businesses | 1 | ~1s | Single read |
| Update 1 email | 1 | ~0.5s | Single write |
| Update 50 emails | 50 | ~25s | Sequential writes |

**Optimization Opportunities:**
- Batch email updates (reduce to 1 API call)
- Cache Sheet data locally (reduce reads)
- Use Sheet formulas for timestamps (no API call needed)

---

## Security Considerations

### Credentials Storage

- ✅ `credentials.json` in `.gitignore`
- ✅ `token.json` in `.gitignore`
- ✅ Tokens auto-refresh (no manual intervention)
- ✅ OAuth2 (no password storage)

### Sheet Access

- ✅ User controls sharing (private by default)
- ✅ Read/write access only to authorized spreadsheet
- ✅ No access to other user files

---

## Future Enhancements

- [ ] **Multiple Sheets Support:** Separate sheet per campaign
- [ ] **Sheet Templates:** Pre-configured sheet structure
- [ ] **Conditional Formatting:** Auto-highlight statuses (red=failed, green=sent)
- [ ] **Data Validation:** Dropdown menus for status column
- [ ] **Protected Ranges:** Lock generated email columns
- [ ] **Audit Log Sheet:** Track all changes (who, when, what)
- [ ] **Batch Operations:** Update multiple rows in single API call
- [ ] **Sheet Export:** Export to CSV/Excel for backup

---

## Related Stories

- **Depends on:** US-001 (Project Setup)
- **Blocks:** US-003 (Business Data Collection) - requires Sheet for upload
- **Blocks:** US-005 (AI Email Generation) - requires Sheet for reading/writing
- **Blocks:** US-007 (Gmail Integration) - requires Sheet for business list

---

## Definition of Done

- [x] OAuth2 authentication working
- [x] Batch upload implemented and tested
- [x] Status filtering working (get Draft/Approved/Sent)
- [x] Email update function working
- [x] Status update function working
- [x] Error handling for all API failures
- [x] Constants defined in constants.py
- [x] Documentation complete (docstrings)
- [x] Manual testing with real Sheet (20+ businesses)

---

**Created:** 2026-02-02
**Completed:** 2026-02-05
**Last Updated:** 2026-02-11
