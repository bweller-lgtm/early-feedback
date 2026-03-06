"""Tests that validate real example reports against format expectations.

These tests run the same structural validators used for the sample_report
fixture against actual pipeline output in examples/. This proves the
pipeline produces well-formed reports, not just that the test suite passes
on a hand-written fixture.
"""

import re
import pytest
from test_report_format import (
    extract_sections,
    extract_scores,
    count_interview_summaries,
)


# ---------------------------------------------------------------------------
# Helpers (extended for real-report format variations)
# ---------------------------------------------------------------------------

def extract_overall_score_flexible(report: str) -> float | None:
    """Extract overall score, handling multiple formats.

    Matches:
      - "Overall Score: 6.8/10"
      - "### 4.4 / 10"
      - "4.4/10" anywhere near "overall"
    """
    # Format 1: "Overall Score: 6.8/10" or "Overall Score: 6.8 / 10"
    m = re.search(r"overall\s+score[:\s]*(\d+\.?\d*)\s*/\s*10", report, re.IGNORECASE)
    if m:
        return float(m.group(1))
    # Format 2: "### X.X / 10" under an Overall Score heading
    m = re.search(r"###\s+(\d+\.?\d*)\s*/\s*10", report)
    if m:
        return float(m.group(1))
    return None


def count_experts(report: str) -> int:
    """Count expert assessment subheadings under the Expert Assessments section.

    Handles both "### E1: Name" and "### Name — Title" formats.
    Excludes meta-headings like Pre-Mortem Consensus.
    """
    sections = extract_sections(report)
    expert_text = ""
    for k, v in sections.items():
        if "expert" in k:
            expert_text = v
            break
    if not expert_text:
        return 0
    headings = re.findall(r"^###\s+(.+)", expert_text, re.MULTILINE)
    # Filter out non-expert headings
    exclude = {"pre-mortem", "consensus", "follow-up", "tension"}
    return sum(
        1 for h in headings
        if not any(ex in h.lower() for ex in exclude)
    )


# ---------------------------------------------------------------------------
# Section presence
# ---------------------------------------------------------------------------

class TestRealReportSections:
    """All required sections exist in real reports."""

    def test_has_executive_summary(self, real_report):
        sections = extract_sections(real_report)
        assert any("executive summary" in k for k in sections)

    def test_has_overall_score(self, real_report):
        sections = extract_sections(real_report)
        assert any("overall score" in k or "score" in k for k in sections)

    def test_has_key_findings(self, real_report):
        sections = extract_sections(real_report)
        assert any("finding" in k for k in sections)

    def test_has_expert_assessments(self, real_report):
        sections = extract_sections(real_report)
        assert any("expert" in k for k in sections)

    def test_has_audience_segmentation(self, real_report):
        sections = extract_sections(real_report)
        assert any("audience" in k or "segmentation" in k for k in sections)

    def test_has_risks(self, real_report):
        sections = extract_sections(real_report)
        assert any("risk" in k or "concern" in k for k in sections)

    def test_has_recommendations(self, real_report):
        sections = extract_sections(real_report)
        assert any("recommendation" in k for k in sections)

    def test_has_appendix(self, real_report):
        sections = extract_sections(real_report)
        assert any("appendix" in k or "interview" in k or "transcript" in k for k in sections)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

class TestRealReportScoring:
    """Scores are present, in range, and verdict matches."""

    STANDARD_DIMENSIONS = {
        "problem validity",
        "solution fit",
        "market demand",
        "competitive position",
        "monetization potential",
    }

    def test_overall_score_present(self, real_report):
        score = extract_overall_score_flexible(real_report)
        assert score is not None, "Overall score not found"

    def test_overall_score_in_range(self, real_report):
        score = extract_overall_score_flexible(real_report)
        assert score is not None
        assert 1.0 <= score <= 10.0, f"Score {score} out of range"

    def test_standard_dimensions_scored(self, real_report):
        scores = extract_scores(real_report)
        for dim in self.STANDARD_DIMENSIONS:
            assert any(dim in k for k in scores), f"Missing dimension: {dim}"

    def test_dimension_scores_in_range(self, real_report):
        scores = extract_scores(real_report)
        for name, value in scores.items():
            if any(dim in name for dim in self.STANDARD_DIMENSIONS):
                assert 1.0 <= value <= 10.0, f"{name} = {value} out of range"

    def test_verdict_present(self, real_report):
        lower = real_report.lower()
        verdicts = ["strong opportunity", "promising", "significant concerns", "reconsider"]
        assert any(v in lower for v in verdicts), "No recognized verdict"


# ---------------------------------------------------------------------------
# Key findings
# ---------------------------------------------------------------------------

class TestRealReportFindings:
    """Key findings are substantive with evidence."""

    def test_at_least_three_findings(self, real_report):
        sections = extract_sections(real_report)
        findings_text = next((v for k, v in sections.items() if "finding" in k), "")
        if not findings_text:
            pytest.skip("Key findings section not found")
        count = len(re.findall(r"###\s+\d+\.", findings_text))
        if count == 0:
            count = len(re.findall(r"^\d+\.\s+", findings_text, re.MULTILINE))
        assert count >= 3, f"Expected 3+ findings, found {count}"

    def test_findings_have_quotes(self, real_report):
        sections = extract_sections(real_report)
        findings_text = next((v for k, v in sections.items() if "finding" in k), "")
        if not findings_text:
            pytest.skip("Key findings section not found")
        # Match "quoted text" or > blockquotes
        quotes = re.findall(r'"[^"]{10,}"', findings_text)
        blockquotes = re.findall(r"^>\s+.{10,}", findings_text, re.MULTILINE)
        assert len(quotes) + len(blockquotes) >= 1, "Findings should include supporting quotes"


# ---------------------------------------------------------------------------
# Expert assessments
# ---------------------------------------------------------------------------

class TestRealReportExperts:
    """Expert panel has 3+ substantive assessments."""

    def test_at_least_three_experts(self, real_report):
        assert count_experts(real_report) >= 3, "Expected 3+ expert assessments"

    def test_expert_text_substantive(self, real_report):
        sections = extract_sections(real_report)
        expert_text = next((v for k, v in sections.items() if "expert" in k), "")
        if not expert_text:
            pytest.skip("Expert section not found")
        assert len(expert_text.split()) >= 150, "Expert assessments too short"


# ---------------------------------------------------------------------------
# Interview transcripts
# ---------------------------------------------------------------------------

class TestRealReportTranscripts:
    """Appendix has full Q&A transcripts with metadata."""

    def test_persona_transcripts_present(self, real_report):
        count = count_interview_summaries(real_report)
        assert count >= 8, f"Expected 8+ persona transcripts, found {count}"

    def test_qa_exchanges_present(self, real_report):
        sections = extract_sections(real_report)
        appendix = next(
            (v for k, v in sections.items() if "appendix" in k or "interview" in k),
            "",
        )
        if not appendix:
            pytest.skip("Appendix not found")
        qa_count = len(re.findall(r"\*\*Q:", appendix))
        assert qa_count >= 16, f"Expected 16+ Q&A exchanges, found {qa_count}"

    def test_sentiment_labels_present(self, real_report):
        sections = extract_sections(real_report)
        appendix = next(
            (v for k, v in sections.items() if "appendix" in k or "interview" in k),
            "",
        )
        if not appendix:
            pytest.skip("Appendix not found")
        lower = appendix.lower()
        assert "positive" in lower or "negative" in lower or "mixed" in lower


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

class TestRealReportRecommendations:
    """Recommendations are numbered and actionable."""

    def test_at_least_three_recommendations(self, real_report):
        sections = extract_sections(real_report)
        rec_text = next((v for k, v in sections.items() if "recommendation" in k), "")
        if not rec_text:
            pytest.skip("Recommendations section not found")
        items = re.findall(r"^\s*\d+\.\s+", rec_text, re.MULTILINE)
        assert len(items) >= 3, f"Expected 3+ recommendations, found {len(items)}"
