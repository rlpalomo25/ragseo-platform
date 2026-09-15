# Prompt 1 — Copy Weekly Exports into the Source Folder

Copy your weekly GSC / GA4 / Ubersuggest / calls / leads exports into:

```
/home/roberto/RAGv2/ragseo-platform/09042026/
```

Keep the same filename format as the existing files, e.g.
`KleanGutter_GSC_Export_[09042026].csv.zip.zip`, `*_Backlinks.csv`,
`*_Traffic_Overview.pdf (...).md`, `calls export from ... .csv`,
`*-AI-Features-... .zip`, `Leads_Summary_Week_... .txt`, etc.

When done, confirm the files are present in the folder before continuing.

<details>
<summary>Details for the operator</summary>

- This is the EXTERNAL_SRC that `sync_doctrine.sh` mirrors into the build
  context (default `$REPO_ROOT/09042026`).
- Files are hash-deduped at import time, so byte-identical duplicates arriving
  under different names are safe to include.
- No file type restrictions: zips, CSVs, markdown, and txt are all handled.
</details>