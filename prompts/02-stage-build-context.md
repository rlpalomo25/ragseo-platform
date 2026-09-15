# Prompt 2 — Stage Exports into the Build Context

Stage the weekly exports (and doctrine) into `backend/external` / `backend/doctrine`
so the Docker build bakes them into the image:

```
cd /home/roberto/RAGv2/ragseo-platform/backend && ./scripts/sync_doctrine.sh
```

Verify the printed file counts match the source folder before continuing.

<details>
<summary>Details for the operator</summary>

- `sync_doctrine.sh` mirrors the weekly folder into `backend/external/` using a
  `find ... -maxdepth 1 -type f -print0 | cp` loop (whitespace-safe file names).
- It also copies doctrine `.md` docs into `backend/doctrine/`, dropping
  Windows `:Zone.Identifier` ADS twins.
- The Dockerfile bakes these paths: `COPY doctrine/ /app/doctrine` and
  `COPY external/ /app/external`.
- This step must run before any backend image build (dev or prod).
</details>