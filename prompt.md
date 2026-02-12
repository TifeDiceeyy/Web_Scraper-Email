# WAT Framework Business Outreach Automation

## Overview

This system uses the **WAT Architecture** (Workflows, Agents, Tools):

- **Workflows** = Instructions (markdown SOPs in `workflows/`)
- **Agent** = Decision-maker (orchestrates tool execution)
- **Tools** = Execution layer (Python scripts that do the work)

## The Critical Decision Point

Your system has **ONE CRITICAL DECISION POINT** that determines the entire email strategy:

```
┌─────────────────────────────────────────┐
│  Ask: General Help OR Specific Focus?   │
│                                         │
│  1. GENERAL HELP                        │
│     → "Ask about problems, offer help"  │
│     → Discovery-focused emails          │
│     → Broader positioning               │
│                                         │
│  2. SPECIFIC AUTOMATION                 │
│     → Focus on one problem              │
│     → Narrower but clearer value prop   │
│     → Warmer leads                      │
└─────────────────────────────────────────┘
          ↓
         This decision changes EVERYTHING about email generation
```

This decision point is in `agent.py` → `ask_outreach_type()` and is saved to `campaign_config.json` for later use.

---

## Project Structure

```
business_outreach/
├── agent.py                      # Main agent (orchestrator)
│
├── workflows/                    # Your instructions (markdown)
│   ├── start_campaign.md
│   ├── manage_sheet.md
│   ├── generate_emails.md        ← CRITICAL (two paths based on decision)
│   ├── send_emails.md
│   └── track_responses.md
│
├── tools/                        # Execution layer (Python scripts)
│   ├── generate_general_email.py     ← Path A (general help)
│   ├── generate_specific_email.py    ← Path B (specific automation)
│   ├── scrape_website.py
│   ├── upload_to_sheets.py
│   ├── get_draft_businesses.py
│   ├── update_sheet_emails.py
│   ├── load_config.py
│   └── (other tools...)
│
├── .tmp/                         # Temporary files (regenerated)
│   ├── campaign_config.json      # Stores decision: outreach_type
│   └── website_data.json
│
├── requirements.txt
├── .env                          # API keys
└── .gitignore                    # Ignore .tmp, .env, credentials
```

---

## How It Works: The Flow

### 1. User Runs Agent
```bash
python agent.py
```

### 2. Start Campaign
Agent asks:
1. **Business type?** (Dentists, Restaurants, etc.)
2. **Outreach strategy?** ← **CRITICAL DECISION**
   - Option A: General Help
   - Option B: Specific Automation (then asks which one)
3. **How to get businesses?** (Maps/Manual/JSON)

### 3. Agent Saves Decision
```python
# agent.py saves to .tmp/campaign_config.json
config = {
    "business_type": "Dentists",
    "outreach_type": "general_help",  # OR "specific_automation"
    "automation_focus": ""             # Only if specific_automation
}
```

### 4. Businesses Added to Sheet
- Agent calls `tools/upload_to_sheets.py`
- All businesses set to Status = "Draft"
- Ready for email generation

### 5. Generate Emails
Agent reads `campaign_config.json`:
- If `outreach_type == "general_help"` → Use `tools/generate_general_email.py`
- If `outreach_type == "specific_automation"` → Use `tools/generate_specific_email.py`

Each tool calls Claude API with **different prompt**:

**Path A (General Help):**
```
Ask about problems, offer general help
No specific automation focus
Discovery-focused
```

**Path B (Specific Automation):**
```
Lead with specific benefit
Focus on ONE automation
Warm up the lead
```

### 6. User Reviews & Approves
- Go to Google Sheet
- Read Subject & Body columns
- Change Status from "Draft" to "Approved"

### 7. Send & Track
- Agent sends all "Approved" emails
- Monitors Gmail for replies
- Notifies via Telegram/Email
- Auto-updates sheet status

---

## Critical Files to Create

### 1. agent.py (Your Main Script)
Main entry point. Already created above. Key method: `ask_outreach_type()`

This method:
- Shows user two options
- Returns either `"general_help"` or `"specific_automation"`
- Agent uses this to determine which tool to call

### 2. workflows/generate_emails.md (Your Instructions)
Defines two paths:
- **Path A: General Help Email Generation**
- **Path B: Specific Automation Email Generation**

Each path has different Claude prompt, different benefits highlighted, different tone.

### 3. tools/generate_general_email.py
Claude prompt that generates discovery-focused emails:
- Asks about problems
- Offers general help
- No specific automation focus
- Opens door for discovery call

### 4. tools/generate_specific_email.py
Claude prompt that generates focused emails:
- Leads with specific benefit
- Focuses on ONE automation
- Warm leads
- More confident tone

### 5. .env (Your API Keys)
```
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_SPREADSHEET_ID=...
GOOGLE_CREDENTIALS_FILE=credentials.json
NOTIFICATION_METHOD=telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

---

## Quick Start (15 minutes)

### Step 1: Create Project
```bash
mkdir business_outreach && cd business_outreach
python3 -m venv venv
source venv/bin/activate
pip install anthropic google-auth-oauthlib google-api-python-client python-dotenv requests beautifulsoup4
```

### Step 2: Create .env
```
ANTHROPIC_API_KEY=your-key
GOOGLE_SPREADSHEET_ID=your-sheet-id
GOOGLE_CREDENTIALS_FILE=credentials.json
NOTIFICATION_METHOD=telegram
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_CHAT_ID=your-chat-id
```

### Step 3: Copy Files
From this guide:
- `agent.py` (main)
- `workflows/start_campaign.md`
- `workflows/generate_emails.md`
- `tools/` (all Python scripts)

### Step 4: Run
```bash
python agent.py
```

### Step 5: First Campaign
```
Select: 1 (Start new campaign)
Choose business type: 1 (Dentists)
Choose outreach: 1 (General Help)  ← CRITICAL DECISION
Choose source: 2 (Manual entry)
Add 3 dentists
Check Google Sheet (they appeared!)
```

### Step 6: Generate & Send
```
Select: 3 (Generate emails)
Agent reads campaign_config.json → sees "general_help"
Calls tools/generate_general_email.py for each
Updates Google Sheet with emails

Go to Google Sheet → Change Status to "Approved"

Select: 4 (Send approved emails)
Emails sent!

Select: 5 (Track responses)
Monitor for replies...
```

---

## The Decision Tree

```
START (agent.py)
  ↓
Ask: Business type?
  ↓
Ask: Outreach strategy?
  │
  ├─ Option 1: General Help
  │  └─ Save to campaign_config.json: outreach_type = "general_help"
  │  └─ Later: Use tools/generate_general_email.py
  │  └─ Email approach: Ask about problems
  │
  └─ Option 2: Specific Automation
     ├─ Ask: Which automation?
     └─ Save to campaign_config.json:
        outreach_type = "specific_automation"
        automation_focus = "Appointment Scheduling"
     └─ Later: Use tools/generate_specific_email.py
     └─ Email approach: Lead with benefit
```

---

## Why This Architecture Works

**Problem:** Different strategies need different prompts, different questions, different follow-ups

**Solution:** WAT separates concerns:
1. **Workflow** = Define what to do (start_campaign.md, generate_emails.md)
2. **Agent** = Make decisions (ask_outreach_type())
3. **Tools** = Execute (generate_general_email.py, generate_specific_email.py)

**Benefit:** You can change strategies without touching code. Just read the workflow, agent asks the questions, tools handle execution.

---

## Customization Examples

### Want to change general help email tone?
1. Edit `workflows/generate_emails.md` Path A section
2. Update Claude prompt in `tools/generate_general_email.py`
3. Test

### Want to add a new automation focus?
1. Edit `workflows/generate_emails.md` section on automation options
2. Add to agent.py → `ask_automation_focus()`
3. Claude will handle the specifics automatically

### Want different notification method?
1. Edit `.env`: `NOTIFICATION_METHOD=email` (instead of telegram)
2. Tool already handles both
3. Done

---

## Email Examples

### General Help Email (Path A)

**Input:**
- Business: "Smile Dental Care"
- Type: "Dentist"
- Location: "Downtown"

**Output:**
```
Subject: Quick question about how you stay organized

Body:
Hi Sarah,

I work with dental practices to streamline their operations with automation.

I'm curious - what's the biggest challenge your team faces day-to-day? 
Is it scheduling, client communication, admin work, or something else?

I've helped practices tackle everything from appointment management to 
follow-up automation, and I'd love to explore what might help Smile Dental most.

Would you have 15 minutes for a quick call?

Best,
[Your name]
```

**Why this approach:**
- Discovery-focused
- Opens door for conversation
- No hard sell
- Relevant to them (mentions their type)

---

### Specific Automation Email (Path B)

**Input:**
- Business: "Smile Dental Care"
- Type: "Dentist"
- Focus: "Appointment Scheduling"

**Output:**
```
Subject: Reduce no-shows at Smile Dental by 30%

Body:
Hi Sarah,

I work with dental practices like Smile Dental to automate appointment 
reminders via SMS/email. Most practices see a 30% drop in no-shows 
and save 4-6 hours per week.

Given your location and practice size, this could be a quick win for your team.

Would you be open to a 15-minute conversation about how this works?

Best,
[Your name]
```

**Why this approach:**
- Specific benefit (30% reduction)
- Focused value prop
- Warm lead (knows what you do)
- Confident tone

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: anthropic` | `pip install anthropic` |
| `ANTHROPIC_API_KEY not set` | Check `.env` file exists, key is there |
| `Google auth fails` | Make sure `credentials.json` exists in project folder |
| `Claude returns invalid JSON` | Tool has fallback cleanup code |
| `Email not generated` | Check internet, API credits at console.anthropic.com |

---

## Next Features (After MVP)

Once this works, you can add:

1. **A/B Testing**
   - Test general_help vs specific_automation
   - Track which gets better response rate

2. **Follow-up Sequences**
   - If no reply after 5 days, send follow-up
   - Different follow-up for each strategy

3. **Response Handling**
   - Auto-detect interest level
   - Suggest next steps

4. **Scaling**
   - Batch processing
   - Rate limiting for API calls
   - Better error recovery

---

## Key Takeaway

Your system's **super power** is the decision point:

```
User decides: General Help or Specific Automation?
         ↓
         Entire email strategy changes
         ↓
         Different Claude prompts
         ↓
         Different engagement approach
         ↓
         Different follow-up needed
```

This single decision cascades through the whole system. Everything else follows from it.

That's why it's baked into `campaign_config.json` and checked before every email generation.
