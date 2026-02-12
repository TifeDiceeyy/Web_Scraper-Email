# US-015: Automated Follow-up Sequences

**Status:** 📝 Planned
**Priority:** P1 (High)
**Estimated Effort:** 14 hours

---

## User Story

**As a** user managing outreach campaigns
**I want** automated follow-up sequences for non-responders
**So that** I can maximize response rates without manual tracking

---

## Acceptance Criteria

1. [ ] 3-step follow-up sequence configuration
2. [ ] Customizable delay between steps (3, 7, 14 days)
3. [ ] AI-generated follow-up emails (different angle each time)
4. [ ] Auto-stop on reply detection
5. [ ] Follow-up templates per industry
6. [ ] Sequence analytics (open rates, reply rates per step)
7. [ ] Manual override (skip/pause sequence)
8. [ ] Sequence preview before activation
9. [ ] Multiple sequence templates
10. [ ] Webhook triggers on sequence events

---

## Sequence Example

```yaml
name: "3-Step Follow-up for Dentists"
trigger: "No reply after 3 days"

steps:
  - step: 1
    delay_days: 3
    type: "soft_reminder"
    subject: "Quick follow-up for {business_name}"
    approach: "Gentle nudge, acknowledge they're busy"
    
  - step: 2
    delay_days: 7
    type: "value_add"
    subject: "Thought you'd find this useful"
    approach: "Share case study or industry insight"
    
  - step: 3
    delay_days: 14
    type: "final_touchpoint"
    subject: "Last time reaching out"
    approach: "Clear CTA, offer to close loop"
```

---

## AI Follow-up Generation

```python
def generate_followup_email(original_email, step_number, business_name):
    """
    Generate follow-up email with different angle
    
    Step 1: Soft reminder
    Step 2: Value-add (case study, tip)
    Step 3: Final touchpoint (break-up email)
    """
    
    prompts = {
        1: f"Generate a gentle follow-up email to {business_name}...",
        2: f"Generate a value-add follow-up with case study...",
        3: f"Generate a final touchpoint email..."
    }
    
    return gemini_api.generate(prompts[step_number])
```

---

## Sequence Analytics

```
Follow-up Sequence Performance:
├─ Step 0 (Initial): 100 sent, 25 replied (25%)
├─ Step 1 (Day 3):   75 sent, 12 replied (16%)
├─ Step 2 (Day 10):  63 sent, 8 replied (13%)
└─ Step 3 (Day 24):  55 sent, 5 replied (9%)

Total Response Rate: 50% (50/100)
Without Follow-ups: 25% (25/100)
Lift from Follow-ups: +100%
```

---

## Related Stories

- **Depends on:** US-007 (Gmail), US-010 (Response Tracking)
- **Related:** US-011 (Analytics) - sequence performance
- **Related:** US-013 (Templates) - follow-up templates

---

**Created:** 2026-02-11
**Target Completion:** 2026-04-15
