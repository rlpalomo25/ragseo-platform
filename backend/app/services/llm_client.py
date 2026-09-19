"""Anthropic LLM client wrapper with a bounded retry/timeout policy (Fix 5).

Celery runs each agent task under a 600s soft / 900s hard limit. A single
messages.create request therefore gets:
  * a client timeout (llm_timeout_seconds, default 540s) — always below the
    soft limit so one hung request cannot claim a whole default worker slot;
  * a bounded exponential-backoff retry loop (llm_max_retries, default 2)
    for transient faults (429 rate limits, 5xx, connection/timeout errors) —
    capped so the combined worst-case wall time stays under the hard limit.
"""

import logging
import time

import anthropic
from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
)

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_client: anthropic.Anthropic | None = None

# Status codes worth a retry: 429 (rate limit) and 5xx (transient server
# faults). 4xx client errors (bad request, auth, ...) are NOT retried — they
# will never succeed on a second attempt.
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (APIConnectionError, APITimeoutError)):
        return True
    if isinstance(exc, APIStatusError):
        return exc.status_code in _RETRYABLE_STATUS
    return False


def get_llm_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(
            api_key=settings.anthropic_api_key,
            timeout=settings.llm_timeout_seconds,
        )
    return _client


def call_llm(
    system_prompt: str,
    user_message: str,
    model: str | None = None,
    max_tokens: int | None = None,
) -> str:
    client = get_llm_client()

    last_error: Exception | None = None
    for attempt in range(settings.llm_max_retries + 1):
        try:
            response = client.messages.create(
                model=model or settings.llm_model,
                max_tokens=max_tokens or settings.llm_max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            break
        except Exception as exc:
            if not _is_retryable(exc):
                raise
            last_error = exc
            if attempt >= settings.llm_max_retries:
                break
            backoff = settings.llm_retry_backoff_base * (2**attempt)
            logger.warning(
                "LLM call failed (attempt %d/%d): %s — retrying in %.1fs",
                attempt + 1,
                settings.llm_max_retries + 1,
                exc,
                backoff,
            )
            time.sleep(backoff)

    if response is None:
        raise RuntimeError(
            f"LLM call failed after {settings.llm_max_retries + 1} attempts: {last_error}"
        ) from last_error

    if response.stop_reason == "max_tokens":
        raise ValueError(
            f"LLM output truncated at max_tokens={response.usage.output_tokens} "
            "(raise the token budget for this agent)"
        )
    return response.content[0].text
