<p align="center"><strong>Simulated Innovation</strong></p>

<h3 align="center">Brutally honest startup evaluation. 8 synthetic personas. 3 domain experts. No sugar-coating.</h3>

<p align="center">
Feed it a pitch deck, a README, or a one-liner. It interviews 8 synthetic users, assembles a domain expert panel, and produces a scored evaluation report that tells you what's actually wrong — not what you want to hear.
</p>

---

## Demo: Real Evaluation Output

An organizational cognition platform was evaluated. Here's what came back:

**Score: 6.4/10 — "Promising but needs refinement"**

```
| Dimension              | Score |
|------------------------|-------|
| Problem Validity       | 8.5   |
| Solution Fit           | 5.5   |
| Market Demand          | 8.0   |
| Competitive Position   | 8.5   |
| Monetization Potential | 7.5   |
| Execution Feasibility  | 3.0   |  ← product-specific critical dimension
```

The standard 5 dimensions averaged 7.6 — the strategic logic is genuinely strong. But the tool identified **execution feasibility** as the critical dimension for this specific product and scored it 3.0, bringing the honest overall to 6.4.

**Organic persona sentiment** (not forced):

```
3 enthusiastic · 3 neutral · 2 skeptic
```

Both enthusiastic enterprise buyers conditioned their interest on seeing a team and funding: *"We don't buy critical infrastructure from one-person companies."*

**Expert disagreement surfaced real tension:**

> Dr. Webb (systems architect): "Build the coordination layer first — prove multi-role workflows beat single-agent before optimizing cost."
>
> Priya Chandrasekaran (GTM strategist): "Find a paying customer first and build backward from their pain. The coordination layer in the abstract is a research project."

**The viability gate didn't trigger** — 3 enthusiasts prevented early termination — but the report led with execution risk in the executive summary.

<details>
<summary><strong>Sample persona interview excerpt</strong></summary>

> **Q: What's your experience with multi-agent AI systems today?**
>
> A: We tried CrewAI for our data pipeline — had a "data engineer" agent, a "data analyst" agent, and a "reporter" agent. In production, the agents would hallucinate context about each other's work. The data analyst would reference tables the data engineer hadn't actually created. There's no real shared state — it's just prompt-passing with role labels. We scrapped it after 3 months.
>
> — Raj Patel, Head of AI/ML, growth-stage fintech (Enthusiastic)

> **Q: What's your reaction to an organizational cognition layer for AI agents?**
>
> A: The concept is academically interesting but I've heard this pitch before with different branding. "Shared context across agents" — that's what MCP claims to do. What specifically does organizational cognition provide that these don't?
>
> — Sarah Okonkwo, Enterprise Architect, Fortune 500 (Skeptic)

</details>

<details>
<summary><strong>Full sample report</strong></summary>

See [outputs/2026-03-04-flux-organizational-cognition.md](outputs/2026-03-04-flux-organizational-cognition.md) for the complete 600+ line evaluation with all 8 persona transcripts, 3 expert assessments, 6 follow-up exchanges, and scored recommendations.

</details>

---

## What Makes This Different

Most AI evaluation tools produce encouraging summaries. This one is designed to be **adversarial by default**:

- **Organic sentiment** — personas react honestly. A terrible idea gets mostly skeptics. No forced "2 enthusiasts, 3 neutral" distribution.
- **Viability gate** — if interviews reveal universal rejection, the tool produces a short critical-issues report and stops. No 5,000-word report for a dead idea.
- **Experts must disagree** — where their domains conflict (e.g., product-first vs. sales-first), the tension is preserved, not smoothed over.
- **Information gaps flagged** — missing info is called out as gaps, not filled with optimistic assumptions.
- **Full scoring scale** — scores of 2 or 9 are valid when evidence supports them. No gravitating to the safe 5-7 range.
- **Product-specific critical dimensions** — the tool identifies the 1-2 dimensions that matter most for *this specific product* and calls them out.

---

## Quick Start

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with an active subscription.

```bash
git clone https://github.com/bweller-lgtm/SimulatedInnovation
cd SimulatedInnovation
```

Then in Claude Code:

```
# Evaluate from a pitch deck
/evaluate pitch-deck.pdf

# Evaluate an entire project folder
/evaluate ../my-startup/

# Evaluate an idea directly
/evaluate A marketplace for freelance data scientists with built-in project scoping and escrow

# With optional features
/evaluate --web-search --deep ../my-startup/
/evaluate --experts 5 --personas 10 pitch-deck.pdf
```

That's it. No API keys, no dependencies, no setup.

---

## What You Get

| Output | File | When |
|---|---|---|
| **Evaluation report** | `outputs/YYYY-MM-DD-product-name.md` | Always |
| **Critical issues report** | `outputs/YYYY-MM-DD-product-name-critical.md` | If the idea fails the viability gate |
| **Deep research report** | `outputs/YYYY-MM-DD-product-name-deep-research.md` | With `--deep` flag |

Each evaluation report includes:

1. **Executive Summary** — leads with the most important truth, positive or negative
2. **Scored Breakdown** — 5 standard dimensions + product-specific dimensions, full 1-10 scale
3. **Key Findings** — top 5, each with supporting quotes from interviews
4. **Expert Assessments** — domain expert syntheses including where they disagree
5. **Audience Segmentation** — who this is for and who it isn't
6. **Risks and Concerns** — including information gaps from the input
7. **Recommendations** — prioritized, actionable
8. **Full Interview Transcripts** — every Q&A exchange for all personas + expert follow-ups

---

## Input Modes

| Mode | Example | What happens |
|---|---|---|
| **Inline text** | `/evaluate An app that...` | Evaluates the description directly |
| **Single file** | `/evaluate idea.txt` | Reads and evaluates (supports `.pdf`, `.docx`, `.pptx`, `.xlsx`, code files, etc.) |
| **Directory** | `/evaluate ./my-project/` | Reads all project files and synthesizes the idea from everything found |

Directory mode reads: `.md`, `.txt`, `.py`, `.js`, `.ts`, `.tsx`, `.json`, `.yaml`, `.toml`, `.html`, `.css`, `.pdf`, `.docx`, `.pptx`, `.xlsx` — and skips `node_modules/`, `.git/`, and build directories.

---

## Flags

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

---

## Configuration

Create an optional `evaluate.config.yaml` for persistent settings:

```yaml
experts:
  count: 4
  custom:
    - name: "Dan Hockenmeier"
      domain: "Marketplace strategy & network effects"
      credentials: "Former VP Growth at Faire"

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

---

## How It Works

<details>
<summary><strong>Up to 9 steps, with conditional branches</strong></summary>

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

## Scoring Framework

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

---

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

187 tests validate: scoring framework, organic persona sentiment, honesty guardrails, adaptive interviews, viability gate, expert panel, configuration support, inline flags, web research, deep reports, external files, and report structure.

Validate any generated report:

```bash
python tests/validate_report.py outputs/2026-03-04-my-product.md
```

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
