"""Step 1: Parse a raw idea description into structured ProductContext."""

from models import ProductContext
from llm import call_llm_json, load_prompt


SCHEMA = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string", "description": "Name or working title for the product"},
        "one_liner": {"type": "string", "description": "One sentence describing what it does"},
        "value_proposition": {"type": "string", "description": "Core value it provides to users"},
        "product_stage": {"type": "string", "enum": ["idea", "prototype", "mvp", "growth", "mature"]},
        "product_type": {"type": "string", "description": "e.g. b2b_saas, b2c_app, marketplace, api, hardware"},
        "target_users": {"type": "array", "items": {"type": "string"}, "description": "Types of users this targets"},
        "target_industries": {"type": "array", "items": {"type": "string"}},
        "core_features": {"type": "array", "items": {"type": "string"}},
        "key_benefits": {"type": "array", "items": {"type": "string"}},
        "competitors": {"type": "array", "items": {"type": "string"}, "description": "Existing solutions or workarounds"},
        "differentiation": {"type": "string", "description": "How it differs from alternatives"},
        "assumptions_to_test": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key hypotheses that need validation through user research",
        },
    },
    "required": [
        "product_name", "one_liner", "value_proposition", "product_stage",
        "product_type", "target_users", "target_industries", "core_features",
        "key_benefits", "competitors", "differentiation", "assumptions_to_test",
    ],
}


def parse_context(idea_text: str) -> ProductContext:
    system = load_prompt("context_parser.txt")
    user = f"Analyze this product/project idea and extract structured context:\n\n{idea_text}"
    data = call_llm_json(system, user, schema=SCHEMA, tool_name="product_context")
    return ProductContext(**data)
