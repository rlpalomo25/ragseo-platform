# Doc 190: Publishing and Page Assembly System

**Version 6.7** | **Last Updated:** July 31, 2026

> **v6.7 (July 31, 2026, Karen):** Retired remaining live "TL/DR"/"TL;DR" references in favor of "Key Takeaways," part of the system-wide sweep triggered by Karen renaming Doc 155 Section 5 to "Key Takeaways Quality Gate." See RAGSEO System State, Twenty-second finding. This also closes a real contradiction with Doc 192's binding "never label it TL;DR" rule — this doc's own prose was still calling for a "TL;DR summary," which is exactly the wrong signal to a writer. (Schema field names `structure.tldr.bullets` / `structure.tldr.above_fold_faqs` are unchanged — those are Doc 153/193 data fields, not display labels.)

> **Purpose:** This document closes the critical "last mile" gap between a finished draft and a live, fully optimized published asset. It provides the rules and systems for page assembly, visual optimization, and technical publishing to ensure that the strategic and narrative work done in the writing phase translates into maximum performance.

> **v6.6 (July 31, 2026, Karen):** Added a Placeholder Completeness Standard to Section 4 — Karen's direct ruling that a complete placeholder (correct placement + one-line caption + alt-text direction on record) is the correct, complete deliverable at this stage, never a note or a fail. Written here as the source doc so Doc 328/329's own image gates can point at one place instead of re-deciding it per audit. Direct response to placeholder-pending-production repeatedly surfacing as a "PASS WITH NOTES" note across multiple audit reports when it was never a real defect.
> **v6.5 (July 26, 2026, Karen):** Image policy reset, decided after team feedback (Gaby, Christine, Robert). **Kept unchanged and deliberately:** the competitor-matching image count formula (Section 3) — this exists to serve ranking competitiveness, not just to manage workload, and none of the three feedback responses weighed that tradeoff, so the count itself stays. **What changed:** (1) a table or calculator now satisfies the mechanism-diagram requirement when it shows the same relationship clearly — a custom diagram is only required when the concept is genuinely visual/spatial; (2) stock photos are no longer forbidden — allowed with credit; (3) a new fill-order preference for image slots (existing photo → new photo → labeled AI illustration → composite), cheapest/fastest first; (4) AI-generated images get one universal caption line, not a split by mechanism/process/technique (the split proved ambiguous in practice — two reviewers independently hit the same wall); (5) stock photo credit goes in a caption line or footer section, never alt text — alt text stays accessibility/content-description only, per its actual function for screen readers and image search, and per most stock licenses' expectation that attribution be human-visible. See Section 3, Section 4, and the Final Assembly Checklist (Section 11).

---

## How to read this document — audience map

**Publishing a page in the builder? Start at Section 1.** Everything above Section 1 is machine/pipeline material — the writer agent and the auditor handle it automatically before the page reaches you. You do not action it.

- **"Pipeline Publish Contracts" + Section 0A — [AI / PIPELINE — publishers skip].** Input contracts, entity checks, metadata mapping, REJECT/WARN protocols. Not a human task.
- **Sections 1–10 — [ASSEMBLY RULES].** How the page is built and optimized. Most are produced upstream by the writer and verified by the auditor; you apply the ones that live in the CMS (the above-the-fold container styling, schema, image filenames/alt/captions).
- **Sections 11–12 — [PUBLISHER — DO THESE].** Your pre-publish checklist and the post-publish Google Search Console verification. This is your core to-do.

If you only read two sections, read **11 and 12**.

---

## Pipeline Publish Contracts  — [AI / PIPELINE — publishers skip to Section 1]

| Pipeline | Publish Contract | Shared Mechanics |
|----------|-------------------|------------------|
| **Main Pipeline** | Execution Plan structure, Win Vector enforcement, CTA positions per Doc 180 | WordPress, schema, internal linking |
| **SOT answers (embedded)** | SOT answer set (Doc 163/354), metadata packet, entity-passed status — embedded into the host pillar/cluster by the writer, not published as its own page | Embedded in host page; schema; internal linking |

**SOT-Specific Requirements:**
- Metadata packet from Doc 354 required
- FAQ schema for AI extraction where the page has real FAQ content (count driven by the question set, not a fixed 20; FAQ rich results deprecated May 7 2026 — extraction only, not a SERP feature)
- Comparison schema if comparison trigger = TRUE
- Registry entry in SOT Asset Registry
- Version tracking for parent-child relationships

---

## 0A. SOT Pipeline Input Contract  — [AI / PIPELINE — publishers skip to Section 1]

When input arrives from the SOT pipeline (instead of main content pipeline), the following apply:

### SOT Input Requirements

| Input | Source | Required |
|-------|--------|---------|
| SOT answer set | Doc 354 | Yes |
| Metadata packet | Doc 354/358 | Yes |
| Comparison trigger flag | Doc 163 | If TRUE |
| FAQ eligibility | Doc 163 | If TRUE |
| Entity consistency passed | Doc 358 | Yes |
| Local variant status | Doc 355 | If local |

### Entity Check as Publish Prerequisite

**Doc 358 MUST pass before assembly/publish.**

- Verify entity consistency status is "passed"
- If failed → do NOT proceed to assembly
- Return to Doc 354 with failure report

### Version-Bound Verification (Gap 6 Fix)

Before proceeding to assembly, verify:

| Check | Validation |
|-------|-----------|
| Asset ID present | SOT asset has unique identifier |
| Version matches pass status | Pass status applies to this version, not stale |
| Local derivative links | If local: parent SOT ID + version confirmed |

**Error:** If asset ID missing or version mismatch → DO NOT PROCEED. Return to Doc 354/355 with version mismatch report.

### Metadata Mapping Error Protocol (Gap 4 Fix)

If metadata packet is incomplete or unmappable:

| Missing Field | Action |
|-------------|-------|
| primary_question | REJECT - return to Doc 354 |
| entity_definitions | REJECT - return to Doc 358 |
| product_identifiers | REJECT - return to Doc 354 |
| mechanism | REJECT - return to Doc 142 |
| comparison_fields present but empty | WARN - proceed without comparison |
| faq_pairs present but empty | WARN - proceed without FAQ |
| Local variant incomplete geo | REJECT - return to Doc 356 |

**Error Protocol:**
1. Check all required fields present
2. If REJECT → do NOT proceed, return with failure report
3. Log all WARN conditions for manual review

### Page Type Assembly Rules

| SOT Type | Schema | Image Localization | CTA Behavior |
|----------|-------|------------------|----------------|
| Base SOT | Standard SOT schema | No localization | Standard |
| Local SOT | LocalBusiness schema | Local images + geo-modifiers | Local CTA |
| B2B SOT | Article + professionalService | Professional images | B2B CTA |

### Comparison Trigger Implementation

If comparison trigger flag = TRUE:
- Insert comparison table per Section 2 rules
- Implement comparison schema (Review or Product)
- Link to comparison asset if separate page

### FAQ Block Implementation

If FAQ eligibility = TRUE:
- Populate FAQ schema from metadata FAQ pairs
- Format as Q&A per E-E-A-T guidelines
- Link to search visibility enhancement

### External Validation Priority Handling

The metadata packet includes `external_validation_priority` (high/medium/low). Handle as:

| Priority | Action |
|----------|--------|
| HIGH | Flag for manual review before publish |
| MEDIUM | Auto-publish, log for weekly review batch |
| LOW | Auto-publish, no logging |

*High-priority assets require human review before going live.*

---

## 1. Above-the-Fold Design Rule  — [PUBLISHER — START HERE]

The above-the-fold section is not content; it is a **decision interface**. It must be visually distinct from the body of the article to signal its purpose to the user.

*   **Visual Distinction:** The entire above-the-fold section must be contained within a visually distinct container (e.g., a light gray box) to separate it from the main article narrative.
*   **Information Density:** This section must be highly scannable and prioritize direct answers over narrative. It must contain:
    *   A concise Key Takeaways summary in bullet points (content defined in Execution Plan `structure.tldr.bullets` — Writer must not alter).
    *   The top 2 FAQ answers immediately below Key Takeaways (content defined in Execution Plan `structure.tldr.above_fold_faqs`).
    *   A prominent, tool-like Call-to-Action (CTA).
*   **Typography:** Use a slightly smaller paragraph width and tighter line height to increase information density. Use bolding to emphasize key phrases.
*   **Visual Support:** May include small icons or a simple diagram, but **no full-width images**.

---

## 2. The Expert Callout Block System

This is a critical E-E-A-T signal. It provides a structured way to inject direct, first-person expertise from our named expert (Aaron Kapfer) into the content.

*   **Purpose:** To add a layer of unique, human authority that cannot be replicated by AI, and to visually break the page with a high-value insight.
*   **Placement:** One Expert Callout Block should be placed within the first 1,000 words of an article, typically after a key mechanism has been explained or a common myth has been debunked.
*   **Format:** The block must be visually distinct (e.g., a colored border, an icon with our expert's headshot) and must contain:
    *   A clear heading, such as **"Expert Insight"** or **"A Note from Aaron Kapfer."**
    *   A direct quote of 2-4 sentences, written in a first-person, authoritative voice.
    *   The expert's name and title.

---

## 3. Visual Dominance Rules

Text alone is not enough to win. We must dominate the page visually to improve user engagement and provide AI systems with a rich, multimodal understanding of our content.

*   **Minimum Image Count (kept deliberately, July 26, 2026 — ranking rationale, not just workload):** The final published page must have an image count equal to the average of the top 3 ranking competitors, **plus 20%**. If the top competitors have 8, 10, and 12 images, our page must have a minimum of 12 images (10 avg + 2). This formula stays exactly as-is — the fixes below make it cheaper and faster to *reach* that count, they do not lower the count itself.
*   **Required Visuals:**
    *   **Mechanism Diagrams (exception added July 26, 2026):** Every time a core engineering mechanism is explained, it must be accompanied by a diagram, table, or calculator that shows the relationship clearly. **A table or calculator satisfies this requirement on its own** when it does the same job a diagram would — a custom diagram is only required when the concept is genuinely visual/spatial and can't be shown any other way (e.g., water flow geometry, physical installation angle). Do not commission a diagram redundant with a table or calculator that already covers the same point.
    *   **Comparison Tables:** Every section that compares options (e.g., product types, materials) **must** use a comparison table.
    *   **Filling an image slot — order of preference (added July 26, 2026, cheapest/fastest first):** (1) an existing real photo or illustration already in the library — check first; (2) a new real photo, only if it's realistically shootable before publish; (3) a clearly labeled AI-generated illustration, when the real thing isn't practically obtainable (e.g., a cutaway showing how a guard gets nailed to a shingle — not a shot you can schedule on demand, but one you can illustrate honestly); (4) a composite/multi-panel image — rare and deliberate, only when a genuine comparison or sequence needs to be seen at once (before/after, correct-vs-incorrect, product/feature comparison, step-by-step process) and nothing else carries it; this is real design time, not a quick asset grab, and is not a default move.
    *   **Stock photos (reversed July 26, 2026): allowed, with credit.** Previously forbidden outright — now permitted as long as properly credited to the source or creator (see Section 4 for where the credit goes).
    *   **Photo reuse across pages is expected, not a problem.** No SEO penalty for the same image on multiple pages the way there is for duplicate text — each placement needs its own filename and alt text. The only thing to avoid: the identical hero shot on two pages chasing nearly identical search intent.

---

## 4. Image SEO & AEO System

Images are not decoration; they are ranking and citation assets. They must be optimized accordingly.

*   **Filename Structure:** Image filenames must be descriptive and keyword-rich, following a `[primary-entity]-[function-or-context].jpg` format.
    *   *Example:* `micromesh-gutter-guard-blocking-pine-needles.jpg`
*   **Alt Text Structure — accessibility and content-description ONLY (rule clarified July 26, 2026):** Alt text must include the entity, its function, and the context of the image, and nothing else. Alt text has one job — a screen reader reads it as the image's description, and it's a search-indexing signal for image content — and both of those degrade if anything else gets loaded into it. **Never put stock-photo credit/attribution in alt text.** See "Stock Photo Credit" below for where that goes instead.
    *   *Example:* `"A close-up of a MasterShield micro-mesh gutter guard filtering heavy rainfall away from a roofline."`
*   **Caption Strategy (AEO Lever):** Captions should be short, factual, and written as self-contained, quotable statements.
    *   *Example:* `"Figure 1: The patented HydroVortex action pulls water in while preventing debris from clogging the screen."`
*   **Stock Photo Credit (added July 26, 2026):** Credit goes in a caption line directly below the image, or in a footer credits section on pages carrying multiple stock assets (to avoid cluttering every image with its own caption). Never in alt text — most stock licenses that require attribution expect it to be visible to a human reader, and alt text isn't visible outside a screen reader or the page source, so burying credit there may not even satisfy the license.
*   **AI-Generated Image Labeling (added July 26, 2026, finalized after team review):** Every AI-generated image carries one universal caption line, directly on the image — do not split the wording by mechanism/process/technique; that distinction proved ambiguous in practice (is a cutaway of water moving through HydroVortex a "mechanism," a "process," or a "technique"? different people label it differently) and two independent reviewers converged on simplifying it. Use: **"This image was generated with AI, for illustrative purposes."**
*   **Local Page Image Optimization:** For local pages, image filenames, alt text, and schema must be localized.
    *   *Filename Example:* `gutter-guard-installation-charlotte-nc.jpg`
    *   *Alt Text Example:* `"A MasterShield certified installer fitting a gutter guard on a home in the Dilworth neighborhood of Charlotte, NC."`
*   **Placeholder Completeness Standard (added July 31, 2026, per Karen — governs every audit that checks images, not just this doc).** At the draft/pre-production stage, a placeholder image is **not** a deficiency, a gap, or a "pending" note — it is the correct, complete deliverable for this step, exactly as Doc 192 §3 specifies (`<figure><div class="ph">📷 [one-line caption]</div></figure>`). A placeholder is **complete** when it has: (1) correct placement in the body per the placement/cadence rules above, (2) a one-line caption describing what the image will show, and (3) an alt-text direction recorded in the Media Assets table. **An audit gate must never downgrade a result, add a note, or flag anything for a placeholder that has all three.** "Photo/asset not yet produced" is not itself a Non-Critical issue and must never be listed as one. The only thing that is a real defect is an *incomplete* placeholder — missing its caption, missing its alt-text direction, or missing its Media Assets table row entirely. Stock credit and AI-image labeling (above) are the only things that genuinely wait for a produced asset — flag those as N/A at placeholder stage, not as open notes.

---

## 5. Visual Placement Rules

Visuals must be placed strategically to break up text and reinforce key points.

*   **Image Placement (Doc 144):** roughly one relevant image per major section within the image budget — placed at paragraph boundaries (never mid-paragraph), never stacked, no images in the above-the-fold block, and none in the paragraph immediately before a section-end CTA. The hero is page-appropriate (beauty or problem) and thumbnail-legible.
*   **Table Placement:** A comparison table must be inserted immediately following any section that introduces multiple options or categories.
*   **Diagram Placement:** A mechanism diagram must be placed directly beside or below the first explanation of that mechanism.

---

## 6. CTA Engine (Enforced)

Calls-to-action must be placed systematically to guide the user down the funnel.

*   **CTA Placement (Doc 144):** CTAs are placed by structural milestone — a soft CTA after the above-the-fold block, a hard CTA before the FAQ, a hard CTA at the bottom, and middle CTAs only at the end of a tension-resolving H2 section — not on a word-count cadence. Never two back-to-back; never a ~3,000-word stretch with none.
*   **Contextual Offers:** CTAs must be contextual. Do not repeat the same generic CTA. The offer should align with the reader's current stage of awareness based on their position in the article.

---

## 7. Table Strategy

Tables are powerful tools for AEO and user clarity.

*   **Mandatory Comparison Tables:** All comparison sections **must** use a table.
*   **Pillar-Aligned:** The columns and rows of comparison tables must align with our 5 Engineering Pillars, reinforcing our core evaluation framework.

---

## 8. Schema & Technical Layer (Ref: Doc 123)

The publisher is responsible for ensuring the correct schema is applied to the page before it goes live. This is not optional.

*   **FAQ Schema:** Must be applied to all pages with a question-and-answer format.
*   **Product Schema:** Must be applied to all pages that feature a specific product.
*   **ImageObject Schema:** Must be applied to all images, including localized information for local pages.
*   **HowTo Schema:** Must be applied to all pages that provide step-by-step instructions.

---

## 9. The "Extraction Surface Area" Rule

Our goal is to make every element on the page an asset that an AI can extract and cite. This means text, tables, lists, and images must all be optimized for extraction.

*   **Text:** Follows AEO rules from Doc 173.
*   **Tables:** Clearly structured with descriptive headers.
*   **Lists:** Use proper HTML list formatting (`<ul>`, `<ol>`, `<li>`).
*   **Images:** Use descriptive filenames, alt text, and captions.

---

## 10. Post-Publishing: LLM Seeding Trigger

Once the page is live, trigger the LLM Seeding Protocol (Doc 125) for off-page distribution:

1. **Notify Distributor Agent** (Doc 332) that new content is live
2. **Provide target channels** from Doc 125's approved list
3. **Set seeding timeline** - begin within 24 hours of publish
4. **Track distribution** - log seeding activities in KPI system (Doc 241)

---

## 11. Final Assembly Checklist

Before hitting "Publish," the assembler must verify every item on this checklist.

| Task | ✅ Done |
|---|:---:|
| **Above-the-Fold:** Is the ATF section visually distinct and structured as a decision interface? | ☐ |
| **Expert Callout:** Is there one Expert Callout Block placed correctly in the article? | ☐ |
| **Visuals:** Image count meets the Visual Dominance rule. | ☐ |
| **Visuals:** All required diagrams and tables are present. | ☐ |
| **Image SEO:** All image filenames are keyword-rich and descriptive. | ☐ |
| **Image SEO:** All images have complete, entity-driven alt text. | ☐ |
| **Image SEO:** All key images have factual, quotable captions. | ☐ |
| **Image Policy:** Every mechanism image is a diagram, table, or calculator (not a redundant diagram on top of a table that already covers it). | ☐ |
| **Image Policy:** Any stock photo is credited in a caption/footer — never in alt text. | ☐ |
| **Image Policy:** Every AI-generated image carries the universal label ("This image was generated with AI, for illustrative purposes.") — not a split by mechanism/process/technique. | ☐ |
| **Placement:** Images and CTAs are placed according to the specified cadence. | ☐ |
| **Schema:** All relevant schema types have been correctly applied and validated. | ☐ |
| **Internal Links:** All internal links are correct and functional. | ☐ |

---

## 12. Post-Publish Technical Verification (MANDATORY)

Publishing is not the final step. A live page that cannot be crawled or indexed is useless. Immediately after hitting "Publish," the publisher must execute this verification loop.

1. **Copy the Live URL:** Copy the exact published URL.
2. **Open Google Search Console (GSC):** Navigate to the GSC property for the brand.
3. **URL Inspection Tool:** Paste the live URL into the top search bar and hit Enter.
4. **Verify Accessibility:** Confirm that:
   - Page is not blocked by `robots.txt`
   - Page does not contain a `noindex` tag (often accidentally carried over from staging)
5. **Request Indexing:** Click the "Request Indexing" button. This raises our hand to Google's crawlers rather than waiting weeks for passive discovery.
6. **Log Verification:** Check off the final verification box below.

| Task | ✅ Done |
|---|:---:|
| **GSC Verification:** URL inspected, crawlable, and "Request Indexing" clicked. | ☐ |

---

*End of Document*