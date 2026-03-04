"""Shared fixtures for SimulatedInnovation tests."""

import pytest
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
SKILL_PATH = PROJECT_DIR / ".claude" / "commands" / "evaluate.md"
OUTPUTS_DIR = PROJECT_DIR / "outputs"


@pytest.fixture
def skill_content():
    """Load the evaluate.md skill file content."""
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture
def sample_report():
    """A minimal well-formed report for testing the validator."""
    return """\
# InvoiceFlow Evaluation

## Executive Summary

InvoiceFlow addresses a genuine pain point for freelance designers who struggle
with invoicing and cash flow prediction. The synthetic user interviews revealed
strong interest from the target audience, though concerns about integration
with existing tools and pricing remain.

Overall, the concept shows promise with a clear path to product-market fit
if the team addresses the identified adoption barriers.

## Overall Score: 6.8/10

| Dimension | Score |
|---|---|
| Problem Validity | 7.5 |
| Solution Fit | 7.0 |
| Market Demand | 6.5 |
| Competitive Position | 5.5 |
| Monetization Potential | 7.5 |

## Key Findings

### 1. Time tracking integration is essential
Most personas (6/8) emphasized that invoicing without automatic time tracking
integration would be a dealbreaker. "I already track my time in Toggl -- if
this doesn't sync, I'm not switching." -- Sarah, Freelance Designer

### 2. Cash flow prediction is the real differentiator
The 90-day cash flow prediction feature generated the most excitement across
personas. "That's the killer feature -- I never know if I can afford to take
time off next month." -- Marcus, Independent Consultant

### 3. Pricing sensitivity varies by segment
Solo freelancers showed price sensitivity at $20+/month, while small agencies
were comfortable up to $50/month per seat.

### 4. Trust is a barrier for financial tools
Several personas expressed concern about connecting bank accounts or financial
data. "I'd need to see serious security credentials." -- David, Cautious Adopter

### 5. Mobile access is expected, not optional
All personas assumed mobile access would be available, treating it as table
stakes rather than a feature.

## Audience Segmentation

**Most promising:** Freelance designers and consultants billing hourly (high pain, clear WTP).

**Least promising:** Agency owners with existing accounting systems (switching costs too high).

## Risks and Concerns

- Competitive pressure from FreshBooks and Wave adding similar features
- Cash flow prediction accuracy could erode trust if wrong
- Integration complexity with dozens of time-tracking and banking tools

## Recommendations

1. Build Toggl and Harvest integrations before launch
2. Start with freelancers billing hourly -- clearest pain point and fastest feedback loop
3. Offer a free tier with limited invoices to reduce adoption barrier
4. Partner with freelancer communities for initial distribution

## Appendix: Interview Transcripts

### P1: Sarah Chen (Enthusiastic)
Freelance UI designer, age 29.

**Q: Walk me through how you currently handle invoicing.**
A: I track my hours in Toggl, then at the end of each month I manually copy everything into a Google Sheets template. Then I export it as a PDF and email it. It takes about 3 hours every month and I always dread it.

**Q: What's your initial reaction to InvoiceFlow?**
A: Oh, automatic invoices from time tracking? That's exactly what I need. I spend 3 hours a month on invoicing that could be automated.

**Q: Which features interest you most?**
A: The Toggl integration is make-or-break. If it pulls my time entries automatically, I'm sold. The cash flow prediction is a nice bonus -- I never know if I can afford to take a week off.

**Q: What concerns do you have?**
A: Honestly, I've tried apps that promise Toggl integration and it's always buggy. I'd need to see it actually work reliably before I commit.

**Q: What would you pay for this?**
A: I'd pay $15/month easily. That's less than one hour of my billing rate, and it saves me three hours.

**Q: What would need to be true for you to switch?**
A: Reliable Toggl sync, professional-looking invoice templates, and the ability to send directly from the app. If I still have to export PDFs, what's the point?

**Q: Overall, would you recommend this?**
A: Absolutely. This is solving a real pain point. Just make sure the integrations actually work.

Sentiment: positive. Would adopt: yes.
Key quotes: "I spend 3 hours a month on invoicing that could be automated." "The Toggl integration is make-or-break."

### P2: Marcus Johnson (Neutral)
Independent consultant, age 42.

**Q: How do you handle invoicing today?**
A: Excel spreadsheet I've been using for 8 years. It's ugly but it works. I know exactly where everything is.

**Q: What's your reaction to InvoiceFlow?**
A: Interesting concept. The cash flow prediction catches my eye -- I've been burned by feast-and-famine cycles. But I'm wary of switching from something that works.

**Q: What features matter most to you?**
A: The 90-day cash flow prediction. If it's accurate, that alone might be worth it. I've tried forecasting in Excel and it's painful.

**Q: What concerns do you have?**
A: Accuracy. If the prediction says I'm fine and I'm not, that's worse than no prediction at all. Show me it works for 3 months and I'm in.

**Q: What would you pay?**
A: Maybe $25/month if the predictions are accurate. But I'd need a free trial long enough to validate the forecasting.

**Q: What would make you switch from Excel?**
A: Prove the cash flow prediction works. That's the only thing my spreadsheet can't do well.

Sentiment: mixed. Would adopt: unclear.
Key quotes: "Show me it works for 3 months and I'm in."

### P3: David Park (Skeptic)
Freelance developer, age 35.

**Q: How do you invoice clients currently?**
A: Google Sheets. Simple template, takes me 20 minutes a month. Not broken.

**Q: What do you think of InvoiceFlow?**
A: Another invoicing SaaS? I've tried FreshBooks, Wave, Bonsai, and HoneyBook. Always come back to my spreadsheet. They all add complexity I don't need.

**Q: Is there anything here that interests you?**
A: The cash flow prediction is mildly interesting but I don't trust an algorithm to predict my pipeline. My income depends on landing contracts, not forecasting.

**Q: What would change your mind?**
A: Honestly, probably nothing. I've tried 4 invoicing apps and always come back to my spreadsheet. The switching cost isn't worth it for the marginal benefit.

**Q: Would you pay for this?**
A: No. Free tools do what I need. I'm not paying $15/month to save 20 minutes.

**Q: Any final thoughts?**
A: Build for people who actually have invoicing pain. Solo devs with 3-4 clients don't. Target agencies or people with complex billing.

Sentiment: negative. Would adopt: no.
Key quotes: "I've tried 4 invoicing apps and always come back to my spreadsheet."

### P4: Lisa Morgan (Enthusiastic)
Small agency owner, age 38. Manages 5 designers.

**Q: How does your agency handle invoicing?**
A: It's a mess. Each designer tracks time differently. I consolidate in QuickBooks but it takes my office manager a full day each month.

**Q: What's your reaction to InvoiceFlow?**
A: If this handles all my contractors too, it's worth $50/month easy. The consolidation problem is what kills us.

**Q: Which features matter most?**
A: Multi-user support and consolidated reporting. I need to see all 5 designers' billable hours in one place.

**Q: Concerns?**
A: Does it handle different billing rates per designer per client? That's where QuickBooks actually works okay.

**Q: What would you pay?**
A: $50/month for the whole team. Maybe more if it replaces QuickBooks entirely.

**Q: What would make you switch?**
A: A proper multi-user setup where each designer logs time and I see everything. If it's single-user only, it's useless to me.

Sentiment: positive. Would adopt: yes.
Key quotes: "If this handles all my contractors too, it's worth $50/month easy."

### P5: Tom Williams (Neutral)
Part-time freelancer, age 26.

**Q: How do you invoice currently?**
A: I use Wave -- it's free. I only invoice 2-3 clients a month so it's fine.

**Q: What do you think of InvoiceFlow?**
A: Seems cool but I'm not sure I need it. Wave does the basics and costs nothing.

**Q: Anything here that appeals to you?**
A: The cash flow prediction would be nice since I'm part-time and my income is unpredictable. But is it worth paying for?

**Q: What would you pay?**
A: Honestly, maybe $5/month max. I only invoice 2-3 clients a month, so free tools work okay for now.

**Q: What would make you switch from Wave?**
A: If InvoiceFlow had a free tier that did basic invoicing plus the cash flow prediction, I'd try it. But I'm not paying for invoicing when free options exist.

Sentiment: mixed. Would adopt: unclear.
Key quotes: "I only invoice 2-3 clients a month, so free tools work okay for now."

### P6: Rachel Kim (Enthusiastic)
Freelance brand strategist, age 33.

**Q: What do you use for invoicing?**
A: FreshBooks. I've been on it for 3 years but I'm increasingly frustrated.

**Q: What's wrong with FreshBooks?**
A: FreshBooks keeps raising prices and the UX has gotten worse. They added a bunch of accounting features I don't need and buried the simple invoicing.

**Q: What's your reaction to InvoiceFlow?**
A: Very interested. If it does invoicing well without trying to be QuickBooks, that's what I want.

**Q: What features matter most?**
A: Clean invoice templates, automatic time tracking integration, and the cash flow prediction. Keep it focused.

**Q: What would you pay?**
A: I'm paying $22/month for FreshBooks now. I'd pay the same or slightly more for something better.

**Q: What would make you switch?**
A: An import tool for my FreshBooks data so I don't lose history. And better templates than what FreshBooks offers.

Sentiment: positive. Would adopt: yes.
Key quotes: "FreshBooks keeps raising prices and the UX has gotten worse."

### P7: James O'Brien (Neutral)
Freelance photographer, age 45. Low tech savviness.

**Q: How do you handle invoicing?**
A: My wife does it in Word. She types up each invoice manually. It works but she complains about it.

**Q: What do you think of InvoiceFlow?**
A: If it's simpler than what I use now, maybe. But I'm not great with technology and I don't want to learn a complicated system.

**Q: What features would help you?**
A: Something dead simple. I photograph a wedding, I type in the amount, it sends the invoice. That's it.

**Q: What concerns do you have?**
A: That it'll be one of those apps with a million settings and I'll never figure it out. My wife would need to use it too.

**Q: What would you pay?**
A: $10/month if it genuinely saves my wife an hour each week. But I'd need someone to set it up for me.

**Q: Would you recommend this?**
A: If it's truly simple, yes. If it looks like accounting software, no.

Sentiment: mixed. Would adopt: unclear.
Key quotes: "If it's simpler than what I use now, maybe."

### P8: Aisha Patel (Skeptic)
Design agency CFO, age 40. Already has accounting systems.

**Q: How does your agency handle invoicing?**
A: Xero. Fully integrated with our bank, payroll, and expense tracking. We have a bookkeeper who manages it.

**Q: What's your reaction to InvoiceFlow?**
A: We use Xero and it does everything we need. I don't see why I'd add another tool.

**Q: Is the cash flow prediction interesting?**
A: Xero already has cash flow forecasting. It's not perfect but it's integrated with our actual bank data.

**Q: What would make you consider switching?**
A: Nothing, honestly. The switching cost is enormous -- all our financial history, bank connections, tax integrations. No invoicing tool is worth that disruption.

**Q: Any advice for the team building this?**
A: Don't try to compete with Xero or QuickBooks for agencies. Target solo freelancers who don't have accounting systems yet. That's where the pain is.

Sentiment: negative. Would adopt: no.
Key quotes: "We use Xero and it does everything we need."
"""
