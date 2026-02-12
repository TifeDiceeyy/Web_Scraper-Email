# US-019: API Access & Webhooks

**Status:** 📝 Planned
**Priority:** P2 (Nice to have)
**Estimated Effort:** 18 hours

---

## User Story

**As a** developer integrating with other systems
**I want** REST API access and webhooks
**So that** I can automate workflows and integrate with my tech stack

---

## Acceptance Criteria

### REST API
1. [ ] API authentication (API keys)
2. [ ] Rate limiting (100 req/min)
3. [ ] Full CRUD operations on campaigns
4. [ ] Trigger email generation via API
5. [ ] Send emails via API
6. [ ] Get campaign analytics via API
7. [ ] OpenAPI/Swagger documentation
8. [ ] SDK libraries (Python, JavaScript)

### Webhooks
1. [ ] Register webhook endpoints
2. [ ] Event types (email_sent, reply_received, campaign_complete)
3. [ ] Retry logic (3 attempts with backoff)
4. [ ] Webhook signature verification (HMAC)
5. [ ] Webhook logs (delivery status)
6. [ ] Test webhook feature

---

## API Endpoints

```
POST   /api/v1/campaigns                  # Create campaign
GET    /api/v1/campaigns                  # List campaigns
GET    /api/v1/campaigns/{id}             # Get campaign
PUT    /api/v1/campaigns/{id}             # Update campaign
DELETE /api/v1/campaigns/{id}             # Delete campaign

POST   /api/v1/campaigns/{id}/businesses  # Add businesses
POST   /api/v1/campaigns/{id}/generate    # Generate emails
POST   /api/v1/campaigns/{id}/send        # Send emails
GET    /api/v1/campaigns/{id}/analytics   # Get analytics

POST   /api/v1/webhooks                   # Register webhook
GET    /api/v1/webhooks                   # List webhooks
DELETE /api/v1/webhooks/{id}              # Delete webhook

GET    /api/v1/health                     # Health check
GET    /api/v1/usage                      # API usage stats
```

---

## Webhook Events

### email_sent
```json
{
  "event": "email_sent",
  "timestamp": "2026-02-11T15:30:00Z",
  "campaign_id": "campaign_001",
  "business_id": "12345",
  "data": {
    "business_name": "Smile Dental",
    "email": "info@smiledental.com",
    "subject": "Reduce no-shows by 30%",
    "sent_at": "2026-02-11T15:30:00Z"
  }
}
```

### reply_received
```json
{
  "event": "reply_received",
  "timestamp": "2026-02-11T18:45:00Z",
  "campaign_id": "campaign_001",
  "business_id": "12345",
  "data": {
    "business_name": "Smile Dental",
    "reply_date": "2026-02-11T18:40:00Z",
    "sentiment": "positive",
    "snippet": "Yes, I'd be interested..."
  }
}
```

---

## Authentication

```python
import requests

API_KEY = "sk_live_abc123..."
headers = {"Authorization": f"Bearer {API_KEY}"}

# Create campaign
response = requests.post(
    "https://api.outreach.com/v1/campaigns",
    headers=headers,
    json={
        "name": "Dentists SF",
        "business_type": "Dentists",
        "strategy": "specific_automation"
    }
)
```

---

## Related Stories

- **Depends on:** US-012 (Campaigns), US-010 (Response Tracking)
- **Related:** US-016 (CRM) - similar integration patterns
- **Related:** US-018 (White Label) - tenant-specific API keys

---

**Created:** 2026-02-11
**Target Completion:** 2026-06-15
