# US-012: Multi-Campaign Management

**Status:** 📝 Planned
**Priority:** P1 (High)
**Estimated Effort:** 12 hours

---

## User Story

**As a** user running multiple outreach campaigns
**I want** to manage multiple campaigns independently
**So that** I can target different industries or use different strategies simultaneously

---

## Acceptance Criteria

1. [ ] Create multiple campaigns with unique IDs
2. [ ] List all campaigns with status
3. [ ] Switch between campaigns
4. [ ] Separate Google Sheets per campaign (or tabs)
5. [ ] Campaign comparison view
6. [ ] Archive old campaigns
7. [ ] Campaign templates for quick setup
8. [ ] Search/filter campaigns
9. [ ] Bulk operations (pause, resume, delete)
10. [ ] Performance comparison across campaigns

---

## Data Model

### Campaign Structure

```json
{
  "campaigns": [
    {
      "id": "campaign_001",
      "name": "Dentists - San Francisco",
      "business_type": "Dentists",
      "location": "San Francisco, CA",
      "strategy": "specific_automation",
      "automation_focus": "Appointment Reminders",
      "status": "active",
      "created_at": "2026-02-11T10:00:00Z",
      "sheet_id": "1abc123...",
      "stats": {
        "collected": 50,
        "generated": 48,
        "sent": 35,
        "replied": 12
      }
    },
    {
      "id": "campaign_002",
      "name": "Restaurants - NYC",
      "business_type": "Restaurants",
      "location": "New York, NY",
      "strategy": "general_help",
      "status": "paused",
      "created_at": "2026-02-15T14:00:00Z",
      "sheet_id": "1xyz789...",
      "stats": {
        "collected": 100,
        "generated": 95,
        "sent": 80,
        "replied": 28
      }
    }
  ]
}
```

---

## CLI Interface

### Campaign List View

```
╔═══════════════════════════════════════════════════════════╗
║                    MY CAMPAIGNS                           ║
╠═══════════════════════════════════════════════════════════╣
║ [1] Dentists - San Francisco                    ACTIVE   ║
║     Created: Feb 11, 2026                                 ║
║     Sent: 35/50 (70%)  |  Response: 12 (34.3%)           ║
║                                                           ║
║ [2] Restaurants - NYC                            PAUSED   ║
║     Created: Feb 15, 2026                                 ║
║     Sent: 80/100 (80%)  |  Response: 28 (35.0%)          ║
║                                                           ║
║ [3] Plumbers - Los Angeles                      COMPLETE  ║
║     Created: Feb 01, 2026                                 ║
║     Sent: 25/25 (100%)  |  Response: 7 (28.0%)           ║
╚═══════════════════════════════════════════════════════════╝

[C] Create New Campaign    [S] Switch Campaign
[A] Archive Campaign       [D] Delete Campaign
[M] Back to Main Menu
```

---

## Key Features

### 1. Campaign Templates

```python
CAMPAIGN_TEMPLATES = {
    "dentist_appointment_reminders": {
        "business_type": "Dentists",
        "strategy": "specific_automation",
        "automation_focus": "Appointment Reminder System",
        "expected_response_rate": "30-35%"
    },
    "restaurant_review_requests": {
        "business_type": "Restaurants",
        "strategy": "specific_automation",
        "automation_focus": "Review Request Automation",
        "expected_response_rate": "25-30%"
    },
    "generic_discovery": {
        "business_type": "[To be specified]",
        "strategy": "general_help",
        "expected_response_rate": "15-25%"
    }
}
```

### 2. Campaign Comparison

```
╔═══════════════════════════════════════════════════════════╗
║              CAMPAIGN COMPARISON                          ║
╠═══════════════════════════════════════════════════════════╣
║ Metric          | Dentists SF | Restaurants NYC | Avg     ║
║─────────────────|─────────────|─────────────────|─────────║
║ Response Rate   | 34.3%       | 35.0%           | 34.7%   ║
║ Avg Time Reply  | 2.4 days    | 1.8 days        | 2.1 days║
║ Positive Rate   | 67%         | 71%             | 69%     ║
║ Cost per Reply  | $0.004      | $0.003          | $0.0035 ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Related Stories

- **Depends on:** US-002 (Google Sheets), US-006 (Email Strategies)
- **Blocks:** US-014 (A/B Testing) - compare campaigns
- **Related:** US-011 (Analytics) - per-campaign analytics

---

**Created:** 2026-02-11
**Target Completion:** 2026-03-20
