"""Step 3: Simulate interviews with each persona."""

import asyncio
from models import ProductContext, SyntheticPersona, InterviewTranscript, InterviewExchange
from llm import load_prompt, get_client
from config import MODEL, MAX_CONCURRENT


INTERVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "exchanges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "response": {"type": "string"},
                },
                "required": ["question", "response"],
            },
        },
        "overall_sentiment": {"type": "string", "enum": ["positive", "negative", "mixed"]},
        "key_quotes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "3-5 most notable direct quotes from the persona",
        },
        "would_adopt": {
            "type": ["boolean", "null"],
            "description": "Whether this persona would adopt the product. null if unclear.",
        },
    },
    "required": ["exchanges", "overall_sentiment", "key_quotes", "would_adopt"],
}


def _build_interview_prompt(persona: SyntheticPersona, context: ProductContext) -> tuple[str, str]:
    base_system = load_prompt("interviewer.txt")
    system = f"""{base_system}

YOUR PERSONA:
Name: {persona.name}, Age: {persona.age}
Role: {persona.role}
Company: {persona.company_context}
Tech Savviness: {persona.tech_savviness}
Budget Authority: {persona.budget_authority}
Current Workflow: {persona.current_workflow}
Pain Points: {', '.join(persona.pain_points)}
Enthusiasm Level: {persona.enthusiasm_level}
Background: {persona.relevant_experience}"""

    user = f"""You are being interviewed about this product concept. Respond to each question in character.

PRODUCT CONCEPT:
{context.product_name}: {context.one_liner}
Value Proposition: {context.value_proposition}
Core Features: {', '.join(context.core_features)}
Key Benefits: {', '.join(context.key_benefits)}

Conduct a realistic interview with 6-7 exchanges covering:
1. Your current workflow and biggest frustrations
2. Your initial reaction to this product concept
3. Which features interest you most and why
4. Concerns or objections you have
5. What you'd be willing to pay (or why you wouldn't pay)
6. What would need to be true for you to switch
7. Your overall recommendation

Return the full interview as structured data."""

    return system, user


async def _interview_one(persona: SyntheticPersona, context: ProductContext, sem: asyncio.Semaphore) -> InterviewTranscript:
    async with sem:
        system, user = _build_interview_prompt(persona, context)
        client = get_client()
        message = await asyncio.to_thread(
            client.messages.create,
            model=MODEL,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
            tools=[{
                "name": "interview_result",
                "description": "Return the structured interview transcript.",
                "input_schema": INTERVIEW_SCHEMA,
            }],
            tool_choice={"type": "tool", "name": "interview_result"},
        )
        for block in message.content:
            if block.type == "tool_use":
                data = block.input
                return InterviewTranscript(
                    persona_id=persona.persona_id,
                    persona_name=persona.name,
                    exchanges=[InterviewExchange(**e) for e in data["exchanges"]],
                    overall_sentiment=data["overall_sentiment"],
                    key_quotes=data["key_quotes"],
                    would_adopt=data.get("would_adopt"),
                )
        raise ValueError(f"No tool_use in interview response for {persona.name}")


async def simulate_interviews(personas: list[SyntheticPersona], context: ProductContext) -> list[InterviewTranscript]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = [_interview_one(p, context, sem) for p in personas]
    return await asyncio.gather(*tasks)
