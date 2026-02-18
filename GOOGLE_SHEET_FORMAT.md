# 📊 Google Sheet Column Format

This document shows the exact column structure used by the Business Outreach scraper.

---

## 📋 Column Layout (A to N)

| Column | Name | Description | Populated By | Example |
|--------|------|-------------|--------------|---------|
| **A** | Business Name | Name of the business | Scraper | "Istanbul Dental Center" |
| **B** | Location | Full address or city | Scraper | "Istanbul, Turkey" |
| **C** | Email | Email address | Enrichment/Scraper | "info@dentalcenter.com" |
| **D** | Phone | Phone number | Scraper | "+90 212 555 1234" |
| **E** | Website | Website URL | Scraper | "https://dentalcenter.com" |
| **F** | Contact Person | Name of contact | User/AI | "Dr. Mehmet" |
| **G** | Generated Subject | Email subject line | AI Email Generator | "Transform Your Practice with..." |
| **H** | Generated Body | Email content | AI Email Generator | "Dear Dr. Mehmet,\n\nI noticed..." |
| **I** | Your Notes | Manual notes | User | "Follow up in 2 weeks" |
| **J** | Status | Campaign status | System/User | "Draft", "Approved", "Sent" |
| **K** | Date Approved | When email approved | User | "2026-02-12" |
| **L** | Date Sent | When email sent | Email Sender | "2026-02-12 14:30" |
| **M** | Last Response | Last response date | Response Tracker | "2026-02-15" |
| **N** | Response Details | Response content | Response Tracker | "Interested! Please call." |

---

## 🔄 Workflow & Column Population

### 1️⃣ **Initial Scraping** (Columns A-E)
When you scrape from Google Maps or Instagram:
- ✅ **A (Name)**: Business name
- ✅ **B (Location)**: Address
- ✅ **C (Email)**: Email (if found)
- ✅ **D (Phone)**: Phone number
- ✅ **E (Website)**: Website URL
- ⚪ **F-N**: Empty

**Status**: "Draft"

---

### 2️⃣ **Contact Enrichment** (Updates C, D, E)
When you run "Enrich Contact Info":
- 🔄 **C (Email)**: Adds missing emails
- 🔄 **D (Phone)**: Adds missing phones
- 🔄 **E (Website)**: Adds missing websites

**Status**: Still "Draft"

---

### 3️⃣ **Email Generation** (Columns G, H)
When you run "Generate Emails":
- ✅ **G (Subject)**: AI-generated subject
- ✅ **H (Body)**: AI-generated email body
- ✅ **F (Contact Person)**: May be filled if AI finds name

**Status**: Still "Draft"

---

### 4️⃣ **Email Approval** (Column J, K)
When you approve emails in Google Sheet:
- 🔄 **J (Status)**: Change from "Draft" to "Approved"
- ✅ **K (Date Approved)**: Automatically set to today

---

### 5️⃣ **Email Sending** (Column L)
When you run "Send Approved Emails":
- 🔄 **J (Status)**: "Approved" → "Sent"
- ✅ **L (Date Sent)**: Timestamp of send

---

### 6️⃣ **Response Tracking** (Columns M, N)
When you run "Track Responses":
- ✅ **M (Last Response)**: Date of reply
- ✅ **N (Response Details)**: Reply content preview

**Status**: "Sent" (unchanged)

---

## 📊 Column Letter Reference

Quick reference for formulas or scripts:

```
A = Business Name
B = Location
C = Email
D = Phone
E = Website
F = Contact Person
G = Generated Subject
H = Generated Body
I = Your Notes
J = Status
K = Date Approved
L = Date Sent
M = Last Response
N = Response Details
```

---

## 🎨 Recommended Sheet Formatting

### Column Widths:
- **A (Name)**: 200px
- **B (Location)**: 250px
- **C (Email)**: 180px
- **D (Phone)**: 130px
- **E (Website)**: 180px
- **F (Contact)**: 120px
- **G (Subject)**: 250px
- **H (Body)**: 400px (widest)
- **I (Notes)**: 150px
- **J (Status)**: 100px
- **K-N (Dates)**: 110px each

### Conditional Formatting:
- **Status = "Draft"**: Yellow background
- **Status = "Approved"**: Blue background
- **Status = "Sent"**: Green background
- **Last Response not empty**: Light green row

---

## 📝 Example Row

| A | B | C | D | E | F | G | H | I | J | K | L | M | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Istanbul Dental | Istanbul, TR | info@dental.com | +90 212... | dental.com | Dr. Mehmet | Transform Your... | Dear Dr. Mehmet... | VIP client | Sent | 2026-02-12 | 2026-02-12 14:30 | 2026-02-15 | Interested! |

---

## 🔧 Custom Fields

### Want to Add More Columns?

You can add custom columns **after column N** (O, P, Q, etc.):
- **O**: Industry
- **P**: Company Size
- **Q**: Follow-up Date
- **R**: Priority (High/Med/Low)

The scraper won't populate these, but you can fill them manually.

**Important**: Don't insert columns before N - it will break the scraper!

---

## 📱 Platform-Specific Fields

Different scrapers populate different fields:

### **Google Maps Scraper**:
- ✅ Name, Location, Phone, Website
- ⚠️ Email: Rarely available

### **Instagram Scraper**:
- ✅ Name (username), Website (profile URL)
- ❌ Email, Phone: Not available
- 💡 Use Contact Enrichment after!

### **Contact Enrichment**:
- ✅ Email, Phone
- 🎯 Scrapes from Website column

---

## 🎯 Pro Tips

1. **Filter by Status**: Use Google Sheets filter to show only "Draft" or "Approved"
2. **Sort by Date**: Sort by column L (Date Sent) to see recent sends
3. **Response Rate**: Use formula: `=COUNTIF(M:M,"<>"")/COUNTIF(J:J,"Sent")`
4. **Add Notes**: Use column I for campaign-specific notes

---

**This format is fixed in the code.** If you need different columns, let me know and I can update the scraper! 🚀
