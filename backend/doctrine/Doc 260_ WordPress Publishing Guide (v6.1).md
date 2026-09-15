# Doc 260: WordPress Page Assembly & Publishing Guide

**Version:** 6.4 | **Last Updated:** July 30, 2026 | **Series:** 600 (Execution Guides)

*(Header bumped 2026-07-21 by system consistency audit — this file's content already carried the URL-preservation step; the version header just hadn't been updated to match. This is now the sole canonical copy; see `Doc 260_ WordPress Publishing Guide.md` for the superseded duplicate.)*

> **v6.4 (July 30, 2026, Karen):** Added a note in Purpose: this guide now assumes a saved, passing Doc 195 (Pre-Publication Packaging Audit) report exists for the exact version being transferred, in addition to the existing Doc 328/329 approval. See Doc 208.
> **v6.3 (July 29, 2026, Karen):** Step 3 was stale on two points, found while fixing the same gap in Doc 192/328/329: (1) it told the publisher to paste "the Article + FAQPage JSON-LD," but Doc 192 has required the fuller Article + Organization + BreadcrumbList + FAQPage set since Stage 2 was written — the step just never caught up to its own template; (2) it assumed the JSON-LD was something to copy from a rendered view of the document, but a `<script>` tag's contents never render in a browser — there was no visible text to copy. Doc 192 v2.7 fixed the second problem at the source (the schema now also ships as a visible, HTML-escaped `<pre><code>` block, labeled for copy-paste, right below the functional one); this step now points the publisher at that visible block by name so nobody has to view page source.

---

## Purpose
This guide explains how to take an approved article from the Auditor Agent (Doc 328, or Doc 329 on the 361 refresh track) and format it correctly in WordPress for publication. This ensures the technical SEO and CRO elements are preserved during the transfer.

**Added July 30, 2026, Karen:** this guide assumes the page also carries a saved, passing **Doc 195 (Pre-Publication Packaging Audit)** report — a separate, non-content check confirming every field below (meta title/description, JSON-LD, etc.) is actually present and consistently formatted, run after Doc 328/329 and before this guide. If no Doc 195 report exists for this exact version, stop and get one before proceeding — do not treat a Doc 328/329 pass alone as sufficient to start this guide.

---

## Step 1: Transfer Content & Structure
1. **Create New Page/Post:** Log into WordPress and create a new Page (for Pillar/Cluster) or Post (for blog content).
2. **Set the URL:** Paste the exact URL slug provided by the Architect Agent (Doc 312) into the permalink field. **If this is a refresh of an existing page, keep the existing URL — do NOT create a new page or change the slug.** When the deliverable's head keyword differs from the page's old name, or a 301 is listed, that is intentional: read the **Publisher Note** in the deliverable's Appendix (Doc 192 §7A). We preserve a ranking page's URL and traffic history and re-target it to the term now pulling the most traffic — we never delete a page with equity and start fresh.
3. **Paste Content:** Copy the approved article and paste it into the WordPress editor.
4. **Verify Headings:** Ensure all H1, H2, and H3 tags transferred correctly. The title should be H1, main sections H2, and sub-sections H3.

---

## Step 2: Format the Above-the-Fold CRO Section
This is the most critical section of the page. It must appear immediately after the opening hook paragraph.
1. **Format the 3 FAQs:** Use an accordion or toggle block for the 3 PAA questions if available in your theme. If not, use bold H3s.
2. **Insert the Soft CTA:** Place the brand-specific soft CTA immediately below the FAQs. Make it a distinct button or styled callout box.

---

## Step 3: Technical SEO & Schema
1. **Meta Data:** Copy the Meta Title and Meta Description from the article document's Build Metadata block (Appendix item 8) and paste them into your SEO plugin (e.g., Yoast, RankMath). They are visible as plain text there — no need to open the file's raw HTML.
2. **Author Assignment:** Set the author to the name specified in the article (e.g., Karen Sager or Aaron Kapfer).
3. **Schema Markup:**
   - **The JSON-LD should already exist in the article document, in the appendix (Doc 192 item 7A-SCHEMA, added July 21, 2026) — you're pasting it, not building it.** If it's not there, stop and send the page back rather than publishing without it or writing your own; five live MasterShield pages shipped with none because this step assumed it existed upstream when nothing was generating it.
   - **Copy the visible block, not the functional one (added July 29, 2026, Karen).** The Appendix carries the schema twice on purpose: a functional `<script type="application/ld+json">` block (for a browser/crawler if this file is ever served as-is) and, directly below it, the exact same JSON repeated inside a labeled, visible `<pre><code>` block ("Copy the JSON below into your SEO plugin's schema field"). Opening the file in a browser never shows the functional block's contents — that's normal, not a defect — copy from the labeled visible block instead. If only the functional block is present with no labeled visible copy beneath it, the page didn't ship to current Doc 192 spec; send it back rather than digging into view-source to extract it yourself.
   - Paste the full schema set — Article, Organization, BreadcrumbList, and FAQPage where present — into the page's header, or use your SEO plugin's schema/FAQ block. All four (or three, if the page has no FAQ section) should be there; a page with only Article + FAQPage is missing two required types.
   - Confirm the Author schema's `sameAs` links match the byline actually on the page.

---

## Step 4: Internal Linking
1. **Insert Links:** Apply the exact internal links and anchor text specified by the Architect Agent (Doc 312).
2. **Check Links:** Click each link in the preview mode to ensure it resolves correctly.

---

## Step 5: Final Review & Publish
1. **Preview:** Open the page preview. Check for formatting errors, broken tables, or missing images.
2. **Run Doc 1710:** Complete the final human QA checklist (Doc 1710) before hitting publish.
3. **Publish:** Once the checklist is clear, click Publish.
4. **Notify Distributor:** Pass the published URL to the Distributor Agent (Doc 332) to generate the amplification package.

---
**End of Guide**