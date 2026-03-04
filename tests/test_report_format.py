"""Tests for validating generated evaluation reports.

These tests verify that reports produced by the /evaluate skill contain
all required sections, proper scoring, and complete interview coverage.
Run against any generated report or the sample_report fixture.
"""

import re
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_sections(report: str) -> dict[str, str]:
    """Split a markdown report into {heading_lower: body} by ## headings."""
    sections: dict[str, str] = {}
    current_heading = None
    current_lines: list[str] = []

    for line in report.split("\n"):
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = line.lstrip("# ").strip().lower()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def extract_scores(report: str) -> dict[str, float]:
    """Extract dimension scores from a breakdown table."""
    scores: dict[str, float] = {}
    # Match lines like "| Problem Validity | 7.5 |"
    pattern = re.compile(r"\|\s*(.+?)\s*\|\s*(\d+\.?\d*)\s*\|")
    for match in pattern.finditer(report):
        name = match.group(1).strip().lower()
        try:
            scores[name] = float(match.group(2))
        except ValueError:
            continue
    return scores


def extract_overall_score(report: str) -> float | None:
    """Extract the overall score (e.g., 'Overall Score: 6.8/10')."""
    match = re.search(r"overall\s+score[:\s]*(\d+\.?\d*)\s*/\s*10", report, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def count_interview_summaries(report: str) -> int:
    """Count persona interview summaries in the appendix (### P1: ..., ### P2: ..., etc.)."""
    return len(re.findall(r"###\s+P\d+:", report))


# ---------------------------------------------------------------------------
# Section presence tests
# ---------------------------------------------------------------------------

class TestReportSections:
    """Verify all 7 required sections exist in the report."""

    REQUIRED_SECTIONS = [
        "executive summary",
        "key findings",
        "audience segmentation",
        "recommendations",
    ]

    def test_has_executive_summary(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("executive summary" in k for k in sections), "Missing Executive Summary"

    def test_has_overall_score(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("overall score" in k or "score" in k for k in sections), "Missing Overall Score section"

    def test_has_key_findings(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("key findings" in k or "findings" in k for k in sections), "Missing Key Findings"

    def test_has_audience_segmentation(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("audience" in k or "segmentation" in k for k in sections), "Missing Audience Segmentation"

    def test_has_risks(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("risk" in k or "concern" in k for k in sections), "Missing Risks and Concerns"

    def test_has_recommendations(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("recommendation" in k for k in sections), "Missing Recommendations"

    def test_has_appendix(self, sample_report):
        sections = extract_sections(sample_report)
        assert any("appendix" in k or "interview" in k for k in sections), "Missing Appendix/Interview Summaries"


# ---------------------------------------------------------------------------
# Scoring tests
# ---------------------------------------------------------------------------

class TestScoring:
    """Verify scores are present and within valid ranges."""

    EXPECTED_DIMENSIONS = {
        "problem validity",
        "solution fit",
        "market demand",
        "competitive position",
        "monetization potential",
    }

    def test_overall_score_present(self, sample_report):
        score = extract_overall_score(sample_report)
        assert score is not None, "Overall score not found (expected 'Overall Score: X.X/10')"

    def test_overall_score_in_range(self, sample_report):
        score = extract_overall_score(sample_report)
        assert score is not None
        assert 1.0 <= score <= 10.0, f"Overall score {score} out of range [1, 10]"

    def test_all_dimensions_scored(self, sample_report):
        scores = extract_scores(sample_report)
        for dim in self.EXPECTED_DIMENSIONS:
            assert any(dim in k for k in scores), f"Missing score for dimension: {dim}"

    def test_dimension_scores_in_range(self, sample_report):
        scores = extract_scores(sample_report)
        for name, value in scores.items():
            if any(dim in name for dim in self.EXPECTED_DIMENSIONS):
                assert 1.0 <= value <= 10.0, f"{name} score {value} out of range [1, 10]"

    def test_breakdown_table_exists(self, sample_report):
        assert "|" in sample_report, "No markdown table found for score breakdown"
        scores = extract_scores(sample_report)
        assert len(scores) >= 5, f"Expected 5+ dimension scores in table, found {len(scores)}"


# ---------------------------------------------------------------------------
# Verdict tests
# ---------------------------------------------------------------------------

class TestVerdict:
    """Verify verdict is consistent with score."""

    VERDICTS = {
        (7.5, 10.0): "strong opportunity",
        (5.5, 7.5): "promising",
        (3.5, 5.5): "significant concerns",
        (0.0, 3.5): "reconsider",
    }

    def test_verdict_present(self, sample_report):
        lower = sample_report.lower()
        has_verdict = any(v in lower for v in self.VERDICTS.values())
        assert has_verdict, "No recognized verdict found in report"

    def test_verdict_matches_score(self, sample_report):
        score = extract_overall_score(sample_report)
        if score is None:
            pytest.skip("No overall score found")
        lower = sample_report.lower()
        for (lo, hi), phrase in self.VERDICTS.items():
            if lo <= score < hi:
                # The verdict should match OR the report should contain this phrase
                # Allow some flexibility since the report may phrase it slightly differently
                assert phrase in lower, (
                    f"Score {score} expects verdict containing '{phrase}' but not found"
                )
                return
        # Score of exactly 10.0
        assert "strong opportunity" in lower


# ---------------------------------------------------------------------------
# Key findings tests
# ---------------------------------------------------------------------------

class TestKeyFindings:
    """Verify key findings are substantive."""

    def test_at_least_three_findings(self, sample_report):
        # Count ### subheadings under key findings, or numbered items
        sections = extract_sections(sample_report)
        findings_text = ""
        for k, v in sections.items():
            if "finding" in k:
                findings_text = v
                break
        if not findings_text:
            pytest.skip("Key findings section not found")
        # Count subheadings (### 1., ### 2., etc.) or numbered lines
        count = len(re.findall(r"###\s+\d+\.", findings_text))
        if count == 0:
            count = len(re.findall(r"^\d+\.\s+", findings_text, re.MULTILINE))
        assert count >= 3, f"Expected at least 3 key findings, found {count}"

    def test_findings_have_quotes(self, sample_report):
        sections = extract_sections(sample_report)
        findings_text = ""
        for k, v in sections.items():
            if "finding" in k:
                findings_text = v
                break
        if not findings_text:
            pytest.skip("Key findings section not found")
        # Look for quoted text (in double quotes or italics)
        quotes = re.findall(r'"[^"]{10,}"', findings_text)
        assert len(quotes) >= 1, "Key findings should include supporting quotes"


# ---------------------------------------------------------------------------
# Interview summaries tests
# ---------------------------------------------------------------------------

class TestInterviewTranscripts:
    """Verify interview transcripts cover all personas with Q&A dialogue."""

    def test_at_least_eight_transcripts(self, sample_report):
        count = count_interview_summaries(sample_report)
        assert count >= 8, f"Expected 8 interview transcripts, found {count}"

    def test_transcripts_have_qa_exchanges(self, sample_report):
        """Verify interviews contain actual Q&A dialogue, not just summaries."""
        sections = extract_sections(sample_report)
        appendix = ""
        for k, v in sections.items():
            if "appendix" in k or "interview" in k or "transcript" in k:
                appendix = v
                break
        if not appendix:
            pytest.skip("Appendix section not found")
        # Look for Q: or **Q: patterns indicating interview questions
        qa_patterns = re.findall(r"\*\*Q:", appendix)
        assert len(qa_patterns) >= 16, (
            f"Expected at least 16 Q&A exchanges (2+ per persona), found {len(qa_patterns)}"
        )

    def test_transcripts_include_sentiment(self, sample_report):
        sections = extract_sections(sample_report)
        appendix = ""
        for k, v in sections.items():
            if "appendix" in k or "interview" in k:
                appendix = v
                break
        if not appendix:
            pytest.skip("Appendix section not found")
        lower = appendix.lower()
        assert "positive" in lower or "negative" in lower or "mixed" in lower, (
            "Interview summaries should include sentiment"
        )

    def test_summaries_include_would_adopt(self, sample_report):
        sections = extract_sections(sample_report)
        appendix = ""
        for k, v in sections.items():
            if "appendix" in k or "interview" in k:
                appendix = v
                break
        if not appendix:
            pytest.skip("Appendix section not found")
        lower = appendix.lower()
        assert "would adopt" in lower or "adopt:" in lower, (
            "Interview summaries should include adoption verdict"
        )

    def test_summaries_include_quotes(self, sample_report):
        sections = extract_sections(sample_report)
        appendix = ""
        for k, v in sections.items():
            if "appendix" in k or "interview" in k:
                appendix = v
                break
        if not appendix:
            pytest.skip("Appendix section not found")
        quotes = re.findall(r'"[^"]{10,}"', appendix)
        assert len(quotes) >= 4, (
            f"Expected key quotes in interview summaries, found {len(quotes)}"
        )


# ---------------------------------------------------------------------------
# Recommendations tests
# ---------------------------------------------------------------------------

class TestRecommendations:
    """Verify recommendations are present and actionable."""

    def test_at_least_three_recommendations(self, sample_report):
        sections = extract_sections(sample_report)
        rec_text = ""
        for k, v in sections.items():
            if "recommendation" in k:
                rec_text = v
                break
        if not rec_text:
            pytest.skip("Recommendations section not found")
        items = re.findall(r"^\s*\d+\.\s+", rec_text, re.MULTILINE)
        assert len(items) >= 3, f"Expected at least 3 recommendations, found {len(items)}"


# ---------------------------------------------------------------------------
# Overall structure tests
# ---------------------------------------------------------------------------

class TestReportStructure:
    """Verify general report quality signals."""

    def test_minimum_length(self, sample_report):
        word_count = len(sample_report.split())
        assert word_count >= 500, f"Report seems too short ({word_count} words)"

    def test_has_markdown_headings(self, sample_report):
        headings = re.findall(r"^#{1,3}\s+", sample_report, re.MULTILINE)
        assert len(headings) >= 7, f"Expected at least 7 markdown headings, found {len(headings)}"

    def test_has_table(self, sample_report):
        table_rows = re.findall(r"^\|.+\|$", sample_report, re.MULTILINE)
        assert len(table_rows) >= 3, "Expected a score breakdown table with at least 3 rows"
