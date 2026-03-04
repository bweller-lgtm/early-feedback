# Simulated Innovation

Evaluate project ideas using synthetic user personas and simulated interviews. Takes a product idea as input and produces a structured evaluation report with scores, findings, and recommendations.

## Setup

```bash
pip install -e .
cp .env.example .env
# Edit .env with your Anthropic API key
```

## Usage

```bash
# Evaluate an idea directly
python evaluate.py "A desktop app for freelance designers that automatically generates invoices from time-tracking data and predicts cash flow for 90 days"

# From a file
python evaluate.py --file idea.txt

# With options
python evaluate.py "..." --personas 12 --output my-report.md
```

## How It Works

1. **Parse Context** — Extracts structured product information from your idea description
2. **Generate Personas** — Creates diverse synthetic users (skeptics, neutrals, enthusiasts)
3. **Simulate Interviews** — Conducts realistic interviews with each persona (in parallel)
4. **Analyze Feedback** — Identifies themes, pain points, adoption barriers, and WTP signals
5. **Generate Report** — Produces a scored evaluation with actionable recommendations

Reports are saved to `outputs/` as Markdown files.

## Cost

~$0.40-0.60 per evaluation using Claude Sonnet.
