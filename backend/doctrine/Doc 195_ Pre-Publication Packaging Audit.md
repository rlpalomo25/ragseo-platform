# Doc 195 — Pre-Publication Packaging Audit

**Version:** 1.2 | **Created:** July 30, 2026 | **Last Updated:** July 31, 2026 | **Series:** 100 (Doctrine / System) — sits alongside Doc 192, Doc 193, Doc 194 in the publish-handoff cluster.

> **v1.2 (July 31, 2026, Karen):** Strengthened PKG1 after the same page (best-gutter-guards-mastershield v4.2) that surfaced the v1.1 question above also passed this gate the same day while visibly using the wrong Your Questions Answered label ("Often answered Questions") — this gate's own "recompute independently" instruction wasn't enough to catch it in practice. Added an explicit enumerate-and-compare-verbatim step to PKG1 (below).
> **v1.1 (July 31, 2026, Karen):** Added an explicit ruling closing the "does the saved Doc 328/329 report conflict with the retired reviewer-facing report" question, which the very first real audit run through this gate (best-gutter-guards-mastershield v4.2) flagged as open. It doesn't conflict — the saved report is an internal system trail, the retirement rule governs the page's own reader-facing checklist — and this is now stated in the doc itself so the next audit doesn't have to re-derive and re-flag the same answer.
**Authority for:** the final gate before a page reaches WordPress, on **both** the main pipeline and the Doc 361 refresh track. Confirms WordPress-ready completeness and confirms both systems produce output that looks identical in shape — same fields, same names, same order, same formatting — regardless of which one built the page.
**Companion to:** Doc 328 (main-pipeline content auditor), Doc 329 (361-track content auditor), Doc 192 (the handoff template this audit verifies against), Doc 260 (the WordPress guide this audit clears the page for).
**Not a companion to, and does not replace:** Doc 312 (the planner's auditor — validates the Execution Plan, upstream of all of this). This document has no opinion on plans.

---

## Why this exists

Doc 328 and Doc 329 each already carry structural/completeness checks (meta title/description visible, JSON-LD both forms, `article_archetype` present, the Publish-Readiness Manifest itself present, single-deliverable-file) — added July 29, 2026 after Karen found several of these missing on a live page. Those checks work, but each one only ever runs **inside its own track.** Doc 328 never looks at a 361-track deliverable; Doc 329 never looks at a main-pipeline deliverable. Neither one can answer the question Karen actually needs answered before a page reaches WordPress: **does this page look like every other page the system produces, regardless of which track built it?**

That is a different kind of question than "is this page's content good" (Doc 328/329's job) or "is this plan sound" (Doc 312's job). It is a packaging question: are the same fields present, in the same order, under the same names, formatted the same way, on every deliverable this system produces — main pipeline or 361, MasterShield, Klean, or MMGG. Doc 195 exists to ask only that question, independently, on every page, after its content auditor has already passed it.

**This is not a content auditor.** It does not evaluate voice, argument quality, FAQ sourcing, guardian mapping, structural asset preservation, competitor coverage, or anything Doc 328/329 already checks. A page cannot reach Doc 195 without a saved, passing Doc 328 or Doc 329 report already in hand for its exact slug and version — if that report is missing, stop and send the page back; do not perform a content review here as a substitute, and do not let this audit become a second content gate by accident.

---

## How the gate proves it ran (non-negotiable)

Same standard as Doc 328/329: every check below gets a one-line evidence note in the saved report — quote the exact field/value found, or state the count — not a bare "Pass." No unevidenced item is presumed to have been checked.

**Required input before this audit may begin:** the delivered file, and the filename + location of its already-passing Doc 328 or Doc 329 report in `company/audits/`. Record both in this audit's own report. No content auditor report on file = stop, do not proceed.

**Saved report (mandatory):** `company/audits/doc195-packaging-audit-[slug]-v[ver].md`, every item below marked PASS/FAIL/FLAG with its evidence note. No report, no ship — same rule as Doc 328/329.

**This is settled doctrine, not an open question (added July 31, 2026, per Karen) — do not re-flag it.** The saved Doc 328/329 report this gate requires, and Karen's earlier ruling retiring the *reviewer-facing* audit report, are two different things and do not conflict: the `company/audits/` report is an internal **system/gate-sequencing trail** — proof a prior gate actually ran, checked the same way Doc 328/329's own C17/Phase-0 provenance checks work — and nobody besides the pipeline itself needs to open it. Karen's retirement rule governs a different surface entirely: what gets embedded in or attached to the **page itself** when it's handed to Karen or the reader — that stays as outstanding items folded into the page's own Pre-Publish Checklist (Doc 328's own text: "not the deliverable Karen or the page reader ever sees"), never a freestanding Audit Report block. Keep saving the `company/audits/` report exactly as this doc already requires. Do not attach it to, or summarize it inside, the page itself.

---

## Critical checks (any FAIL = does not go to WordPress)

**PKG1 — Required Block Order (Doc 192).** Recompute independently — do not trust a self-declared checklist — that the delivered file's top-to-bottom order matches Doc 192's Required Block Order exactly: H1 → Key Takeaways → Your Questions Answered (+ post-Your-Questions-Answered CTA) → Body → Frequently Asked Questions → About the Author → (Appendix, below the `<hr>`) → Pre-Publish Checklist/Publish-Readiness Manifest → Build metadata (YAML) → CTA Summary → Media Assets → Internal Links → Changelog. **Verbatim check (added July 31, 2026, Karen — a live page passed this exact check while using "Often answered Questions" instead of "Your Questions Answered," and this report transcribed the wrong label back without flagging it):** list every on-page H2 heading exactly as it appears, in order, then compare each to Doc 192's fixed labels character-for-character. A heading that means the same thing but isn't the verbatim label is a relabel, not a pass — do not let thematic equivalence substitute for an exact match. A block present but out of order, relabeled (including a near-match that isn't verbatim), or missing = **FAIL**.

**PKG2 — YAML front matter completeness (Doc 192).** Every required field present and non-empty: `plan_id`, `version`, `writer_id`, `brand`, `page_classification`, `page_type`, `page_subtype`, `meta_title` (≤60 chars, keyword-front, no TM/®), `meta_description`, `url_slug`, `image_budget`, `author`, `trust_chip`, `article_archetype`, `extractable_blocks`, `cta_blocks`, `internal_links`, `entity_usage`, `execution_plan_alignment`. `writer_id` must use the fixed form `<Doc nnn> / <Brand> Writer Agent` (never free text like "GPT-WRITER-AGENT"). Any field missing, empty, or malformed = **FAIL**.

**PKG3 — Meta Title / Meta Description visibility.** Confirm both are visibly readable as plain text in the Build Metadata block (item 8) — not only present in a raw HTML `<title>` tag that a publisher would have to view-source to find.

**PKG4 — JSON-LD, both forms, full schema set (Doc 192 7A-SCHEMA / Doc 123 §3.0).** Confirm: (a) the functional `<script type="application/ld+json">` block(s) exist and are well-formed; (b) the exact same JSON is repeated immediately below, HTML-escaped, in a visible `<pre><code>` block labeled for copy-paste; (c) the schema set covers Article + Organization + BreadcrumbList, plus FAQPage whenever the page carries a Frequently Asked Questions section — not just Article + FAQPage. FAQPage `Question`/`Answer` text must match the visible FAQ answers verbatim, not a shortened or reworded version. Any one of these missing = **FAIL**.

**PKG5 — Article archetype present and valid (Doc 135).** `article_archetype` in the YAML is present and names a real archetype from Doc 135's set of 12 (primary, plus secondary if blended) — not blank, not a placeholder, not a value that doesn't correspond to an actual Doc 135 archetype.

**PKG6 — Author + bio.** Exactly one author assigned (matching the YAML `author` field), bio present. Any second quoted expert is labeled Contributor/Field Expert, never a co-equal second author.

**PKG7 — CTA Summary / Media Assets / Internal Links tables.** All three present at the bottom of the Appendix, and populated — not empty shells or placeholder rows. Every CTA in the body appears in the CTA Summary table; every image/placeholder in the body appears in the Media Assets table.

**PKG8 — Publisher Note, when required.** If the page keeps an existing URL, changes its head keyword, or carries a 301, confirm the Publisher Note (Doc 192 §7A) is present and states the URL, the new head keyword and why, and any 301s. If none of these situations apply, confirm the file says so in one line rather than omitting the section silently.

**PKG9 — Single deliverable file.** Look at the actual folder in `company/pages/`, not just the file in hand: exactly one candidate delivered file exists for this page's exact version. A second file — draft, alternate attempt, differently-suffixed name — is a **FAIL** even when the file in hand is correct, same standard as Doc 328/329's own single-file check. (This audit re-checks it independently rather than assuming the content auditor's pass already covers it, since the two failure modes — content quality and file hygiene — are unrelated and one passing says nothing about the other.)

**PKG10 — Cross-track format parity (the reason this audit exists as its own document).** Pull one other recently-passed deliverable — ideally from the opposite track (main pipeline vs. 361) or a different brand — as a reference. Confirm this page's YAML field names, Appendix item order, table column headers, and component class names (`.callout.benefits`, `.qa`, `.cta`, `.askthis`, etc., per Doc 194) are identical in shape to the reference, not merely "close" or "equivalent." A deliverable that contains everything PKG1–9 require, but names a field differently, orders the Appendix differently, or uses a different table column set than the reference, is a **FAIL** here — the point of this check is that a publisher (or an automated WordPress importer) should never have to special-case which track produced a page. Note the reference file used in the saved report so the comparison is reproducible.

---

## What this audit does not do

Does not evaluate: voice, argument continuity, competitor coverage, structural asset preservation, FAQ sourcing/relevance, guardian mapping, image *quality* (only that the Media Assets table is populated — Doc 328/329 own the budget/cadence check), trademark usage, or any other content dimension. Does not re-run or duplicate Doc 328/329. Does not evaluate the Execution Plan (Doc 312's job). If a packaging gap is found that turns out to be caused by a content-stage decision (e.g., a missing FAQPage schema because the page has no FAQ section by design), note it as a FLAG for the content auditor to confirm was intentional, not as this audit's own judgment call.

---

## Routing

- All PKG checks pass → **PASS** → clear to Doc 260 (WordPress Publishing Guide) / the publisher.
- Any PKG check fails → **FAIL** → return to the writer/producing track with the specific field(s) named. Do not forward a FAIL to WordPress or to Karen as publish-ready.
- A FLAG (see above) does not block, but must be noted in the saved report and resolved before the next version of this page runs through this audit again.

---

## One-Sentence Summary
Confirms the delivered file has everything WordPress needs and looks the same as every other deliverable this system produces, independent of which track built it — nothing more, nothing less.

---

**Version 1.0 (July 30, 2026, Karen):** Created. Built after Karen asked for a distinct pre-publication packaging audit, separate from the planner auditor (Doc 312) and the writer auditors (Doc 328/329), to confirm WordPress-ready completeness and cross-track format parity before a page reaches WordPress. Grounded directly in Doc 192's existing Publish-Readiness Manifest, Required Block Order, and YAML front matter fields — no new field list invented. Wired into both pipelines' routing: Doc 328 and Doc 329 now forward a PASS to this gate before Doc 260; Doc 361-MS/KG/MMGG Step 5 and Doc 153's handoff chain reference it. See Doc 208.