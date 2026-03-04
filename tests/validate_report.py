#!/usr/bin/env python3
"""Standalone report validator -- run against any generated report.

Usage:
    python tests/validate_report.py outputs/2026-03-04-invoiceflow.md
    python tests/validate_report.py outputs/*.md
"""

import re
import sys
from pathlib import Path


def extract_overall_score(text: str) -> float | None:
    match = re.search(r"overall\s+score[:\s]*(\d+\.?\d*)\s*/\s*10", text, re.IGNORECASE)
    return float(match.group(1)) if match else None


def extract_dimension_scores(text: str) -> dict[str, float]:
    scores = {}
    for match in re.finditer(r"\|\s*(.+?)\s*\|\s*(\d+\.?\d*)\s*\|", text):
        name = match.group(1).strip().lower()
        try:
            scores[name] = float(match.group(2))
        except ValueError:
            continue
    return scores


def count_persona_summaries(text: str) -> int:
    return len(re.findall(r"###\s+P\d+:", text))


def validate(report_path: Path) -> list[str]:
    """Return list of issues found. Empty list means the report is valid."""
    issues = []
    text = report_path.read_text(encoding="utf-8")
    lower = text.lower()

    # --- Sections ---
    required = [
        ("executive summary", "Executive Summary section"),
        ("key findings", "Key Findings section"),
        ("audience segmentation", "Audience Segmentation section"),
        ("recommendations", "Recommendations section"),
        ("appendix", "Appendix / Interview Summaries section"),
    ]
    for keyword, label in required:
        if keyword not in lower:
            issues.append(f"MISSING: {label}")

    if "risk" not in lower and "concern" not in lower:
        issues.append("MISSING: Risks and Concerns section")

    # --- Overall score ---
    score = extract_overall_score(text)
    if score is None:
        issues.append("MISSING: Overall score (expected 'Overall Score: X.X/10')")
    elif not (1.0 <= score <= 10.0):
        issues.append(f"INVALID: Overall score {score} outside [1, 10]")

    # --- Dimension scores ---
    dims = extract_dimension_scores(text)
    expected_dims = [
        "problem validity", "solution fit", "market demand",
        "competitive position", "monetization potential",
    ]
    for dim in expected_dims:
        if not any(dim in k for k in dims):
            issues.append(f"MISSING: Score for {dim}")
    for name, val in dims.items():
        if any(d in name for d in expected_dims):
            if not (1.0 <= val <= 10.0):
                issues.append(f"INVALID: {name} score {val} outside [1, 10]")

    # --- Verdict ---
    verdicts = ["strong opportunity", "promising", "significant concerns", "reconsider"]
    if not any(v in lower for v in verdicts):
        issues.append("MISSING: No recognized verdict phrase")

    # --- Interview summaries ---
    persona_count = count_persona_summaries(text)
    if persona_count < 8:
        issues.append(f"INCOMPLETE: Found {persona_count}/8 persona interview summaries")

    # --- Recommendations ---
    rec_items = re.findall(r"^\s*\d+\.\s+", text, re.MULTILINE)
    if len(rec_items) < 3:
        issues.append(f"SPARSE: Only {len(rec_items)} numbered items found (expected 3+ recommendations)")

    # --- Minimum length ---
    word_count = len(text.split())
    if word_count < 500:
        issues.append(f"SHORT: Report is only {word_count} words (expected 500+)")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/validate_report.py <report.md> [report2.md ...]")
        sys.exit(1)

    exit_code = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"ERROR: {path} does not exist")
            exit_code = 1
            continue

        issues = validate(path)
        if issues:
            print(f"\nFAIL: {path}")
            for issue in issues:
                print(f"  - {issue}")
            exit_code = 1
        else:
            print(f"PASS: {path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
