# Doc 193: Canonical Execution Plan Format

**Version:** 2.5 | **Created:** June 25, 2026 | **Updated:** August 6, 2026 | **Series:** 100 (Doctrine / System) | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Authority for:** every execution plan produced by the execution-plan-writer agent / Doc 153 (Execution Plan Generator).
**Companion to:** Doc 192 (Canonical Page Handoff Template) — Doc 192 standardizes the *page* deliverable; Doc 193 standardizes the *plan* the writer builds from.
**Enforced by:** the writer skills (which stop if the plan is non-conformant). *(The former Doc 154 reviewer is retired.)*

---

## Principle

The execution plan is the writer's brief. Anyone — writer, reviewer, or Karen — opens any plan and finds each part in the same place every time. **One front-matter block, one section order, one set of labels — every plan, every page type.** The format exists to guarantee that every input which must reach the published page (the keyword→heading map, the H1–H3 outline, the image budget, the CTA cadence and trust signals, the meta and internal links) is present and unambiguous before a writer touches it.

---

## Two Documents, Not More (added July 28, 2026, Karen)

**Exactly two documents exist per page: the Execution Plan (this format) and the Writer's output (Doc 192's article/HTML deliverable).** Both iterate by replacement — the same file gets a version bump and updated content, not a new sibling file. No other pipeline agent (Architect/Doc 312, SOT/Doc 354, or anything downstream) produces its own separate deliverable file for a single page. Their output either:
- becomes an edit to the Execution Plan (a new/updated Open Question, a filled-in field, a corrected Appendix table row) — this is how Doc 312's Architect validation now works, or
- becomes an edit to the Writer's article — this is how the audit gate's fixes work (Doc 328/329 findings get applied to the article, not written up as a third document).

**Do not create a document type described as "not quite the plan, not quite the article yet."** If something is a plan, it's the plan file, updated in place. If something is the writing, it's the writer's article, updated in place. A stage-status word ("draft," "in progress," "not final") describes where one of those two documents is in its own iteration — it is never grounds to call it, or treat it as, a new third document. This was found and fixed as a real, live problem: Doc 312 had been producing a standalone `_Architecture-Brief.md` file alongside the actual plan (see Doc 312 v11.3).

---

## Required front matter (pre-H1 YAML)

```yaml
---
plan_id: PLAN-<topic-or-guardian>-<brand>-<audience>-v<n>
version: <n.n>
brand: <MasterShield | Klean Gutter | MicroMeshGutterGuards.com>
page_classification: <brand-conversion | source-of-truth | b2b-trade>
page_type: <pillar | cluster | local>
page_subtype: <mechanism | comparison | pricing | symptom | installation | faq | b2b | guide_pillar | technology_architecture_pillar | "">
primary_keyword: <string>  # with volume + SERP-confirmed date when available
secondary_keywords: [ ... ]  # the keyword bundle: up to 20, each with search volume (and difficulty) where available, RANKED by traffic, highest first
url_slug: /<path>/
meta_title: <string>                  # <=60 chars, keyword-front, brand suffix, no TM/®
meta_description: <string>           # keyword-front
author: <Karen Sager | Aaron Kapfer> # byline + About block + Article schema author
trust_chip: <string>                 # the page-relevant 5th proof for the trust bar (e.g. EPA-registered copper | ASTM B117-16 | 5 shingle-mfr approvals | all-metal)
redirects: [ ]                        # old-url -> this-url, for refresh/consolidation only; otherwise empty
target_body_words: <number>          # drives the image budget
image_budget: <number>               # = max(ceil(target_body_words/500), ceil(competitor_avg*1.2), page_type_floor) — Doc 153 Step 14 / Doc 190
cta_count: <number>                  # by structural milestone (Doc 144): 3 fixed anchors + each tension-resolving section end — NOT a word-count formula
status: <Draft | Review | Approved>
---
```

`image_budget` and `target_body_words` are mandatory — they are the contract the page deliverable and the Doc 328 media-budget gate are checked against.

---

## Required section order — what the reviewer reads, in this order

**One copy of everything; the argument leads so you know what the page is, in context, before the details.** Nothing machine-facing sits in the reading path.

### Reviewer Path — the whole readable plan, in this order

1. **`## The Argument`** — the **Win Vector** (one sentence) + the **Core Argument** (one short paragraph). Leads, so the reviewer knows what the page is about and why before anything else.
2. **`## H1`** — the headline.
3. **`## Key Takeaways`** — the stakes-setter bullets, then the **3 above-fold questions** (truncated teasers). (On-page: `## Key Takeaways` + `## Your Questions Answered`, Doc 192.)
4. **`## Outline`** — **the meat.** Every H2/H3 with its detail inline (narrative_role, pays_off/opens, proof, citation blocks with claim text, media, schema) and its keyword noted inline. The **only** place the structure and the arc appear.
5. **`## FAQ Questions`** — the proposed FAQ set: at least the questions, each with its source (PAA row / bundle theme). Answers are written later by the SOT agent; the reviewer sees the coverage here.
6. **`## Open Questions & Decisions Needed`** — a short, scannable list of **only the things that need the reviewer**: a decision to make or an input to supply before writing. Be ruthless about what goes here:
   - **Already-decided calls do NOT go here** (a routing choice you've made, a resolved question). They live where they were decided, or as a "Decided / to schedule" note in the Appendix — never padded into this list.
   - **Mark true blockers** — anything that stops the writer hand-off — with a **`[BLOCKS HANDOFF]`** tag, so the one hard stop is visible at a glance.
   - Data-pending items and inputs the reviewer will supply later are fine here, but tag them **`[non-blocking]`** so they don't read as stops.
   **Sits at the end of the reading path** so "what do you need from me?" is the last thing found before the deep appendix.

Everything below is reference — reached by inline pointers, never in the reading path above.

### The duplications this bans
- **No second outline** — the ranked keyword→heading table is appendix-only; the Outline notes each keyword inline.
- **No second arc** — opens/pays_off live only in the Outline, never restated under The Argument.
- **No machine data on top** — YAML front matter / structured fields live in the Appendix (or the Phase-2 JSON), never in the reading path. The H1 appears once.

### Appendix — production & reference (pointers only)
Front matter / structured fields · Plan Overview · Buyer State · Consolidation Map & 301s · SERP Intelligence · **Competitor Coverage Map** (cover/refute/omit per point) · Keyword Governance table · Story Units · Media Plan · CTA Placement Plan · Execution Targets · Schema Plan · Prohibited Moves · Fact Nuggets · Story Conversation Guide · Revision Log.

---

## Keyword Deployment Rule (the PLAN does this — the writer never decides placement)

The plan receives a **primary keyword** plus a **bundle of up to 20 secondary keywords**. Place them mechanically and show the work:

1. **H1 = the primary keyword**, keyword-front. The head term defines the page.
2. **Rank the bundle by search volume**, highest traffic first. The plan must show the ranked list with each term's volume (and difficulty where available).
3. **Highest-traffic bundle terms go in the top H2s.** H2 1 and H2 2 take the biggest non-primary terms *that fit the section's job*; mid-traffic terms go to the middle H2s and their H3s; long-tail and question terms go to lower H3s and the FAQ.
4. **Relevance beats volume.** A high-volume term only goes where it matches the section's intent. If it doesn't fit anywhere on this page, it gets routed, not forced.
5. **Every bundle keyword is either placed or routed** — nothing is silently dropped. A term that belongs on another page is marked `route → [page]` (cannibalization check, Doc 111).
6. **The Outline notes each heading's keyword inline; the full ranked table lives in the Appendix (Keyword Governance)** — so the writer and Karen see exactly where each term lives, no guesswork. The table:

   | Rank | Keyword | Volume | Assigned to (H1 / H2 n / H3 / FAQ) | or Route → |
   |------|---------|--------|------------------------------------|-----------|
   | 1 (primary) | … | … | H1 | |
   | 2 | … | … | H2 1 | |
   | … | … | … | … | |

A plan that doesn't place-or-route **every** bundle term — shown inline in the Outline, with the full table in the Appendix — is incomplete (the writer skills return it). The writer executes this placement; it never invents it.

---

## The Eugene Schwartz CTA Lens (every CTA, every page)

CTA button text is **page-specific** — drawn from the page's Win Vector and the desire the page just built, not a house-wide label. (Doctrinal home: Doc 140; this is the operating copy the plan and auditor enforce.) Schwartz's principle: copy cannot create desire, it can only channel the desire already in the reader's mind onto the next step. A button passes the lens only if:

1. **Channels existing desire, not our process** — names what the reader wants now (an answer, relief, protection), not what we do. Reject process words ("assessment," "consultation," "evaluation," "audit") and invented terms ("Peak-Volume").
2. **No mechanism, no jargon** — no product/internal terms on the button (AEGIS 5X, HydroVortex, micromesh).
3. **Specific and personal** — "your roof," "your home," the concrete outcome.
4. **Matches the awareness stage** — soft/early = curiosity ("see if…"); hard/after the argument = a confident, direct step.
5. **Completes the page's emotional arc** — pays off the exact tension the page built.
6. **Lowest friction** — warm, active, often first-person phrasing over formal "Request a…/Schedule a…".

**One-line test:** *Does the button name what the reader wants, in their words, or what we do?* If it's what we do, rewrite.

**Example:** "Request a Peak-Volume Assessment" → **"See if your roof will overflow"** (soft) / "See if your roof overflows in the next storm" (hard). Destination unchanged. The plan records each button's text **and the desire it channels**; the auditor (Doc 328) fails any CTA that doesn't pass the lens.

---

## Page-type note

This format applies to **every** page type, including pricing/cost pages. A cost page uses this same structure — its pricing rule lives inside `## Core Argument` or a clearly labeled subsection. The section order above is the structure for all topics; do not invent a per-topic or numbered skeleton.

---

## Minimal conformance checklist (the writer skills enforce; Doc 154 is retired)

- Pre-H1 YAML front matter present with all required fields, including `meta_title`, `meta_description`, `author`, `trust_chip`, `target_body_words`, `image_budget`, `cta_count`.
- The **reviewer path leads** (The Argument → H1 → Key Takeaways + above-fold questions → Outline → FAQ Questions → Open Questions & Decisions Needed) with **no reference or production material above `## The Argument`**; all other sections in the Appendix, reached by inline pointers. Revision Log never at the top.
- `## Outline` present, with **every heading carrying its detail inline** — never titles-only with the substance in a separate section — and including the **keyword→heading map** (H1 = primary keyword; highest-traffic bundle terms in the top H2s; every one of the up-to-20 bundle terms placed or routed), plus `pays_off` / `opens` per heading.
- Media Plan rows ≥ `image_budget`; a diagram on every mechanism section.
- CTA Placement Plan places CTAs by structural milestone (Doc 144: the 3 fixed anchors + tension-resolving section ends), each with a trust signal, and lists every internal link (anchor / target / placement).
- A plan missing any of the above is **incomplete** — the writer stops and returns it (Doc 153 / writer skills).