"""Embedding service supporting two self-contained providers.

- ``ollama`` (default): a local/self-hosted Ollama server (e.g.
  ``nomic-embed-text``). No API key, no egress. ``OLLAMA_BASE_URL`` points at
  the server.
- ``voyage`` (Voyage AI REST API): the original cloud option. Requires
  ``VOYAGE_API_KEY``.

When no provider is configured (``EMBEDDING_PROVIDER=none``) the service
degrades gracefully: ingestion still stores chunks, they simply have no
vectors, and retrieval falls back to keyword-only search.
"""
import logging
import time

import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

VOYAGE_API_URL = "https://api.voyageai.com/api/v1/embeddings"

# nomic-embed-text follows the MTEB task-prefix convention; applying it
# distinguishes documents from queries and improves retrieval quality.
_TASK_PREFIXES = {"document": "search_document: ", "query": "search_query: "}

_MAX_RETRIES = 3
_RETRY_BACKOFF = 1.0


class EmbeddingError(Exception):
    pass


def _ollama_embeddings_url() -> str:
    return f"{settings.ollama_base_url}/api/embeddings"


def _post_json(url: str, headers: dict, payload: dict) -> dict:
    """POST with retry/backoff on transient failures (429, 5xx, network)."""
    last_error: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = httpx.post(url, headers=headers, json=payload, timeout=60.0)
            if response.status_code == 429 or response.status_code >= 500:
                raise httpx.HTTPStatusError(
                    f"Retryable status {response.status_code}", request=response.request, response=response
                )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response is not None and e.response.status_code not in (429,) and e.response.status_code < 500:
                raise  # non-retryable client error
            if (
                e.response is not None
                and e.response.status_code == 500
                and "exceeds the context length" in e.response.text
            ):
                raise  # Ollama input overflow: not transient, caller shrinks the prompt
            last_error = e
        except httpx.HTTPError as e:
            last_error = e
        if attempt == _MAX_RETRIES - 1:
            break
        wait = _RETRY_BACKOFF * (2 ** attempt)
        logger.warning("Embedding POST failed (attempt %s); retrying in %.1fs", attempt + 1, wait)
        time.sleep(wait)
    raise last_error or EmbeddingError("Embedding POST failed")


def _embed_voyage(texts: list[str], input_type: str) -> list[list[float]]:
    all_vectors: list[list[float]] = []
    batch_size = max(1, settings.embedding_batch_size)
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        try:
            data = _post_json(
                VOYAGE_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.voyage_api_key}",
                    "Content-Type": "application/json",
                },
                payload={
                    "input": batch,
                    "model": settings.embedding_model,
                    "input_type": input_type,
                    "output_dimension": settings.embedding_dimensions,
                },
            )
        except httpx.HTTPStatusError as e:
            raise EmbeddingError(f"Voyage API error {e.response.status_code}: {e.response.text[:300]}") from e
        except httpx.HTTPError as e:
            raise EmbeddingError(f"Voyage API request failed: {e}") from e
        sorted_data = sorted(data["data"], key=lambda item: item["index"])
        all_vectors.extend(item["embedding"] for item in sorted_data)
    return all_vectors


def _truncate_to_context(text: str) -> str:
    """First shrink target for embedding inputs that exceed the context ceiling.

    Ollama's nomic-embed-text clamps to a 2048-token context regardless of the
    advertised num_ctx, so oversized doctrine chunks (kept whole per Doc 122)
    trip "input length exceeds the context length". Truncating only the vector
    input to a head window is graceful degradation: the chunk stays whole in
    the DB and keyword/search still sees full content. Very token-dense content
    can overflow even here; the caller shrinks further on demand.
    """
    max_chars = int(settings.embedding_context_length * settings.embedding_chars_per_token)
    if max_chars <= 0:
        return text
    return text[:max_chars]


_OVERFLOW_ERROR = "exceeds the context length"
# Progressive windows to retry with when ollama reports an overflow; the token
# budget of dense table/number content varies (measured ~2.9 chars/token), so a
# single char-based cap is not reliable.
_SHRINK_STEPS = (6144, 5120, 4096, 3072, 2048, 1536, 1024)


def _embed_ollama(text: str, input_type: str) -> list[float]:
    model = (settings.embedding_model or "").lower()
    prefix = _TASK_PREFIXES.get(input_type, "") if "nomic" in model else ""

    candidates = [prefix + text]
    first_cap = len(_truncate_to_context(text))
    limits = [first_cap]
    limits += [s for s in _SHRINK_STEPS if s < first_cap]
    for limit in limits:
        if limit >= len(text):
            continue
        candidates.append(prefix + text[:limit])

    for candidate in candidates:
        try:
            data = _post_json(
                _ollama_embeddings_url(),
                headers={"Content-Type": "application/json"},
                payload={
                    "model": settings.embedding_model,
                    "prompt": candidate,
                    "options": {"num_ctx": settings.embedding_context_length},
                },
            )
            embedding = data.get("embedding")
            break
        except httpx.HTTPStatusError as e:
            if _OVERFLOW_ERROR in (e.response.text or ""):
                if candidate is not candidates[-1]:
                    logger.info("Embedding overflow (%d chars); shrinking window", len(candidate))
                    continue
                raise EmbeddingError(
                    f"Ollama: input overflows context at all windows (max {len(candidates[-1])} chars)"
                ) from e
            raise EmbeddingError(f"Ollama API error {e.response.status_code}: {e.response.text[:300]}") from e
        except httpx.HTTPError as e:
            raise EmbeddingError(f"Ollama API request failed: {e}") from e
    else:
        if not candidates:
            raise EmbeddingError("Ollama: no embeddable input")

    if not embedding:
        raise EmbeddingError("Ollama returned an empty embedding")
    if len(embedding) != settings.embedding_dimensions:
        raise EmbeddingError(
            f"Ollama embedding dimension {len(embedding)} != configured {settings.embedding_dimensions} "
            f"(model {settings.embedding_model})"
        )
    return embedding


def embed_texts(texts: list[str], input_type: str = "document") -> list[list[float]] | None:
    """Embed a batch of texts. Returns None when embeddings are disabled.

    Raises EmbeddingError on API failure so callers can decide whether to
    persist chunks without vectors or abort.
    """
    if not settings.embeddings_enabled:
        return None
    if not texts:
        return []

    if settings.embedding_provider == "voyage":
        return _embed_voyage(texts, input_type)
    if settings.embedding_provider == "ollama":
        return [_embed_ollama(t, input_type) for t in texts]
    return None


def embed_query(query: str) -> list[float] | None:
    """Embed a single query for retrieval. Returns None when disabled."""
    vectors = embed_texts([query], input_type="query")
    if vectors is None:
        return None
    return vectors[0]