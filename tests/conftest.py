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

## Appendix: Interview Summaries

### P1: Sarah Chen (Enthusiastic)
Freelance UI designer, age 29. Excited about the cash flow prediction but
needs Toggl integration. Would pay $15/month. Sentiment: positive. Would adopt: yes.
Key quotes: "I spend 3 hours a month on invoicing that could be automated."

### P2: Marcus Johnson (Neutral)
Independent consultant, age 42. Interested but cautious about switching from
Excel. Wants to see accuracy of predictions first. Sentiment: mixed. Would adopt: unclear.
Key quotes: "Show me it works for 3 months and I'm in."

### P3: David Park (Skeptic)
Freelance developer, age 35. Skeptical about another SaaS tool. Uses a
spreadsheet and is "fine with it." Sentiment: negative. Would adopt: no.
Key quotes: "I've tried 4 invoicing apps and always come back to my spreadsheet."

### P4: Lisa Morgan (Enthusiastic)
Small agency owner, age 38. Manages 5 designers. Needs multi-user support.
Sentiment: positive. Would adopt: yes.
Key quotes: "If this handles all my contractors too, it's worth $50/month easy."

### P5: Tom Williams (Neutral)
Part-time freelancer, age 26. Low volume of invoices. Price sensitive.
Sentiment: mixed. Would adopt: unclear.
Key quotes: "I only invoice 2-3 clients a month, so free tools work okay for now."

### P6: Rachel Kim (Enthusiastic)
Freelance brand strategist, age 33. Currently uses FreshBooks but unhappy
with it. Sentiment: positive. Would adopt: yes.
Key quotes: "FreshBooks keeps raising prices and the UX has gotten worse."

### P7: James O'Brien (Neutral)
Freelance photographer, age 45. Low tech savviness. Wants simplicity above
all. Sentiment: mixed. Would adopt: unclear.
Key quotes: "If it's simpler than what I use now, maybe."

### P8: Aisha Patel (Skeptic)
Design agency CFO, age 40. Already has accounting systems in place. Very
skeptical about adding another tool. Sentiment: negative. Would adopt: no.
Key quotes: "We use Xero and it does everything we need."
"""
