"""Step 2: Generate diverse synthetic personas from ProductContext."""

from models import ProductContext, SyntheticPersona
from llm import call_llm_json, load_prompt
from config import NUM_PERSONAS


PERSONA_SCHEMA = {
    "type": "object",
    "properties": {
        "personas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "persona_id": {"type": "string"},
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "role": {"type": "string", "description": "Job title or life role"},
                    "company_context": {"type": "string", "description": "Company size, industry, stage"},
                    "tech_savviness": {"type": "string", "enum": ["low", "medium", "high"]},
                    "budget_authority": {"type": "string", "enum": ["none", "influencer", "decision-maker"]},
                    "current_workflow": {"type": "string", "description": "How they solve this problem today"},
                    "pain_points": {"type": "array", "items": {"type": "string"}},
                    "enthusiasm_level": {"type": "string", "enum": ["skeptic", "neutral", "enthusiastic"]},
                    "relevant_experience": {"type": "string"},
                },
                "required": [
                    "persona_id", "name", "age", "role", "company_context",
                    "tech_savviness", "budget_authority", "current_workflow",
                    "pain_points", "enthusiasm_level", "relevant_experience",
                ],
            },
        },
    },
    "required": ["personas"],
}


def generate_personas(context: ProductContext, num_personas: int | None = None) -> list[SyntheticPersona]:
    n = num_personas or NUM_PERSONAS
    system = load_prompt("persona_generator.txt")
    user = f"""Generate {n} diverse synthetic user personas for evaluating this product:

Product: {context.product_name}
Description: {context.one_liner}
Value Proposition: {context.value_proposition}
Target Users: {', '.join(context.target_users)}
Target Industries: {', '.join(context.target_industries)}
Core Features: {', '.join(context.core_features)}
Key Benefits: {', '.join(context.key_benefits)}
Competitors: {', '.join(context.competitors)}

Ensure enthusiasm distribution: ~25% skeptics, ~37% neutral, ~38% enthusiastic.
Assign persona_id as P1, P2, ... P{n}."""

    data = call_llm_json(system, user, schema=PERSONA_SCHEMA, tool_name="personas", max_tokens=8192)
    return [SyntheticPersona(**p) for p in data["personas"]]
