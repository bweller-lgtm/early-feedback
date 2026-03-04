"""Step 5: Generate the final evaluation report."""

from models import (
    ProductContext, InterviewTranscript, FeedbackAnalysis,
    EvaluationReport, ScoreBreakdown,
)
from llm import call_llm, load_prompt
import json


def generate_report(
    context: ProductContext,
    transcripts: list[InterviewTranscript],
    analysis: FeedbackAnalysis,
) -> EvaluationReport:
    system = load_prompt("report_writer.txt")

    # Build structured summary of findings for the report writer
    analysis_summary = json.dumps(analysis.model_dump(), indent=2)

    # Build interview summary
    interview_summaries = []
    for t in transcripts:
        adoption = "Yes" if t.would_adopt else ("No" if t.would_adopt is False else "Unclear")
        interview_summaries.append(
            f"- **{t.persona_name}** ({t.persona_id}): {t.overall_sentiment} sentiment, "
            f"would adopt: {adoption}. Key quotes: {'; '.join(t.key_quotes[:2])}"
        )

    user = f"""Write a comprehensive evaluation report for this product idea.

PRODUCT:
Name: {context.product_name}
Description: {context.one_liner}
Value Proposition: {context.value_proposition}
Target Users: {', '.join(context.target_users)}
Competitors: {', '.join(context.competitors)}
Differentiation: {context.differentiation}
Assumptions to Test: {', '.join(context.assumptions_to_test)}

ANALYSIS RESULTS:
{analysis_summary}

INTERVIEW SUMMARIES:
{chr(10).join(interview_summaries)}

Write the full report in Markdown format with these sections:
1. Executive Summary (2-3 paragraphs)
2. Overall Score (1-10) with breakdown table (Problem Validity, Solution Fit, Market Demand, Competitive Position, Monetization Potential)
3. Key Findings (top 5, each with supporting evidence/quotes)
4. Audience Segmentation (which user types are most promising)
5. Risks and Concerns
6. Recommendations (prioritized, actionable)
7. Appendix: Individual Interview Summaries

At the very end of the report, on a new line, output a JSON block with scores:
```json
{{"overall_score": X.X, "problem_validity": X.X, "solution_fit": X.X, "market_demand": X.X, "competitive_position": X.X, "monetization_potential": X.X, "verdict": "...", "executive_summary": "...", "top_recommendations": ["...", "..."]}}
```"""

    response = call_llm(system, user, max_tokens=8192)

    # Extract the JSON scores block from end of response
    scores = _extract_scores(response)

    # The markdown is everything before the JSON block
    markdown = response
    json_start = response.rfind("```json")
    if json_start != -1:
        markdown = response[:json_start].rstrip()

    return EvaluationReport(
        overall_score=scores.get("overall_score", 5.0),
        score_breakdown=ScoreBreakdown(
            problem_validity=scores.get("problem_validity", 5.0),
            solution_fit=scores.get("solution_fit", 5.0),
            market_demand=scores.get("market_demand", 5.0),
            competitive_position=scores.get("competitive_position", 5.0),
            monetization_potential=scores.get("monetization_potential", 5.0),
        ),
        verdict=scores.get("verdict", "Needs further evaluation"),
        markdown_report=markdown,
        executive_summary=scores.get("executive_summary", ""),
        top_recommendations=scores.get("top_recommendations", []),
    )


def _extract_scores(text: str) -> dict:
    """Extract the JSON scores block from the report text."""
    try:
        # Find last JSON code block
        json_start = text.rfind("```json")
        if json_start == -1:
            json_start = text.rfind("```")
        if json_start == -1:
            return {}

        block_start = text.index("{", json_start)
        block_end = text.rindex("}") + 1
        return json.loads(text[block_start:block_end])
    except (ValueError, json.JSONDecodeError):
        return {}
