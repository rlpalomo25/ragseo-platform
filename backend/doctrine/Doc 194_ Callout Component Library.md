# Doc 194: Callout Component Library

**Version:** 1.9 | **Created:** 2026-07-01 | **Last Updated:** 2026-08-01 | **Series:** 100 (Doctrine / System)

> **v1.9 (August 1, 2026, Karen):** Root-cause fix for the AEGIS 5X CTA/callout overcrowding complaint. The Placement rules never explicitly said a callout can't carry its own heading, and the phrase "callouts sit between sections" (mirrored verbatim in Doc 316/320/324) was ambiguous enough to read as license to give a callout its own H2 -- which is exactly what happened on the live page (two testimonial-type callouts, each promoted to a full H2 section with its own photo). Added an explicit "never its own heading" rule and closed the "separated only by a bare heading" loophole in the never-two-in-a-row rule. See RAGSEO System State.
> **v1.8 (August 1, 2026, Karen):** Confirmed the `.callout.testimonial` CSS class is now present in Doc 192 (v2.13) and updated this doc's own Style Reference note to match, closing a gap this doc flagged as unconfirmed since v1.6. Also the anchor for a full callout-propagation pass: all pipeline writer docs (316/320/324 and 316-B2B/C/FAQ/G/Ins/L/M/P/Sym) and all three 361 refresh tracks (Instructions + Knowledge, plus the shared Workflow Reference) now carry this library's full eight-component menu and the Mix requirement in their own text, not just a pointer here. See RAGSEO System State.

> **v1.7 (July 31, 2026, Karen):** Added a callout-mix requirement (below, under Placement rules): Karen noted, looking at a live page, that "How This Benefits You" and "In Their Words" go unused far more often than "From the Field," even when a page has several callouts. No prior rule required variety — a page could legally run all-From-the-Field and pass. Added a mix rule and a matching non-critical audit flag (Doc 328/329).
> **v1.6 (July 31, 2026, Karen):** Added **In Their Words**, a customer-testimonial callout — a genuine structural gap: we had testimonial content requirements (Doc 141) and, as of this pass, an approved testimonial bank (Doc 113 §3.4), but no named format component to carry them, so testimonials never had a place to consistently land on a page. Teal accent (unused prior to this addition). Added to the content-required-by table and the Doc 192 CSS-class list below.
> **v1.5 (July 27, 2026, Karen):** This doc's seven-color style reference had never been reconciled with Doc 192's actual embedded stylesheet — every page shipped with `.callout`/`.askthis` in one generic gray, regardless of which named component it was, because the CSS to render the difference simply didn't exist. Found on a real page (Gutter Guard Cost, MasterShield) where the callouts weren't even labeled, compounding the gap. Doc 192 v2.5 now has real classes for all seven (`.askthis`, `.callout.benefits`, `.callout.field`, `.callout.short`, `.cta`, `.callout.compare`, `.callout.watch`) matching the colors below exactly. Writers: label the component with its bold name AND its class; a named-but-unclassed callout still renders gray.
**Authority for:** the named "callout" sections that break up long pages, used by every brand writer (Doc 316 / 320 / 324) and the publisher.
**Companion to:** Doc 192 (Canonical Page Handoff Template) — these are approved components the build sheet can drop in. Enforced by Doc 328 (Auditor).

---

## Why callouts exist

Our pillar pages are long. Long pages read as heavy, and a heavy page loses the reader before the argument lands. Callouts are the fix: short, visually distinct, **named** blocks that give the eye a rest, hand the skimmer the point, and double as clean extraction units for AI answer boxes. Each one must *say something* (a question, a field truth, a verdict, an offer), never just decorate. Where competitor "review" pages use boxes as affiliate furniture, ours carry substance.

**Placement rules (enforced by Doc 328):**
- **A callout is never its own heading (added August 1, 2026, Karen).** A callout is an inline component embedded inside the H2 section whose argument it supports -- it must never carry its own H2/H3 title, and it must never be paired with a photo as if that photo were its section hero. "Callouts sit between sections" (below) describes *where in the reading flow* a callout lands -- between paragraphs, breaking up a section's body -- not a license to promote it to section-level with a heading of its own. **Found on a live MasterShield page (AEGIS 5X):** a From the Field quote and an In Their Words testimonial were each given their own H2 ("In Her Own Words," "Installed on Their Homes. Not Just Their Word.") with a photo apiece, turning two lightweight callouts into two full mini-sections -- a direct contributor to a page reading as if it had "way too many" CTA/callout sections. This rule closes that failure mode.
- Roughly **one callout per dense section**, and **never two in a row -- including when only a bare heading with no real body paragraph separates them.** A heading is not content. Two callouts separated only by a heading (no intervening paragraph of real prose) are still back-to-back for this rule.
- A callout must carry real content, not a restatement of the paragraph beside it.
- Images sit at paragraph seams; callouts sit inline between paragraphs, inside a section's body. The two do not stack.
- **Mix requirement (added July 31, 2026, Karen):** A page must draw from at least three distinct named components across its body — never let one type (most often **From the Field**) carry the whole page while **How This Benefits You** and **In Their Words** sit unused. **In Their Words** specifically must be used whenever Doc 113 §3.4 holds an approved testimonial relevant to the page's topic and a natural social-proof moment exists (per that component's own placement rule above) — having testimonials available and not using one is itself a gap, not a neutral choice. This is a mix requirement, not a quota: don't force a callout where it doesn't fit, but don't default to one type out of habit either.

---

## The named components

Each callout carries its **name as a bold label** so it reads as a recognized component. Use these names verbatim.

| Name | Job | Where it goes | Style tier |
|------|-----|---------------|-----------|
| **Ask This** | The question(s) to ask any company on this topic. The page's "take this to the estimate" moment. | After the failure/criteria section | Branded dark box (like the six-question ASK THIS block) |
| **How This Benefits You** | Translates a mechanism into the homeowner's payoff (less maintenance, safety, savings). | After a mechanism or a type verdict | Green accent |
| **From the Field** | A real Karen or Aaron quote/observation, labeled "From the Field: [name]." Replaces awkward in-body "as Karen puts it." | Beside the mechanism or situation it illuminates | Gold accent |
| **The Short Version** | One-line takeaway that compresses a dense section for the skimmer. | End of a long/dense section | Blue accent (info) |
| **CTA / action box** | A conversion offer built lead → button → trust bar (e.g., **Free Roof-Line Check**, **Get the six-question checklist**). Named by the action, one button, trust bar directly below. | At the Doc 144 CTA milestones | Orange accent |
| **Compare This** (added July 21, 2026) | A compact comparison matrix: guard/product type down the side, "what it solves / what it exposes / where it performs best / what to ask before buying" across the top. Defeats category-level competitor recommendations ("perforated aluminum is best") without naming competitors. | After the section introducing guard types or categories | Purple accent (fixed July 21, 2026 — originally assigned Blue, which collided with The Short Version) |
| **Watch For This** (added July 21, 2026) | An early-warning checklist — observable signs a reader can check themselves before a failure becomes visible/severe (water marks, debris line, sagging, growth underneath, icicles in new spots). Answers the "hidden damage" / serviceability objection with something actionable, not just reassurance. | Near a hidden-failure or inspection-access section | Amber/warning accent (fixed July 21, 2026 — originally assigned Gold, which collided with From the Field) |
| **In Their Words** (added July 31, 2026) | A named, attributed customer testimonial (first name + city, evidence-backed per Doc 141 §5), pulled from the approved bank in Doc 113 §3.4. Distinct from **From the Field**: that's Karen or Aaron's own expert observation; this is an external customer's voice. | Near an existing trust/social-proof moment — a Local page's bottom-of-funnel section (required there, per Doc 141), or a Cluster/Pillar page's late-page confidence section. **Not inserted at random, and not on every page** — only where a natural social-proof moment already exists. | Teal accent (new — first use of this color in the library) |

**This is the single owner of the format requirement for every named component (added/expanded July 21, 2026).** Every row in the table above has a content-requirement living in another doc — the content doc mandates that something must *exist*; this doc mandates what it must *look like*. Both are required, and they are graded separately. A content check passing does not mean the format check passes.

| Named component | Content required by |
|---|---|
| From the Field | Doc 102 §E (Authority Layer, attributed quote); Doc 316-M (field stories); Doc 328 Field Story Presence; 361 tracks' Named Author Citation |
| Ask This | Doc 142 §11B (six-question framework, universal on every page except pure utility pages — scope fixed July 29, 2026, Karen); Doc 328 §7D Ask This check (broadened v16.8, presence required, not just format-when-present); Doc 329 C10 (broadened v1.17, every page except comparison/buying-only) |
| How This Benefits You | Doc 328 Core Argument: Life Outcome check |
| Compare This | Doc 329 C9 (comparison depth) |
| Watch For This | (recommended, not yet mandated by a content check — available for use) |
| In Their Words | Doc 113 §3.4 (Approved Customer Testimonials); Doc 141 (Master Trust Asset Inventory; Local-page bottom-of-funnel testimonial requirement); Doc 141 §5 No Generic Testimonials rule |

**Found missing on a live MasterShield page (July 21, 2026):** From the Field existed as unpackaged prose. Checking the pattern surfaced the same gap for Ask This and How This Benefits You — content required, format never connected, on both the main pipeline and the 361 track. All three are now fixed at both the content-owner doc and the relevant audit gate (Doc 328 and/or Doc 329). **Do not restate the format rule elsewhere — point here.** If a new named component is added to this table, add its content-owner to this list in the same edit, so this table stays the one place that shows whether every component actually has a connected content requirement.

**Reserved / to-build (approved names for future use):**
- **Score Your Guard** — an interactive, tickable version of the six questions (the Zero-Click tool).
- **Is This You?** — a fit box in a types section ("right for you if / skip it if"), framed to homeowner benefit, never a "we recommend us" box.

---

## Style reference (publish-time)

From the styled preview: Ask This = dark navy box, white text, orange numbers; How This Benefits You = green left-accent; From the Field = gold left-accent, italic quote; The Short Version = blue left-accent; CTA = orange bordered box with a button and a trust line beneath; Compare This = purple left-accent, table styling; Watch For This = amber/warning left-accent, checklist styling; In Their Words = teal left-accent, italic quote with name/city byline. Eight components, eight distinct accent treatments — no two share a color, so each reads as its own recognized shape at a glance. Publisher builds these as reusable builder components; the writer marks them in the copy with the bold name label. **Doc 192 CSS class:** `.callout.testimonial` (teal) — confirmed added to Doc 192's stylesheet, v2.13 (August 1, 2026), closing the gap this note originally flagged.

---

## Handoff & audit

- In the pipeline `.md`, a callout is a blockquote led by its bold name (`> **Ask This.** …`).
- In the Doc 192 build sheet, it is `▸ COMPONENT: Callout — [name]` followed by the copy.
- Doc 328 checks: callouts are named from this list, carry substance, obey the one-per-dense-section / never-two-in-a-row rule, and CTAs follow the lead → button → trust order.

*This library is extensible: a genuinely new callout kind gets a name here before it is used, so the vocabulary stays consistent across every page and brand.*