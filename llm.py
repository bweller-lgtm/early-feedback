"""Thin wrapper around the Anthropic client for structured LLM calls."""

import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL


_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def call_llm(system: str, user: str, max_tokens: int = 4096) -> str:
    """Simple text completion call."""
    client = get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


def call_llm_json(system: str, user: str, schema: dict, tool_name: str = "output", max_tokens: int = 4096) -> dict:
    """Structured output call using tool_use to get reliable JSON."""
    client = get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        tools=[{
            "name": tool_name,
            "description": f"Return the structured {tool_name} data.",
            "input_schema": schema,
        }],
        tool_choice={"type": "tool", "name": tool_name},
    )
    for block in message.content:
        if block.type == "tool_use":
            return block.input
    raise ValueError("No tool_use block in response")


def load_prompt(filename: str) -> str:
    """Load a prompt template from the prompts/ directory."""
    from config import PROMPTS_DIR
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")
