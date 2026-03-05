#!/usr/bin/env python3
"""Convert an Early Feedback markdown report to a styled, navigable HTML file."""

import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Install markdown: pip install markdown")
    sys.exit(1)


def extract_score_info(md_text):
    """Extract overall score and dimension scores from markdown."""
    overall = re.search(r"##\s+Overall Score:\s*([\d.]+)\s*/\s*10", md_text)
    overall_score = float(overall.group(1)) if overall else None

    verdict = re.search(r"\*\*Verdict:\s*(.+?)\*\*", md_text)
    verdict_text = verdict.group(1) if verdict else ""

    dimensions = []
    for m in re.finditer(
        r"\|\s*(.+?)\s*\|\s*(\d+(?:\.\d+)?)\s*\|\s*(.+?)\s*\|", md_text
    ):
        name, score, assessment = m.group(1).strip(), m.group(2), m.group(3).strip()
        if name.lower() not in ("dimension", "---", ""):
            dimensions.append((name, float(score), assessment))

    return overall_score, verdict_text, dimensions


def score_color(score):
    """Return CSS color class for a score value."""
    if score >= 7.5:
        return "score-strong"
    elif score >= 5.5:
        return "score-solid"
    elif score >= 3.5:
        return "score-moderate"
    else:
        return "score-weak"


def build_toc(md_text):
    """Extract h2/h3 headers for navigation."""
    toc = []
    for m in re.finditer(r"^(#{2,3})\s+(.+)$", md_text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"[\s]+", "-", slug).strip("-")
        toc.append((level, title, slug))
    return toc


def inject_heading_ids(html):
    """Add id attributes to h2/h3 tags for anchor navigation."""
    def add_id(match):
        tag = match.group(1)
        content = match.group(2)
        slug = re.sub(r"[^\w\s-]", "", content.lower())
        slug = re.sub(r"<[^>]+>", "", slug)
        slug = re.sub(r"[\s]+", "-", slug).strip("-")
        return f"<{tag} id=\"{slug}\">{content}</{tag}>"

    return re.sub(r"<(h[23])>(.+?)</\1>", add_id, html)


def make_transcripts_collapsible(html):
    """Wrap interview transcript sections in collapsible details elements."""
    parts = re.split(r"(<h[23][^>]*>)", html)
    result = []
    in_appendix = False
    in_persona = False

    for i, part in enumerate(parts):
        if re.search(r"id=[\"'].*appendix", part, re.IGNORECASE):
            in_appendix = True
            if in_persona:
                result.append("</div></details>")
                in_persona = False
            result.append(part)
            continue

        if in_appendix and re.match(r"<h3", part):
            next_content = parts[i + 1] if i + 1 < len(parts) else ""

            # Only wrap persona transcripts (P1:, P2:, ...) and follow-ups
            is_transcript = re.search(
                r"[PE]\d+:|[Ff]ollow-up", next_content
            )

            if not is_transcript:
                # Non-transcript h3 — close any open details, render normally
                if in_persona:
                    result.append("</div></details>")
                    in_persona = False
                result.append(part)
                continue

            if in_persona:
                result.append("</div></details>")

            # Split at </h3> — heading goes in summary, rest in body
            h3_close = next_content.find("</h3>")
            if h3_close >= 0:
                heading_text = next_content[: h3_close + 5]
                body_text = next_content[h3_close + 5 :]
            else:
                heading_text = next_content
                body_text = ""

            result.append(
                f'<details class="transcript"><summary>{part}{heading_text}</summary>'
                f'<div class="transcript-body">{body_text}'
            )
            in_persona = True
            # skip the next content part since we consumed it
            if i + 1 < len(parts):
                parts[i + 1] = ""
            continue

        if in_persona:
            if re.match(r"<h[12]", part):
                result.append("</div></details>")
                in_persona = False
                result.append(part)
            else:
                result.append(part)
        else:
            result.append(part)

    if in_persona:
        result.append("</div></details>")

    return "".join(result)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg: #fafaf9;
  --fg: #1c1917;
  --muted: #78716c;
  --border: #e7e5e4;
  --accent: #2563eb;
  --surface: #ffffff;
  --strong-bg: #ecfdf5; --strong-fg: #065f46;
  --solid-bg: #eff6ff; --solid-fg: #1e40af;
  --moderate-bg: #fefce8; --moderate-fg: #854d0e;
  --weak-bg: #fef2f2; --weak-fg: #991b1b;
  --sidebar-w: 260px;
  --max-w: 780px;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #1c1917; --fg: #e7e5e4; --muted: #a8a29e;
    --border: #44403c; --surface: #292524; --accent: #60a5fa;
    --strong-bg: #064e3b; --strong-fg: #6ee7b7;
    --solid-bg: #1e3a5f; --solid-fg: #93c5fd;
    --moderate-bg: #713f12; --moderate-fg: #fde68a;
    --weak-bg: #7f1d1d; --weak-fg: #fca5a5;
  }}
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg); color: var(--fg);
  line-height: 1.65; font-size: 15px;
}}
nav {{
  position: fixed; top: 0; left: 0;
  width: var(--sidebar-w); height: 100vh;
  overflow-y: auto; padding: 24px 16px;
  background: var(--surface); border-right: 1px solid var(--border);
  font-size: 13px; z-index: 10;
}}
nav .nav-title {{ font-weight: 700; font-size: 14px; margin-bottom: 16px; color: var(--fg); }}
nav a {{
  display: block; padding: 4px 8px; margin: 2px 0;
  color: var(--muted); text-decoration: none; border-radius: 4px;
  transition: background 0.15s, color 0.15s;
}}
nav a:hover {{ background: var(--border); color: var(--fg); }}
nav a.active {{ color: var(--accent); font-weight: 600; }}
nav a.level-3 {{ padding-left: 20px; font-size: 12px; }}
main {{
  margin-left: var(--sidebar-w); padding: 40px 48px;
  max-width: calc(var(--max-w) + 96px);
}}
h1 {{ font-size: 28px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.02em; }}
h2 {{ font-size: 22px; font-weight: 700; margin: 40px 0 16px; padding-top: 24px; border-top: 1px solid var(--border); }}
h3 {{ font-size: 17px; font-weight: 600; margin: 28px 0 12px; }}
p {{ margin: 12px 0; }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 32px 0; }}
a {{ color: var(--accent); }}
strong {{ font-weight: 600; }}
blockquote {{
  border-left: 3px solid var(--accent); padding: 8px 16px;
  margin: 16px 0; color: var(--muted); font-style: italic;
  background: var(--surface); border-radius: 0 6px 6px 0;
}}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
th {{ text-align: left; font-weight: 600; padding: 10px 12px; border-bottom: 2px solid var(--border); }}
td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }}
tr:hover {{ background: var(--surface); }}
code {{ font-family: 'SF Mono', Consolas, monospace; font-size: 13px; background: var(--surface); padding: 2px 5px; border-radius: 3px; }}
pre {{ background: var(--surface); padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0; }}
pre code {{ background: none; padding: 0; }}
ol, ul {{ margin: 12px 0; padding-left: 24px; }}
li {{ margin: 6px 0; }}
.score-badge {{
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 32px; font-weight: 800; margin: 8px 0 4px;
  letter-spacing: -0.03em;
}}
.score-badge .out-of {{ font-size: 18px; font-weight: 400; color: var(--muted); }}
.score-strong {{ color: var(--strong-fg); }}
.score-solid {{ color: var(--solid-fg); }}
.score-moderate {{ color: var(--moderate-fg); }}
.score-weak {{ color: var(--weak-fg); }}
.verdict {{
  display: inline-block; padding: 4px 12px; border-radius: 20px;
  font-size: 13px; font-weight: 600; margin: 4px 0 16px;
}}
.verdict.score-strong {{ background: var(--strong-bg); }}
.verdict.score-solid {{ background: var(--solid-bg); }}
.verdict.score-moderate {{ background: var(--moderate-bg); }}
.verdict.score-weak {{ background: var(--weak-bg); }}
.dim-score {{
  display: inline-block; width: 32px; height: 32px; line-height: 32px;
  text-align: center; border-radius: 6px; font-weight: 700; font-size: 14px;
  margin-right: 4px;
}}
.dim-score.score-strong {{ background: var(--strong-bg); color: var(--strong-fg); }}
.dim-score.score-solid {{ background: var(--solid-bg); color: var(--solid-fg); }}
.dim-score.score-moderate {{ background: var(--moderate-bg); color: var(--moderate-fg); }}
.dim-score.score-weak {{ background: var(--weak-bg); color: var(--weak-fg); }}
details.transcript {{
  margin: 12px 0; border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden;
}}
details.transcript summary {{
  padding: 12px 16px; cursor: pointer; background: var(--surface);
  font-weight: 600; list-style: none;
}}
details.transcript summary::-webkit-details-marker {{ display: none; }}
details.transcript summary::before {{
  content: '+'; display: inline-block; width: 20px;
  font-weight: 400; color: var(--muted); font-size: 16px;
}}
details.transcript[open] summary::before {{ content: '-'; }}
details.transcript summary h3 {{
  display: inline; margin: 0; font-size: 15px;
}}
details.transcript .transcript-body {{ padding: 16px; }}
.meta {{ color: var(--muted); font-size: 13px; margin-bottom: 24px; }}
@media (max-width: 900px) {{
  nav {{ display: none; }}
  main {{ margin-left: 0; padding: 24px 20px; }}
}}
</style>
</head>
<body>
<nav>
  <div class="nav-title">{nav_title}</div>
  {toc_html}
</nav>
<main>
{body}
</main>
<script>
// Highlight active nav link on scroll
const headings = document.querySelectorAll('h2[id], h3[id]');
const links = document.querySelectorAll('nav a');
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{
    if (e.isIntersecting) {{
      links.forEach(l => l.classList.remove('active'));
      const active = document.querySelector(`nav a[href="#${{e.target.id}}"]`);
      if (active) active.classList.add('active');
    }}
  }});
}}, {{ rootMargin: '-20% 0px -70% 0px' }});
headings.forEach(h => observer.observe(h));
</script>
</body>
</html>"""


def render(md_path):
    md_text = Path(md_path).read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(md_path).stem

    overall_score, verdict_text, dimensions = extract_score_info(md_text)

    # Convert markdown to HTML
    md_converter = markdown.Markdown(extensions=["tables", "fenced_code"])
    body_html = md_converter.convert(md_text)

    # Inject heading IDs for navigation
    body_html = inject_heading_ids(body_html)

    # Enhance score display
    if overall_score is not None:
        color = score_color(overall_score)
        score_html = (
            f'<div class="score-badge {color}">{overall_score}'
            f' <span class="out-of">/ 10</span></div>'
            f'<div class="verdict {color}">{verdict_text}</div>'
        )
        body_html = re.sub(
            r"<h2[^>]*>Overall Score.*?</h2>\s*<p><strong>Verdict:.*?</strong></p>",
            f'<h2 id="overall-score">Overall Score</h2>{score_html}',
            body_html,
            flags=re.DOTALL,
        )

    # Color-code dimension scores in tables
    for name, score, _ in dimensions:
        color = score_color(score)
        score_str = str(int(score)) if score == int(score) else str(score)
        body_html = body_html.replace(
            f"<td>{score_str}</td>",
            f'<td><span class="dim-score {color}">{score_str}</span></td>',
            1,
        )

    # Make interview transcripts collapsible
    body_html = make_transcripts_collapsible(body_html)

    # Build TOC
    toc = build_toc(md_text)
    toc_items = []
    for level, t, slug in toc:
        cls = "level-3" if level == 3 else ""
        toc_items.append(f'<a href="#{slug}" class="{cls}">{t}</a>')
    toc_html = "\n  ".join(toc_items)

    nav_title = re.sub(r"\s*[-—].*", "", title).strip()

    html = HTML_TEMPLATE.format(
        title=title,
        nav_title=nav_title,
        toc_html=toc_html,
        body=body_html,
    )

    out_path = Path(md_path).with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    print(f"Rendered: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_report.py <report.md>")
        print("       python render_report.py outputs/*.md")
        sys.exit(1)

    for path in sys.argv[1:]:
        render(path)
