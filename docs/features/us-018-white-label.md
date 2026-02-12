# US-018: White Label & Multi-Tenant Support

**Status:** 📝 Planned
**Priority:** P2 (Nice to have)
**Estimated Effort:** 24 hours

---

## User Story

**As a** agency owner
**I want** to white-label the platform for my clients
**So that** I can offer outreach services under my own brand

---

## Acceptance Criteria

1. [ ] Custom branding (logo, colors, domain)
2. [ ] Tenant isolation (separate data per client)
3. [ ] Tenant admin portal
4. [ ] Usage limits per tenant (emails/month, AI calls/month)
5. [ ] Tenant-level API keys (separate Gemini keys)
6. [ ] Custom SMTP servers per tenant
7. [ ] Tenant billing and invoicing
8. [ ] Multi-tenant database architecture
9. [ ] Tenant-specific templates
10. [ ] White-label documentation

---

## Multi-Tenant Architecture

```
┌─────────────────────────────────────────┐
│         Platform (Agency)               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐    │
│  │  Tenant A    │  │  Tenant B    │    │
│  │  (Client 1)  │  │  (Client 2)  │    │
│  ├──────────────┤  ├──────────────┤    │
│  │ Users: 5     │  │ Users: 10    │    │
│  │ Campaigns: 3 │  │ Campaigns: 8 │    │
│  │ API Key: ××× │  │ API Key: ××× │    │
│  └──────────────┘  └──────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Tenant Configuration

```python
TENANT_CONFIG = {
    "tenant_id": "acme_agency",
    "name": "ACME Marketing",
    "domain": "outreach.acmemarketing.com",
    "logo_url": "https://cdn.acme.com/logo.png",
    "primary_color": "#0066CC",
    "secondary_color": "#FF6600",
    "gemini_api_key": "AIza...tenant_specific",
    "smtp_server": "smtp.acmemarketing.com",
    "usage_limits": {
        "emails_per_month": 10000,
        "ai_calls_per_month": 5000,
        "users": 10
    },
    "features": {
        "crm_integration": True,
        "white_label_reports": True,
        "custom_templates": True
    }
}
```

---

## Tenant Admin Portal

```
╔═══════════════════════════════════════════════════════════╗
║              TENANT ADMIN DASHBOARD                       ║
║                   ACME Marketing                          ║
╠═══════════════════════════════════════════════════════════╣
║ Usage This Month:                                         ║
║   Emails Sent:     7,543 / 10,000 (75%)                  ║
║   AI Calls:        3,210 / 5,000  (64%)                  ║
║   Active Users:    8 / 10                                 ║
║                                                           ║
║ Revenue This Month: $1,250                                ║
║ MRR: $1,500                                               ║
║                                                           ║
║ [Manage Users]  [Billing]  [Branding]  [API Keys]        ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Related Stories

- **Depends on:** US-017 (Team Collaboration), US-012 (Campaigns)
- **Related:** US-023 (Stripe) - tenant billing

---

**Created:** 2026-02-11
**Target Completion:** 2026-06-01
