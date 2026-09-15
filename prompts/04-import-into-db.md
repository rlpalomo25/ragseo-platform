# Prompt 4 — Import Exports into the DB

Import the newly staged exports via the admin API (auth required):

```
curl -u <admin_user>:<admin_password> -X POST https://<domain>/api/ingest/external
```

Verify the result: expected `imported` = number of new files, `skipped` = N
(already-hashed duplicates), `errors` = 0. Cross-check with:

```
curl -u <admin_user>:<admin_password> https://<domain>/api/ingest/external/status
```

<details>
<summary>Details for the operator</summary>

- On **first boot** the import auto-runs via `RUN_EXTERNAL=1`
  (`docker-compose.prod.yml:64-68` → `backend/docker-entrypoint.sh` →
  `python scripts/import_external.py`). Re-up with `RUN_SEED=0 RUN_EXTERNAL=0`
  (or unset) afterwards so it does not re-run on every restart.
- On **subsequent weeks** run the POST step explicitly as above.
- Forced reload of an already-imported file: CLI
  `python scripts/import_external.py --path <folder> --force`.
- The importer is in-memory (`zipfile`, no `unzip` binary), hash-deduped, and
  classifies files by content, not extension.
</details>