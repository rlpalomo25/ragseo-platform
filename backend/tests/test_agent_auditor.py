import json

import pytest
from app.models.agent_task import AgentTask
from app.services.agents import auditor as auditor_module
from app.services.agents.auditor import run_auditor


def _verdict_response(verdict="pass_with_notes", findings=None):
    return json.dumps(
        {
            "verdict": verdict,
            "summary": "Audited against rubric.",
            "findings": findings
            or [
                {
                    "check": "Above-fold questions",
                    "severity": "minor",
                    "status": "warn",
                    "notes": "Only two teasers present.",
                },
            ],
        }
    )


def test_auditor_happy_path(doctrine_corpus, monkeypatch):
    monkeypatch.setattr(auditor_module, "call_llm", lambda **kw: _verdict_response())
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody text."})

    out = result["output"]
    assert out["verdict"] == "pass_with_notes"
    assert out["findings"][0]["check"] == "Above-fold questions"
    stamped = {p["doc_number"]: p["version"] for p in result["provenance"]}
    assert stamped == {"328": "16.15"}


def test_auditor_coerces_non_standard_status(doctrine_corpus, monkeypatch):
    findings = [
        {
            "check": "Meta keywords",
            "severity": "major",
            "status": "flag",
            "notes": "Prioritize primary keyword.",
        }
    ]
    monkeypatch.setattr(
        auditor_module,
        "call_llm",
        lambda **kw: _verdict_response(findings=findings),
    )
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody."})
    assert result["output"]["findings"][0]["status"] == "warn"


def test_auditor_critical_fail_forces_fail_verdict(doctrine_corpus, monkeypatch):
    findings = [
        {
            "check": "Structure deviation",
            "severity": "critical",
            "status": "fail",
            "notes": "H2 order violates Doc 102.",
        }
    ]
    # Model wrongly self-reports pass despite a critical fail.
    monkeypatch.setattr(
        auditor_module,
        "call_llm",
        lambda **kw: _verdict_response(verdict="pass", findings=findings),
    )
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody."})
    assert result["output"]["verdict"] == "fail"
    assert "critical" in result["output"]["summary"].lower()


def test_auditor_scopes_packaging_criticals(doctrine_corpus, monkeypatch):
    findings = [
        {
            "check": "JSON-LD in both forms (Doc 192 7A)",
            "severity": "critical",
            "status": "fail",
            "scope": "packaging",
            "notes": "No script tag.",
        }
    ]
    monkeypatch.setattr(
        auditor_module,
        "call_llm",
        lambda **kw: _verdict_response(verdict="fail", findings=findings),
    )
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody."})
    out = result["output"]
    assert out["verdict"] == "pass_with_notes"
    assert out["findings"][0]["severity"] == "major"
    assert out["findings"][0]["status"] == "warn"


def test_auditor_content_critical_still_fails_with_packaging(doctrine_corpus, monkeypatch):
    findings = [
        {
            "check": "Stylesheet",
            "severity": "critical",
            "status": "fail",
            "scope": "packaging",
            "notes": "Missing style block.",
        },
        {
            "check": "Claim trust level",
            "severity": "critical",
            "status": "fail",
            "scope": "content",
            "notes": "No Level 2 claim sourced.",
        },
    ]
    monkeypatch.setattr(
        auditor_module,
        "call_llm",
        lambda **kw: _verdict_response(verdict="fail", findings=findings),
    )
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody."})
    assert result["output"]["verdict"] == "fail"


def test_auditor_unknown_scope_defaults_content(doctrine_corpus, monkeypatch):
    findings = [
        {
            "check": "Manifest",
            "severity": "critical",
            "status": "fail",
            "scope": "artifact",
            "notes": "Missing.",
        }
    ]
    monkeypatch.setattr(
        auditor_module,
        "call_llm",
        lambda **kw: _verdict_response(verdict="fail", findings=findings),
    )
    result = run_auditor(doctrine_corpus, {"content": "# Draft\n\nBody."})
    assert result["output"]["verdict"] == "fail"
    assert result["output"]["findings"][0]["scope"] == "content"


def test_auditor_unparseable_json_raises(doctrine_corpus, monkeypatch):
    calls = {"n": 0}

    def bad_llm(**kw):
        calls["n"] += 1
        return "I cannot audit this"

    monkeypatch.setattr(auditor_module, "call_llm", bad_llm)
    with pytest.raises(ValueError, match="parseable JSON"):
        run_auditor(doctrine_corpus, {"content": "# Draft"})
    assert calls["n"] == 2  # initial + one retry, both failed


def test_auditor_retries_once_then_parses(doctrine_corpus, monkeypatch):
    calls = {"n": 0}

    def flaky_llm(**kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return "sure, here you go"
        return _verdict_response()

    monkeypatch.setattr(auditor_module, "call_llm", flaky_llm)
    result = run_auditor(doctrine_corpus, {"content": "# Draft"})
    assert result["output"]["verdict"] == "pass_with_notes"
    assert calls["n"] == 2


def test_auditor_invalid_findings_raise(doctrine_corpus, monkeypatch):
    bad = json.dumps({"verdict": "excellent", "summary": "", "findings": []})
    monkeypatch.setattr(auditor_module, "call_llm", lambda **kw: bad)
    with pytest.raises(ValueError, match="validation"):
        run_auditor(doctrine_corpus, {"content": "# Draft"})


def test_auditor_reads_writer_task_output(doctrine_corpus, monkeypatch):
    task = AgentTask(
        agent_type="writer",
        status="completed",
        input_data={"request": "x"},
        output_data={
            "agent": "writer",
            "provenance": [],
            "output": {
                "title": "T",
                "meta_title": "MT",
                "meta_description": "MDesc",
                "content_markdown": "# T\n\nDraft body.",
            },
        },
        created_by=None,  # not enforced by FK check on SQLite insert path? keep valid below
    )
    # created_by is non-nullable FK; create a user to satisfy it.
    from app.models.user import User
    from app.services.auth_service import hash_password

    from tests.conftest import login  # noqa: F401

    user = User(username="auditor_tester", password_hash=hash_password("pw"), role="writer")
    doctrine_corpus.add(user)
    doctrine_corpus.commit()
    doctrine_corpus.refresh(user)
    task.created_by = user.id
    doctrine_corpus.add(task)
    doctrine_corpus.commit()
    doctrine_corpus.refresh(task)

    captured = {}

    def fake_call_llm(system_prompt, user_message, max_tokens=4096):
        captured["user_message"] = user_message
        return _verdict_response()

    monkeypatch.setattr(auditor_module, "call_llm", fake_call_llm)
    result = run_auditor(doctrine_corpus, {"source_task_id": str(task.id)})
    assert "Draft body." in captured["user_message"]
    assert "MDesc" in captured["user_message"]
    assert result["output"]["verdict"] == "pass_with_notes"


def test_auditor_missing_input_raises(doctrine_corpus):
    with pytest.raises(ValueError, match=r"content.*source_task_id"):
        run_auditor(doctrine_corpus, {})


def test_auditor_unknown_source_task_raises(doctrine_corpus, monkeypatch):
    import uuid

    monkeypatch.setattr(auditor_module, "call_llm", lambda **kw: _verdict_response())
    with pytest.raises(ValueError, match="not found"):
        run_auditor(doctrine_corpus, {"source_task_id": str(uuid.uuid4())})
