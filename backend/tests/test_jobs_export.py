import pytest

from app.models.agent_task import AgentTask
from app.models.job import AgentJob, JobStage
from app.services.markdown_export import build_markdown, slugify
from tests.conftest import login


@pytest.fixture(autouse=True)
def no_celery(monkeypatch):
    monkeypatch.setattr(
        "app.tasks.run_agent_task.delay",
        lambda *args, **kwargs: None,
    )


def _writer_output(**overrides):
    output = {
        "title": "Gutter Guard Review Roundup",
        "meta_title": "Best Gutter Guards: 6 Picks for 2026",
        "meta_description": "We tested 6 gutter guards: " 'prices, coverage, and install time.',
        "brand": "mastershield",
        "content_type": "comparison",
        "archetype": "comparison",
        "content_markdown": "# Gutter Guard Review Roundup\n\nBody stays verbatim.\n",
    }
    output.update(overrides)
    return output


def _make_job(db, user, status="approved", title="Gutter Guard Review Roundup", with_writer=True):
    job = AgentJob(
        title=title,
        request="Write a comparison page",
        status=status,
        created_by=user.id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    if with_writer:
        task = AgentTask(
            agent_type="writer",
            status="completed",
            input_data={},
            output_data={"agent": "writer", "output": _writer_output()},
            created_by=user.id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        stage = JobStage(
            job_id=job.id,
            sequence=2,
            agent_type="writer",
            task_id=task.id,
            status="completed",
        )
        db.add(stage)
        db.commit()

    return job


def _export(client, job):
    return client.get(f"/api/jobs/{job.id}/export.md")


# --- auth -------------------------------------------------------------------


def test_export_requires_auth(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    assert _export(client, job).status_code == 401


def test_export_unknown_job_is_404(client, test_user):
    login(client, "testwriter", "secret123")
    assert client.get("/api/jobs/00000000-0000-0000-0000-000000000000/export.md").status_code == 404


def test_export_admin_allowed(client, db_session, admin_user):
    job = _make_job(db_session, admin_user)
    login(client, "testadmin", "adminpass")
    assert _export(client, job).status_code == 200


# --- status gate ------------------------------------------------------------


@pytest.mark.parametrize("status", ["running", "awaiting_approval", "failed", "cancelled"])
def test_export_rejected_unless_approved(client, db_session, test_user, status):
    job = _make_job(db_session, test_user, status=status)
    login(client, "testwriter", "secret123")
    response = _export(client, job)
    assert response.status_code == 409
    assert "approved" in response.json()["detail"]


def test_export_approved_without_draft_is_404(client, db_session, test_user):
    job = _make_job(db_session, test_user, with_writer=False)
    login(client, "testwriter", "secret123")
    assert _export(client, job).status_code == 404


# --- happy path -------------------------------------------------------------


def test_export_returns_markdown_headers_and_body(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    login(client, "testwriter", "secret123")

    response = _export(client, job)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert response.headers["content-disposition"] == (
        'attachment; filename="gutter-guard-review-roundup.md"'
    )

    body = response.text
    assert body.startswith("---\n")
    assert "\n---\n\n# Gutter Guard Review Roundup\n" in body
    # Draft content is preserved verbatim.
    assert body.endswith("# Gutter Guard Review Roundup\n\nBody stays verbatim.\n")


def test_export_front_matter_carries_all_six_fields(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    login(client, "testwriter", "secret123")

    body = _export(client, job).text
    front_matter = body.split("---")[1]
    assert 'title: "Gutter Guard Review Roundup"' in front_matter
    assert 'meta_title: "Best Gutter Guards: 6 Picks for 2026"' in front_matter
    # A colon inside the value must not break the YAML mapping.
    assert 'meta_description: "We tested 6 gutter guards: prices, coverage, and install time."' in front_matter
    assert 'brand: "mastershield"' in front_matter
    assert 'content_type: "comparison"' in front_matter
    assert 'archetype: "comparison"' in front_matter


def test_export_omits_absent_optional_fields(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    task = db_session.query(AgentTask).filter(AgentTask.agent_type == "writer").one()
    task.output_data = {
        "agent": "writer",
        "output": _writer_output(archetype=None, brand=None, content_type=None),
    }
    db_session.commit()

    login(client, "testwriter", "secret123")
    front_matter = _export(client, job).text.split("---")[1]
    assert "archetype" not in front_matter
    assert "brand" not in front_matter
    assert "content_type" not in front_matter
    assert "null" not in front_matter
    assert 'title: "Gutter Guard Review Roundup"' in front_matter


def test_export_escapes_quotes_and_newlines(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    task = db_session.query(AgentTask).filter(AgentTask.agent_type == "writer").one()
    task.output_data = {
        "agent": "writer",
        "output": _writer_output(title='He said "best"\nsecond line'),
    }
    db_session.commit()

    login(client, "testwriter", "secret123")
    front_matter = _export(client, job).text.split("---")[1]
    # json.dumps escapes the quote and keeps the newline on one logical line.
    assert 'title: "He said \\"best\\"\\nsecond line"' in front_matter


# --- stage selection --------------------------------------------------------


def test_export_prefers_highest_sequence_writer_stage(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    login(client, "testwriter", "secret123")

    # A revision loop: a newer writer stage with different content.
    task = AgentTask(
        agent_type="writer",
        status="completed",
        input_data={},
        output_data={"agent": "writer", "output": _writer_output(title="Second Draft")},
        created_by=test_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    db_session.add(
        JobStage(job_id=job.id, sequence=4, agent_type="writer", task_id=task.id, status="completed")
    )
    db_session.commit()

    body = _export(client, job).text
    assert 'title: "Second Draft"' in body
    assert "Gutter Guard Review Roundup\"" not in body


def test_export_skips_writer_stage_with_empty_content(client, db_session, test_user):
    job = _make_job(db_session, test_user)
    login(client, "testwriter", "secret123")

    # Newest stage ran but produced nothing usable (e.g. failed mid-write).
    task = AgentTask(
        agent_type="writer",
        status="failed",
        input_data={},
        output_data={"agent": "writer", "output": _writer_output(content_markdown="   ")},
        created_by=test_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    db_session.add(
        JobStage(job_id=job.id, sequence=5, agent_type="writer", task_id=task.id, status="failed")
    )
    db_session.commit()

    assert 'title: "Gutter Guard Review Roundup"' in _export(client, job).text


def test_export_ignores_router_stage_output(client, db_session, test_user):
    """Router output has no `output` wrapper; it must not raise."""
    job = _make_job(db_session, test_user)
    router_task = AgentTask(
        agent_type="router",
        status="completed",
        input_data={},
        output_data={"agent": "router", "brand": "mastershield", "content_type": "comparison"},
        created_by=test_user.id,
    )
    db_session.add(router_task)
    db_session.commit()
    db_session.refresh(router_task)
    db_session.add(
        JobStage(job_id=job.id, sequence=3, agent_type="router", task_id=router_task.id, status="completed")
    )
    db_session.commit()

    login(client, "testwriter", "secret123")
    assert _export(client, job).status_code == 200


# --- filename ---------------------------------------------------------------


def test_export_filename_falls_back_to_job_id(client, db_session, test_user):
    """Neither the draft title nor the job title is usable, so the job id carries it."""
    job = _make_job(db_session, test_user, title="!!! ??? ***", with_writer=False)
    login(client, "testwriter", "secret123")

    task = AgentTask(
        agent_type="writer",
        status="completed",
        input_data={},
        output_data={"agent": "writer", "output": _writer_output(title="!!! ??? ***")},
        created_by=test_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    db_session.add(
        JobStage(job_id=job.id, sequence=2, agent_type="writer", task_id=task.id, status="completed")
    )
    db_session.commit()

    disposition = _export(client, job).headers["content-disposition"]
    assert disposition == f'attachment; filename="{job.id}.md"'


def test_export_filename_falls_back_to_job_title_before_job_id(client, db_session, test_user):
    """Draft title unusable but the job title is fine: prefer the job title."""
    job = _make_job(db_session, test_user, title="Gutter Guard Roundup", with_writer=False)
    login(client, "testwriter", "secret123")

    task = AgentTask(
        agent_type="writer",
        status="completed",
        input_data={},
        output_data={"agent": "writer", "output": _writer_output(title="!!! ??? ***")},
        created_by=test_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    db_session.add(
        JobStage(job_id=job.id, sequence=2, agent_type="writer", task_id=task.id, status="completed")
    )
    db_session.commit()

    disposition = _export(client, job).headers["content-disposition"]
    assert disposition == 'attachment; filename="gutter-guard-roundup.md"'


def test_slugify_rules():
    assert slugify("Gutter Guard Review: 6 Picks!", "fb") == "gutter-guard-review-6-picks"
    assert slugify(None, "fallback title") == "fallback-title"
    assert slugify("!!!", "fallback") == "fallback"
    assert slugify("", "") == "draft"
    # Non-ASCII is transliterated, not dropped.
    assert slugify("Café Sweep — Révision", "fb") == "cafe-sweep-revision"


# --- audit ------------------------------------------------------------------


def test_export_writes_audit_row(client, db_session, test_user):
    from app.models.audit import AuditLog

    job = _make_job(db_session, test_user)
    login(client, "testwriter", "secret123")
    _export(client, job)

    entries = db_session.query(AuditLog).filter(AuditLog.action == "job.export").all()
    assert len(entries) == 1
    assert str(job.id) in entries[0].detail
    assert entries[0].username == "testwriter"


def test_export_rejection_writes_no_audit_row(client, db_session, test_user):
    from app.models.audit import AuditLog

    job = _make_job(db_session, test_user, status="running")
    login(client, "testwriter", "secret123")
    assert _export(client, job).status_code == 409
    assert db_session.query(AuditLog).filter(AuditLog.action == "job.export").count() == 0


# --- routing regression -----------------------------------------------------


def test_fastapi_docs_does_not_shadow_frontend_docs(client):
    """The frontend owns /docs; FastAPI's explorers live under /api/meta."""
    from app.main import app

    assert app.docs_url == "/api/meta/docs"
    assert app.redoc_url == "/api/meta/redoc"


# --- pure helpers -----------------------------------------------------------


def test_build_markdown_separator_shape():
    body = build_markdown(_writer_output())
    assert body.startswith("---\n")
    assert "\n---\n\n" in body
    # Front matter is the opening fence plus exactly the six fields, and no value
    # leaks a raw newline (json.dumps escapes them).
    block = body.split("\n---\n")[0]
    lines = block.split("\n")
    assert lines[0] == "---"
    assert [line.split(":")[0] for line in lines[1:]] == [
        "title",
        "meta_title",
        "meta_description",
        "brand",
        "content_type",
        "archetype",
    ]