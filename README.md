<p align="center">
  <img src="assets/logo_icon.png" alt="Simulated Innovation" width="200">
</p>

<h1 align="center">Simulated Innovation</h1>

<p align="center"><strong>Brutally honest product evaluation. No sugar-coating.</strong></p>

Feed it a pitch deck, a README, or a one-liner. It interviews synthetic users, assembles a domain expert panel, and produces a scored evaluation report that tells you what's actually wrong — not what you want to hear.

We fed it "a freelancer invoicing tool with cash flow prediction." It came back 6.8/10 and flagged a cold-start problem nobody mentioned — the flagship feature needs 6 months of data to work, which new users don't have.

---

## Demo

<p align="center">
  <img src="assets/demo_scores.png" alt="Scored evaluation with color-coded dimension breakdown" width="720">
</p>

Scored across standard dimensions plus product-specific critical dimensions identified automatically.

<p align="center">
  <img src="assets/demo_interview.png" alt="Full Q&A persona interview transcripts" width="720">
</p>

Full Q&A transcripts — not summaries. Enthusiasts voice concerns. Skeptics acknowledge strengths.

<p align="center">
  <img src="assets/demo_experts.png" alt="Expert panel with independent domain assessments" width="720">
</p>

Independent expert assessments. When their conclusions conflict, the tension is preserved.

---

## What Makes This Different

- **Organic sentiment** — personas react honestly. A terrible idea gets mostly skeptics. No forced distribution.
- **Viability gate** — universal rejection produces a short critical-issues report and stops. No 5,000-word report for a dead idea.
- **Independent experts** — each evaluates through their own lens. Natural conflicts are signal, not noise.
- **Information gaps flagged** — missing info is called out, not filled with optimistic assumptions.
- **Full scoring scale** — scores of 2 or 9 are valid when evidence supports them.
- **Product-specific critical dimensions** — identifies what matters most for *this specific product*.

---

## Quick Start

### Claude Code (full features)

```bash
git clone https://github.com/bweller-lgtm/SimulatedInnovation
cd SimulatedInnovation
```

```
/evaluate A marketplace for freelance data scientists with built-in project scoping and escrow

/evaluate pitch-deck.pdf

/evaluate ../my-startup/

/evaluate --web-search --deep ../my-startup/
```

Handles file/directory scanning, config files, web research, and automatic report saving.

### Claude Desktop / API (core evaluation)

Copy the contents of `evaluate/SKILL.md` (everything after the frontmatter) into any Claude conversation. Replace `$ARGUMENTS` with your idea description. You get the full evaluation pipeline — personas, interviews, expert panel, scored report — without the file I/O features.

---

## What You Can Evaluate

| Input | Example | What happens |
|---|---|---|
| **A one-liner** | `/evaluate An app that...` | Evaluates the description directly |
| **A pitch deck** | `/evaluate pitch-deck.pdf` | Reads the PDF and evaluates |
| **A codebase** | `/evaluate ./my-project/` | Reads all project files and synthesizes the idea |
| **A doc** | `/evaluate idea.docx` | Supports `.pdf`, `.docx`, `.pptx`, `.xlsx`, code files |

Add `--web-search` to research real competitors first. Add `--deep` for a full research report with TAM/SAM, GTM playbook, and experiments to run.

---

## What You Get

| Output | File | When |
|---|---|---|
| **Evaluation report** | `outputs/YYYY-MM-DD-product-name.md` | Always |
| **Critical issues report** | `outputs/YYYY-MM-DD-product-name-critical.md` | If the idea fails the viability gate |
| **Deep research report** | `outputs/YYYY-MM-DD-product-name-deep-research.md` | With `--deep` flag |

Each report includes: Executive Summary, Scored Breakdown, Key Findings with quotes, Expert Assessments, Audience Segmentation, Risks and Concerns, Recommendations, and Full Interview Transcripts.

<details>
<summary><strong>Flags</strong></summary>

| Flag | What it does |
|---|---|
| `--web-search` | Research real competitors, market data, user complaints before generating personas |
| `--deep` | Produce a deep research report (TAM/SAM, competitive landscape, GTM playbook, experiments) |
| `--experts N` | Set expert count (1-5, default 3) |
| `--personas N` | Set persona count (4-12, default 8) |
| `--no-experts` | Skip expert panel (faster, persona-only evaluation) |
| `--full` | Force full pipeline even if viability gate triggers early termination |
| `--questions path` | Load custom interview questions from a file |
| `--config path` | Use alternate config file |

</details>

<details>
<summary><strong>Configuration</strong></summary>

Create an optional `evaluate.config.yaml` for persistent settings:

```yaml
experts:
  count: 4
  custom:
    - name: "Jane Smith"
      domain: "Marketplace strategy & network effects"
      credentials: "Former VP Growth at a top marketplace startup"

personas:
  count: 10
  must_include:
    - "enterprise buyer at Fortune 500"

required_questions:
  - "How does this compare to your current Salesforce workflow?"

web_research: true
deep_report: false

scoring:
  additional_dimensions:
    - name: "Regulatory Risk"
      strong: "Clear regulatory path"
      moderate: "Some ambiguity"
      weak: "Major regulatory barriers"
```

Optional external files (`experts.md`, `questions.md`, `context.md`) provide detailed expert profiles, custom questions, or additional market context.

</details>

<details>
<summary><strong>Scoring Framework</strong></summary>

| Dimension | 8+ (Strong) | 6-7 (Solid) | 4-5 (Moderate) | <4 (Weak) |
|---|---|---|---|---|
| Problem Validity | Universal pain | Clear pain, limited scope | Nice-to-have | Solution looking for problem |
| Solution Fit | Elegant fit | Good fit, gaps remain | Partial | Mismatch |
| Market Demand | Large eager market | Mid-size or growing | Niche | Too small or shrinking |
| Competitive Position | Clear differentiation | Differentiated but contested | Crowded but viable | Dominated |
| Monetization Potential | Clear willingness to pay | Some WTP signals | Uncertain pricing | Hard to monetize |

| Overall Score | Verdict |
|---|---|
| 7.5+ | Strong opportunity — pursue with confidence |
| 5.5 - 7.4 | Promising but needs refinement |
| 3.5 - 5.4 | Significant concerns — pivot or validate further |
| < 3.5 | Reconsider fundamentally |

</details>

<details>
<summary><strong>How It Works (8 steps + conditional branches)</strong></summary>

```
Preamble   Parse flags, load config, load external files
Step 1     Parse product context (flag gaps, don't infer)
Step 1.5   Web research (conditional: --web-search)
Step 2     Generate personas with organic sentiment
Step 3     Simulate interviews (core + product-type-specific questions)
Step 3.5   Viability gate — kill bad ideas early (unless --full)
Step 4     Expert panel review (configurable, skippable)
Step 5     Follow-up interviews from expert questions
Step 6     Expert synthesis + feedback analysis
Step 7     Generate scored report
Step 8     Deep research report (conditional: --deep)
```

</details>

---

## Tests

<details>
<summary><strong>187 tests</strong> — scoring, honesty guardrails, organic sentiment, viability gate, expert panel, configuration, report structure</summary>

```bash
pip install pytest
python -m pytest tests/ -v
```

Validate any generated report:

```bash
python tests/validate_report.py outputs/YYYY-MM-DD-my-product.md
```

</details>

---

## Project Structure

```
evaluate/SKILL.md               # The skill (Agent Skills standard format)
.claude/commands/evaluate.md    # Legacy command (keeps /evaluate working without plugin install)
tests/
  test_skill_content.py         # 158 tests: skill methodology + SKILL.md format validation
  test_report_format.py         # 29 tests: report structure validation
  validate_report.py            # Standalone CLI report validator
  conftest.py                   # Shared fixtures and sample report
outputs/                        # Generated reports (gitignored)
evaluate.config.yaml            # Optional configuration
experts.md / questions.md / context.md  # Optional external files
```
