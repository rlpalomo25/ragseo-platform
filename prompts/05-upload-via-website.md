# Prompt 5 — Upload Weekly Exports via the Website

Any logged-in user can upload this week's exports through the website — no
admin / SSH / rsync needed.

1. Log in at the platform (role `writer` or `admin`).
2. Open **Weekly Exports** in the sidebar (`/exports`).
3. In the "Upload this week's exports" box, pick all exported files at once
   (`.zip`, `.csv`, `.txt`, `.md`) and click **Upload & Import**.

The upload form is also on the admin **Data Ingest** page (`/ingest`, bottom
card).

<details>
<summary>Details for the operator</summary>

- Backend: `POST /api/ingest/external/upload` (multipart, auth required —
  `require_writer`); files are saved to the writable `external_upload_path`
  (`/app/uploads/external`, bind-mounted to `./external_uploads`) and imported
  immediately.
- Per-file isolation: one bad file reports an error; the rest still import.
- Filenames are basename-sanitized (path traversal stripped); 200 MB/file cap.
- Hash-dedup stays intact: re-uploading identical bytes reports "skipped".
- This supersedes the copy-files-to-folder flow for regular users; the
  rsync + `sync_doctrine.sh` path (prompts 01-03) still works for the baked
  seed folder and offline ops.
</details>