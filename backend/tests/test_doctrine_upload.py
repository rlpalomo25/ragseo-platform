"""Doctrine upload (POST /api/ingest/doctrine/upload) and the folder-union scan.

The load-bearing test here is :func:`test_reconcile_does_not_mark_uploads_missing`.
``reconcile_doctrine`` runs hourly on the celery worker and used to glob only
``settings.doctrine_path``; the missing-sweep then flipped every uploaded
document to ``status="missing"`` within the hour. That blocked all upload work,
so it gets its own explicit regression test rather than riding along with the
endpoint tests.
"""

from pathlib import Path

import pytest
from app.config import get_settings
from app.models.chunk import DocChunk
from app.models.document import Document
from app.routers import ingest as ingest_router
from app.services.doc_ingestion import (
    ingest_all_docs,
    ingest_files,
    reconcile_doctrine,
    scan_doctrine_files,
)
from app.services.uploads import safe_filename


def write_doc(directory, name, body="# Title\n\nBody text.\n"):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(body, encoding="utf-8")
    return path


@pytest.fixture()
def doctrine_dirs(tmp_path, monkeypatch):
    """A baked library folder and a separate writable upload folder."""
    settings = get_settings()
    baked = tmp_path / "baked"
    uploads = tmp_path / "uploads_doctrine"
    baked.mkdir()
    monkeypatch.setattr(settings, "doctrine_path", str(baked))
    monkeypatch.setattr(settings, "doctrine_upload_path", str(uploads))
    return baked, uploads


def upload(client, names_contents):
    files = [("files", (name, body, "text/markdown")) for name, body in names_contents]
    return client.post("/api/ingest/doctrine/upload", files=files)


def login_writer(client):
    from tests.conftest import login

    return login(client, "testwriter", "secret123")


def login_admin(client):
    from tests.conftest import login

    return login(client, "testadmin", "adminpass")


# --------------------------------------------------------------- folder union


def test_reconcile_does_not_mark_uploads_missing(db_session, doctrine_dirs):
    """THE blocker: an upload in a non-baked folder must survive the hourly sweep."""
    _baked, uploads = doctrine_dirs
    write_doc(uploads, "Doc 400_ Uploaded Protocol.md", "# Uploaded Protocol\n\nNew guidance.\n")

    first = reconcile_doctrine(db_session)
    assert first["created"] == 1
    assert first["missing"] == 0

    doc = db_session.query(Document).filter(Document.doc_number == "400").one()
    assert doc.status == "active"
    assert doc.filename == "Doc 400_ Uploaded Protocol.md"

    # Run the sweep repeatedly: this is what the hourly beat schedule does.
    for _ in range(3):
        stats = reconcile_doctrine(db_session)
        assert stats["missing"] == 0
        assert stats["created"] == 0

    db_session.refresh(doc)
    assert doc.status == "active", "upload was flipped to missing by reconcile"
    assert db_session.query(DocChunk).filter(DocChunk.document_id == doc.id).count() >= 1


def test_reconcile_marks_baked_doc_missing_when_its_file_disappears(db_session, doctrine_dirs):
    """The union must not stop the sweep from doing its actual job."""
    baked, _uploads = doctrine_dirs
    write_doc(baked, "Doc 100_ Library Doc.md")
    reconcile_doctrine(db_session)

    (baked / "Doc 100_ Library Doc.md").unlink()
    stats = reconcile_doctrine(db_session)
    assert stats["missing"] == 1

    doc = db_session.query(Document).filter(Document.doc_number == "100").one()
    assert doc.status == "missing"


def test_reconcile_restores_a_doc_whose_file_comes_back(db_session, doctrine_dirs):
    """A restored file must become active again, not stay invisible forever."""
    baked, _uploads = doctrine_dirs
    path = write_doc(baked, "Doc 100_ Library Doc.md")
    reconcile_doctrine(db_session)

    path.unlink()
    reconcile_doctrine(db_session)
    assert db_session.query(Document).filter(Document.doc_number == "100").one().status == "missing"

    write_doc(baked, "Doc 100_ Library Doc.md", "# Library Doc\n\nBack again.\n")
    stats = reconcile_doctrine(db_session)
    assert stats["missing"] == 0
    assert stats["updated"] == 1

    doc = db_session.query(Document).filter(Document.doc_number == "100").one()
    assert doc.status == "active"
    assert "Back again." in doc.content


def test_ingest_all_docs_scans_both_folders(db_session, doctrine_dirs):
    baked, uploads = doctrine_dirs
    write_doc(baked, "Doc 100_ Library Doc.md")
    write_doc(uploads, "Doc 400_ Uploaded Protocol.md")

    stats = ingest_all_docs(db_session)
    assert stats["created"] == 2
    numbers = {d.doc_number for d in db_session.query(Document).all()}
    assert numbers == {"100", "400"}


def test_scan_deduplicates_by_filename_with_baked_first(db_session, doctrine_dirs):
    """A shadowing upload is ignored by the scan (and refused at upload time)."""
    baked, uploads = doctrine_dirs
    write_doc(baked, "Doc 100_ Shared Name.md", "# Shared Name\n\nBaked body.\n")
    write_doc(uploads, "Doc 100_ Shared Name.md", "# Shared Name\n\nUploaded body.\n")

    scanned = scan_doctrine_files()
    assert [p.parent for p in scanned] == [
        baked,
    ]
    assert len(scanned) == 1

    ingest_all_docs(db_session)
    doc = db_session.query(Document).filter(Document.doc_number == "100").one()
    assert "Baked body." in doc.content


def test_scan_skips_dotfiles_and_zone_identifiers(doctrine_dirs):
    baked, _uploads = doctrine_dirs
    write_doc(baked, "Doc 100_ Real Doc.md")
    (baked / ".hidden.md").write_text("nope", encoding="utf-8")
    (baked / "Doc 101_ Real Doc.md:Zone.Identifier").write_text("nope", encoding="utf-8")

    assert [p.name for p in scan_doctrine_files()] == ["Doc 100_ Real Doc.md"]


def test_upload_folder_absence_does_not_break_the_scan(db_session, tmp_path, monkeypatch):
    """A missing upload dir (fresh prod before the mount exists) is not fatal."""
    settings = get_settings()
    baked = tmp_path / "baked"
    baked.mkdir()
    write_doc(baked, "Doc 100_ Library Doc.md")
    monkeypatch.setattr(settings, "doctrine_path", str(baked))
    monkeypatch.setattr(settings, "doctrine_upload_path", str(tmp_path / "nope"))

    assert reconcile_doctrine(db_session)["created"] == 1


# ------------------------------------------------------------- upload: happy path


def test_upload_requires_auth(client, doctrine_dirs):
    assert upload(client, [("Doc 100_X.md", b"# X\n")]).status_code == 401


def test_writer_can_upload(client, test_user, db_session, doctrine_dirs):
    baked, uploads = doctrine_dirs
    login_writer(client)

    r = upload(client, [("Doc 400_ Brand Voice.md", b"# Brand Voice\n\nWarm and direct.\n")])
    assert r.status_code == 200
    body = r.json()
    assert body["created"] == 1
    assert body["errors"] == 0
    assert body["files"][0]["filename"] == "Doc 400_ Brand Voice.md"
    assert body["files"][0]["doc_number"] == "400"
    assert body["files"][0]["title"] == "Brand Voice"
    assert body["files"][0]["status"] == "created"
    assert body["files"][0]["chunks"] >= 1
    assert body["files"][0]["superseded"] is None

    # Saved in the writable folder only; the baked library stays untouched.
    assert (uploads / "Doc 400_ Brand Voice.md").is_file()
    assert not (baked / "Doc 400_ Brand Voice.md").exists()

    doc = db_session.query(Document).filter(Document.doc_number == "400").one()
    assert doc.status == "active"
    assert db_session.query(DocChunk).filter(DocChunk.document_id == doc.id).count() >= 1


def test_admin_can_upload(client, admin_user, db_session, doctrine_dirs):
    login_admin(client)
    assert upload(client, [("Doc 401_ Admin Doc.md", b"# Admin Doc\n\nBody.\n")]).status_code == 200


def test_upload_audits_the_action(client, admin_user, db_session, doctrine_dirs):
    from app.models.audit import AuditLog

    login_admin(client)
    upload(client, [("Doc 402_ Audited Doc.md", b"# Audited Doc\n\nBody.\n")])

    row = db_session.query(AuditLog).filter(AuditLog.action == "doctrine.upload").one()
    assert row.username == "testadmin"
    assert row.route == "/api/ingest/doctrine/upload"
    assert "1 created" in row.detail


def test_upload_multiple_files_in_one_request(client, admin_user, db_session, doctrine_dirs):
    _baked, uploads = doctrine_dirs
    login_admin(client)

    r = upload(
        client,
        [
            ("Doc 403_ First.md", b"# First\n\nOne.\n"),
            ("Doc 403-1_ Sub.md", b"# Sub\n\nTwo.\n"),
        ],
    )
    assert r.status_code == 200
    body = r.json()
    assert body["created"] == 2
    assert {f["doc_number"] for f in body["files"]} == {"403", "403-1"}
    assert len(list(uploads.glob("*.md"))) == 2


# ------------------------------------------------------------- upload: supersede


def test_upload_supersedes_the_active_doc_and_names_it(client, admin_user, db_session, doctrine_dirs):
    """Auto-supersede stays, but the response says what it displaced."""
    from tests.conftest import seed_doc

    _baked, _uploads = doctrine_dirs
    old = seed_doc(db_session, "500", "Old Protocol", "# Old\n\nOld body.\n", version="1.0")
    old.filename = "Doc 500_ Old Protocol.md"
    db_session.commit()

    login_admin(client)
    r = upload(client, [("Doc 500_ New Protocol.md", b"# New Protocol\n\nVersion 2.0\n\nNew body.\n")])
    body = r.json()
    assert body["created"] == 1
    assert body["files"][0]["superseded"] == "500 (Old Protocol)"

    db_session.refresh(old)
    assert old.status == "superseded"
    new = db_session.query(Document).filter(Document.doc_number == "500", Document.status == "active").one()
    assert new.filename == "Doc 500_ New Protocol.md"
    assert new.version == "2.0"


def test_upload_same_name_updates_in_place_without_superseding(client, admin_user, db_session, doctrine_dirs):
    """Re-uploading an unchanged filename updates in place and reports no supersede."""
    _baked, _uploads = doctrine_dirs
    login_admin(client)

    first = upload(client, [("Doc 501_ Stable Doc.md", b"# Stable\n\nVersion 1.0\n\nOne.\n")]).json()
    assert first["files"][0]["superseded"] is None

    second = upload(client, [("Doc 501_ Stable Doc.md", b"# Stable\n\nVersion 2.0\n\nTwo.\n")]).json()
    assert second["updated"] == 1
    assert second["created"] == 0
    assert second["files"][0]["superseded"] is None

    rows = db_session.query(Document).filter(Document.doc_number == "501").all()
    assert len(rows) == 1
    assert rows[0].version == "2.0"


def test_upload_identical_bytes_reports_unchanged(client, admin_user, db_session, doctrine_dirs):
    _baked, uploads = doctrine_dirs
    login_admin(client)
    payload = ("Doc 502_ Idempotent.md", b"# Idempotent\n\nSame bytes.\n")

    assert upload(client, [payload]).json()["created"] == 1
    second = upload(client, [payload]).json()
    assert second["unchanged"] == 1
    assert second["created"] == 0
    assert second["updated"] == 0
    assert len(list(uploads.glob("*.md"))) == 1


def test_upload_changed_superseded_filename_reactivates_it(client, admin_user, db_session, doctrine_dirs):
    """A doc whose file changed after being superseded must return to active."""
    from tests.conftest import seed_doc

    _baked, _uploads = doctrine_dirs
    old = seed_doc(db_session, "503", "Old", "# Old\n\nOld.\n")
    old.filename = "Doc 503_ Renamed.md"
    old.status = "superseded"
    db_session.commit()

    login_admin(client)
    upload(client, [("Doc 503_ Renamed.md", b"# Old\n\nEdited.\n")])

    db_session.refresh(old)
    assert old.status == "active"
    assert "Edited." in old.content


# ------------------------------------------------------------ upload: validation


def test_upload_rejects_non_markdown(client, admin_user, doctrine_dirs):
    _baked, uploads = doctrine_dirs
    login_admin(client)
    r = upload(client, [("Doc 600_ Notes.txt", b"plain text")])
    assert r.status_code == 400
    assert "not a markdown" in r.json()["detail"]
    assert not uploads.exists() or not list(uploads.glob("*"))


def test_upload_rejects_filename_without_a_doc_number(client, admin_user, db_session, doctrine_dirs):
    """`random.md` would become doc_number="random" — permanent under the partial unique index."""
    _baked, uploads = doctrine_dirs
    login_admin(client)
    r = upload(client, [("random.md", b"# Random\n\nBody.\n")])
    assert r.status_code == 400
    assert "recognisable doc number" in r.json()["detail"]
    assert not list(uploads.glob("*.md"))
    assert db_session.query(Document).count() == 0


def test_upload_rejects_doc_number_without_a_title_separator(client, admin_user, doctrine_dirs):
    """`Doc 100 - Something.md` parses the whole name as the doc_number."""
    login_admin(client)
    r = upload(client, [("Doc 100 - Something.md", b"# Something\n\nBody.\n")])
    assert r.status_code == 400
    assert "recognisable doc number" in r.json()["detail"]


def test_upload_rejects_a_doc_number_that_is_not_at_the_start(client, admin_user, doctrine_dirs):
    """`old Doc 100_Title.md` must not be allowed to become Doc 100.

    The frontend card anchors its DOC_NAME check, so an unanchored backend
    pattern would let an API-only caller slip a name past the UI's own rule.
    """
    login_admin(client)
    r = upload(client, [("old Doc 100_Title.md", b"# Sneaky\n\nBody.\n")])
    assert r.status_code == 400
    assert "recognisable doc number" in r.json()["detail"]


def test_uppercase_extension_survives_the_hourly_sweep(client, admin_user, db_session, doctrine_dirs):
    """A Windows-authored `.MD` is accepted, so the scan must see it too.

    `glob("*.md")` is case-sensitive on Linux: without a case-insensitive suffix
    match the file would be ingested, reported as live, and then flipped to
    `missing` by the next hourly reconcile.
    """
    _baked, uploads = doctrine_dirs
    login_admin(client)
    r = upload(client, [("Doc 603_ Windows Authored.MD", b"# Windows Authored\n\nBody.\n")])
    assert r.status_code == 200
    assert r.json()["created"] == 1

    for _ in range(2):
        assert reconcile_doctrine(db_session)["missing"] == 0
    doc = db_session.query(Document).filter(Document.doc_number == "603").one()
    assert doc.status == "active"
    assert (uploads / "Doc 603_ Windows Authored.MD").is_file()


def test_scan_matches_extensions_case_insensitively(doctrine_dirs):
    """Unit-level guard on the scan itself, independent of the HTTP path."""
    _baked, uploads = doctrine_dirs
    write_doc(uploads, "Doc 604_ Mixed Case.Md", "# Mixed\n")
    write_doc(uploads, "Doc 605_ Ignored.txt", "not markdown\n")
    names = {p.name for p in scan_doctrine_files()}
    assert "Doc 604_ Mixed Case.Md" in names
    assert "Doc 605_ Ignored.txt" not in names


def test_upload_rejects_overlong_filename(client, admin_user, doctrine_dirs):
    login_admin(client)
    name = "Doc 601_" + ("a" * 300) + ".md"
    r = upload(client, [(name, b"# Too long\n")])
    assert r.status_code == 400
    assert "longer than 255" in r.json()["detail"]


def test_upload_rejects_oversized_file(client, admin_user, doctrine_dirs):
    _baked, uploads = doctrine_dirs
    login_admin(client)
    r = upload(client, [("Doc 602_ Huge.md", b"x" * (10 * 1024 * 1024 + 1))])
    assert r.status_code == 413
    assert "10 MB" in r.json()["detail"]
    assert not list(uploads.glob("*.md"))


def test_upload_rejects_a_baked_library_filename(client, admin_user, db_session, doctrine_dirs):
    """409, mirroring the baked-name refusal on the external delete handler."""
    baked, _uploads = doctrine_dirs
    write_doc(baked, "Doc 100_ Library Doc.md")
    login_admin(client)

    r = upload(client, [("Doc 100_ Library Doc.md", b"# Library Doc\n\nHijacked.\n")])
    assert r.status_code == 409
    assert "baked doctrine library" in r.json()["detail"]
    assert "Baked body." not in (baked / "Doc 100_ Library Doc.md").read_text()
    assert db_session.query(Document).count() == 0


def test_upload_rejects_the_whole_batch_on_one_bad_name(client, admin_user, db_session, doctrine_dirs):
    """No half-applied batch: a typo must not leave half of it on disk."""
    _baked, uploads = doctrine_dirs
    login_admin(client)

    r = upload(
        client,
        [
            ("Doc 603_ Good.md", b"# Good\n\nBody.\n"),
            ("oops.pdf", b"%PDF-1.4"),
        ],
    )
    assert r.status_code == 400
    assert not list(uploads.glob("*.md"))
    assert db_session.query(Document).count() == 0


def test_upload_rejects_a_batch_that_sanitises_to_nothing(client, admin_user, doctrine_dirs):
    """Every part reduces to an unusable basename -> 400, not a silent no-op."""
    login_admin(client)
    r = upload(client, [("..", b"whatever")])
    assert r.status_code == 400
    assert "No usable .md files" in r.json()["detail"]


def test_upload_leaves_nothing_behind_when_a_later_file_is_oversized(
    client, admin_user, db_session, doctrine_dirs, monkeypatch
):
    """A 413 must not half-apply the batch.

    The caller reads a 413 as "nothing was saved". If the earlier file were
    already in the upload dir, the hourly reconcile would ingest it on the next
    sweep and the database would hold a document the response disowned.
    """
    import app.routers.ingest as ingest_router

    _baked, uploads = doctrine_dirs
    monkeypatch.setattr(ingest_router, "MAX_DOCTRINE_UPLOAD_BYTES", 32)
    login_admin(client)
    r = upload(
        client,
        [
            ("Doc 610_First.md", b"# First\n\nFine on its own.\n"),
            ("Doc 611_ Too Big.md", b"x" * 256),
        ],
    )
    assert r.status_code == 413
    # Ideally the folder is never created at all — nothing is moved in until
    # every file has passed the cap.
    assert not uploads.exists() or not list(uploads.iterdir())
    assert db_session.query(Document).count() == 0


def test_upload_streams_rather_than_buffering_the_batch(client, admin_user, doctrine_dirs, monkeypatch):
    """Peak memory must not scale with file size.

    `UploadFile.size` is hardcoded to 0 by starlette's multipart parser and never
    updated, so the only way to enforce a byte cap is to read the bytes — which
    is exactly why they have to be streamed in chunks and staged, not collected
    into a list. A single read() of a 256-byte file is larger than CHUNK_BYTES,
    so counting distinct reads proves the stream is being used.
    """
    import app.routers.ingest as ingest_router
    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    monkeypatch.setattr(ingest_router, "MAX_DOCTRINE_UPLOAD_BYTES", 4096)
    monkeypatch.setattr(uploads_service, "CHUNK_BYTES", 64)

    reads: list[int] = []
    real_stage = uploads_service.stage_uploads

    async def counting_stage(entries, dest_dir, *, max_bytes, max_total_bytes=None):
        for _name, upload in entries:
            original_read = upload.read

            async def read(size=-1, _o=original_read):
                reads.append(size)
                return await _o(size)

            upload.read = read
        return await real_stage(entries, dest_dir, max_bytes=max_bytes)

    monkeypatch.setattr(uploads_service, "stage_uploads", counting_stage)
    monkeypatch.setattr(ingest_router, "stage_uploads", counting_stage)

    login_admin(client)
    r = upload(client, [("Doc 612_ Streamed.md", b"y" * 256)])
    assert r.status_code == 200
    assert r.json()["created"] == 1
    assert reads and set(reads) == {uploads_service.CHUNK_BYTES}, f"not chunked: {reads}"
    assert (uploads / "Doc 612_ Streamed.md").is_file()


def test_staging_dir_is_not_left_in_the_system_temp(client, admin_user, doctrine_dirs, tmp_path):
    """A rejected batch must not leave a partial file where an import can find it.

    `import_external_folder` walks its folder with rglob("*"), so a staging
    directory placed beside the uploads would be ingested after a crash.
    """
    import tempfile
    from pathlib import Path

    before = set(Path(tempfile.gettempdir()).glob("ragseo-upload-*"))
    login_admin(client)
    upload(client, [("Doc 613_ Fine.md", b"# Fine\n\nBody.\n")])
    assert set(Path(tempfile.gettempdir()).glob("ragseo-upload-*")) == before


# ------------------------------------------------- upload: atomicity of commit


def test_commit_stages_on_the_destination_filesystem(client, admin_user, doctrine_dirs, monkeypatch):
    """The commit must be a rename, not a copy.

    `/tmp` and the upload bind mount are different devices (st_dev 59 vs 38 in
    the containers), so `shutil.move` between them silently falls back to
    copy+unlink. The destination then becomes observable part-written and a
    concurrent reconcile can ingest a truncated file. Staging in a subdirectory
    of the destination makes the commit a same-device `os.replace` rename, so
    this asserts the precondition that makes the rename atomic.
    """
    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    seen: list[dict] = []

    def record(staging: Path) -> None:
        # Stat inside the hook: the staging dir is removed once the call returns.
        seen.append(
            {
                "name": staging.name,
                "parent": staging.parent,
                "st_dev": staging.stat().st_dev,
                "dest_st_dev": uploads.stat().st_dev,
            }
        )

    real_stage = uploads_service.stage_uploads

    async def capturing_stage(entries, dest_dir, *, max_bytes, max_total_bytes=None, before_commit=None):
        return await real_stage(entries, dest_dir, max_bytes=max_bytes, before_commit=before_commit or record)

    monkeypatch.setattr(uploads_service, "stage_uploads", capturing_stage)
    monkeypatch.setattr(ingest_router, "stage_uploads", capturing_stage)

    login_admin(client)
    r = upload(client, [("Doc 614_ Same Device.md", b"# Same\n\nBody.\n")])
    assert r.status_code == 200

    assert seen, "before_commit hook never fired"
    info = seen[0]
    assert info["parent"] == uploads, "staging must live inside the destination dir"
    assert info["name"].startswith(uploads_service.STAGING_PREFIX)
    assert info["st_dev"] == info["dest_st_dev"], (
        "staging and destination must share a filesystem or the commit is a non-atomic copy"
    )


def test_commit_renames_and_never_copies(client, admin_user, doctrine_dirs, monkeypatch):
    """The commit must be `os.replace`, and `shutil.move` must never be called.

    This is the load-bearing regression test, and it is deliberately about the
    *mechanism* rather than the observable result. The test suite runs in
    `tmp_path` under `/tmp`, so a `/tmp`-staged implementation would be on the
    same filesystem as the destination and its `shutil.move` would be an atomic
    rename anyway — a "was any partial size ever visible?" assertion passes for
    such a mutant and proves nothing. The bug only appears in the containers,
    where the upload dir is a bind mount on a different `st_dev` from `/tmp` and
    `shutil.move` degrades to copy+unlink. Asserting the mechanism is the only
    way to catch it here; `test_commit_stages_on_the_destination_filesystem`
    covers the same ground from the path side.
    """
    import shutil as shutil_module

    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    moved: list[str] = []
    replaced: list[tuple] = []

    real_move = shutil_module.move

    def record_move(src, dst, *a, **k):
        moved.append(f"{src} -> {dst}")
        return real_move(src, dst, *a, **k)

    real_replace = uploads_service.os.replace

    def record_replace(src, dst, *a, **k):
        replaced.append((str(src), str(dst)))
        return real_replace(src, dst, *a, **k)

    monkeypatch.setattr(shutil_module, "move", record_move)
    monkeypatch.setattr(uploads_service.os, "replace", record_replace)

    login_admin(client)
    r = upload(client, [("Doc 617_ Renamed.md", b"r" * 2048), ("Doc 618_ Also Renamed.md", b"q" * 2048)])
    assert r.status_code == 200

    assert moved == [], f"commit used shutil.move, which copies across filesystems: {moved}"
    assert len(replaced) == 2, f"expected two atomic renames, got {replaced}"
    for src, _dst in replaced:
        assert src.startswith(str(uploads)), f"rename source must be staged inside the destination: {src}"


def test_nothing_is_visible_in_the_upload_dir_before_commit(client, admin_user, doctrine_dirs, monkeypatch):
    """Staged bytes must be invisible to a scanner until the batch is committed.

    The `before_commit` hook is the seam that makes this deterministic: it runs
    after every file is staged and validated but before any rename. A concurrent
    scan at that moment must see no `.md` file at all, only the dot-prefixed
    staging dir, which `is_hidden_path` excludes.

    Note the scope: this proves the *staging* directory is correctly hidden, not
    that the commit is atomic. See `test_commit_renames_and_never_copies` for
    the cross-filesystem case a result-based assertion cannot catch in `tmp_path`.
    """
    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    observed: list[list[str]] = []

    def peek(_staging: Path) -> None:
        # Exactly what a concurrent scan would see: iterdir + is_file + .md.
        visible = [p for p in uploads.iterdir() if p.is_file() and p.suffix.lower() == ".md"]
        observed.append(sorted(p.name for p in visible))

    real_stage = uploads_service.stage_uploads

    async def injecting_stage(entries, dest_dir, *, max_bytes, max_total_bytes=None, before_commit=None):
        return await real_stage(entries, dest_dir, max_bytes=max_bytes, before_commit=before_commit or peek)

    monkeypatch.setattr(uploads_service, "stage_uploads", injecting_stage)
    monkeypatch.setattr(ingest_router, "stage_uploads", injecting_stage)

    login_admin(client)
    r = upload(client, [("Doc 615_ Atomic.md", b"z" * 4096), ("Doc 616_ Also.md", b"y" * 4096)])
    assert r.status_code == 200
    assert r.json()["created"] == 2

    assert observed, "before_commit hook never fired"
    assert observed[0] == [], f"a partial file was visible before commit: {observed[0]}"
    # And afterwards both files are complete and correctly sized.
    assert (uploads / "Doc 615_ Atomic.md").stat().st_size == 4096
    assert (uploads / "Doc 616_ Also.md").stat().st_size == 4096


def test_failed_commit_rolls_back_already_committed_files(
    client, admin_user, db_session, doctrine_dirs, monkeypatch
):
    """A commit that fails partway must not leave the earlier files behind.

    This is the failure that a temp-path-based rollback silently misses: after a
    successful rename the staged path no longer exists, so unlinking it is a
    no-op and the destination copy survives. Injected on the *commit*, not the
    staging, so the rollback has real committed paths to clean up.
    """
    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    real_replace = uploads_service.os.replace
    calls = {"n": 0}

    def flaky(src, dst, *a, **k):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError(28, "No space left on device")
        return real_replace(src, dst, *a, **k)

    monkeypatch.setattr(uploads_service.os, "replace", flaky)

    login_admin(client)
    # A disk-full during commit is not an expected client error, so it surfaces as
    # a 500 in production. The TestClient re-raises it rather than returning a
    # response; what matters for this regression is the on-disk state after.
    with pytest.raises(OSError, match="No space left on device"):
        upload(
            client,
            [
                ("Doc 617_ First.md", b"# First\n\nA.\n"),
                ("Doc 618_ Second.md", b"# Second\n\nB.\n"),
                ("Doc 619_ Third.md", b"# Third\n\nC.\n"),
            ],
        )
    assert calls["n"] == 2, "expected the injected failure on the second rename"

    # The first file had been committed by the time the second failed. It must be
    # gone, or the next reconcile ingests a document this response disowned.
    leftovers = sorted(p.name for p in uploads.iterdir()) if uploads.exists() else []
    assert leftovers == [], f"rollback left files in the upload dir: {leftovers}"
    assert db_session.query(Document).count() == 0, "a rolled-back upload must not be ingested"


def test_staging_dir_never_survives_a_crash(client, admin_user, db_session, doctrine_dirs, monkeypatch):
    """A staging dir left behind by a hard kill must be inert.

    Simulates the one case the `finally` cleanup cannot cover: the process dies
    between staging and commit. Such a dir must be (a) invisible to both
    scanners, which check the whole path rather than the basename, and (b) not
    disturb the next upload.
    """
    from app.services import uploads as uploads_service
    from app.services.doc_ingestion import scan_doctrine_files
    from app.services.external_ingest import import_external_folder

    _baked, uploads = doctrine_dirs
    # rglob("*") descends INTO a dot-prefixed dir, so a basename-only check would
    # ingest the file inside it. This is the regression the any-component rule fixes.
    orphan = uploads / f"{uploads_service.STAGING_PREFIX}orphan"
    orphan.mkdir(parents=True)
    (orphan / "Doc 620_ Never Seen.md").write_text(
        "# Never seen\n\nShould not be ingested.\n", encoding="utf-8"
    )
    (uploads / "Doc 621_ Real.md").write_text("# Real\n\nBody.\n", encoding="utf-8")

    scanned = {p.name for p in scan_doctrine_files() if p.parent == uploads}
    assert "Doc 620_ Never Seen.md" not in scanned, "doctrine scan ingested a staged file"
    assert "Doc 621_ Real.md" in scanned

    results = import_external_folder(uploads, db_session)
    imported = {r.get("filename") for r in results if r.get("status") == "imported"}
    assert "Doc 620_ Never Seen.md" not in imported, "external import ingested a staged file"

    # A fresh upload still works with the orphan present.
    login_admin(client)
    r = upload(client, [("Doc 622_ After Crash.md", b"# After\n\nBody.\n")])
    assert r.status_code == 200
    assert (uploads / "Doc 622_ After Crash.md").is_file()


def test_staging_dir_is_removed_from_the_upload_folder(client, admin_user, doctrine_dirs, monkeypatch):
    """No staging dir may survive a successful request in the upload folder."""
    from app.services import uploads as uploads_service

    _baked, uploads = doctrine_dirs
    login_admin(client)
    r = upload(client, [("Doc 623_ Clean.md", b"# Clean\n\nBody.\n")])
    assert r.status_code == 200
    leftovers = [p.name for p in uploads.iterdir() if p.name.startswith(uploads_service.STAGING_PREFIX)]
    assert leftovers == [], f"staging dir left in the upload folder: {leftovers}"


def test_upload_strips_directory_traversal(client, admin_user, db_session, doctrine_dirs):
    """A multipart part may claim any path; only the basename may survive."""
    _baked, uploads = doctrine_dirs
    login_admin(client)

    r = upload(client, [("../../Doc 700_ Sneaky.md", b"# Sneaky\n\nBody.\n")])
    assert r.status_code == 200
    assert r.json()["files"][0]["filename"] == "Doc 700_ Sneaky.md"
    assert [p.name for p in uploads.iterdir()] == ["Doc 700_ Sneaky.md"]


def test_safe_filename_units():
    assert safe_filename("../../etc/passwd") == "passwd"
    assert safe_filename("..\\..\\windows\\file.md") == "file.md"
    assert safe_filename("/absolute/path/file.md") == "file.md"
    assert safe_filename("..") == ""
    assert safe_filename("") == ""
    assert safe_filename("   ") == ""
    assert safe_filename("normal.md") == "normal.md"


# ----------------------------------------------------- upload: scoped ingest


def test_upload_does_not_sweep_unrelated_docs(client, admin_user, db_session, doctrine_dirs):
    """The upload path is scoped: it must never be able to mark anything missing."""
    from tests.conftest import seed_doc

    baked, _uploads = doctrine_dirs
    write_doc(baked, "Doc 800_ Baked Doc.md")
    ingest_all_docs(db_session)

    orphan = seed_doc(db_session, "801", "Never On Disk", "# Orphan\n\nNo file exists.\n")
    orphan.filename = "Doc 801_ Never On Disk.md"
    db_session.commit()

    login_admin(client)
    upload(client, [("Doc 802_ Fresh Upload.md", b"# Fresh\n\nBody.\n")])

    db_session.refresh(orphan)
    assert orphan.status == "active", "a scoped upload must not run the missing sweep"


def test_ingest_files_reports_per_file_outcomes(db_session, doctrine_dirs):
    _baked, uploads = doctrine_dirs
    paths = [
        write_doc(uploads, "Doc 810_ One.md", "# One\n\nBody one.\n"),
        write_doc(uploads, "Doc 811_ Two.md", "# Two\n\nBody two.\n"),
    ]

    stats = ingest_files(db_session, paths)
    assert stats["created"] == 2
    entries = {e["filename"]: e for e in stats["files"]}
    assert entries["Doc 810_ One.md"]["status"] == "created"
    assert entries["Doc 810_ One.md"]["doc_number"] == "810"
    assert entries["Doc 810_ One.md"]["title"] == "One"
    assert entries["Doc 810_ One.md"]["chunks"] >= 1


def test_ingest_files_isolates_a_bad_file(db_session, doctrine_dirs):
    """One unreadable file must not discard the good ones ingested alongside it."""
    _baked, uploads = doctrine_dirs
    good_a = write_doc(uploads, "Doc 820_ Good A.md", "# Good A\n\nBody.\n")
    bad = write_doc(uploads, "Doc 821_ Bad.md", "# Bad\n\nBody.\n")
    good_b = write_doc(uploads, "Doc 822_ Good B.md", "# Good B\n\nBody.\n")
    # Non-UTF-8 bytes: read_text(encoding="utf-8") raises inside the per-file try.
    bad.write_bytes(b"# Bad\n\n\xff\xfe not utf-8\n")

    stats = ingest_files(db_session, [good_a, bad, good_b])

    assert stats["created"] == 2
    assert len(stats["errors"]) == 1
    assert "Doc 821_ Bad.md" in stats["errors"][0]
    numbers = {d.doc_number for d in db_session.query(Document).all()}
    assert numbers == {"820", "822"}, "a later file was lost to the earlier failure"


def test_ingest_files_rebuilds_references_for_new_docs(db_session, doctrine_dirs):
    from app.models.document import DocReference

    _baked, uploads = doctrine_dirs
    path = write_doc(
        uploads,
        "Doc 830_ Referencing Doc.md",
        "# Referencing\n\nSee Doc 100 for the master doctrine.\n",
    )
    ingest_files(db_session, [path])

    doc = db_session.query(Document).filter(Document.doc_number == "830").one()
    refs = db_session.query(DocReference).filter(DocReference.source_doc_id == doc.id).all()
    assert [r.target_doc_number for r in refs] == ["100"]


# ------------------------------------------------------------- batch caps
# The per-file cap alone does not bound a request. These cover the two aggregate
# limits: file count and total bytes across the batch.


def test_upload_rejects_a_batch_over_the_file_count_cap(client, admin_user, db_session, doctrine_dirs):
    login_admin(client)
    n = ingest_router.MAX_DOCTRINE_FILES + 1
    resp = upload(client, [(f"Doc {4000 + i}_ Cap.md", b"body") for i in range(n)])

    assert resp.status_code == 413
    assert str(ingest_router.MAX_DOCTRINE_FILES) in resp.json()["detail"]
    assert list(db_session.query(Document).all()) == [], "nothing may be ingested past the cap"
    assert not list(doctrine_dirs[1].glob("*.md")), "nothing may be written past the cap"


def test_upload_accepts_a_batch_exactly_at_the_file_count_cap(client, admin_user, db_session, doctrine_dirs):
    login_admin(client)
    n = ingest_router.MAX_DOCTRINE_FILES
    resp = upload(client, [(f"Doc {4100 + i}_ Cap.md", b"body") for i in range(n)])

    assert resp.status_code == 200
    assert resp.json()["created"] == n
    assert len(list(doctrine_dirs[1].glob("*.md"))) == n


def test_upload_rejects_a_batch_over_the_total_byte_cap(
    client, admin_user, db_session, doctrine_dirs, monkeypatch
):
    """Total cap trips even though every single file is under the per-file cap.

    The per-file cap is monkeypatched high on purpose: the point is that a batch
    of individually-legal files must still be refused as a batch.
    """
    login_admin(client)
    monkeypatch.setattr(ingest_router, "MAX_DOCTRINE_UPLOAD_BYTES", 10 * 1024 * 1024)
    monkeypatch.setattr(ingest_router, "MAX_DOCTRINE_TOTAL_BYTES", 40 * 1024)

    # 6 files x 10 KB = 60 KB, all individually legal, batch total over 40 KB.
    resp = upload(client, [(f"Doc {4200 + i}_ Big.md", b"z" * 10_000) for i in range(6)])

    assert resp.status_code == 413
    assert "total limit" in resp.json()["detail"]
    assert list(db_session.query(Document).all()) == [], "an over-cap batch must not be partially ingested"
    assert not list(doctrine_dirs[1].glob("*.md")), "staging must be discarded, not committed"
    assert not list(doctrine_dirs[1].glob(".staging-*")), "the staging dir must be cleaned up"


def test_upload_accepts_a_batch_exactly_at_the_total_byte_cap(
    client, admin_user, db_session, doctrine_dirs, monkeypatch
):
    login_admin(client)
    monkeypatch.setattr(ingest_router, "MAX_DOCTRINE_TOTAL_BYTES", 40 * 1024)

    # 4 x 10 KB = 40 KB exactly, which is allowed (the cap trips on > limit).
    resp = upload(client, [(f"Doc {4300 + i}_ Ok.md", b"y" * 10_000) for i in range(4)])

    assert resp.status_code == 200
    assert resp.json()["created"] == 4


def test_stage_uploads_total_cap_stops_at_the_crossing_byte(tmp_path):
    """The aggregate check aborts mid-stream, not after buffering the whole batch.

    Asserting on read counts matters: a check placed after the read loop would
    still cap the damage on disk but would pull every byte over the wire first.
    """
    import asyncio

    from app.services.uploads import BatchTooLarge, stage_uploads

    dest = tmp_path / "dest"
    calls: list[str] = []

    class CountingUpload:
        def __init__(self, name, size):
            self.name, self.size, self.remaining = name, size, size

        async def read(self, n):
            calls.append(self.name)
            chunk = b"a" * min(n, self.remaining)
            self.remaining -= len(chunk)
            return chunk

    with pytest.raises(BatchTooLarge):
        asyncio.run(
            stage_uploads(
                [("a.md", CountingUpload("a.md", 40_000)), ("b.md", CountingUpload("b.md", 40_000))],
                dest,
                max_bytes=200_000,
                max_total_bytes=10_000,
            )
        )

    # The first read of a.md alone already exceeds the 10 KB batch cap, so the
    # exception is raised on that read and b.md is never opened. An over-cap
    # batch is refused at the crossing byte rather than after the whole body has
    # been pulled over the wire and spooled.
    assert calls == ["a.md"], f"cap should trip on the first file, got {calls}"
    assert not list(dest.glob("*.md"))
    assert not list(dest.glob(".staging-*"))


def test_stage_uploads_without_a_total_cap_is_unbounded_by_batch(tmp_path):
    """max_total_bytes is opt-in, so existing callers keep their old behaviour."""
    import asyncio

    from app.services.uploads import stage_uploads

    dest = tmp_path / "dest"

    class Upload:
        def __init__(self, size):
            self.remaining = size

        async def read(self, n):
            chunk = b"a" * min(n, self.remaining)
            self.remaining -= len(chunk)
            return chunk

    saved = asyncio.run(
        stage_uploads(
            [("a.md", Upload(30_000)), ("b.md", Upload(30_000))],
            dest,
            max_bytes=100_000,
        )
    )
    assert len(saved) == 2
