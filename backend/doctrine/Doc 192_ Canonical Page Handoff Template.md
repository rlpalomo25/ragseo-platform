# Doc 192: Canonical Page Handoff Template

**Version:** 2.22 | **Created:** June 24, 2026 | **Updated:** August 7, 2026 | **Series:** 100 (Doctrine / System) | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Authority for:** every page deliverable handed from a writer agent (Doc 316 MasterShield, Doc 320 Klean Gutter, Doc 324 MMGG) or the Doc 361 refresh agent to the web/publishing team.
**Enforced by:** Doc 328 / the ragseo-auditor (Handoff Conformance gate).

---

## Principle

The publishing team opens any page deliverable and knows exactly where each part lives — metadata, CTAs, image briefs, changelog — without hunting. One shape, every time, so nothing (a trust bar, an image slot, a CTA) gets dropped on the way to publish.

**Block order and labels below are mandatory. Do not rename, reorder, or relocate blocks.**

**Two-stage workflow, one canonical shape.**

**Stage 1 — draft & revise in Markdown (the review format).** Every first draft and all content back-and-forth happen in a clean **Markdown** file (`##`/`###` headings, plain prose, plain-text CTA/image notes; no schema, no styled HTML, no Appendix chrome). This is what Karen reads and iterates in. **Do NOT produce the styled HTML for a first draft or during content revision** — HTML is unreadable to edit and wastes the reviewer's time. A writer that returns HTML before the copy is approved has skipped a stage.

**Nothing changelog-shaped ever leads the file (added July 27, 2026, Karen).** No version note, image-plan summary, "prior fixes" list, or any other build/pipeline commentary — as an HTML comment, a blockquote, or plain text — appears above the H1 in a Markdown draft. That is exactly the "Appendix chrome" the rule above already prohibits, named explicitly here because the habit kept recurring anyway. Changelog-shaped content has exactly one home: the bottom, in the Stage-2 Appendix's Changelog table (item 12), never trailing italic notes and never a leading comment block at either stage.

**Audit Gate — between the stages (revised August 7, 2026, Karen — split into two passes; root cause below).** No page reaches Karen — as a review draft *or* a publish file — until it clears two separate checks, not one self-declared pass.

**(1) Independent mechanical pre-check, before Stage 1 ever reaches Karen — automatic, no decision for the human writer to make (revised August 7, 2026, Karen).** The writer's own read of its draft against Doc 328/329 is not sufficient for the mechanical portion of the gate — counts, symbol placement, banned phrases, structural spacing (see Doc 328/329's gate-stage map, added August 7, 2026). A self-report on that category is the same self-graded gap that let a page ship labeled "FINAL COPY — READY TO PUBLISH" with nothing independently checking it (Doc 329 v1.15/v1.19; Doc 361-MS Step 5's own "this checklist is the writer's own self-check, not the gate" note). Before the Markdown draft reaches Karen or any reviewer, run it through an independent pass against only the Stage 1/Mechanical gates — executed by something that reads the **current** Doc 328/329/192/194/100 fresh off disk at run time, never a cached or pasted-in knowledge-file snapshot, since a stale snapshot is the confirmed root cause of two real version-drift failures already (Doc 329 C11/C27, added Aug 5/Aug 3, 2026). **This is never presented to the human writer as a choice ("should I run this or not") — only the person who built this system knows what the mechanical gates actually check for, and asking someone else to decide whether to skip a check they can't evaluate defeats the point of separating mechanical from judgment gates in the first place.** The check simply runs, every time, and the writer reports the result as a short status line, not a question: *"Running the independent formatting/rules check now,"* then *"Passed — sending for review"* or *"Found [N] issues — fixing before send."* No answer required. Anything that fails goes back to the writer before the reviewer opens the file. This is what actually narrows a reviewer's job to judgment calls — is this comparison good, does this quote sound like the named person — rather than formatting they shouldn't have to be catching by eye.

**(1B) Flag resolution, before the human review checkpoint below, not after (added August 7, 2026, Karen — root cause: FLAG items were being logged in the Pre-Publish Checklist and then never actually chased down by anyone, reaching Karen unresolved or not reaching her at all).** A FLAG is not a FAIL — it doesn't block the page on its own — but logging it as a passive checklist bullet is exactly how it goes unresolved indefinitely; a flag nobody is asked to act on is a flag that gets scrolled past. Before the draft reaches the human review checkpoint below, the writer makes one real attempt to close every FLAG the audit raised, using information already available (the KB, an existing Karen clearance already on record, the source page, a prior approved quote) — not just repeating the flag as a note. Where a flag genuinely can't be resolved from data on hand and needs a specific person's decision, it is not left as a generic open item — it is named explicitly, who the question is for and exactly what's being asked, e.g. *"Needs Karen: is 'Ice Shield' cleared to name as a current MasterShield accessory? Every KB entry for it is Needs Review, not Approved."* A named, specific question is something a person can actually go get an answer to before this reaches someone senior; an unnamed checklist bullet is something a person can keep scrolling past. This applies to judgment-tier flags (Doc 329's gate-stage map) — the mechanical pre-check above doesn't produce flags of this kind, it produces pass/fail on countable things, so this step doesn't apply there.

**(1C) Human review checkpoint — before Stage 2, and again before publish (added August 7, 2026, Karen).** Once flag resolution above is complete, ask two short questions in sequence rather than one long compound one — this is judgment, not something the system can answer for itself: **"Has someone with hands-on field experience looked over this content yet?"** If not yet, stop there; do not ask about publish-readiness in the same breath. Once that answer is yes: **"Is this ready to go to publishing?"** Only an explicit yes on both moves the page forward — no inferring readiness from silence or from a general "looks good."

**(2) Full Doc 328/329, self-run by the writer as before (v2.2, July 20, 2026), still gates Stage 2.** Once content is approved and the styled HTML is built, the writer still runs the full gate on its own output before it reaches Karen or a publisher — re-checking every gate, including the mechanical ones already cleared at Stage 1, not only the new HTML-only checks (JSON-LD, Appendix wrapper, single-file check). A later edit pass can silently break something that was already clean — see the JSON-LD visible/functional mismatch, self-caught August 6, 2026, which is exactly this failure mode.

**"Publish" is a standing trigger, not a separate request (added July 27, 2026, ruled by Karen).** Any time Karen asks for a page's publish-viewable version — a brand-new page, a refresh, or simply re-opening/re-serving a page that already shipped — Doc 328 (or Doc 329 for a 361 refresh) runs first, automatically, before the file is handed back. This holds exactly as much for an already-published page being re-requested as for a first draft; re-serving an old file with no audit re-check is the same gate-skip as shipping new HTML with no audit at all. Karen should never have to separately ask "did we audit this" or decide to start one — asking for the audit on top of "publish" is never jumping a queue, because there is no queue: the audit is not a line item after publish, it's what "publish" already means. (Root cause this closed: Klean Gutter's and MMGG's micro-mesh pages shipped July 10 marked "audit pending" and sat that way for over two weeks before anyone actually ran Doc 328 against them — the self-run instruction existed the whole time but nothing forced it to fire on an existing, already-shipped page. See Doc 208 Worked Example #8.) The gate is what enforces the rules the owners already define (entity-bind per Doc 121 §3.4, noun-first, claim calibration, four-beat FAQ, etc.). **Loading those docs is not the same as executing them** — a writer (including a Claude session running the writer skill with every canonical doc open) can have the whole law in front of it and still jump straight to HTML or leave FAQ answers naked. So the gate is *self-run, not assumed*: **(a)** the writer may not present Stage-1 Markdown as approval-ready until it has audited its own draft against Doc 328/329 and stated the result; **(b)** the writer may not produce Stage-2 HTML at all until Stage-1 has passed — jumping to HTML first *is* a gate-skip, whatever produced it. This is exactly the hole that let an ungated draft (HTML-first, naked FAQ answers) reach Karen: the rules weren't missing and were even loaded — the writer simply didn't run them on its own output. Skipping the self-audit is itself a handoff failure, and the writer is accountable for running it, not the reviewer for catching what it missed.

**Stage 2 — publish format, only after the content is approved.** Once the copy is signed off, and only then, build the **styled HTML file** described below (real CSS + the production Appendix) **plus the page's JSON-LD structured data — good, paste-ready schema for whatever the page carries — the types are chosen mechanically per **Doc 123 §3.0 Schema Decision Matrix** (always `Article` + `Organization` + `BreadcrumbList` + `FAQPage`; add `ItemList`/`Product`/`HowTo`/`LocalBusiness` only if the page has that feature; never `Review`/`AggregateRating` without real first-party ratings)** — as the deliverable handed to the publisher. The JSON-LD is a Stage-2 artifact only: generate it once the content is approved, not during drafting. The HTML build is the required last step, not the drafting format. So: don't hand a publisher the Markdown and call it done — and don't hand Karen the HTML to review, either.

---

## Output format: styled, standalone HTML preview (canonical, v2.0)

The deliverable handed to the publisher is a **self-contained HTML file that already looks like the live page** — real CSS, real headings, real button-styled CTAs, reader-facing captions on placeholder images. The publisher should be able to open it in a browser and see almost exactly what will ship. There is no blue/black instructional annotation anywhere in the reader-facing body; that convention is retired as of v2.0. An agent that cannot render/preview HTML directly must still produce the file in this exact structure for the publisher to open.

**1. Canonical stylesheet — embed verbatim, do not restyle.** Every page uses the same `<style>` block (from Karen's approved template), so every page looks consistent regardless of which brand or writer agent produced it. **Re-sync on every touch, not just at creation (added August 1, 2026, Karen).** "Embed verbatim" means matching this doc's *current* stylesheet, not whatever version was embedded when the page was first built. A page that sits untouched while this doc's stylesheet gains a new rule (e.g. v2.12's `pre` wrap fix) silently drifts out of sync and nothing re-checks it until someone visually inspects the rendered page. Any time a page goes through Doc 328/329 or a refresh pass, diff its embedded `<style>` block against this doc's current one and patch the gap — see Doc 328's Embedded Stylesheet Currency check.

```html
<style>
body{font-family:Georgia,'Times New Roman',serif;max-width:740px;margin:0 auto;padding:30px 22px;color:#1a1a1a;line-height:1.62;font-size:18px;}
h1{font-family:Arial,Helvetica,sans-serif;font-size:31px;line-height:1.2;margin:0 0 18px;}
h2{font-family:Arial,Helvetica,sans-serif;font-size:23px;margin:34px 0 10px;border-bottom:2px solid #eee;padding-bottom:6px;}
h3{font-family:Arial,Helvetica,sans-serif;font-size:19px;margin:22px 0 8px;}
p{margin:0 0 14px;} .byline{color:#555;font-size:16px;margin-bottom:18px;}
ul{margin:0 0 14px;padding-left:22px;} li{margin:5px 0;}
figure{margin:20px 0;text-align:center;}
figure .ph{background:#eef3fb;border:1px dashed #9db8de;border-radius:8px;padding:26px 14px;color:#5b7aa8;font-family:Arial,Helvetica,sans-serif;font-size:14px;}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:15px;}
th,td{border:1px solid #bbb;padding:8px 10px;text-align:left;vertical-align:top;} th{background:#f0f0f0;}
.askthis{background:#0f1b2d;color:#fff;border-radius:10px;padding:22px 24px;margin:24px 0;font-family:Arial,Helvetica,sans-serif;}
.askthis h3{font-size:22px;margin:0 0 6px;color:#fff;font-family:Arial,Helvetica,sans-serif;}.askthis .k{color:#f2792b;}
.askthis ol{list-style:none;counter-reset:q;padding:0;margin:14px 0;}
.askthis li{counter-increment:q;padding:10px 0;border-top:1px solid #2a3a52;font-size:16px;}
.askthis li:before{content:counter(q);display:inline-block;width:26px;height:26px;line-height:24px;text-align:center;border:1px solid #f2792b;color:#f2792b;border-radius:5px;margin-right:12px;font-weight:bold;}
.askthis .foot{background:#20314d;border-radius:6px;padding:12px 14px;margin-top:12px;font-size:15px;}
.callout{background:#f4f6f8;border-left:4px solid #2f5d8a;border-radius:6px;padding:14px 18px;margin:20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;}
.callout .l{font-weight:bold;color:#2f5d8a;text-transform:uppercase;letter-spacing:.4px;font-size:12px;display:block;margin-bottom:4px;}
/* Doc 194 named callout accents — five components, five colors, no two share one. Benefits/Field match the Best Gutter Guards reference exactly (2026-07-29). */
.callout.benefits{background:#eef7ef;border-left-color:#3a8f4d;} .callout.benefits .l{color:#3a8f4d;}
.callout.field{background:#faf7f0;border-left-color:#b5892f;} .callout.field .l{color:#8a6a20;} .callout.field .quote{font-style:italic;font-size:18px;}
.callout.short{border-left-color:#1565c0;} .callout.short .l{color:#1565c0;}
.callout.compare{border-left-color:#6a1b9a;} .callout.compare .l{color:#6a1b9a;}
.callout.watch{background:#fff8ee;border-left-color:#e65100;} .callout.watch .l{color:#e65100;}
.callout.testimonial{background:#eefaf9;border-left-color:#00897b;} .callout.testimonial .l{color:#00695c;} .callout.testimonial .quote{font-style:italic;font-size:18px;}
.quote{font-style:italic;}
.links{font-size:15px;background:#f4f6f8;border-radius:6px;padding:9px 14px;}
.qa .q,.faq .q{font-weight:bold;margin-bottom:3px;} .faq,.qa{margin:0 0 15px;}
.cta{border:2px solid #f2792b;border-radius:10px;padding:18px 20px;margin:26px 0;text-align:center;font-family:Arial,Helvetica,sans-serif;}
.cta .lead{font-size:17px;margin-bottom:12px;}
.cta .btn{display:inline-block;background:#f2792b;color:#fff;font-weight:bold;padding:12px 24px;border-radius:6px;font-size:17px;}
.cta .trust{font-size:13px;color:#666;margin-top:12px;}
.auth{background:#f7f7f7;border-radius:8px;padding:14px 18px;font-family:Arial,Helvetica,sans-serif;font-size:15px;}
.appx{border-top:2px solid #333;margin-top:40px;padding-top:6px;} .appx h2,.appx h3{color:#555;font-family:Arial,Helvetica,sans-serif;}
.appx pre{background:#0f1b2d;color:#e6edf5;border-radius:8px;padding:14px 16px;overflow:auto;font-size:12px;line-height:1.45;white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere;}
</style>
```

**2. Body content is real, publishable copy only.** No instructional text, no component labels, no color-coded annotation appears anywhere in the reader-facing flow. If it's in the body, it ships as written.

**3. Missing images are reader-facing placeholder captions, not instruction lines.** Use `<figure><div class="ph">📷 [one-line caption describing what the image will show]</div></figure>` inline, at the point the image belongs. This caption is real copy — it can ship as the image's caption once the photo/diagram is produced. **Spread these through the body — roughly one every 400–600 words. Never place two back-to-back, and never place one as the last element of a section (added August 1, 2026, Karen) — trailing into the next H2 boundary — or at the end of the page.** An image belongs at an internal paragraph seam; a section's closing beat is argument, not a placeholder photo. **Never place an image inside the Frequently Asked Questions section (added August 7, 2026, Karen — found on a live MasterShield refresh page, where 4 of 9 images had been placed inside FAQ groups and had to be relocated to the Body section in a later pass; this was never written down anywhere in canon before now).** FAQ answers are compact, self-contained retrieval chunks (item 5 below, Doc 122 chunking standard) — an image has no natural home inside a `.faq` block and breaks that shape. All body images belong in the Body section, before the FAQ begins. Work in beauty/installed-on-a-home shots, not only diagrams and failure photos. The full production brief for each (type, exact placement, alt text, purpose, status) lives once, in the Media Assets table in the Appendix (§5) — never inline.

**4. CTAs use the `.cta` component; the required build order is structural, not instructional.** `<div class="cta"><div class="lead">…persuasive close…</div><span class="btn">…button text…</span><div class="trust">…trust bar…</div></div>`. Because the component's own markup runs lead → button → trust bar top to bottom, CTA-Trust Pairing & Order (Doc 328) is satisfied automatically by using the component correctly — there is no separate build-order instruction to write. One button per CTA, labeled by what the reader wants, with its destination captured in the Appendix's CTA Summary table (not inline).

**5. All production/pipeline material consolidates into one Appendix at the very bottom**, separated from reader content by an `<hr>` and a muted, clearly-non-body heading (e.g. `<h2 style="color:#888;font-size:16px;border-bottom:none;">Internal Production Notes — Not for Publish</h2>`). In order, the Appendix carries: the Pre-Publish Checklist (audit result + only outstanding go-live items, as checkboxes), the machine schema/front matter (YAML), the CTA Summary table, the Media Assets table, the Internal Links table, and the Changelog table. Nothing in the Appendix renders as part of the reader-facing page above it — a publisher who deletes everything from the `<hr>` down is left with the exact live page. (Per Karen, 2026-07-10: this replaces scattering blue instructional annotation through the body — "keep a production checklist," but keep it in one place.)

**6. Paragraph spacing is handled by the stylesheet's own `p{margin:0 0 13px;}` rule.** Do not add ad-hoc inline spacing on top of it, and do not omit the stylesheet — an unstyled page reading as a dense wall of text is still a Doc 328 §4D fail.

**7. Production mechanics.** This HTML file is itself the deliverable — viewable directly in any browser, no Drive HTML→Doc conversion step required. If a Google Doc copy is separately wanted for editing/commenting/tracked changes, generate one by importing this same HTML, but the audited, canonical artifact is the HTML file, not a converted Doc.

---

## Required block order

**Reader-facing flow (top to bottom, no annotation of any kind):**

1. **H1** (`<h1>`) — exactly one.
1A. **Hero image (added August 7, 2026, Karen).** Immediately below the H1, before Key Takeaways — exactly **one**, page-appropriate to the page's dominant emotion (beauty/aspiration on brand/conversion pages, the **problem** itself on problem-aware pages: cost, failure, hail) and **thumbnail-legible** (it doubles as the social/OG and SERP thumbnail; see Doc 144's Hero spec, not restated here per Doc 208 Step 0). This block was already required in practice — Doc 144/190/328 all describe it — but had never actually been added to this doc's own mandatory block order, the one place "block order and labels below are mandatory" is stated. A placeholder is acceptable pre-production (Doc 190 §4 Placeholder Completeness Standard). Not to be confused with Doc 144/328's separate **zero images above the fold** rule, which covers only the space between Key Takeaways and Your Questions Answered — the hero sits before that block and is required, not banned by that rule.
2. **`## Key Takeaways`** — the stakes-setter block (internally the "TL;DR"/"Summary"). The on-page heading is always `Key Takeaways`; never label it `TL;DR`, `Summary`, or `Above the fold`. **(Updated per Karen, 2026-07-01; replaces the former `Summary` opener label across the stack.)**
3. **`## Your Questions Answered`** — the 3 broadest reader questions, shown **truncated**: 1-2 sentences that answer a bit more than just the opening line, not the full answer, followed by a link to the full answer in the FAQ. **The link is embedded in the teaser's own closing words, never a separate bolted-on tag (updated 2026-07-31, Karen — replaces the old `<a href="#faq-slug">Jump to full answer</a>` convention):** the teaser sentence simply ends, and its last few words carry the `<a href="#faq-slug">` anchor — e.g. "...and that's where a reverse-curve design earns its keep," with "reverse-curve design earns its keep" as the link. No visible "Jump to full answer"/"Continue reading" tag ever follows the sentence. Each of the 3 teasers' link text is drawn from that question's own content, never the same boilerplate phrase repeated three times. The link still renders with normal hyperlink styling (underline/accent color) so its clickability is obvious without announcing itself — same principle as Doc 221 §3.3's Link Discipline, applied here to an in-page jump instead of a cross-page one. Use the `.qa` component (`<div class="qa"><p class="q">…</p><p>…</p></div>`). Then the **post-Your-Questions-Answered soft CTA + trust bar** (`.cta` component) — it comes after this block, not after Key Takeaways alone. The above-fold block is the *preview*; the full answers live once in the FAQ (see item 5), so nothing is duplicated. (Renamed from `Quick Answers` per Karen, 2026-07-01; truncate-and-link convention added per Karen, 2026-07-04; widened from a single sentence to 1-2 sentences per Karen, 2026-07-10; embedded-link convention per Karen, 2026-07-31.)
4. **Body** — `## ` / `### ` sections. Image placeholders per Output format §3; `.cta` blocks at cadence, each self-contained per Output format §4. The "Ask These Six Questions" section (where present) uses the `.askthis` component. **Named callouts (Doc 194) use `.callout` plus a modifier class matching the component:** `.callout.benefits` (How This Benefits You, green), `.callout.field` (From the Field, gold), `.callout.short` (The Short Version, blue), `.callout.compare` (Compare This, purple), `.callout.watch` (Watch For This, amber), `.callout.testimonial` (In Their Words, teal) — e.g. `<div class="callout field"><span class="l">From the Field: Aaron Kapfer</span>…</div>`. Ask This stays `.askthis` (dark navy); CTA stays `.cta` (orange). Eight components, eight classes, no two share a color — matching Doc 194's style reference exactly (added `.callout.testimonial`, August 1, 2026, closing the gap Doc 194 v1.6 itself flagged as unconfirmed).
5. **`## Frequently Asked Questions`** — grouped under `### ` category headers (`.faq` component per answer), ordered by **reader state**: **Group 1 "The three questions most people start with"** (the full answers for the 3 above-fold questions, each carrying an `id` attribute matching the Your-Questions-Answered jump links), then broad → **mechanism** → **evaluation** → **decision/reassurance**. Answers are front-loaded (first word is part of the answer) and standalone (each makes full sense lifted out alone).
6. **`## About the Author`** — **one author per page** (the `author` from the front matter), whose bio carries the byline and the Article schema `author`. If a second named expert is actually quoted on the page, add their bio **below the author's, labeled as a Contributor / Field Expert** — never a co-equal second author. The contributor bio appears only when that person is genuinely cited on this page, and each bio must carry a real, verifiable credential. Keep the heading singular (`## About the Author`); the schema `author` stays singular so the author entity isn't split across pages.
6A. **`## Technical Sources`** (added August 2, 2026, Karen). Required whenever the page cites external technical/scientific claims — every guardian/mechanism page (Doc 316-M), and per Doc 113 §2.0 "preferred for most pages" beyond that. A **numbered, anchor-targeted list** (`<ol><li id="src-N">`), not a flat paragraph — **format and sourcing rules live in Doc 113 §2.0 (Proof Notes Format) — follow that spec, do not restate it here** (Doc 208 Step 0). Still reader-facing, before the Appendix `<hr>`. Every source listed here must be reachable from a matching body superscript (`<sup><a href="#src-N">N</a></sup>`) — see the Skeleton below for the wired pattern. **Root-cause fix:** three live 361-refresh pages shipped with zero citations section — no doc anywhere had a required slot for one, and the one audit gate that could plausibly have caught it (C13) is scoped to comparison/buying pages, not this. **Second root-cause fix (August 3, 2026, Karen):** even where a Technical Sources section existed, Karen found published pages where its entries had no matching body superscripts at all, or the superscripts were bare Unicode glyphs that link nowhere — the old flat `<br>`-separated paragraph shown here had no `id` for anything to link to, and nothing in this doc or Doc 328/329 checked the body-to-list wiring. Fixed by numbering the list and requiring the anchor pattern; see Doc 113 §2.0, Doc 317 §4.1, and the new Doc 328/329 Technical Sources Link Integrity check. See RAGSEO System State.

**Appendix (below an `<hr>`, muted heading, everything after this point is internal-only — see Output format §5):**

7. **Pre-Publish Checklist** — audit result + only the outstanding go-live items, as checkboxes, **plus the Publish-Readiness Manifest (added July 29, 2026, Karen — see below).** The audit lives here, in the page; there is no separate audit report.

**Publish-Readiness Manifest (added July 29, 2026, Karen).** This one delivered file is the single source for everything the publishing team needs — nothing required to publish lives anywhere else, in a companion file, a separate report, or a chat message. Before handoff, confirm every one of these is actually present and visibly readable by opening this file alone, no other tool, no view-source:

**Independently verified, not just self-declared (added July 30, 2026, Karen).** This Manifest is checked twice, by two different gates, for the same reason C16/C10D recompute other self-declared calls rather than trusting them: Doc 328/329 check it as part of the content audit, and **Doc 195 (Pre-Publication Packaging Audit)** checks it again, independently, as a dedicated non-content pass — plus confirms this deliverable's field names, order, and formatting match every other deliverable the system produces, main pipeline or 361 track alike. A page needs both a passing content audit and a passing Doc 195 report before it reaches Doc 260.

- [ ] Meta Title and Meta Description — visible in the Build Metadata block (item 8), not just present as a raw HTML `<title>` tag
- [ ] URL slug — visible in the Build Metadata block
- [ ] JSON-LD schema — visible AND functional (item 7A below — both forms required, not just the functional one)
- [ ] Article archetype (Doc 135) — visible in the Build Metadata block (item 8)
- [ ] Author assigned, bio present
- [ ] CTA Summary table (item 9), Media Assets table (item 10), Internal Links table (item 11) all present
- [ ] Publisher Note (item 7B) present if this page keeps an existing URL, changes its head keyword, or carries a 301
- [ ] Exactly one delivered file exists for this version in `company/pages/` (added July 29, 2026, Karen) — no duplicate, orphaned, or superseded draft attempt sitting alongside it. The Changelog's most recent row names the one real filename; if a second candidate file exists, that is itself a publish-blocking failure, not housekeeping. **A filename carrying anything other than the `version` field's day.draft stamp — `v6`, `FINAL`, `PUBLISH`, `HANDOFF`, `DRAFT`, or similar — is itself evidence of this violation, not a legitimate naming style (added August 2, 2026, Karen; format defined at the YAML `version` field above).**

If anything on this list is missing, the page is not handoff-ready, regardless of how polished the reader-facing content is — same standing as a missing schema field. Fold any additional publish-blocking gap found in production into this list rather than handling it as a one-off email or side note; if the team needs something to publish that isn't on this list, that's this list's bug, flag it to get added here.

**One deliverable, no orphaned attempts (added July 29, 2026, Karen — root-cause fix).** The moment a corrected or final version of a delivered page is produced, any earlier same-day draft or attempt at that version must be moved out of `company/pages/` immediately (e.g. to `company/pages/_to_delete/`), not left for someone to guess between later. Never let two files both look like "the" deliverable for the same version — the more polished-sounding filename is not a reliable signal for which one is correct, and it can be the broken one.

7A. **Real JSON-LD (added July 21, 2026) — required, separate from the build metadata below.** A `<script type="application/ld+json">` block containing Article schema (headline, author matching the YAML `author` field, datePublished/dateModified, publisher), Organization schema, BreadcrumbList schema, and, when the page has a Frequently Asked Questions section, FAQPage schema (one Question/Answer pair per published FAQ, text matching the visible answer verbatim — never a shortened or reworded version) — the full set per Doc 123 §3.0's Schema Decision Matrix, not just Article + FAQPage. **This was found completely missing from five live MasterShield pages (July 21, 2026)** — the YAML front matter below was mislabeled "Machine schema" and mistaken for this. The two are not the same thing: the YAML block is internal plan metadata for the pipeline; this block is the actual search-engine-readable markup that ships in the page. FAQPage schema is no longer chased for rich-result eligibility (Google deprecated FAQ rich results May 7, 2026) but remains required for AI/LLM extraction, which is this system's whole purpose — see Doc 328's schema check for the fail condition.

**Visible copy required alongside the functional block (added July 29, 2026, Karen — root-cause fix).** The `<script type="application/ld+json">` tags above are correct and required for any workflow that publishes this HTML file directly, but browsers never render a `<script>` tag's contents — opening the file and looking at it, or double-clicking it, shows nothing where the schema lives. That made the schema invisible to a publisher who just wants to copy it into WordPress's SEO plugin, and Karen does not want a separate companion `.jsonld` file to solve that — one document, everything in it. Fix: immediately below the functional `<script>` block(s), repeat the exact same JSON, HTML-escaped, inside a visible `<pre><code>` block, labeled `<p style="color:#888;font-size:13px;margin:4px 0;">Copy the JSON below into your SEO plugin's schema field:</p>` right above it. Same content, twice, two different jobs: the `<script>` tags are what a browser/crawler reads if this file is ever served as-is; the `<pre><code>` block is what a human reads and copies by hand. Both required, in this exact order (functional first, then the labeled visible copy), for every schema block on the page.
7B. **Publisher Note — URL & keyword decisions (REQUIRED whenever the page keeps an existing URL, changes its head keyword, or carries a 301).** A short, plain-language explanation of *why*, written for the person publishing — so an unusual decision reads as planned, not weird. State: (a) **this page keeps its existing URL `[X]` — do NOT create a new page or change the slug;** (b) its head keyword is now `[term]`, chosen because it is the **highest-traffic term this page can rank for** (from GSC/SERP data), even if it isn't the page's name; (c) other strong terms are covered as sub-keywords on this same page; (d) a one-line reason, e.g. *"This page already ranks and has traffic history — we preserve that equity and re-target it to the term now pulling the most traffic, rather than starting a new page from zero."* List any 301s with the same rationale. If it's a brand-new page with none of these situations, say so in one line. The point: the publisher sees the decision was thought through and is executing a plan, not guessing.
8. **Build metadata (YAML front matter) — renamed from "Machine schema" July 21, 2026 to stop the naming collision with item 7A above.** The YAML fields (below), presented as plain text, not rendered as page metadata. This is internal pipeline tracking data, not search-engine schema — see item 7A for the actual schema requirement.
9. **CTA Summary** — table (every CTA in the body).
10. **Media Assets** — table (every placeholder/image in the body).
11. **Internal Links** — table.
12. **Changelog** — table. (Never trailing italic notes.)

---

## YAML front matter — required fields

```yaml
---
plan_id: PLAN-<guardian>-<brand>-<audience>-v<n>
version: <n.n>   # day.draft (defined August 2, 2026, Karen): day increments only when work resumes on a calendar day after the last draft; draft increments once per draft produced that day, starting at 1 -- e.g. 3.11 = 3rd day of work on this page, 11th draft made that day. A draft overwrites the same one file in company/pages/ in place -- the version number carries the history, never a new filename per draft -- and lives only in company/pages/, never company/execution-plans/ (Doc 153 plans and Doc 312 architecture briefs only).
writer_id: <Doc 316 | Doc 320 | Doc 324 | Doc 361> / <Brand> Writer Agent
brand: <MasterShield | Klean Gutter | MicroMeshGutterGuards.com>
page_classification: <brand-conversion | source-of-truth | b2b-trade>
page_type: <pillar | cluster | local>
page_subtype: <mechanism | comparison | pricing | symptom | installation | faq | b2b | "">
meta_title: <=60 chars, keyword-front, brand suffix, no TM/®
meta_description: <string>
url_slug: /aegis-5x/<slug>/
image_budget: <number from media_plan.image_budget>
author: <Karen Sager | Aaron Kapfer>   # from the plan; byline + About block + Article schema author
trust_chip: <page-relevant 5th proof>  # from the plan; the trust bar's 5th chip on this page
article_archetype:   # added July 29, 2026, Karen; shape fixed August 1, 2026 — this is an object, not a string, carried forward verbatim from the Execution Plan's Doc 153 "Argument Archetype & Decision Axis Selection" fields (added Doc 153 v12.7) so the selection survives even if the plan file itself is later lost, and so it's pullable straight off the delivered page for Karen's tracker
  primary: <one of Doc 135's 12 archetypes>
  secondary: <second archetype, only if the page genuinely blends two structures — omit this key entirely if not>
  rationale: <one-line reason tied to the Win Vector and buyer_state, per Doc 153>
  decision_axis: <per Doc 153 — flag "undefined — pending Karen confirmation" until Doc 153's Decision Axis definition is resolved system-wide; never guess at a value>
extractable_blocks:   # array of objects; shape fixed August 1, 2026 -- matches Doc 153's citation_intent_map.blocks[] (id/location/plain_language_statement/extractable) so the Auditor can diff delivered-vs-planned directly
  - id: <matches the plan's citation_intent_map block id>
    location: <H2/section this block lives under>
    content: <the delivered 2-4 sentence extractable statement, verbatim>
  # one entry per citation_intent_map block marked extractable:true in the plan
cta_blocks: [ ... ]   # flat array of CTA IDs only (e.g. [cta-soft, cta-medium, cta-hard-1]) -- shape fixed August 1, 2026. This is an index into the CTA Summary table (item 9) below, not a second copy of it: location/type/text/destination live once, in that table. An ID here with no matching row there, or vice versa, is a mismatch.
internal_links: [ ... ]   # flat array of link target slugs only -- shape fixed August 1, 2026. Same principle as cta_blocks: an index into the Internal Links table (item 11) below, not a duplicate of it.
entity_usage: { }   # flat count map, <Entity Name>: <real mention count, reader body only, counted programmatically> -- shape fixed August 1, 2026, e.g. {AEGIS 5X: 14, ShingleSafe: 7, CopperCare: 4}. Every entity named in the Build Metadata's guardian/brand references should appear as a key; a page that only ever needs to report one entity's count still uses this shape, not a different one.
execution_plan_alignment: { ... }
---
```

`writer_id` uses the fixed form `<Doc nnn> / <Brand> Writer Agent` — not free text like "GPT-WRITER-AGENT" or "Opus."

---

## Table column standards (fixed)

**CTA Summary** — one button per CTA, labeled by what the user does. No orphan secondary link beside a CTA (e.g., a stray "Contact us").

| # | CTA ID | Location | Type (soft/medium/hard) | Button text | Destination | Trust signal paired |

**Media Assets**

| # | Asset description | Placement section | Claim it supports | Alt text | Status |

**Internal Links**

| # | Anchor text | Target URL | Placement | Purpose |

**Changelog**

| Version | Date | Summary |

---

## Skeleton (copy this shape)

```html
<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title><Meta Title></title><style>
[canonical stylesheet, verbatim, Output format §1]
</style></head><body>

<h1><H1></h1>
<p class="byline"><em>By <Author>, <role/brand tie-in></em></p>

<h2>Key Takeaways</h2>
<ul><li><stakes-setter bullet></li><li>...</li></ul>

<h2>Your Questions Answered</h2>
<div class="qa"><p class="q"><Q1>?</p><p><1-2 sentence teaser ending in its own <a href="#faq-1">linked closing words</a>.></p></div>
<div class="qa"><p class="q"><Q2>?</p><p><1-2 sentence teaser ending in its own <a href="#faq-2">linked closing words</a>.></p></div>
<div class="qa"><p class="q"><Q3>?</p><p><1-2 sentence teaser ending in its own <a href="#faq-3">linked closing words</a>.></p></div>

<div class="cta"><div class="lead"><persuasive close></div><span class="btn"><button text> →</span><div class="trust"><trust bar></div></div>

<h2><Body H2></h2>
<p><prose></p>
<figure><div class="ph">📷 <one-line caption></div></figure>
<p><prose ending in an external technical/scientific claim.><sup><a href="#src-1">1</a></sup></p>

<div class="cta"><div class="lead">...</div><span class="btn">...</span><div class="trust">...</div></div>

<h2>Frequently Asked Questions</h2>
<h3><Category></h3>
<div class="faq" id="faq-1"><p class="q">1. <Q>?</p><p><full answer.></p></div>

<h2>About the Author</h2>
<div class="auth"><Author bio.></div>
<!-- only if a second expert is quoted on this page -->
<div class="auth"><strong>Contributor / Field Expert:</strong> <name, role, bio.></div>

<h2>Technical Sources</h2>
<!-- required whenever the page cites external technical/scientific claims -- format per Doc 113 §2.0, not restated here -->
<!-- numbered + anchor-targeted so body superscripts actually link here (fixed August 3, 2026 -- the old flat <br>-separated paragraph had no ids to link to) -->
<ol>
<li id="src-1"><Topic>: <source description.></li>
<li id="src-2"><Topic>: <source description.></li>
</ol>

<hr>
<h2 style="color:#888;font-size:16px;border-bottom:none;">Internal Production Notes — Not for Publish</h2>
<p>▸ PRE-PUBLISH CHECKLIST — Audit: <PASS / PASS WITH NOTES></p>
<p>☐ <outstanding item></p>
<p>▸ PUBLISH-READINESS MANIFEST — meta title/description ☐, url slug ☐, JSON-LD visible+functional ☐, article archetype ☐, author/bio ☐, CTA/media/links tables ☐, publisher note (if applicable) ☐</p>

<pre><YAML front matter, fields above, including article_archetype></pre>

<h3>Schema (JSON-LD)</h3>
<script type="application/ld+json">{...Article schema...}</script>
<script type="application/ld+json">{...Organization schema...}</script>
<script type="application/ld+json">{...BreadcrumbList schema...}</script>
<script type="application/ld+json">{...FAQPage schema, if applicable...}</script>
<p style="color:#888;font-size:13px;margin:4px 0;">Copy the JSON below into your SEO plugin's schema field:</p>
<pre><code>&lt;script type="application/ld+json"&gt;{...same Article schema, HTML-escaped...}&lt;/script&gt;
&lt;script type="application/ld+json"&gt;{...same Organization schema, HTML-escaped...}&lt;/script&gt;
&lt;script type="application/ld+json"&gt;{...same BreadcrumbList schema, HTML-escaped...}&lt;/script&gt;
&lt;script type="application/ld+json"&gt;{...same FAQPage schema, HTML-escaped, if applicable...}&lt;/script&gt;</code></pre>

<h3>CTA Summary</h3>
<table><tr><th>#</th><th>CTA ID</th><th>Location</th><th>Type</th><th>Button Text</th><th>Destination</th><th>Trust Signal Paired</th></tr>...</table>

<h3>Media Assets</h3>
<table><tr><th>#</th><th>Placement Section</th><th>Image Type</th><th>Purpose</th><th>Alt Text Direction</th><th>Status</th></tr>...</table>

<h3>Internal Links</h3>
<table><tr><th>#</th><th>Anchor Text</th><th>Target URL</th><th>Placement</th><th>Purpose</th></tr>...</table>

<h3>Changelog</h3>
<table><tr><th>Version</th><th>Date</th><th>Summary</th></tr>...</table>

</body></html>
```