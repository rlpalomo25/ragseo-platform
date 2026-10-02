"""Reject oversized request bodies before anything reads them.

Why this exists as middleware rather than as a route argument
--------------------------------------------------------------
Both upload endpoints are ``multipart/form-data``, and Starlette's
``MultiPartParser`` spools the *entire* body to a temp file before the endpoint
function is entered. Per-file byte caps checked inside the handler therefore run
only after the disk write has already happened. With the parser's stock
``max_files=1000`` and a 200 MB per-file export cap, a single authenticated
request could put ~200 GB into ``/tmp`` before a line of our code ran.

The file *count* cannot be capped at the parser either, without hand-rolling a
custom Request class: ``File(..., max_length=N)`` looks like it should do it, but
on FastAPI 0.115 that argument is only recorded in the pydantic ``FieldInfo`` and
is never forwarded to ``Request.form(max_files=...)``, so it is silently ignored
for a ``list[UploadFile]``. Verified, not assumed.

What this does
--------------
A ``Content-Length`` check that answers 413 *before* the body is read. This is the
only place the large case can be stopped early, and it costs one header parse. It
cannot be the whole story, because ``Content-Length`` is optional and an attacker
may simply omit it or lie about it — so the routes also enforce the count and the
aggregate byte total on the stream itself. Defence in depth: cheap rejection for
the honest-but-mistaken case, stream enforcement for the rest.

The ceiling is per-route and deliberately above the batch cap, to leave room for
multipart framing overhead. It is not a substitute for the in-handler caps.
"""

import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

#: Per-route request ceilings, keyed by path. Mirrors the batch caps in
#: ``app.routers.ingest`` and must stay slightly above them for multipart
#: framing (boundaries and part headers).
UPLOAD_REQUEST_LIMITS: dict[str, int] = {
    "/api/ingest/doctrine/upload": 60 * 1024 * 1024,
    "/api/ingest/external/upload": 510 * 1024 * 1024,
}

#: Applied to any other multipart upload path that is added without an explicit
#: entry here, so a future endpoint is bounded by default rather than open.
DEFAULT_UPLOAD_LIMIT = 512 * 1024 * 1024


def _limit_for(path: str) -> int | None:
    if path in UPLOAD_REQUEST_LIMITS:
        return UPLOAD_REQUEST_LIMITS[path]
    if path.startswith("/api/ingest/") and path.endswith("/upload"):
        return DEFAULT_UPLOAD_LIMIT
    return None


class RequestBodyLimitMiddleware(BaseHTTPMiddleware):
    """Answer 413 on Content-Length before the request body is read."""

    async def dispatch(self, request: Request, call_next):
        limit = _limit_for(request.url.path)
        if limit is not None:
            raw = request.headers.get("content-length")
            if raw is not None:
                try:
                    length = int(raw)
                except ValueError:
                    length = None
                if length is not None and length > limit:
                    return Response(
                        status_code=413,
                        content=json.dumps(
                            {
                                "detail": (
                                    f"Request body of {length} bytes exceeds the "
                                    f"{limit} byte limit for this endpoint. "
                                    "Send fewer files at a time."
                                )
                            }
                        ),
                        media_type="application/json",
                        headers={"Connection": "close"},
                    )
        return await call_next(request)
