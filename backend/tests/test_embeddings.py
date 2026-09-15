import httpx
import pytest

import app.services.embeddings as emb
from app.config import get_settings
from app.services.embeddings import EmbeddingError, embed_query, embed_texts

DIM = 768


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.request = httpx.Request("POST", "http://fake")

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"{self.status_code} {self.text}", request=self.request, response=self
            )

    def json(self):
        return self._json_data


@pytest.fixture()
def ollama_ok(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "ollama")
    monkeypatch.setattr(settings, "ollama_base_url", "http://ollama:11434")
    monkeypatch.setattr(settings, "embedding_model", "nomic-embed-text")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(settings, "embedding_context_length", 2048)
    monkeypatch.setattr(settings, "embedding_chars_per_token", 4.0)

    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["payload"] = json
        return FakeResponse(json_data={"embedding": [0.1] * DIM})

    monkeypatch.setattr(httpx, "post", fake_post)
    return captured


@pytest.fixture()
def voyage_ok(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "voyage")
    monkeypatch.setattr(settings, "voyage_api_key", "test-key")
    monkeypatch.setattr(settings, "embedding_model", "voyage-3-lite")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)

    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["payload"] = json
        return FakeResponse(json_data={
            "data": [{"index": i, "embedding": [0.1] * DIM} for i in range(len(json["input"]))],
        })

    monkeypatch.setattr(httpx, "post", fake_post)
    return captured


def test_embed_texts_disabled_returns_none():
    emb.settings.embedding_provider = "none"
    assert embed_texts(["hello"]) is None
    assert embed_query("hello") is None


def test_embed_texts_empty_returns_empty(ollama_ok):
    assert embed_texts([]) == []


def test_ollama_embeds_with_task_prefix(ollama_ok):
    vectors = embed_texts(["pine needles clog gutters"])
    assert len(vectors) == 1
    assert len(vectors[0]) == DIM
    assert ollama_ok["url"] == "http://ollama:11434/api/embeddings"
    assert ollama_ok["payload"]["model"] == "nomic-embed-text"
    assert ollama_ok["payload"]["options"] == {"num_ctx": 2048}
    assert ollama_ok["payload"]["prompt"] == "search_document: pine needles clog gutters"


def test_ollama_shrinks_oversized_input_on_overflow(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "ollama")
    monkeypatch.setattr(settings, "embedding_model", "nomic-embed-text")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(settings, "embedding_context_length", 2048)
    monkeypatch.setattr(settings, "embedding_chars_per_token", 4.0)

    calls = []

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append(json["prompt"])
        if len(json["prompt"]) > len("search_document: ") + 6144:
            return FakeResponse(status_code=500, text='{"error":"the input length exceeds the context length"}')
        return FakeResponse(json_data={"embedding": [0.1] * DIM})

    monkeypatch.setattr(httpx, "post", fake_post)
    vectors = embed_texts(["x" * 20_000])
    assert vectors == [[0.1] * DIM]
    # full input first (no gratuitous truncation), then first shrink window passes
    assert calls[0] == "search_document: " + "x" * 20_000
    assert calls[-1] == "search_document: " + "x" * 6144
    assert calls[1] == "search_document: " + "x" * 8192


def test_ollama_raises_when_all_windows_overflow(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "ollama")
    monkeypatch.setattr(settings, "embedding_model", "nomic-embed-text")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(httpx, "post", lambda url, headers=None, json=None, timeout=None: FakeResponse(
        status_code=500, text='{"error":"the input length exceeds the context length"}',
    ))
    with pytest.raises(EmbeddingError, match="overflows context"):
        embed_texts(["y" * 5_000])


def test_ollama_leaves_small_input_intact(ollama_ok):
    embed_texts(["short text"])
    assert ollama_ok["payload"]["prompt"] == "search_document: short text"


def test_embed_query_uses_query_prefix(ollama_ok):
    embed_query("best gutter guard for pine needles")
    assert ollama_ok["payload"]["prompt"] == "search_query: best gutter guard for pine needles"


def test_ollama_non_nomic_model_no_prefix(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "ollama")
    monkeypatch.setattr(settings, "embedding_model", "bge-base-en-v1.5")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(httpx, "post", lambda url, headers=None, json=None, timeout=None: FakeResponse(
        json_data={"embedding": [0.1] * DIM},
    ))
    vectors = embed_texts(["plain text"])
    assert vectors == [[0.1] * DIM]


def test_ollama_dimension_mismatch_raises(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "ollama")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(httpx, "post", lambda url, headers=None, json=None, timeout=None: FakeResponse(
        json_data={"embedding": [0.2] * 512},
    ))
    with pytest.raises(EmbeddingError, match="dimension"):
        embed_texts(["x"])


def test_voyage_batches_and_sets_input_type(voyage_ok):
    vectors = embed_texts(["a", "b", "c"], input_type="document")
    assert len(vectors) == 3
    assert voyage_ok["url"] == "https://api.voyageai.com/api/v1/embeddings"
    assert voyage_ok["payload"]["input_type"] == "document"
    assert voyage_ok["payload"]["output_dimension"] == DIM
    assert voyage_ok["payload"]["input"] == ["a", "b", "c"]


def test_voyage_retries_transient_failure(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "voyage")
    monkeypatch.setattr(settings, "voyage_api_key", "test-key")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)

    calls = {"n": 0}

    def fake_post(url, headers=None, json=None, timeout=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return FakeResponse(status_code=429, text="rate limited")
        return FakeResponse(json_data={"data": [{"index": 0, "embedding": [0.1] * DIM}]})

    monkeypatch.setattr(httpx, "post", fake_post)
    monkeypatch.setattr(emb.time, "sleep", lambda s: None)
    vectors = embed_texts(["a"])
    assert vectors == [[0.1] * DIM]
    assert calls["n"] == 2


def test_voyage_non_retryable_client_error(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "voyage")
    monkeypatch.setattr(settings, "voyage_api_key", "bad-key")
    monkeypatch.setattr(settings, "embedding_dimensions", DIM)
    monkeypatch.setattr(httpx, "post", lambda url, headers=None, json=None, timeout=None: FakeResponse(
        status_code=401, text="unauthorized",
    ))
    with pytest.raises(EmbeddingError, match="401"):
        embed_texts(["a"])


def test_voyage_disabled_when_no_key(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "embedding_provider", "voyage")
    monkeypatch.setattr(settings, "voyage_api_key", "")
    assert settings.embeddings_enabled is False
    assert embed_texts(["a"]) is None