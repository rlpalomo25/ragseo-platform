import anthropic
from app.config import get_settings

settings = get_settings()

_client: anthropic.Anthropic | None = None


def get_llm_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def call_llm(
    system_prompt: str,
    user_message: str,
    model: str | None = None,
    max_tokens: int | None = None,
) -> str:
    client = get_llm_client()
    response = client.messages.create(
        model=model or settings.llm_model,
        max_tokens=max_tokens or settings.llm_max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    if response.stop_reason == "max_tokens":
        raise ValueError(
            f"LLM output truncated at max_tokens={response.usage.output_tokens} "
            "(raise the token budget for this agent)"
        )
    return response.content[0].text
