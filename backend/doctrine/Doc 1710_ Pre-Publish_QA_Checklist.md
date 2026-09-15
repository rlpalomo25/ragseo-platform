# Doc 1710: Pre-Publish Quality Assurance Checklist

**Version 8.1** | **Last Updated: July 31, 2026**

> **v8.1 (July 31, 2026, Karen):** Retired remaining live "TL/DR"/"TL;DR" references in favor of "Key Takeaways," part of the system-wide sweep triggered by Karen renaming Doc 155 Section 5 to "Key Takeaways Quality Gate." See RAGSEO System State, Twenty-second finding.
**Status:** Tier 1 Governance | **Owns:** Final human sanity check AFTER Auditor (Doc 328) PASS

> **Purpose:** This is the final human validation layer. It runs AFTER Doc 328 (Auditor) passes the content. Doc 1710 validates outcomes, not compliance re-checks. Let Doc 328 do heavy lifting; this is a sanity check.
>
> **Pipeline Position:** Writer → Doc 328 (Auditor) → [PASS] → Doc 1710 (Human Check) → Publish
>
> **MANDATORY PRE-CHECK:** Before starting this checklist, open **Doc 900 (Validation Reference)** and **Doc 317 (Premium Builder / Simple Science Voice Standard)**. Doc 900 is the master quick-reference for page-type specs and common failure patterns; Doc 317 is the voice standard this checklist sanity-checks against. Note the page's `page_type` / `page_subtype` (Doc 153) so you know which page kind you are validating.

---

## DECISION SYSTEM (Aligned with Doc 328)

| Result | Meaning | Action |
|--------|---------|--------|
| **PASS** | Content is ready - no critical issues | Proceed to publish |
| **PASS WITH NOTES** | Minor issues - fix before publish | Fix and republish |
| **FAIL** | Critical issues - return to Writer | Do not publish |

**No scoring percentages. Matches Doc 328 logic.**

---

## CRITICAL ITEMS (Auto-Fail)

If ANY of these fail, automatic **FAIL** regardless of anything else:
- [ ] Execution Plan deviation (any deviation = FAIL)
- [ ] Prohibited moves violated (any = automatic FAIL)
- [ ] Missing traceability (plan_id, version, writer_id)
- [ ] Win Vector weak or inconsistent
- [ ] Generic content (could apply to any competitor)
- [ ] Narrative strategy failure — buyer_state ignored, narrative_attack not followed, language_translation not applied, field_stories missing, or proof_entity_ownership violated

---

## Section 1: STRUCTURED OUTPUT VALIDATION (NEW - Must Pass)

This validates the Writer Output Schema, not re-checking compliance.

| What to Check | ✅ Done |
|---|:---:|
| **Schema Fields Present** — Does output include: plan_id, version, writer_id, meta, article_body, extractable_blocks, cta_blocks, internal_links, entity_usage, execution_plan_alignment? | ☐ |
| **Traceability** — plan_id, version, writer_id all present? | ☐ |
| **Extractable Blocks** — Do blocks match citation_intent_map from Execution Plan? | ☐ |
| **CTA Blocks** — Do CTA types (soft/medium/hard) match Execution Plan? | ☐ |
| **Internal Links** — Do links follow Execution Plan intent (not writer discretion)? | ☐ |
| **Alignment Flags** — Are execution_plan_alignment flags accurate? | ☐ |

---

## Section 2: EXECUTION PLAN ENFORCEMENT (Hard - Must Pass)

| What to Check | ✅ Done |
|---|:---:|
| **H1 Matches Plan** — Exact match to Execution Plan? | ☐ |
| **H2s Match Plan** — Exact match to Execution Plan? | ☐ |
| **Prohibited Moves** — Any violation = automatic FAIL | ☐ |
| **Structure Deviation** — Any deviation from plan = FAIL | ☐ |

---

## Section 3: WIN VECTOR QUALITY (Must Pass)

| What to Check | ✅ Done |
|---|:---:|
| **Clarity** — Is Win Vector clear and specific? | ☐ |
| **Consistency** — Is Win Vector reinforced throughout? | ☐ |
| **Dominance** — Is Win Vector the dominant argument (not diluted)? | ☐ |
| **No Competing Narratives** — Does article NOT introduce multiple explanations? | ☐ |

---

## Section 4: "DOES THIS WIN?" CHECK (Outcome-Based - Must Pass)

| What to Check | ✅ Done |
|---|:---:|
| **Information Gain** — Does this include insight NOT in top competitors? | ☐ |
| **Generic Content Filter** — Could this apply to any generic competitor? If yes = FAIL | ☐ |
| **Extraction Dominance** — Are extractable blocks clearer/directer than typical SERP answers? | ☐ |
| **Decision Driver** — Would this article make a reader choose this brand or take the next step? If no/unclear = FAIL | ☐ |
| **Section Purpose** — Does each section advance the Win Vector? | ☐ |

---

## Section 5: EXTRACTABLE BLOCK QUALITY

| What to Check | ✅ Done |
|---|:---:|
| **Answers Question** — Does each block answer ONE specific question? | ☐ |
| **Stand Alone** — Is block understandable without context? | ☐ |
| **Better than SERP** — Is block clearer than typical search result? | ☐ |
| **No Filler** — Does block contain only essential information? | ☐ |

---

## Section 6: BRAND & VOICE (Quick Check)

| What to Check | ✅ Done |
|---|:---:|
| **Brand Voice** — Does content match brand (Knowledgeable/Helpful/Generous)? | ☐ |
| **Prohibited Phrases** — No "best in world", "guaranteed", etc.? | ☐ |
| **Klean Gutter Clarity** — For KG: Does it simplify decisions, not sound like MasterShield? | ☐ |
| **MMGG Business Outcomes** — For B2B: Does each section state business outcome? | ☐ |

---

## Section 7: CTA & CONVERSION (Quick Check)

| What to Check | ✅ Done |
|---|:---:|
| **CTA Type Matches Plan** — soft/medium/hard correct per plan? | ☐ |
| **No FAQ CTAs** — No CTAs inside FAQ section? | ☐ |
| **CTA-Trust Pairing** — Each CTA has adjacent trust signal? | ☐ |

> **Full CTA placement check → See Section 12 (per Doc 180)**

---

## Section 8: HUMAN READABILITY (Final Gate)

| What to Check | ✅ Done |
|---|:---:|
| **Natural Flow** — Does content read naturally? | ☐ |
| **Not Mechanical** — Does it NOT feel forced or robotic? | ☐ |
| **Clear Journey** — Can a human follow the argument? | ☐ |

---

## Section 9: E-E-A-T & AUTHORITY

| What to Check | ✅ Done |
|---|:---:|
| **Author Bio (technical)** — Is Karen Sager bio present (Experience/Expertise/Trust)? | ☐ |
| **Author Bio (field)** — Where field claims appear, is Aaron Kapfer credited as field authority? (Karen = technical/mechanism; Aaron = field/what-actually-happens, per Doc 317 §4.2) | ☐ |
| **Date Published** — Original publish date present? | ☐ |
| **Date Updated** — Last modified date present? | ☐ |
| **Third-Party Citations** — 3–5 external sources, cited as superscript numbers → references at the bottom, with NO source names in the prose ("According to…")? (Doc 317 §4.1) | ☐ |
| **Patents Credited** — Patent numbers or documentation referenced? | ☐ |
| **Testing Data** — ASTM, lab tests, or field reviews cited? | ☐ |

---

## Section 10: SCHEMA READINESS

| What to Check | ✅ Done |
|---|:---:|
| **FAQ answers (SOT-sourced)** — embedded FAQ answers present, count driven by the question set (not a fixed 20); above-the-fold **Your Questions Answered** renders as the `.qa` component (bold question + 1-2 sentence teaser + jump link), NOT flowing prose (Doc 192 v2.0 reversed the earlier de-staged-prose rule) | ☐ |
| **FAQ Schema Markup** — FAQPage schema present where the page has real FAQ content (AI-extraction only; FAQ rich results deprecated May 7 2026) | ☐ |
| **PAA Mapping** — Questions match actual search intent? | ☐ |
| **Breadcrumbs** — Navigation breadcrumbs present? | ☐ |
| **Product Schema** — MasterShield specs/pricing in schema? | ☐ |
| **Review Schema** — Star ratings or review blocks? | ☐ |

---

## Section 11: VOICE CHECK (Doc 317 sanity check)

*Doc 328 Section 2B does the hard enforcement (paragraph length, teach-then-prove, source-led, citation quota, page-type voice match). This is the human gut-check that the page sounds right.*

| What to Check | ✅ Done |
|---|:---:|
| **"Matt Risinger" Test** — Does this sound like a trusted expert neighbor talking, not a brochure? | ☐ |
| **Bill Nye accessibility (B2C only)** — Is the science made accessible: an everyday analogy before any technical term, a reading level anyone can follow, engaging but not goofy? Reader should finish thinking "I get exactly why that works, and that was kind of interesting." (Skip for B2B/MMGG.) | ☐ |
| **B2B register (MMGG only)** — On MMGG, is it the business-partner voice (trade audience), with the Bill Nye accessible-science layer OFF? | ☐ |
| **Teach-then-prove** — Is each mechanism explained in plain language BEFORE it is named? No jargon leading a paragraph. | ☐ |
| **Karen + Aaron both present** — Technical authority (Karen) AND field authority (Aaron) appear in their right domains, plainspoken, attribution after the statement? | ☐ |
| **No source-led prose** — No "According to…", "Research shows…"; sources sit quietly in superscript references. | ☐ |
| **Paragraphs not walls** — Body paragraphs stay short (≈4 sentences max)? | ☐ |
| **Direct Language** — Confident claims, not hedging? | ☐ |
| **Job Site Language** — Real conditions, not generic concepts? | ☐ |
| **No Brochure Feel** — Does it feel like a person, not marketing copy? | ☐ |

---

## Section 12: CTA PLACEMENT (per Doc 180)

| What to Check | ✅ Done |
|---|:---:|
| **Post-Answer Soft CTA (never collapses)** — soft CTA + trust bar immediately below Your Questions Answered? Required at every page length. | ☐ |
| **Pre-FAQ Hard CTA** — hard CTA immediately before the FAQ section? | ☐ |
| **Bottom Hard CTA** — primary CTA at the end, resolving the page's anxiety? | ☐ |
| **Section-End Only** — every CTA at an H2 boundary; none mid-section or after a caveat? | ☐ |
| **CTA Spacing** — no two CTAs back-to-back; no ~3,000-word stretch with none? | ☐ |
| **CTA-Trust Pairing** — each CTA adjacent to a trust signal? | ☐ |
| **No FAQ CTAs** — CTAs NOT inside the FAQ section? | ☐ |
| **One Hero, page-appropriate** — exactly one header image fitting the page (problem or beauty), thumbnail-legible? | ☐ |
| **No Above-the-Fold Images** — no images between Key Takeaways and Your Questions Answered? | ☐ |
| **Images Unstacked & At Seams** — body images at paragraph boundaries, none splitting a paragraph, none stacked, none in the paragraph before a section-end CTA? | ☐ |

> **CTA Thinning (Human Judgment Gate):** After confirming all CTAs are correctly placed by structural milestone, read the page as a reader. If any two adjacent middle CTAs feel crowded — particularly if a final body CTA and the pre-FAQ hard CTA sit within ~600 words of each other — remove the earlier one. Fewer, more impactful CTAs in the right locations outperform technically compliant but overcrowded placement. **The three fixed anchors (post-Your Questions Answered soft CTA, pre-FAQ hard CTA, bottom hard CTA) are not subject to thinning.** Thinning authority applies to middle body CTAs only. The human reviewer may remove a middle CTA without returning the page to the writer.

---

## Section 13: INTERNAL LINKS

| What to Check | ✅ Done |
|---|:---:|
| **Cluster Links** — Links to 3 relevant Cluster pages? | ☐ |
| **Anchor Text** — Keyword-rich anchor text (not "click here")? | ☐ |
| **Local Page Link** — Link to installer directory? | ☐ |
| **Next Step Routing** — Bottom of page routes to next logical step? | ☐ |

---

## Section 14: TENSION GRADIENT (per Doc 104)

| Layer | ✅ Done |
|---|:---:|
| **Clarity** — Hook with common belief? | ☐ |
| **Concern** — Shows the problem? | ☐ |
| **Consequence** — Stakes stated? | ☐ |
| **Reassurance** — Proof/credentials? | ☐ |
| **Control** — Mechanism explained? | ☐ |
| **Confidence** — Why this works? | ☐ |
| **Action** — Clear CTA? | ☐ |

---

## Section 15: NARRATIVE STRATEGY ALIGNMENT (from Doc 155)

Validates the article follows the narrative strategy fields from the Execution Plan (governed by Doc 155).

### 15a. Buyer State Alignment

| What to Check | ✅ Done |
|---|:---:|
| **Tone matches buyer_state** — Is the tone/depth appropriate for the declared primary buyer state (first_time_buyer, replacement_buyer, diagnostic_buyer, comparison_buyer)? | ☐ |
| **First-time buyer checklist** — If primary = `first_time_buyer`, does the article use evaluation framing (not diagnosis)? Per Doc 155 Section 6.7, first-time buyers need checklist-style assessment, not problem diagnosis. | ☐ |
| **Replacement buyer failure focus** — If primary = `replacement_buyer`, does the article explain why previous systems fail before presenting the solution? | ☐ |
| **Diagnostic buyer names the problem** — If primary = `diagnostic_buyer`, does the article name the homeowner's unarticulated problem early? | ☐ |
| **Comparison buyer differentiation** — If primary = `comparison_buyer`, does the article lead with differentiation rather than basic education? | ☐ |

### 15b. Narrative Attack Progression

| What to Check | ✅ Done |
|---|:---:|
| **Starting belief honored** — Does the article start where the reader actually is (reader_starting_belief), not where the brand wants them to be? | ☐ |
| **Final belief earned** — Does the section progression logically arrive at final_belief, not start with it? | ☐ |
| **Section purpose** — Does every H2 advance the narrative_attack arc? Edge cases are not the main battlefield (per Doc 155 Section 6.2). | ☐ |
| **No competing narrative** — Does the article avoid introducing a secondary argument that undermines the primary attack? | ☐ |

### 15c. Language Translation Compliance

| What to Check | ✅ Done |
|---|:---:|
| **Internal jargon check** — Are internal mechanism terms ("hydraulic behavior", "velocity exceeds intake stability") replaced with homeowner language ("how water moves", "water jumps the gutter")? | ☐ |
| **Translation applied consistently** — Is the language_translation block from the Execution Plan applied throughout, not just in the first section? | ☐ |
| **7th-grade readability** — Does the language pass the "would a neighbor say this?" test per Doc 155 Section 3? | ☐ |

### 15d. Field Story Presence

| What to Check | ✅ Done |
|---|:---:|
| **Field stories present** — Every mechanism_explanation section has homeowner_observation → field_reality → mechanism_translation? | ☐ |
| **Not abstract** — Are field stories grounded in observable behavior, not hypothetical scenarios? | ☐ |
| **Execution Plan compliance** — If `field_story_required: true` in a section's metadata, is the field story populated and substantive? | ☐ |

### 15e. Proof Entity Ownership

| What to Check | ✅ Done |
|---|:---:|
| **Proof attaches to correct entity** — On TAP pages, does proof attach to AEGIS 5X, not the brand name? | ☐ |
| **Non-TAP pages correct** — On non-TAP pages, does proof attach to the page's target entity? | ☐ |
| **No entity confusion** — Are there any statements where the reader could be unclear which entity the proof supports? | ☐ |

### 15f. Key Takeaways Quality Gate (per Doc 155 Section 5)

| What to Check | ✅ Done |
|---|:---:|
| **Lived homeowner behavior** — Do Key Takeaways bullets describe specific homeowner frustrations, not abstract mechanism benefits? | ☐ |
| **Not jargon-heavy** — Do bullets avoid internal mechanism language? | ☐ |
| **Curiosity hooks** — Would Key Takeaways make a skimming reader think "That's exactly why I'm here"? | ☐ |
| **Above-fold FAQ answers** — Are the 2 above_fold_faq answers direct and self-contained (not requiring paragraph context)? | ☐ |

---

## ESCALATION RULE

If issue originates from Execution Plan (not Writer error):
- **Escalate to Strategist (Doc 304), not Writer**

Examples:
- Win Vector is unclear in plan
- Structure doesn't make sense
- Prohibited moves are contradictory

---

## PRIORITIZATION

**Critical (Auto-Fail):**
- Execution Plan deviation
- Prohibited moves
- Missing schema/tracing
- Win Vector weak
- Generic content
- "Does this win?" = no
- Narrative strategy failure (buyer_state, narrative_attack, language_translation, field_story, proof_entity, Key Takeaways quality)

**Non-Critical (Pass with Notes):**
- Minor tone issues
- Minor formatting
- Minor flow issues
- Minor narrative strategy gaps (e.g., one field story weak but others strong)

---

## FINAL DECISION

**Before approving, answer:**

"Would this article make a reader choose this brand or take the next step?"

- **If answer = no/unclear/weak** → FAIL
- **If answer = yes, clear, compelling** → PASS

---

## NOTE ON REDUNDANCY

This checklist does NOT re-check:
- AEO formatting (checked by Doc 328)
- Technical specs (checked by Doc 328)
- Structure compliance (checked by Doc 328)
- Page type specs (checked by Doc 328)

Doc 1710 is the FINAL sanity check - validates outcomes and makes the human go/no-go decision.

---

**Version 8.1 (June 30, 2026):**
- Section 12: Added CTA Thinning (Human Judgment Gate) — human reviewer has explicit authority to remove a middle body CTA if spacing feels crowded after reading the page. The three fixed anchors are protected; thinning applies to middle CTAs only.

**Version 8.0 (June 8, 2026):**
- Aligned with Doc 317 (Premium Builder / Simple Science Voice Standard) and the new page_type/page_subtype routing.
- Pre-check now also opens Doc 317 and notes the page's page_type/page_subtype.
- Section 9 (E-E-A-T): added Aaron Kapfer as field authority alongside Karen Sager (technical); citations updated to the 3–5 superscript standard with no source names in prose.
- Section 11 (Voice Check): expanded to the Doc 317 model — Bill Nye accessibility (B2C), B2B register (MMGG, Bill Nye off), teach-then-prove, Karen + Aaron presence, no source-led prose, ~4-sentence paragraph feel. Kept as a human sanity check; hard enforcement stays in Doc 328 Section 2B.

**Version 7.0 (May 16, 2026):**
- Added Section 15: Narrative Strategy Alignment (15a-15f) — buyer_state, narrative_attack, language_translation, field_story, proof_entity_ownership, Key Takeaways quality gate
- Added narrative strategy failure to CRITICAL ITEMS auto-fail list
- Added narrative strategy failure to Prioritization Critical list
- Added minor narrative strategy gaps to Non-Critical list

**Version 6.0 (April 22, 2026):**
- Added Section 9: E-E-A-T & Authority (author bio, dates, citations, patents)
- Added Section 10: Schema Readiness (20 PAA questions, FAQ schema, breadcrumbs)
- Added Section 11: Voice Check ("Matt Risinger" test, first person, direct)
- Added Section 12: CTA Placement (per Doc 180 - 4 positions)
- Added Section 13: Internal Links (cluster links, anchor text, routing)
- Added Section 14: Tension Gradient (7 layers per Doc 104)