# US-011: Campaign Analytics Dashboard

**Status:** 📝 Planned
**Priority:** P1 (High)
**Estimated Effort:** 10 hours

---

## User Story

**As a** user managing outreach campaigns
**I want** a visual dashboard showing campaign performance metrics
**So that** I can track progress, measure ROI, and optimize my outreach strategy

---

## Acceptance Criteria

1. [ ] CLI-based dashboard with ASCII art visualization
2. [ ] Campaign overview card (total sent, responses, rates)
3. [ ] Funnel visualization (Collected → Generated → Approved → Sent → Replied)
4. [ ] Time-series chart (daily send volume, response velocity)
5. [ ] Email strategy comparison (General vs Specific performance)
6. [ ] Automation focus breakdown (which automations work best)
7. [ ] Response rate trends (improving/declining over time)
8. [ ] Top performing businesses (by response)
9. [ ] AI insights and recommendations (powered by Gemini)
10. [ ] Export to CSV/PDF (optional)

---

## Dashboard Layout (CLI)

```
╔════════════════════════════════════════════════════════════════════════╗
║                    CAMPAIGN ANALYTICS DASHBOARD                        ║
║              Dentists - San Francisco (Feb 11, 2026)                   ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  📊 CAMPAIGN FUNNEL                                                    ║
║  ─────────────────                                                     ║
║  Collected:     50 ████████████████████████████████████████ 100%      ║
║  Generated:     48 ██████████████████████████████████████   96%       ║
║  Approved:      40 ████████████████████████████████         80%       ║
║  Sent:          35 ██████████████████████████████           70%       ║
║  Replied:       12 ██████████                               34%       ║
║                                                                        ║
║  ✅ Key Metrics                                                        ║
║  ──────────────                                                        ║
║  Response Rate:           34.3% (12/35)                                ║
║  Avg Time to Reply:       2.4 days                                    ║
║  Positive Responses:      8 (67% of replies)                          ║
║  Conversion Rate:         24% (projected)                              ║
║                                                                        ║
║  📈 RESPONSE BREAKDOWN                                                 ║
║  ──────────────────────                                                ║
║  ✅ Positive:     8 ████████████████████████████████ 67%              ║
║  ⚪ Neutral:      3 ████████████ 25%                                   ║
║  ❌ Negative:     1 ████ 8%                                            ║
║                                                                        ║
║  📅 DAILY ACTIVITY (Last 7 Days)                                       ║
║  ─────────────────────────────                                        ║
║  Mon   ████████ 8 sent, 2 replied                                     ║
║  Tue   ██████████ 10 sent, 3 replied                                  ║
║  Wed   ████████████ 12 sent, 4 replied                                ║
║  Thu   ██████ 6 sent, 2 replied                                       ║
║  Fri   ████ 4 sent, 1 replied                                         ║
║  Sat   0 sent, 0 replied                                              ║
║  Sun   0 sent, 0 replied                                              ║
║                                                                        ║
║  🎯 EMAIL STRATEGY PERFORMANCE                                         ║
║  ────────────────────────────                                         ║
║  General Help:        N/A (not used in this campaign)                 ║
║  Specific Automation: 34.3% response rate                             ║
║                                                                        ║
║  🤖 AI INSIGHTS                                                        ║
║  ──────────────                                                        ║
║  • Your response rate (34.3%) is above industry avg (20-25%)          ║
║  • Peak reply times: Tuesday-Thursday, 10am-2pm                       ║
║  • Recommendation: Send remaining emails on Wed morning                ║
║  • "Appointment Reminder" automation performing well                   ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

Commands:
  [1] View detailed metrics    [4] Export to CSV
  [2] Compare campaigns         [5] AI recommendations
  [3] Response timeline         [6] Back to main menu
```

---

## Technical Requirements

### Data Collection

**Data Sources:**
1. Google Sheet (current campaign data)
2. Campaign config JSON (campaign metadata)
3. Outreach log file (event history)

**Metrics to Calculate:**
```python
{
    "total_collected": 50,
    "total_generated": 48,
    "total_approved": 40,
    "total_sent": 35,
    "total_replied": 12,

    "response_rate": 34.3,  # (replied / sent) × 100
    "approval_rate": 83.3,  # (approved / generated) × 100
    "send_rate": 87.5,      # (sent / approved) × 100

    "avg_time_to_reply": 2.4,  # days
    "fastest_reply": 0.17,     # 4 hours
    "slowest_reply": 7.0,      # 7 days

    "positive_replies": 8,
    "neutral_replies": 3,
    "negative_replies": 1,

    "sentiment_breakdown": {
        "positive": 67,  # percentage
        "neutral": 25,
        "negative": 8
    }
}
```

---

## Visualization Components

### 1. Funnel Chart (ASCII)

```python
def render_funnel(metrics):
    """Render funnel visualization"""

    stages = [
        ('Collected', metrics['total_collected'], 100),
        ('Generated', metrics['total_generated'], metrics['approval_rate']),
        ('Approved', metrics['total_approved'], metrics['send_rate']),
        ('Sent', metrics['total_sent'], 70),
        ('Replied', metrics['total_replied'], metrics['response_rate'])
    ]

    print("📊 CAMPAIGN FUNNEL")
    print("─────────────────")

    max_count = metrics['total_collected']

    for stage, count, percent in stages:
        # Calculate bar width (40 chars max)
        bar_width = int((count / max_count) * 40)
        bar = '█' * bar_width

        print(f"{stage:12} {count:3} {bar:40} {percent:.0f}%")
```

### 2. Bar Chart (Daily Activity)

```python
def render_daily_activity(daily_data):
    """Render daily activity chart"""

    print("\n📅 DAILY ACTIVITY (Last 7 Days)")
    print("─────────────────────────────")

    max_value = max(day['sent'] for day in daily_data)

    for day in daily_data:
        day_name = day['date'].strftime('%a')
        sent = day['sent']
        replied = day['replied']

        # Scale to 12 chars max
        bar_width = int((sent / max_value) * 12) if max_value > 0 else 0
        bar = '█' * bar_width

        print(f"{day_name}   {bar:12} {sent} sent, {replied} replied")
```

### 3. Progress Bars (Sentiment Breakdown)

```python
def render_sentiment(sentiment):
    """Render sentiment breakdown"""

    print("\n📈 RESPONSE BREAKDOWN")
    print("──────────────────────")

    total_width = 40

    for category, percent in sentiment.items():
        bar_width = int((percent / 100) * total_width)
        bar = '█' * bar_width

        icon = {
            'positive': '✅',
            'neutral': '⚪',
            'negative': '❌'
        }[category]

        print(f"{icon} {category.title():10} {bar:40} {percent:.0f}%")
```

---

## AI Insights Generation

### Gemini Prompt

```python
insights_prompt = f"""Analyze this email campaign performance data and provide actionable insights:

Campaign: {campaign_name}
Business Type: {business_type}
Strategy: {strategy}

Metrics:
- Total Sent: {total_sent}
- Response Rate: {response_rate}%
- Positive Responses: {positive_replies}
- Average Time to Reply: {avg_time_to_reply} days

Daily Activity:
{daily_activity_summary}

Provide 3-5 bullet-point insights and recommendations in this format:
• [Insight or recommendation]

Focus on:
1. How this response rate compares to industry benchmarks
2. Optimal send times based on reply patterns
3. Which aspects of the strategy are working well
4. Specific recommendations for improvement
5. When to follow up with non-responders
"""

response = gemini_client.generate_content(insights_prompt)
insights = response.text
```

### Example Insights

```
🤖 AI INSIGHTS
──────────────
• Your 34.3% response rate is significantly above the industry average (20-25%) for cold email outreach
• Peak reply times indicate Tuesday-Thursday, 10am-2pm are optimal send windows
• The "Appointment Reminder" automation focus is resonating well with dentist audience
• Consider following up with non-responders after 5-7 days (currently 15 non-responders)
• Your email length (150 words avg) is in the sweet spot for engagement
```

---

## Data Aggregation Logic

### Calculate Response Rate

```python
def calculate_response_rate(businesses):
    """Calculate response rate"""

    sent = [b for b in businesses if b['status'] == 'Sent']
    replied = [b for b in sent if b['response_received']]

    if len(sent) == 0:
        return 0

    return (len(replied) / len(sent)) * 100
```

### Calculate Avg Time to Reply

```python
from datetime import datetime

def calculate_avg_time_to_reply(businesses):
    """Calculate average time to reply in days"""

    times = []

    for b in businesses:
        if b['response_received'] and b['date_sent'] and b['response_date']:
            sent_date = datetime.strptime(b['date_sent'], '%Y-%m-%d %H:%M:%S')
            reply_date = datetime.strptime(b['response_date'], '%Y-%m-%d %H:%M:%S')

            delta = reply_date - sent_date
            times.append(delta.total_seconds() / 86400)  # Convert to days

    if not times:
        return 0

    return sum(times) / len(times)
```

### Group by Date

```python
def group_by_date(businesses, days=7):
    """Group businesses by date sent"""

    from datetime import datetime, timedelta
    from collections import defaultdict

    daily_data = defaultdict(lambda: {'sent': 0, 'replied': 0})

    # Get last N days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    for b in businesses:
        if b['status'] == 'Sent' and b['date_sent']:
            sent_date = datetime.strptime(b['date_sent'], '%Y-%m-%d %H:%M:%S')

            if start_date <= sent_date <= end_date:
                date_key = sent_date.strftime('%Y-%m-%d')
                daily_data[date_key]['sent'] += 1

                if b['response_received']:
                    daily_data[date_key]['replied'] += 1

    # Convert to list sorted by date
    result = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_key = date.strftime('%Y-%m-%d')
        result.append({
            'date': date,
            'sent': daily_data[date_key]['sent'],
            'replied': daily_data[date_key]['replied']
        })

    return result
```

---

## Export Functionality

### CSV Export

```python
def export_to_csv(campaign_data, filename='campaign_report.csv'):
    """Export campaign data to CSV"""

    import csv

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Business Name', 'Email', 'Status',
            'Date Sent', 'Response Received', 'Response Date',
            'Time to Reply (hours)', 'Sentiment'
        ])

        # Rows
        for business in campaign_data:
            writer.writerow([
                business['name'],
                business['email'],
                business['status'],
                business.get('date_sent', ''),
                business.get('response_received', False),
                business.get('response_date', ''),
                business.get('time_to_reply_hours', ''),
                business.get('sentiment', '')
            ])

    print(f"✅ Exported to {filename}")
```

---

## Testing

### Test 1: Metrics Calculation
```python
# Mock data
businesses = [
    {'status': 'Sent', 'response_received': True},
    {'status': 'Sent', 'response_received': True},
    {'status': 'Sent', 'response_received': False},
    {'status': 'Approved', 'response_received': False}
]

response_rate = calculate_response_rate(businesses)
assert response_rate == 66.67  # 2/3 sent emails got replies
```

### Test 2: Daily Grouping
```python
# Should group by date correctly
daily_data = group_by_date(businesses, days=7)
assert len(daily_data) == 7  # 7 days
```

### Test 3: ASCII Rendering
```python
# Should render without errors
render_funnel(metrics)
render_daily_activity(daily_data)
render_sentiment(sentiment)
```

---

## Future Enhancements

- [ ] **Web UI Dashboard:** Interactive charts with Chart.js/Recharts
- [ ] **Email Open Tracking:** Track email opens (requires tracking pixels)
- [ ] **Link Click Tracking:** Track link clicks in emails
- [ ] **Geographic Heatmap:** Map responses by location
- [ ] **Industry Benchmarks:** Compare to industry averages
- [ ] **Predictive Analytics:** Predict response rate for new campaigns
- [ ] **A/B Test Results:** Show winning variant performance
- [ ] **Cost Analysis:** Calculate cost per reply (API costs)
- [ ] **Time-of-Day Analysis:** Best times to send emails
- [ ] **Subject Line Analysis:** Which subject lines perform best

---

## Related Stories

- **Depends on:** US-010 (Response Tracking) - provides response data
- **Related:** US-012 (Multi-Campaign Management) - compare multiple campaigns
- **Related:** US-014 (A/B Testing) - show A/B test results
- **Related:** US-016 (AI Progress Reports) - uses similar AI insights

---

## Definition of Done

- [ ] Dashboard renders correctly in CLI
- [ ] All metrics calculated accurately
- [ ] Funnel visualization working
- [ ] Daily activity chart working
- [ ] Sentiment breakdown working
- [ ] AI insights generation working
- [ ] CSV export working
- [ ] Error handling for missing data
- [ ] Manual testing with sample campaign data
- [ ] Documentation complete

---

**Created:** 2026-02-11
**Target Completion:** 2026-03-15
**Last Updated:** 2026-02-11
