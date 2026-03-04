"""Step 4: Analyze all interview transcripts into structured findings."""

from models import ProductContext, InterviewTranscript, FeedbackAnalysis, Theme
from llm import call_llm_json, load_prompt


ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "frequency": {"type": "integer", "description": "Number of personas who mentioned this"},
                    "sentiment": {"type": "string", "enum": ["positive", "negative", "mixed"]},
                    "supporting_quotes": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "description", "frequency", "sentiment", "supporting_quotes"],
            },
        },
        "pain_points_ranked": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Pain points ranked by frequency/severity",
        },
        "feature_requests": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Features personas wished for or suggested",
        },
        "adoption_barriers": {
            "type": "array",
            "items": {"type": "string"},
            "description": "What would prevent adoption",
        },
        "wtp_signals": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Observations about willingness to pay",
        },
        "segment_interest": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "description": "Persona segment -> interest level (high/medium/low)",
        },
        "overall_sentiment_distribution": {
            "type": "object",
            "properties": {
                "positive": {"type": "integer"},
                "negative": {"type": "integer"},
                "mixed": {"type": "integer"},
            },
            "required": ["positive", "negative", "mixed"],
        },
    },
    "required": [
        "themes", "pain_points_ranked", "feature_requests",
        "adoption_barriers", "wtp_signals", "segment_interest",
        "overall_sentiment_distribution",
    ],
}


def _format_transcripts(transcripts: list[InterviewTranscript]) -> str:
    parts = []
    for t in transcripts:
        lines = [f"## {t.persona_name} ({t.persona_id}) — Sentiment: {t.overall_sentiment}"]
        for ex in t.exchanges:
            lines.append(f"Q: {ex.question}")
            lines.append(f"A: {ex.response}")
            lines.append("")
        parts.append("\n".join(lines))
    return "\n---\n\n".join(parts)


def analyze_feedback(transcripts: list[InterviewTranscript], context: ProductContext) -> FeedbackAnalysis:
    system = load_prompt("analyst.txt")
    formatted = _format_transcripts(transcripts)
    user = f"""Analyze these {len(transcripts)} synthetic user interviews for the product "{context.product_name}" ({context.one_liner}).

INTERVIEW TRANSCRIPTS:

{formatted}

Identify themes, patterns, and actionable insights."""

    data = call_llm_json(system, user, schema=ANALYSIS_SCHEMA, tool_name="feedback_analysis", max_tokens=8192)
    return FeedbackAnalysis(
        themes=[Theme(**t) for t in data["themes"]],
        pain_points_ranked=data["pain_points_ranked"],
        feature_requests=data["feature_requests"],
        adoption_barriers=data["adoption_barriers"],
        wtp_signals=data["wtp_signals"],
        segment_interest=data["segment_interest"],
        overall_sentiment_distribution=data["overall_sentiment_distribution"],
    )
