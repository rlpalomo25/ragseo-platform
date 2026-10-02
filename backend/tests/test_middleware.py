"""Tests for the request-body size middleware.

The middleware is the only thing standing between an authenticated writer and a
~200 GB write into /tmp, because Starlette spools a multipart body to disk before
any route code runs. Its tests therefore check the *rejection* path in detail and
confirm it does not leak into unrelated routes.
"""

import json

from app.main import app
from app.middleware import (
    DEFAULT_UPLOAD_LIMIT,
    UPLOAD_REQUEST_LIMITS,
    RequestBodyLimitMiddleware,
    _limit_for,
)

DOCTRINE = "/api/ingest/doctrine/upload"
EXTERNAL = "/api/ingest/external/upload"


def post_declaring_length(client, path, length):
    """POST a 1-byte body while *declaring* a larger Content-Length.

    If the middleware works the server answers from the header alone and never
    waits for the bytes that will not arrive. The declared length is asserted in
    detail, because the body itself is not what is under test.
    """
    return client.post(
        path,
        content=b"x",
        headers={
            "Content-Type": "multipart/form-data; boundary=zz",
            "Content-Length": str(length),
        },
    )


def test_oversized_body_is_rejected_before_it_is_read(client):
    for path, limit in UPLOAD_REQUEST_LIMITS.items():
        resp = post_declaring_length(client, path, limit + 1)
        assert resp.status_code == 413, f"{path} accepted a body over its limit"
        detail = resp.json()["detail"]
        assert str(limit) in detail
        assert "Send fewer files" in detail


def test_a_body_exactly_at_the_limit_is_not_rejected_by_the_middleware(client):
    """The cap is on the total, so the boundary value itself must pass through.

    Asserting this matters: an off-by-one that rejected `limit` instead of
    `limit + 1` would silently shrink every limit and look correct in testing.
    The pass-through is proven by the 400 from the multipart parser, which only
    runs once the middleware has declined to reject.
    """
    for path, limit in UPLOAD_REQUEST_LIMITS.items():
        resp = post_declaring_length(client, path, limit)
        assert resp.status_code == 400, f"{path} rejected a body of exactly its limit"
        assert "exceeds" not in resp.json()["detail"]


def test_non_upload_routes_are_untouched(client):
    for path in ("/api/health", "/api/auth/login", "/api/docs"):
        resp = client.get(path)
        assert resp.status_code != 413, f"{path} was rejected by the upload middleware"


def test_an_unlisted_ingest_upload_path_is_bounded_by_default(client):
    """A future /api/ingest/*/upload route must be capped even if not registered."""
    assert _limit_for("/api/ingest/somethingnew/upload") == DEFAULT_UPLOAD_LIMIT
    assert _limit_for("/api/ingest/doctrine/scan") is None


def test_a_malformed_content_length_is_not_treated_as_enormous(client):
    """A junk header must not become a 500 or a false rejection.

    Starlette would reject it later as an invalid request; the middleware's job
    is only to not be the thing that crashes or guesses.
    """
    resp = client.post(
        DOCTRINE,
        content=b"x",
        headers={"Content-Type": "multipart/form-data; boundary=zz", "Content-Length": "abc"},
    )
    assert resp.status_code != 413


def test_the_limit_is_checked_per_route_not_globally(client):
    """The doctrine ceiling must not be applied to the external route.

    External exports are 200 MB each and legitimately need a far larger body, so
    a single global cap would break that feature. A body over the *doctrine*
    ceiling must therefore sail through on the *external* route.
    """
    assert UPLOAD_REQUEST_LIMITS[DOCTRINE] < UPLOAD_REQUEST_LIMITS[EXTERNAL]

    over_doctrine_but_under_external = UPLOAD_REQUEST_LIMITS[DOCTRINE] + 1
    resp = post_declaring_length(client, EXTERNAL, over_doctrine_but_under_external)
    assert resp.status_code == 400, "the doctrine cap leaked onto the external route"

    # Above the external ceiling it must be refused, and by the external number.
    resp = post_declaring_length(client, EXTERNAL, UPLOAD_REQUEST_LIMITS[EXTERNAL] + 1)
    assert resp.status_code == 413
    assert str(UPLOAD_REQUEST_LIMITS[EXTERNAL]) in resp.json()["detail"]


def test_the_middleware_is_registered_on_the_app():
    """Guards against the import being added to main.py but never attached."""
    registered = [m.cls for m in app.user_middleware]
    assert RequestBodyLimitMiddleware in registered, registered


def test_middleware_returns_a_json_body_not_a_bare_status(client):
    resp = post_declaring_length(client, DOCTRINE, UPLOAD_REQUEST_LIMITS[DOCTRINE] + 1)
    assert resp.headers["content-type"].startswith("application/json")
    # Must be parseable, since the frontend surfaces `detail` verbatim.
    assert "detail" in json.loads(resp.content)
