# Workflow: Manage Google Sheet

## Purpose
Open and manage the Google Sheet for reviewing/editing emails and changing business statuses.

## When to Use
- After generating emails (to review them)
- To manually approve emails (change Status from "Draft" to "Approved")
- To add notes or edit email content
- To check campaign progress

## Process

### Step 1: Locate Sheet
- Sheet ID is stored in `.env` file: `GOOGLE_SPREADSHEET_ID`
- Or read from campaign config: `.tmp/campaign_config.json`

### Step 2: Open Sheet
- Provide direct URL to user:
  ```
  https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
  ```

### Step 3: What User Can Do

**Review Emails:**
1. Look at "Generated Subject" and "Generated Body" columns
2. Check if emails are personalized correctly
3. Verify business names and contact info

**Edit Emails:**
1. Click on any cell to edit
2. Modify subject or body directly in the sheet
3. Changes are saved automatically

**Approve Emails:**
1. Find "Status" column
2. Change from "Draft" to "Approved" for emails you want to send
3. System will only send "Approved" emails

**Add Notes:**
1. Use "Your Notes" column for any comments
2. Track why certain businesses were skipped
3. Record conversation outcomes

### Step 4: Status Values

| Status | Meaning |
|--------|---------|
| **Draft** | Email generated, needs review |
| **Approved** | Ready to send |
| **Sent** | Email has been sent |
| **Replied** | Business responded |
| **Bounced** | Email bounced/invalid |
| **Auto-Reply** | Received auto-response |

### Step 5: Return to System
- After approving emails, run `/send-emails` to send them
- After businesses reply, run `/track-responses` to detect replies

## Important Notes

⚠️  **Do NOT:**
- Delete the header row
- Change column order
- Delete businesses (just mark as invalid status if needed)

✅  **Do:**
- Edit email content freely
- Add as many notes as you want
- Approve only emails you're confident about
- Use filters/sorting to manage large lists

## Tips

**Efficient Review:**
1. Filter by Status = "Draft" to see only new emails
2. Sort by Business Type to review similar businesses together
3. Use search (Ctrl+F) to find specific businesses

**Batch Operations:**
1. Select multiple cells in Status column
2. Type "Approved" and hit Ctrl+Enter to fill all at once
3. Save time on large campaigns

**Troubleshooting:**
- If sheet won't open: Check `.env` has correct `GOOGLE_SPREADSHEET_ID`
- If can't edit: Make sure you're logged into the Google account that created the sheet
- If columns are wrong: Re-run campaign setup to create fresh sheet

---

**Next Actions:**
- After reviewing → Run "Send Approved Emails"
- After sending → Run "Track Responses"
