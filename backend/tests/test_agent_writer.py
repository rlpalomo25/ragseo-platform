import json
import pytest
from tests.conftest import seed_doc
from app.services.agents import writer as writer_module
from app.services.agents.writer import run_writer, WriterMeta


WRITER_RESPONSE = (
    "===RAGSEO_META===\n"
    '{"title": "MasterShield vs LeafFilter", "meta_title": "MS vs LF", '
    '"meta_description": "A comparison", "archetype": "comparison", '
    '"content_type": "comparison", "brand": "mastershield"}\n'
    "===RAGSEO_CONTENT===\n"
    "# MasterShield vs LeafFilter\n\nShingle grit handling compared.\n"
)


@pytest.fixture()
def captured(monkeypatch):
    calls = {}

    def fake_call_llm(system_prompt, user_message, max_tokens=4096):
        calls["system_prompt"] = system_prompt
        calls["user_message"] = user_message
        calls["max_tokens"] = max_tokens
        return WRITER_RESPONSE

    monkeypatch.setattr(writer_module, "call_llm", fake_call_llm)
    return calls


def test_writer_happy_path(doctrine_corpus, captured):
    result = run_writer(doctrine_corpus, {
        "request": "Comparison page: MasterShield vs LeafFilter shingle grit",
        "content_type": "comparison",
    })

    out = result["output"]
    assert out["title"] == "MasterShield vs LeafFilter"
    assert "content_markdown" in out
    assert result["brand"] == "mastershield"

    # Provenance stamps the governing docs actually loaded, with versions.
    stamped = {p["doc_number"]: p["version"] for p in result["provenance"]}
    assert stamped == {"100": "8.6", "130": "5.8", "316": "13.8", "316-C": "2.1"}


def test_writer_prompt_contains_governing_doctrine(doctrine_corpus, captured):
    run_writer(doctrine_corpus, {
        "request": "MasterShield comparison page",
        "content_type": "comparison",
    })
    user_msg = captured["user_message"]
    assert "Problem-first posture" in user_msg          # brand module body
    assert "Three questions above the fold" in user_msg  # writer playbook body
    assert "comparison table required" in user_msg       # structure companion
    assert "Master Content Doctrine" in user_msg


def test_writer_structure_doc_selected_by_content_type(doctrine_corpus, captured):
    run_writer(doctrine_corpus, {"request": "MasterShield page", "content_type": "local"})
    # The comparison structure doc must NOT be pulled for a local page.
    assert "comparison table required" not in captured["user_message"]


def test_writer_klean_brand_selects_320_131(doctrine_corpus, captured):
    result = run_writer(doctrine_corpus, {"request": "Klean Gutter cleaning page"})
    stamped = {p["doc_number"]: p["version"] for p in result["provenance"]}
    assert stamped.get("320") == "13.8"
    assert stamped.get("131") == "4.2"


def test_writer_unknown_brand_generic_path(doctrine_corpus, captured):
    result = run_writer(doctrine_corpus, {"request": "A page about gutters generally"})
    stamped = {p["doc_number"] for p in result["provenance"]}
    assert stamped == {"100"}
    assert result["brand"] == "generic"


def test_writer_coerces_dict_archetype(doctrine_corpus, monkeypatch):
    response = (
        "===RAGSEO_META===\n"
        '{"title": "T", "meta_title": "MT", "meta_description": "MD", '
        '"archetype": {"primary": "Comparison", "secondary": "Sales"}, '
        '"content_type": "comparison", "brand": "mastershield"}\n'
        "===RAGSEO_CONTENT===\n# T\n\nBody.\n"
    )
    monkeypatch.setattr(writer_module, "call_llm", lambda **kw: response)
    result = run_writer(doctrine_corpus, {"request": "MasterShield comparison page"})
    assert result["output"]["archetype"] == "Comparison"
    assert result["output"]["title"] == "T"


def test_writer_invalid_meta_raises(doctrine_corpus, monkeypatch):
    bad = "===RAGSEO_META===\n{\"meta_title\": \"only\"}\n===RAGSEO_CONTENT===\nbody"
    monkeypatch.setattr(writer_module, "call_llm", lambda **kw: bad)
    with pytest.raises(ValueError, match="validation"):
        run_writer(doctrine_corpus, {"request": "MasterShield page"})


def test_writer_missing_request_raises(doctrine_corpus):
    with pytest.raises(ValueError, match="request"):
        run_writer(doctrine_corpus, {})


def test_writer_meta_model_rejects_empty_title():
    with pytest.raises(Exception):
        WriterMeta(title="", meta_title="x", meta_description="y")
