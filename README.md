# Simulated Innovation

A Claude Code skill that evaluates startup and product ideas using synthetic user personas and simulated interviews. No API keys, no dependencies -- just `/evaluate`.

## Requirements

- [Claude Code](https://claude.com/claude-code) with an active Claude subscription

## Usage

From Claude Code in this project directory, run:

```
# Evaluate an idea directly
/evaluate A desktop app for freelance designers that automatically generates invoices from time-tracking data and predicts cash flow for 90 days

# Evaluate from a file (text, PDF, scripts, Office docs, etc.)
/evaluate pitch-deck.pdf
/evaluate idea.txt
/evaluate prototype.py

# Evaluate an entire project folder
/evaluate ../my-startup/
```

### Input Modes

| Mode | Example | What happens |
|---|---|---|
| Inline text | `/evaluate An app that...` | Evaluates the description directly |
| Single file | `/evaluate idea.txt` | Reads the file and evaluates its contents |
| Directory | `/evaluate ./my-project/` | Reads all project files (code, docs, configs, PDFs, Office files) and synthesizes the idea from everything found |

Directory mode supports: `.md`, `.txt`, `.py`, `.js`, `.ts`, `.tsx`, `.json`, `.yaml`, `.toml`, `.html`, `.css`, `.pdf`, `.docx`, `.pptx`, `.xlsx` -- and automatically skips `node_modules/`, `.git/`, and other dependency directories.

## How It Works

The `/evaluate` skill walks through 5 steps in a single conversation:

1. **Parse Context** -- Extracts structured product information (name, value proposition, target users, competitors, assumptions to test)
2. **Generate Personas** -- Creates 8 diverse synthetic users (2 skeptics, 3 neutral, 3 enthusiastic) with realistic backgrounds, workflows, and pain points
3. **Simulate Interviews** -- Conducts full Q&A interviews (6-7 exchanges each) with each persona covering workflow, reactions, pricing, concerns, and switching intent
4. **Analyze Feedback** -- Identifies recurring themes, ranks pain points, surfaces adoption barriers, and extracts willingness-to-pay signals
5. **Generate Report** -- Produces a scored evaluation with a verdict and actionable recommendations, saved to `outputs/`

## Scoring Framework

Five dimensions, each scored 1-10:

| Dimension | 8+ (Strong) | 4-5 (Moderate) | <3 (Weak) |
|---|---|---|---|
| Problem Validity | Universal pain | Nice-to-have | Solution looking for problem |
| Solution Fit | Elegant fit | Partial | Mismatch |
| Market Demand | Large eager market | Niche | Too small |
| Competitive Position | Clear differentiation | Crowded but viable | Dominated |
| Monetization Potential | Clear willingness to pay | Uncertain pricing | Hard to monetize |

### Verdicts

| Overall Score | Verdict |
|---|---|
| 7.5+ | Strong opportunity -- pursue with confidence |
| 5.5 - 7.4 | Promising but needs refinement |
| 3.5 - 5.4 | Significant concerns -- pivot or validate further |
| < 3.5 | Reconsider fundamentally |

## Output

Reports are saved as Markdown files in `outputs/` with the naming convention `YYYY-MM-DD-product-name.md`. Each report includes:

1. Executive Summary
2. Overall Score with dimension breakdown table
3. Key Findings (top 5 with supporting evidence and quotes)
4. Audience Segmentation
5. Risks and Concerns
6. Prioritized Recommendations
7. Appendix with full interview transcripts (Q&A dialogue for all 8 personas)

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

101 tests validate that the skill file contains all required methodology (scoring framework, persona diversity, interview coverage, report structure) and that generated reports meet the expected format.

You can also validate any generated report directly:

```bash
python tests/validate_report.py outputs/2026-03-04-my-product.md
```

## Project Structure

```
.claude/commands/evaluate.md   # The skill -- all evaluation methodology
tests/
  test_skill_content.py        # Validates skill has complete methodology (76 tests)
  test_report_format.py        # Validates generated report structure (25 tests)
  validate_report.py           # Standalone CLI report validator
  conftest.py                  # Shared fixtures and sample report
outputs/                       # Generated evaluation reports
```
