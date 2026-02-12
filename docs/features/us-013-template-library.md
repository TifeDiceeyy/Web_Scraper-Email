# US-013: Email Template Library

**Status:** 📝 Planned
**Priority:** P1 (High)
**Estimated Effort:** 8 hours

---

## User Story

**As a** user generating outreach emails
**I want** a library of pre-built email templates
**So that** I can quickly generate proven emails for common industries

---

## Acceptance Criteria

1. [ ] 20+ pre-built templates for common industries
2. [ ] Template categories (by industry, strategy, automation)
3. [ ] Template preview before use
4. [ ] Variable substitution (business_name, location, etc.)
5. [ ] Custom template creation
6. [ ] Template versioning
7. [ ] Performance tracking per template
8. [ ] Template search and filtering
9. [ ] Template export/import
10. [ ] Community template sharing (future)

---

## Template Structure

```yaml
id: dentist_appointment_reminders_v1
name: "Dentist - Appointment Reminder System"
industry: "Dentists"
strategy: "specific_automation"
automation_focus: "Appointment Reminder System"
language: "en"

subject: "Reduce no-shows by 30% for {business_name}"

body: |
  Hi {business_name} team,

  Most dental practices lose $150-300 per no-show. That adds up fast.

  We help dentists reduce no-shows by 30-40% with automated SMS/email reminders.

  Dr. Smith (another dentist in {location}) reduced no-shows from 15% to 6% in 60 days.

  Would you be open to a quick call to see if this could work for {business_name}?

  Best,
  {sender_name}

variables:
  - business_name
  - location
  - sender_name

performance:
  times_used: 150
  response_rate: 28.5%
  positive_rate: 65%
  avg_time_to_reply: 2.1 days

tags:
  - dentist
  - appointment
  - no-shows
  - healthcare
