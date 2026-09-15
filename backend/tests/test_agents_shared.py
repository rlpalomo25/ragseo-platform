import json
import pytest
from app.services.agents.llm_output import extract_json, parse_meta_content_response


def test_extract_json_fenced():
    text = 'blah\n```json\n{"verdict": "pass"}\n```\nblah'
    assert extract_json(text) == {"verdict": "pass"}


def test_extract_json_bare():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_garbage_returns_none():
    assert extract_json("no json here at all") is None


def test_extract_json_brace_in_prose_after_json():
    text = '{"verdict": "fail"}\n\nSome trailing prose with } in it.'
    assert extract_json(text) == {"verdict": "fail"}


def test_extract_json_prose_before_and_after():
    text = 'Here it is: {"a": {"b": [1, 2]}} and that is all.'
    assert extract_json(text) == {"a": {"b": [1, 2]}}


def test_extract_json_strings_with_braces():
    text = '{"notes": "use {brace} syntax"} trailing }'
    assert extract_json(text) == {"notes": "use {brace} syntax"}


def test_parse_meta_content_response_valid():
    response = (
        "===RAGSEO_META===\n"
        '{"title": "T", "meta_title": "MT", "meta_description": "MD"}\n'
        "===RAGSEO_CONTENT===\n"
        "# T\n\nBody here.\n"
    )
    meta, content = parse_meta_content_response(response)
    assert meta["title"] == "T"
    assert content == "# T\n\nBody here."


def test_parse_meta_content_response_missing_delimiter_raises():
    with pytest.raises(ValueError, match="delimiters"):
        parse_meta_content_response("just some text")


def test_parse_meta_content_response_bad_json_raises():
    response = "===RAGSEO_META===\nnot json\n===RAGSEO_CONTENT===\nbody"
    with pytest.raises(ValueError, match="valid JSON"):
        parse_meta_content_response(response)


def test_parse_meta_content_response_empty_content_raises():
    response = '===RAGSEO_META===\n{"title":"T"}\n===RAGSEO_CONTENT===\n   '
    with pytest.raises(ValueError, match="empty content"):
        parse_meta_content_response(response)


def test_registry_has_all_agents():
    from app.tasks import AGENT_FUNCTIONS

    assert set(AGENT_FUNCTIONS) == {"router", "writer", "auditor"}
