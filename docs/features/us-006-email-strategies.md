# US-006: Email Strategy System

**Status:** ✅ Complete
**Priority:** P0 (Critical)
**Estimated Effort:** 3 hours
**Actual Effort:** 3 hours

---

## User Story

**As a** user starting an outreach campaign
**I want** to choose between different email strategies
**So that** I can match my approach to my target audience and campaign goals

---

## Acceptance Criteria

1. ✅ Two distinct strategies implemented:
   - General Help (Discovery approach)
   - Specific Automation (Benefit-driven approach)
2. ✅ Interactive strategy selection during campaign setup
3. ✅ Clear descriptions of each strategy
4. ✅ Strategy saved to campaign configuration
5. ✅ Strategy determines which email generator is used
6. ✅ Strategy persists across sessions
7. ✅ Visual indicators in CLI (emojis, formatting)
8. ✅ Cannot proceed without selecting strategy

---

## The Two Strategies

### Strategy 1: General Help (Discovery)

**Philosophy:** Start a conversation, not a sale

**Characteristics:**
- **Goal:** Learn about their problems
- **Tone:** Friendly, curious, non-pushy
- **Length:** 100-150 words
- **Subject:** Casual, curiosity-driven (max 50 chars)
- **CTA:** Open-ended question or invitation to chat

**When to Use:**
- Cold outreach (no prior relationship)
- Building relationships long-term
- Exploring market needs
- Consultative selling approach
- High-value, long sales cycle

**Example:**
```
Subject: Quick question about Smile Dental

Hi Smile Dental team,

I help dentists streamline their operations and save time on repetitive tasks.

I'm curious—what's the biggest time-drain in your day-to-day? Appointment scheduling? Follow-ups? Review requests?

If you're open to it, I'd love to hop on a quick call to learn more about your operations and see if there's any way I could help.

No pressure at all—just reaching out to folks in the dental space.

Best,
[Your Name]
```

**Expected Response Rate:** 15-25% (lower, but warmer leads)

---

### Strategy 2: Specific Automation (Benefit-Driven)

**Philosophy:** Lead with concrete value

**Characteristics:**
- **Goal:** Demonstrate specific ROI
- **Tone:** Confident, expert, results-focused
- **Length:** 120-180 words
- **Subject:** Benefit-focused (max 60 chars)
- **CTA:** Low-pressure invitation to chat

**When to Use:**
- Warm leads (some awareness)
- Clear pain point identified
- Specific solution to offer
- Transactional selling approach
- Short sales cycle

**Example:**
```
Subject: Reduce no-shows by 30% for Smile Dental

Hi Smile Dental team,

Most dental practices lose $150-300 per no-show. That adds up fast.

We help dentists reduce no-shows by 30-40% with automated SMS/email reminders sent 24-48 hours before appointments.

Dr. Smith (another dentist in San Francisco) reduced his no-shows from 15% to 6% in just 60 days using our system.

The setup takes 15 minutes, and it runs on autopilot after that.

Would you be open to a quick 10-minute call to see if this could work for Smile Dental?

Best,
[Your Name]
```

**Expected Response Rate:** 25-35% (higher, more direct)

---

## Strategy Selection Flow

### CLI Interaction

```
🔥 CRITICAL DECISION: Choose Your Outreach Strategy

1️⃣  GENERAL HELP (Discovery Approach)
   📧 Email asks: 'What problems do you face?'
   🎯 Best for: Cold outreach, building relationships
   💡 Offers: General help with any automation needs
   📊 Conversion: Lower initial, but broader appeal

2️⃣  SPECIFIC AUTOMATION (Focused Approach)
   📧 Email says: 'We reduce no-shows by 30%'
   🎯 Best for: Warm leads, targeted solution
   💡 Offers: One specific automation benefit
   📊 Conversion: Higher for those with that problem

Choose strategy (1 or 2): _
```

### Validation

```python
def ask_outreach_type():
    """
    Ask user to choose email strategy
    Returns: 'general_help' or 'specific_automation'
    """

    print("\n" + "="*60)
    print("🔥 CRITICAL DECISION: Choose Your Outreach Strategy")
    print("="*60)

    # Display options
    print("\n1️⃣  GENERAL HELP (Discovery Approach)")
    print("   📧 Email asks: 'What problems do you face?'")
    print("   🎯 Best for: Cold outreach, building relationships")
    print("   💡 Offers: General help with any automation needs")
    print("   📊 Conversion: Lower initial, but broader appeal")

    print("\n2️⃣  SPECIFIC AUTOMATION (Focused Approach)")
    print("   📧 Email says: 'We reduce no-shows by 30%'")
    print("   🎯 Best for: Warm leads, targeted solution")
    print("   💡 Offers: One specific automation benefit")
    print("   📊 Conversion: Higher for those with that problem")

    # Get validated input
    while True:
        choice = input("\nChoose strategy (1 or 2): ").strip()
        if choice == "1":
            print("\n✅ Selected: GENERAL HELP approach")
            return "general_help"
        elif choice == "2":
            print("\n✅ Selected: SPECIFIC AUTOMATION approach")
            return "specific_automation"
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
```

---

## Configuration Storage

### Campaign Config JSON

```json
{
  "campaign_id": "campaign_20260211_103000",
  "business_type": "Dentists",
  "outreach_type": "specific_automation",
  "automation_focus": "Appointment Reminder System",
  "data_source": "google_maps",
  "total_businesses": 25,
  "created_at": "2026-02-11T10:30:00Z"
}
```

**File Location:** `.tmp/campaign_config.json`

**Save Function:**
```python
def save_config(config):
    """Save campaign configuration"""
    with open('.tmp/campaign_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    logger.info(f"Configuration saved: {config['outreach_type']}")
```

**Load Function:**
```python
def load_config():
    """Load campaign configuration"""
    if not os.path.exists('.tmp/campaign_config.json'):
        logger.warning("No campaign config found")
        return None

    with open('.tmp/campaign_config.json', 'r') as f:
        config = json.load(f)
    logger.info(f"Configuration loaded: {config['outreach_type']}")
    return config
```

---

## Strategy Routing Logic

### Email Generation Workflow

```python
def generate_emails():
    """Generate emails based on campaign strategy"""

    # Load campaign config
    config = load_config()
    if not config:
        print("❌ No campaign found. Please start a campaign first.")
        return

    # Get draft businesses
    businesses = get_draft_businesses()

    # Route to correct email generator
    if config['outreach_type'] == 'general_help':
        from tools.generate_general_email import generate_general_email as generate_email
        print("🎯 Using GENERAL HELP email strategy")
    else:
        from tools.generate_specific_email import generate_specific_email as generate_email
        print("🎯 Using SPECIFIC AUTOMATION strategy")
        print(f"   Focus: {config.get('automation_focus', 'N/A')}")

    # Generate emails
    for i, business in enumerate(businesses, 1):
        print(f"\n[{i}/{len(businesses)}] Generating email for: {business['name']}")

        subject, body = generate_email(
            business_name=business['name'],
            business_type=config['business_type'],
            website_content=scrape_website(business['website']),
            automation_focus=config.get('automation_focus')
        )

        update_email(business['row_number'], subject, body)
        print(f"   ✅ Generated: {subject}")
```

---

## Strategy Comparison

### Metrics

| Metric | General Help | Specific Automation |
|--------|--------------|---------------------|
| **Response Rate** | 15-25% | 25-35% |
| **Lead Quality** | Higher (engaged) | Medium (interested) |
| **Sales Cycle** | Longer (relationship) | Shorter (transactional) |
| **Use Case** | Discovery | Solution selling |
| **Best For** | Cold outreach | Warm leads |
| **Risk** | Lower (less pushy) | Higher (may feel salesy) |

### Decision Matrix

**Choose General Help if:**
- ✅ No prior relationship with prospects
- ✅ Long-term relationship building
- ✅ Consultative selling approach
- ✅ Complex/custom solutions
- ✅ High-value, long sales cycle

**Choose Specific Automation if:**
- ✅ Some awareness/warm leads
- ✅ Clear pain point identified
- ✅ Specific solution to offer
- ✅ Standardized/productized solution
- ✅ Short sales cycle

---

## Constants Definition

```python
# constants.py

# Email Strategies
STRATEGY_GENERAL = "general_help"
STRATEGY_SPECIFIC = "specific_automation"

# Strategy Descriptions
STRATEGY_DESCRIPTIONS = {
    STRATEGY_GENERAL: {
        "name": "General Help (Discovery Approach)",
        "goal": "Start a conversation, not a sale",
        "best_for": "Cold outreach, building relationships",
        "tone": "Friendly, curious, non-pushy",
        "expected_response_rate": "15-25%"
    },
    STRATEGY_SPECIFIC: {
        "name": "Specific Automation (Focused Approach)",
        "goal": "Lead with concrete value",
        "best_for": "Warm leads, targeted solution",
        "tone": "Confident, expert, results-focused",
        "expected_response_rate": "25-35%"
    }
}
```

---

## Testing

### Test 1: Strategy Selection
```python
# User selects General Help
outreach_type = ask_outreach_type()
assert outreach_type == "general_help"

# User selects Specific Automation
outreach_type = ask_outreach_type()
assert outreach_type == "specific_automation"
```

### Test 2: Config Persistence
```python
# Save config
config = {"outreach_type": "specific_automation"}
save_config(config)

# Load config
loaded_config = load_config()
assert loaded_config['outreach_type'] == "specific_automation"
```

### Test 3: Strategy Routing
```python
# Config with general_help
config = {"outreach_type": "general_help"}
save_config(config)

# Generate emails
generate_emails()
# Should use generate_general_email.py

# Config with specific_automation
config = {"outreach_type": "specific_automation"}
save_config(config)

# Generate emails
generate_emails()
# Should use generate_specific_email.py
```

---

## User Guidance

### Help Text

```
💡 TIP: Not sure which strategy to choose?

Ask yourself:
1. Do I have a prior relationship with these prospects? (No = General)
2. Do I know their specific pain point? (No = General)
3. Am I offering a standardized solution? (Yes = Specific)
4. Is my sales cycle short (< 30 days)? (Yes = Specific)

Still unsure? Start with General Help—it's less risky for cold outreach.
```

---

## Future Enhancements

- [ ] **Hybrid Strategy:** Combine both approaches
- [ ] **A/B Testing:** Test both strategies simultaneously
- [ ] **Auto Strategy:** AI recommends strategy based on business type
- [ ] **Custom Strategies:** User-defined email templates
- [ ] **Strategy Templates:** Pre-configured for different industries
- [ ] **Performance Tracking:** Track response rate by strategy
- [ ] **Strategy Switching:** Change strategy mid-campaign
- [ ] **Multi-Touch:** Sequence with different strategies

---

## Related Stories

- **Depends on:** US-001 (Project Setup), US-005 (AI Email Generation)
- **Blocks:** US-010 (Response Tracking) - compare strategy performance
- **Related:** US-014 (A/B Testing) - test strategies against each other

---

## Definition of Done

- [x] Two strategies clearly defined
- [x] Interactive selection implemented
- [x] Strategy saved to config
- [x] Strategy routing logic working
- [x] Config persistence working
- [x] Visual indicators in CLI
- [x] Validation prevents invalid selection
- [x] Documentation complete
- [x] Manual testing (both strategies)

---

**Created:** 2026-02-07
**Completed:** 2026-02-08
**Last Updated:** 2026-02-11
