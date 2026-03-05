# Simulated Innovation

A Claude Code skill that evaluates startup and product ideas using synthetic user personas, simulated interviews, and a subject matter expert panel. Honesty-first: personas react authentically, experts disagree where their domains conflict, and bad ideas get harsh verdicts. No API keys, no dependencies -- just `/evaluate`.

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

# With flags
/evaluate --web-search --deep A marketplace for freelance data scientists
/evaluate --experts 5 --personas 10 pitch-deck.pdf
/evaluate --no-experts quick-idea.txt
/evaluate --full terrible-idea.txt
/evaluate --config custom.yaml ./my-project/
```

### Input Modes

| Mode | Example | What happens |
|---|---|---|
| Inline text | `/evaluate An app that...` | Evaluates the description directly |
| Single file | `/evaluate idea.txt` | Reads the file and evaluates its contents |
| Directory | `/evaluate ./my-project/` | Reads all project files (code, docs, configs, PDFs, Office files) and synthesizes the idea from everything found |

Directory mode supports: `.md`, `.txt`, `.py`, `.js`, `.ts`, `.tsx`, `.json`, `.yaml`, `.toml`, `.html`, `.css`, `.pdf`, `.docx`, `.pptx`, `.xlsx` -- and automatically skips `node_modules/`, `.git/`, and other dependency directories.

### Flags

| Flag | Description |
|---|---|
| `--experts N` | Set expert count (1-5, default 3) |
| `--personas N` | Set persona count (4-12, default 8) |
| `--deep` | Generate deep research report (market sizing, competitive analysis, GTM playbook) |
| `--web-search` | Enable web research step (competitor data, market trends, real user complaints) |
| `--no-experts` | Skip expert panel entirely (faster, persona-only evaluation) |
| `--full` | Force full pipeline even if the viability gate triggers early termination |
| `--questions path` | Load custom interview questions from a file |
| `--config path` | Use alternate config file |

Flags override config file values.

## How It Works

The `/evaluate` skill walks through up to 9 steps in a single conversation:

1. **Parse Context** -- Extracts structured product information. Flags information gaps instead of making optimistic assumptions.
2. **Web Research** *(conditional)* -- Searches for real competitor data, market sizing, user complaints, and regulatory landscape.
3. **Generate Personas** -- Creates diverse synthetic users (configurable count, default 8) with organic sentiment -- their reaction to the product emerges from who they are and whether the idea genuinely solves their problems, not a forced distribution.
4. **Simulate Interviews** -- Conducts full Q&A interviews (6-7 core exchanges + product-type-specific questions) with balanced behavioral rules: skeptics acknowledge strengths, enthusiasts voice real concerns.
5. **Viability Gate** -- If interviews reveal universal rejection, produces a short critical-issues report and stops (unless `--full` forces the complete pipeline).
6. **Expert Panel Review** -- Domain experts (configurable count, default 3) review interviews, critique questions, and suggest targeted follow-ups. Experts are encouraged to disagree where their domains conflict.
7. **Follow-up Interviews** -- Expert-suggested questions posed to specific personas for deeper responses.
8. **Expert Synthesis + Analysis** -- Each expert writes their assessment; combined with theme analysis, pain point ranking, and willingness-to-pay signals. Scores use the full 1-10 scale, not clustered in the safe middle.
9. **Generate Report** -- Produces a scored evaluation with blunt verdicts, expert assessments, product-specific critical dimensions, and actionable recommendations.

An optional **Deep Research Report** (Step 9+) adds market sizing, competitive landscape analysis, regulatory review, technical feasibility, GTM playbook, and key experiments.

## Configuration

Create an optional `evaluate.config.yaml` in your project directory:

```yaml
experts:
  count: 4
  custom:
    - name: "Dan Hockenmeier"
      domain: "Marketplace strategy & network effects"
      credentials: "Former VP Growth at Faire, marketplace advisor"

personas:
  count: 10
  must_include:
    - "enterprise buyer at Fortune 500"
    - "budget-conscious freelancer"

required_questions:
  - "How does this compare to your current Salesforce workflow?"
  - "What would your legal/compliance team say about this?"

web_research: true
deep_report: false

scoring:
  additional_dimensions:
    - name: "Regulatory Risk"
      strong: "Clear regulatory path"
      moderate: "Some ambiguity"
      weak: "Major regulatory barriers"
```

All settings are optional. The skill works perfectly without a config file.

### External Files

Place these optional files in your working directory for additional customization:

| File | Purpose |
|---|---|
| `experts.md` | Detailed expert profiles (overrides auto-selection) |
| `questions.md` | Custom interview questions (added to every interview) |
| `context.md` | Additional market context (appended to idea description) |

## Scoring Framework

Five standard dimensions, each scored 1-10 (plus optional custom dimensions from config):

| Dimension | 8+ (Strong) | 6-7 (Solid) | 4-5 (Moderate) | <4 (Weak) |
|---|---|---|---|---|
| Problem Validity | Universal pain | Clear pain, limited scope | Nice-to-have | Solution looking for problem |
| Solution Fit | Elegant fit | Good fit, gaps remain | Partial | Mismatch |
| Market Demand | Large eager market | Mid-size or growing | Niche | Too small or shrinking |
| Competitive Position | Clear differentiation | Differentiated but contested | Crowded but viable | Dominated |
| Monetization Potential | Clear willingness to pay | Some WTP signals | Uncertain pricing | Hard to monetize |

The report also identifies the 1-2 dimensions most critical for the specific product being evaluated.

### Verdicts

| Overall Score | Verdict |
|---|---|
| 7.5+ | Strong opportunity -- pursue with confidence |
| 5.5 - 7.4 | Promising but needs refinement |
| 3.5 - 5.4 | Significant concerns -- pivot or validate further |
| < 3.5 | Reconsider fundamentally |

## Output

Reports are saved as Markdown files in `outputs/`:

- **Evaluation report**: `YYYY-MM-DD-product-name.md`
- **Critical issues report**: `YYYY-MM-DD-product-name-critical.md` (if viability gate triggers)
- **Deep research report**: `YYYY-MM-DD-product-name-deep-research.md` (if `--deep` enabled)

Each evaluation report includes:

1. Executive Summary (leads with the most important truth, positive or negative)
2. Overall Score with dimension breakdown table
3. Key Findings (top 5 with supporting evidence and quotes)
4. Expert Assessments (domain expert syntheses with recommendations, including disagreements)
5. Audience Segmentation
6. Risks and Concerns (including information gaps)
7. Prioritized Recommendations
8. Appendix with full interview transcripts (initial Q&A + expert follow-up questions for all personas)

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

177 tests validate that the skill file contains all required methodology (scoring framework, organic persona sentiment, honesty guardrails, adaptive interviews, viability gate, expert panel, configuration support, report structure) and that generated reports meet the expected format.

You can also validate any generated report directly:

```bash
python tests/validate_report.py outputs/2026-03-04-my-product.md
```

## Project Structure

```
.claude/commands/evaluate.md   # The skill -- all evaluation methodology
tests/
  test_skill_content.py        # Validates skill has complete methodology (148 tests)
  test_report_format.py        # Validates generated report structure (29 tests)
  validate_report.py           # Standalone CLI report validator
  conftest.py                  # Shared fixtures and sample report
outputs/                       # Generated evaluation reports
evaluate.config.yaml           # Optional configuration (not committed)
experts.md                     # Optional custom expert profiles (not committed)
questions.md                   # Optional custom questions (not committed)
context.md                     # Optional additional context (not committed)
```
