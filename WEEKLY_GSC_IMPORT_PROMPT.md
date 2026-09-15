# Weekly GSC / Market-Data Import — Master Prompt

Run the weekly external market-data import end-to-end (GSC / GA4 / Ubersuggest /
calls / leads) into the RAGSEO platform. The import is **idempotent**
(hash-deduped), so re-running is safe.

Follow the steps below in order. Each step has a dedicated prompt with operator
details under `prompts/`.

**0. Regular users upload through the website** (recommended): log in → **Weekly
Exports** (`/exports`) → select files → **Upload & Import**. Files are saved to
the writable upload folder and imported immediately, hash-deduped.
→ `prompts/05-upload-via-website.md`

**Ops/admin offline flow (or to refresh the baked seed folder):**

1. **Copy the new exports** into `09042026/` (same filename format as existing).
   → `prompts/01-copy-exports.md`

2. **Stage into the build context** so the image bakes the data:

   ```
   cd /home/roberto/RAGv2/ragseo-platform/backend && ./scripts/sync_doctrine.sh
   ```

   → `prompts/02-stage-build-context.md`

3. **Push to the VPS via git, rebuild the backend image, redeploy:**

```
   git push origin main
   ssh root@157.230.2.51 'cd /opt/ragseo-platform && git pull origin main && docker compose -f docker-compose.prod.yml build backend && docker compose -f docker-compose.prod.yml up -d'
   ```

   → `prompts/03-push-redeploy.md`

4. **Import into the DB** — admin `POST /api/ingest/external` (auth required).
   On first boot it auto-runs via `RUN_EXTERNAL=1`; subsequent weeks trigger it
   explicitly:

   ```
   curl -u <admin_user>:<admin_password> -X POST https://<domain>/api/ingest/external
   ```

   Expected: `imported` = new files, `skipped` = N dupes, `errors` = 0.
   → `prompts/04-import-into-db.md`

---

## Gotchas / Notes

- Importer runs in-memory via Python `zipfile` (no `unzip` on the VPS); nested
  and renamed archives are handled by probing content, not filename.
- Hash-dedup exempts duplicate files even under different names.
- Forced reload of a skipped file: `python scripts/import_external.py --path ... --force`.
- Relevant files: `backend/app/services/external_ingest.py`,
  `backend/scripts/sync_doctrine.sh`, `backend/docker-entrypoint.sh`,
  `backend/app/routers/ingest.py`, `backend/app/models/external.py`.