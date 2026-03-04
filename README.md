# Simulated Innovation

Evaluate project ideas using synthetic user personas and simulated interviews. Runs as a Claude Code skill -- no API keys, no dependencies, just `/evaluate`.

## Usage

From Claude Code, run:

```
/evaluate A desktop app for freelance designers that automatically generates invoices from time-tracking data and predicts cash flow for 90 days
```

Or from a file:

```
/evaluate idea.txt
```

## How It Works

The `/evaluate` skill walks through 5 steps in a single conversation:

1. **Parse Context** -- Extracts structured product information from your idea
2. **Generate Personas** -- Creates 8 diverse synthetic users (2 skeptics, 3 neutral, 3 enthusiastic)
3. **Simulate Interviews** -- Conducts realistic interviews covering workflow, reactions, pricing, and switching intent
4. **Analyze Feedback** -- Identifies themes, pain points, adoption barriers, and willingness-to-pay signals
5. **Generate Report** -- Produces a scored evaluation (1-10 on 5 dimensions) with actionable recommendations

Reports are saved to `outputs/` as Markdown files.

## Scoring

| Dimension | What It Measures |
|---|---|
| Problem Validity | Is this a real, painful problem? |
| Solution Fit | Does the solution actually address it? |
| Market Demand | Is there enough demand for a business? |
| Competitive Position | Can it win against alternatives? |
| Monetization Potential | Can it make money? |

**Verdicts:** 7.5+ strong opportunity, 5.5-7.4 promising, 3.5-5.4 concerns, <3.5 reconsider.

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

Tests validate that the skill file contains all required methodology and that generated reports meet the expected format.
