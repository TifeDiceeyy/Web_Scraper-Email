# US-016: CRM Integration (HubSpot/Salesforce)

**Status:** 📝 Planned
**Priority:** P1 (High)
**Estimated Effort:** 20 hours

---

## User Story

**As a** sales team using a CRM
**I want** bidirectional sync between outreach system and CRM
**So that** all leads and activities are automatically tracked in one place

---

## Acceptance Criteria

### HubSpot Integration
1. [ ] OAuth2 authentication
2. [ ] Import contacts from HubSpot
3. [ ] Export businesses to HubSpot as contacts
4. [ ] Log sent emails as HubSpot activities
5. [ ] Create deals on positive replies
6. [ ] Update contact properties (status, last contacted)
7. [ ] Webhook for HubSpot events
8. [ ] Two-way sync (HubSpot ↔ Sheets)

### Salesforce Integration
1. [ ] OAuth2 authentication
2. [ ] Import Leads/Contacts from Salesforce
3. [ ] Export businesses as Leads
4. [ ] Create Tasks for sent emails
5. [ ] Create Opportunities on positive replies
6. [ ] Update Lead status automatically
7. [ ] Custom field mapping
8. [ ] Apex trigger for real-time sync

---

## Data Mapping

### HubSpot

```python
HUBSPOT_MAPPING = {
    "business_name": "company.name",
    "email": "email",
    "phone": "phone",
    "website": "website",
    "location": "city",
    "status": "hs_lead_status",
    "last_contacted": "notes_last_contacted",
    "response_received": "custom_property_responded"
}
```

### Salesforce

```python
SALESFORCE_MAPPING = {
    "business_name": "Company",
    "email": "Email",
    "phone": "Phone",
    "website": "Website",
    "location": "City",
    "status": "Status",
    "last_contacted": "LastActivityDate",
    "response_received": "Responded__c"  # Custom field
}
```

---

## API Integration

### HubSpot API

```python
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput

def create_hubspot_contact(business):
    """Create contact in HubSpot"""
    
    client = hubspot.Client.create(access_token=HUBSPOT_API_KEY)
    
    properties = {
        "email": business['email'],
        "firstname": business['name'].split()[0],
        "lastname": business['name'].split()[-1],
        "company": business['name'],
        "phone": business['phone'],
        "website": business['website'],
        "city": business['location']
    }
    
    contact = SimplePublicObjectInput(properties=properties)
    response = client.crm.contacts.basic_api.create(contact)
    
    return response.id
```

### Salesforce API

```python
from simple_salesforce import Salesforce

def create_salesforce_lead(business):
    """Create lead in Salesforce"""
    
    sf = Salesforce(
        username=SF_USERNAME,
        password=SF_PASSWORD,
        security_token=SF_TOKEN
    )
    
    lead_data = {
        'FirstName': business['name'].split()[0],
        'LastName': business['name'].split()[-1],
        'Company': business['name'],
        'Email': business['email'],
        'Phone': business['phone'],
        'Website': business['website'],
        'City': business['location'],
        'Status': 'Open - Not Contacted'
    }
    
    result = sf.Lead.create(lead_data)
    return result['id']
```

---

## Sync Strategy

### Initial Sync
1. User connects CRM account (OAuth)
2. Import all contacts/leads matching criteria
3. Map to Google Sheet structure
4. Create campaign from imported data

### Ongoing Sync
1. **Outbound:** Email sent → Create activity in CRM
2. **Outbound:** Reply received → Update contact, create deal/opportunity
3. **Inbound:** Contact updated in CRM → Update Sheet
4. **Inbound:** Contact deleted in CRM → Mark archived in Sheet

### Conflict Resolution
- **Last Write Wins:** Most recent update takes precedence
- **Manual Resolution:** Flag conflicts for user review
- **Merge Strategy:** Combine non-conflicting fields

---

## Related Stories

- **Depends on:** US-002 (Google Sheets), US-010 (Response Tracking)
- **Blocks:** US-017 (Team Collaboration) - CRM teams
- **Related:** US-019 (API) - expose same data via API

---

**Created:** 2026-02-11
**Target Completion:** 2026-05-01
