"""Data models for the evaluation pipeline."""

from pydantic import BaseModel, Field


class ProductContext(BaseModel):
    product_name: str
    one_liner: str
    value_proposition: str
    product_stage: str = "idea"
    product_type: str = "unknown"
    target_users: list[str]
    target_industries: list[str]
    core_features: list[str]
    key_benefits: list[str]
    competitors: list[str] = Field(default_factory=list)
    differentiation: str = ""
    assumptions_to_test: list[str] = Field(default_factory=list)


class SyntheticPersona(BaseModel):
    persona_id: str
    name: str
    age: int
    role: str
    company_context: str
    tech_savviness: str  # low, medium, high
    budget_authority: str  # none, influencer, decision-maker
    current_workflow: str
    pain_points: list[str]
    enthusiasm_level: str  # skeptic, neutral, enthusiastic
    relevant_experience: str


class InterviewExchange(BaseModel):
    question: str
    response: str


class InterviewTranscript(BaseModel):
    persona_id: str
    persona_name: str
    exchanges: list[InterviewExchange]
    overall_sentiment: str  # positive, negative, mixed
    key_quotes: list[str]
    would_adopt: bool | None = None


class Theme(BaseModel):
    name: str
    description: str
    frequency: int
    sentiment: str  # positive, negative, mixed
    supporting_quotes: list[str]


class FeedbackAnalysis(BaseModel):
    themes: list[Theme]
    pain_points_ranked: list[str]
    feature_requests: list[str]
    adoption_barriers: list[str]
    wtp_signals: list[str]
    segment_interest: dict[str, str]
    overall_sentiment_distribution: dict[str, int]


class ScoreBreakdown(BaseModel):
    problem_validity: float
    solution_fit: float
    market_demand: float
    competitive_position: float
    monetization_potential: float


class EvaluationReport(BaseModel):
    overall_score: float
    score_breakdown: ScoreBreakdown
    verdict: str
    markdown_report: str
    executive_summary: str
    top_recommendations: list[str]
