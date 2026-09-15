# Doc 207: Fact Nugget System (Capture, Check, Promote)

**Version:** 1.0 | **Last Updated:** July 8, 2026 | **Status:** Adopted (200 Series: Workflow & Governance)

**Adopted from:** `PROPOSAL — Fact Nugget System (capture, check, promote).md` (drafted June 30, 2026, approved July 8, 2026 as part of the micro mesh gutter guards execution-plan retrospective). Content below is unchanged from the proposal except for this header and the doc number.

---

A repeatable way to make sure every reusable truth found while building content lands in the **KB Master Library** (the operational fact registry — Doc 114 points to it, this doc governs it) instead of dying on one page, and that nothing unverified gets reused. New knowledge enters the KB as **Needs Review** and is only usable once Karen approves it.

## What a "fact nugget" is
A short, reusable, verifiable statement about the product or category that we would want to say the same way on more than one page. Examples from the best-gutter-guards build: "AEGIS 5X is built into both MasterShield and Klean Gutter," the pine-needle bounce behavior, "beyond generic stainless," the sleep-at-night guarantee.

A nugget is not: a page-specific detail, an opinion, or any claim we can't back.

## The system has three parts

### 1. Capture (built into steps we already run)
Every execution plan and every audit ends with a short **Fact Nuggets** list, candidates surfaced during that build. Because it's a required closing step, capture stops being ad hoc.

### 2. The check — a nugget joins canon only if it passes all five
- **Sourced.** Traces to a citation (Doc 113), a patent or registration number, first-party data, or a named expert. No unsupported claims.
- **Reusable.** True on more than one page, not tied to one address or one section.
- **Ours.** Says something distinctly MasterShield / Klean / MMGG, or says a common thing in our exact words.
- **Safe.** No absolute promise ("never," "100%"), no competitor-litigation claim, no trade-secret leak (for example, never the mesh aperture size).
- **One wording.** Written once, entity-first, the way it should be repeated, and checked against Doc 114 so we don't add a duplicate or a contradiction.

### 2a. Handling a claim that's still in the queue
**Candidate nuggets in the queue may not be used in new content until they pass all five gates and are added to Doc 114. Writers treat them as unavailable until promoted.** This closes the gap where one build surfaces a candidate and the next build starts before the queue is reviewed: until a claim is in Doc 114, it does not exist for writing purposes.

### 3. Promote and sync
Nuggets that pass go into **Doc 114 only** (the verified-fact registry), dated, then synced to all four systems (Brain Trust, Drive, FileZilla, Manus). They do **not** go straight to Doc 432. Doc 432 (Gold Answers) holds answer blocks formatted and framed for AEO extraction, which is a separate job: a verified fact is not automatically an extractable answer. The Doc 354 SOT Agent / Gold Answers team pulls from Doc 114 when it builds or updates an answer block. This keeps the two registries doing distinct jobs: Doc 114 stores what's true, Doc 432 stores how it's answered. Promote in a batch, not mid-build, so canon isn't edited while a page is in flight.

## The loop that makes it self-checking
The Doc 328 auditor already should reject any claim that can't be traced to Doc 113/114. Add one line to that step: **every claim the auditor can't trace is either killed or sent to the nugget queue for vetting.** Nothing reusable is lost, nothing unverified ships.

## Owner and cadence
- **Owner:** Karen (or a delegated reviewer) approves what enters Doc 114.
- **Cadence (a gate, not a calendar):** **the nugget queue is reviewed before any new execution plan is approved.** Tying the review to the build cycle, rather than "weekly," means a candidate can never sit unreviewed while pages ship faster than the review runs. No plan moves forward with an unresolved queue.

## When the harvest runs — the FINAL APPROVED article is the binding pass
The harvest runs on the **final approved article** — the version that actually ships, after Karen's approval edits — not only on the audit-stage draft. This is mandatory and non-negotiable: approval-stage edits routinely introduce new knowledge (a sharper claim, a field detail Karen adds, a reworded proof point), and if the only harvest happened at audit time that knowledge would die on the page. So the last step of shipping any page is: **diff the final approved article against the KB Master Library and route every claim not already there into the KB as `Needs Review`.** The audit-time pass (below) is a useful first draft of the candidate list; the final-approved pass is the one that counts. No page is "done" until its approved knowledge has been harvested back.

## Tooling
Build the **nugget harvester** as a closing step inside the Doc 328 auditor. It diffs a finished page against the **KB Master Library** and lists every claim not yet in the registry, so the candidate list builds itself. This is deterministic pattern-matching, not judgment, so it's cheap to run and reliable. Running it inside Doc 328 means every audited page automatically contributes its candidates with no extra manual step. This is the **first-pass** candidate list; re-run the same diff on the final approved article (above) so approval-stage additions are caught too. Defer the judgment (the five gates) to the human review; do not defer the harvesting.

## Starting queue
The best-gutter-guards patch file already holds the first batch of candidates, run those through the five-point check at the next review and promote the ones that pass.

## Refresh track (Doc 361)
The standalone Refresh GPT has no QA chain to run its own five-gate review. Its obligation is narrower but still binding: flag any new claim surfaced during a refresh and hold it rather than write it in, per Doc 361 §7E; and, **once the article is final-approved, list every claim in it that isn't already in the KB Master Library and route those to the KB as `Needs Review`** — the same final-approved harvest as the main track, just without the five-gate adjudication (that stays here, on Karen's review). The refresh agent captures and routes new knowledge; it never promotes it itself. This is what makes the loop close on the refresh track too: KB feeds the page, the approved page feeds the KB.