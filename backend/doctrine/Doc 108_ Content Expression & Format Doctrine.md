# Doc 108: Content Expression & Format Doctrine
**Version 6.1** | **Last Updated: August 6, 2026** | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Status:** Tier 3 Doctrine (Formatting Rules)

---

> **Quick Reference**
> **Owns:** The visual layout and formatting standards for all written content.
> **Rule 1:** Paragraphs must be 2-4 sentences maximum (White Space Rule).
> **Rule 2:** Use bullet points sparingly (max 20% of content); prefer narrative flow.
> **Rule 3:** Bold text must be used to highlight key concepts, not just for decoration.
> **If/Then:** If a section looks like a wall of text, break it up with an H3, a bulleted list, or a blockquote.

---
## 1.0 Why This Document Matters

This doctrine provides the rules for formatting our content to serve two masters: the human reader who needs a compelling narrative, and the AI that needs perfectly structured, extractable answers. The effectiveness of these formats is measured by **Doc 201 (Content Performance Rubric)**. It resolves the tension between storytelling and machine-readability.

> **Scope Definition:** This document governs **formatting and expression**. It defines *how* our narrative is presented and structured. The authoritative rules for **AEO writing, snippet construction, and citability** are owned exclusively by **Doc 120 (Engineering for Selection)**. This document translates the narrative; Doc 120 engineers the answer.

---

## 2.0 The Answer-First / Tension-First Hybrid Hook

To satisfy both humans and machines from the very first line, every article must open with a specific, two-part hook structure.

> **Line 1: The Direct Answer.** The very first sentence must be a standalone, fact-based, and complete answer to the primary user query. It must be written as if it were the only text on the page, adhering to the citability rules in Doc 120.

> **Lines 2-4: The Narrative Tension.** Immediately following the direct answer, the next 1-3 sentences must pivot to the narrative hook, introducing the conflict, tradeoff, or hidden complexity that pulls the human reader into the rest of the article, as defined in **Doc 102 (Conflict-First Structural Doctrine)**.

This is a non-negotiable hybrid structure. It is the foundational solution to the human vs. machine conflict.

---

## 3.0 Adapting Narrative to SERP-Expected Formats

When SERP analysis shows that readers expect a specific format (e.g., a listicle or comparison table), we do not abandon our narrative principles. Instead, we use the expected format as a container for our Conflict-First logic.

| SERP Format | How We Adapt Our Narrative |
|---|---|
| **Listicle** *(e.g., "7 Best Gutter Guards")* | The list items are not products. They are the **failure modes** or **evaluation criteria** from our mechanism beliefs (Doc 100). The final item becomes our solution, presented as the resolution. |
| **Comparison Table** *(e.g., "Brand A vs. Brand B")* | The columns are not generic features. They are our **5 Pillars** (Doc 100). We force the comparison to happen on our terms. |
| **Step-by-Step Guide** *(e.g., "How to Install...")* | Each step is framed by our **problem beliefs**. Step 1 is not "buy the guards"—it is "Identify Your Home’s Primary Failure Mode." We teach before we instruct. |

---

## 4.0 Formatting for Entity & BAIO Reinforcement

While Doc 120 and Doc 124 govern the rules for entity usage, this document governs how they are formatted for maximum impact.

*   **Entity Repetition:** The writer must meet the minimum mention counts for all entities as defined in **Doc 124 (Entity Relationship Map)**.
*   **Mechanism-Brand Pairing:** The mandatory `Brand + Mechanism` pairing (e.g., "MasterShield’s AEGIS 5X™ system") must be included 2-3 times per page, as required by **Doc 120 (Engineering for Selection)**.

---

## 4.5 Punctuation Rules

| Rule | Limit | Reason |
|------|-------|--------|
| **Em dash (—)** | **Maximum 1 per article** | Em dashes are a known AI writing signal. Overuse flags content as machine-generated. One em dash per article is the hard limit. **Exceeding this limit = automatic FAIL in Auditor (Doc 328).** |
| **Exclamation marks** | 0 in body copy | Exclamation marks undermine the authoritative, knowledgeable-neighbor tone. |
| **Ellipsis (...)** | Maximum 1 per article | Overuse signals informal or AI-generated writing. |

---

## 4.6 AI-Writing Pattern Screen

This document does not restate the AI-writing-tell checklist. The canonical, enforced list lives in **Doc 328 (Auditor Agent Instructions) §3, Brand QC — Prohibited Phrases**, as a FLAG-level check (compiled, non-exhaustive, not a FAIL trigger on its own). Writers should be aware the screen exists and self-edit against it before submission; the Auditor is the authority on its exact contents and enforcement level.

---

## 5.0 QA & Enforcement Checklist

- [ ] **Answer-First Hook:** Does the article open with the mandatory two-part hook?
- [ ] **Narrative Adaptation:** If a SERP-expected format is used, does it contain our Conflict-First logic?
- [ ] **Entity & Pairing Compliance:** Does the content meet the entity repetition and mechanism-brand pairing rules from Doc 124 and Doc 120?
- [ ] **Block Inclusion:** Does the article include the required number and type of AEO-optimized blocks as specified in the content brief (per Doc 120)?
- [ ] **Em Dash Limit:** Does the article contain no more than one em dash (—)? If more than one is present → FAIL.

---

## 6.0 System Integration

This doctrine is the formatting layer of our content system. It must be executed in concert with:

*   **Doc 102 (Conflict-First Structural Doctrine):** Provides the narrative structure that this document formats.
*   **Doc 120 (Engineering for Selection):** Owns all rules for AEO writing, snippet construction, and entity repetition that this document helps format.
*   **Doc 124 (Entity Relationship Map):** Defines the entities that this document formats.
*   **Doc 201 (Content Performance Rubric):** Measures the performance of different content formats.
*   **Doc 204 (Performance Enforcement & Optimization Protocol):** Provides the playbooks for fixing underperforming formats.
*   **Doc 143 (Offer Library & Version Control System):** Provides the approved offers to be used in CTA blocks.

---

*End of Document 108*