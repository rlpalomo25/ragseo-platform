import pytest

from tests.conftest import login


@pytest.fixture(autouse=True)
def no_celery(monkeypatch):
    recorded = []
    monkeypatch.setattr(
        "app.tasks.run_agent_task.delay",
        lambda *args, **kwargs: recorded.append(args),
    )
    return recorded


def test_create_job_requires_auth(client):
    assert client.post("/api/jobs", json={"request": "Write a comparison page please"}).status_code == 401


def test_create_job_dispatches_router(client, test_user, no_celery):
    login(client, "testwriter", "secret123")
    response = client.post(
        "/api/jobs",
        json={
            "request": "Write a MasterShield vs LeafFilter comparison page",
            "brand": "mastershield",
            "content_type": "comparison",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "running"
    assert len(no_celery) == 1  # router dispatched
    assert no_celery[0][1] == "router"


def test_create_job_validates_request_length(client, test_user):
    login(client, "testwriter", "secret123")
    response = client.post("/api/jobs", json={"request": "short"})
    assert response.status_code == 422


def test_list_and_get_job_detail(client, test_user, db_session):
    from app.services.orchestrator import create_job

    job = create_job(db_session, created_by=test_user.id, request="Write a local page for Klean Gutter")
    login(client, "testwriter", "secret123")

    listed = client.get("/api/jobs").json()["jobs"]
    assert any(j["id"] == str(job.id) for j in listed)

    detail = client.get(f"/api/jobs/{job.id}").json()
    assert detail["request"] == "Write a local page for Klean Gutter"
    assert len(detail["stages"]) == 1
    assert detail["stages"][0]["agent_type"] == "router"
    assert detail["stages"][0]["task_id"] is not None


def test_approve_gate_enforced_over_api(client, test_user, db_session):
    from app.services.orchestrator import create_job

    job = create_job(db_session, created_by=test_user.id, request="Write a page about gutter guards")
    login(client, "testwriter", "secret123")

    early = client.post(f"/api/jobs/{job.id}/approve")
    assert early.status_code == 409

    job.status = "awaiting_approval"
    db_session.commit()
    ok = client.post(f"/api/jobs/{job.id}/approve")
    assert ok.status_code == 200
    assert ok.json()["status"] == "approved"


def test_cancel_job_over_api(client, test_user, db_session):
    from app.services.orchestrator import create_job

    job = create_job(db_session, created_by=test_user.id, request="Write a page about gutter guards")
    login(client, "testwriter", "secret123")
    response = client.post(f"/api/jobs/{job.id}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

    again = client.post(f"/api/jobs/{job.id}/cancel")
    assert again.status_code == 409


def test_job_detail_404_on_bad_uuid(client, test_user):
    login(client, "testwriter", "secret123")
    assert client.get("/api/jobs/not-a-uuid").status_code == 422


def test_list_jobs_filters_by_brand_and_status(client, test_user, db_session):
    from app.services.orchestrator import create_job

    job_a = create_job(
        db_session,
        created_by=test_user.id,
        request="MasterShield comparison page",
        brand="mastershield",
        content_type="comparison",
    )
    create_job(
        db_session,
        created_by=test_user.id,
        request="Klean Gutter local page",
        brand="klean_gutter",
        content_type="local_page",
    )
    job_a.status = "awaiting_approval"
    db_session.commit()

    login(client, "testwriter", "secret123")

    by_brand = client.get("/api/jobs", params={"brand": "mastershield"}).json()["jobs"]
    assert len(by_brand) == 1
    assert by_brand[0]["id"] == str(job_a.id)

    by_status = client.get("/api/jobs", params={"status": "awaiting_approval"}).json()["jobs"]
    assert len(by_status) == 1
    assert by_status[0]["id"] == str(job_a.id)

    both = client.get("/api/jobs", params={"brand": "mastershield", "content_type": "comparison"}).json()[
        "jobs"
    ]
    assert len(both) == 1
