> **RETIRED / SUPERSEDED — 2026-07-18.** Document relationships are now maintained in `System_Documentation_Spreadsheet.csv` (`Loads (Inputs)` and `Outputs To` columns), the single source of truth. Do not maintain this file.

# Document Registry

**Version:** 5.0 | **Last Updated:** July 12, 2026 | **Purpose:** Master reference mapping all document numbers to actual files

---

## SOT Asset Registry Initialization Rule

**First row is created by Doc 354** when the first SOT asset is generated.

| SOT_ID | Version | Status | Parent_Child | Created_By | Last_Updated |
|---------|---------|--------|--------------|-------------|--------------|
| Example: SOT-gutter-guards-B2C-20260428-v1 | v1 | active | parent | Doc 354 | 2026-04-28 |

**Ownership by Stage:**
- Doc 354: Creates entry, increments version on rebuild
- Doc 356: Checks version, flags children stale, triggers rebuild
- Doc 355: Uses version provided by Doc 356, passive recipient
- Doc 357: Validates version consistency during QA
- Doc 190: Updates status to "published" on publish

---

## How to Use This Registry

- **Filename** = what's in the folder
- **Internal ID** = what the document claims to be
- **Pulls From (Inputs)** = documents that this doc uses as input/references
- **Pushes To (Outputs)** = documents that this doc provides information TO
- **Status:** ✅ = Active | ⚠️ = Deprecated (Use 350 Series)

---

## 100 Series: Core Doctrine

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Used By | Status |
|----------|-------------|---------------------|---------------------|---------|--------|
| Doc 100_ Master Content Doctrine.md | Doc 100 | — | Doc 230, Doc 312 | ✅ |
| Doc 102_ Conflict-First Structural Doctrine.md | Doc 102 | — | Doc 170, Doc 230 | ✅ |
| Doc 104_ Writing the Tension Gradient.md | Doc 104 | — | Doc 170, Doc 173 | ✅ |
| Doc 106_ Brand Expression Doctrine.md | Doc 106 | — | Doc 316, Doc 310 | ✅ *Single authority for brand expression. Doc 133 retired May 19, 2026.* |
| ~~Doc 133_ Brand Expression Doctrine.md~~ | ~~Doc 133~~ | — | — | ⚠️ RETIRED May 19, 2026 — Moved to RETIRED folder. Superseded by Doc 106. |
| Doc 108_ Content Expression & Format Doctrine.md | Doc 108 | — | Doc 121, Doc 170 | ✅ |
| Doc 110_ Constraint System.md | Doc 110 | — | Doc 230 (all stages) | ✅ |

---

## 111 Series: Data & Evidence

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 111_ Keyword Governance Table.md | Doc 111 | Doc 300, Doc 304 | Doc 300 (loads), Doc 312 | ✅ |
| Doc 112_ Data Source Guardrails.md | Doc 112 | — | Doc 340, Doc 307 | ✅ |
| Doc 113_ Citation Resource Bank.md | Doc 113 | — | Doc 332, Doc 340 | ✅ |
| Doc 114_ Brand Fact Registry.md | Doc 114 | — | Doc 316, Doc 320, Doc 324 | ✅ |

---

## 120 Series: Intelligence & Strategy

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 120_ Master Intelligence Architecture.md | Doc 120 | — | Doc 300, Doc 304 | ✅ |
| Doc 121_ Answer Formatting Doctrine.md | Doc 121 | — | Doc 170, Doc 173 | ✅ |
| Doc 122_ Retrieval & Chunking Doctrine.md | Doc 122 | — | Doc 170, Doc 328 | ✅ |
| Doc 123_ AEO Technical Playbook.md | Doc 123 | — | Doc 170, Doc 190 | ✅ |
| Doc 124_ Entity Relationship Map.md | Doc 124 | — | Doc 170, Doc 300 | ✅ |
| Doc 125_ LLM Seeding Protocol.md | Doc 125 | — | Doc 336, Doc 337, Doc 435 | ✅ |

---

## 130 Series: Brand Modules

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 130_ MasterShield Brand Module.md | Doc 130 | — | Doc 316, Doc 332 | ✅ |
| Doc 131_ Klean Gutter Brand Module.md | Doc 131 | — | Doc 320, Doc 332 | ✅ |
| Doc 132_ MicroMeshGutterGuards.com Brand Module.md | Doc 132 | — | Doc 324, Doc 332 | ✅ |
| Doc 135_ Brand Argument Architecture.md | Doc 135 | — | — | ✅ |

---

## 140 Series: Conversion & Trust

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 140_ Conversion Architecture Module.md | Doc 140 | — | Doc 144, Doc 161, Doc 180-182 | ✅ |
| Doc 141_ Trust Layer System.md | Doc 141 | — | Doc 180-182, Doc 153 | ✅ *Added Doc 153 to Feeds Into July 12, 2026: Doc 153's Step 4 Claim Strength rule referenced this doc's Level 2-4 hierarchy but never cited it or listed it as a required input; found during the 17-step audit and fixed.* |
| Doc 142_ AEGIS 5X Mechanism Authority.md | Doc 142 | — | Doc 222, Doc 354, Doc 357, Doc 358 | ✅ |
| Doc 143_ Offer Library & Version Control.md | Doc 143 | — | Doc 230, Doc 211 | ✅ |
| Doc 144_ Conversion Integration Doctrine.md | Doc 144 | Doc 140 | Doc 180-182 | ✅ |
| Doc 145_ Revenue Intelligence Conversion Feedback Loop.md | Doc 145 | Doc 210 | Doc 140 | ✅ |

---

## 150 Series: Workflow Input

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 150_ Competitive Analysis SOP.md | Doc 150 | — | Doc 300 (loads), Doc 308 | ✅ |
| Doc 151_ Keyword Selection & Prioritization SOP.md | Doc 151 | — | Doc 230, Doc 300 | ✅ |
| Doc 308_ SERP Intelligence Agent.md | Doc 308 | Doc 120, Doc 150 | Doc 304 | ✅ |
| Doc 153_ Execution Plan Generator.md | Doc 153 | Doc 304, Doc 155, Doc 193, Doc 141 (new), Keyword Bundle (Ubersuggest export, new formal input) | Doc 154, Doc 312 | ✅ *v12.6, July 12, 2026: Step 6B's first retroactive run under-credited correctly-sourced MMGG FAQs by phrase-matching instead of topic-matching; added a Reframed-audience pages clause (check the topic, not the literal question text, when buyer_state differs from the source-data population) and a Structural exception for required non-FAQ content (trade-enablement tables, routing blocks). Prior: v12.5, added Keyword Bundle as a Required Input; added Keyword Bundle Mapping and Step 6B (every FAQ traces to a real source, count is not a target); added Doc 141 citation + reject rule for Claim Strength, found during a 17-step audit. See Doc 208 Worked Example #4 and its addendum.* |
| ~~Doc 154_ Execution Plan Reviewer Protocol.md~~ | ~~Doc 154~~ | ~~Doc 153~~ | ~~Doc 312~~ | ⚠️ RETIRED | Moved to RETIRED folder. Function absorbed into Doc 153 Section 8.
| Doc 155_ Narrative Strategy Playbook.md | Doc 155 | — | Doc 153, Doc 304 (loaded as knowledge) | ✅ |

---

## 160 Series: Page Type Modules

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Used By | Status |
|----------|-------------|---------------------|---------------------|---------|--------|
| Doc 160_ Pillar Page Type Module.md | Doc 160 | — | Doc 170, Doc 180 | ✅ |
| Doc 161_ Cluster Page Type Module.md | Doc 161 | Doc 140 | Doc 171, Doc 181 | ✅ |
| Doc 162_ Local Page Type Module.md | Doc 162 | — | Doc 172, Doc 182 | ✅ |
| Doc 163_ SOT Page Type Module.md | Doc 163 | Doc 430 | Doc 354 | ✅ |
| Doc 164_ Mechanism Retrieval Asset.md | Doc 164 | Doc 430, Doc 434 | Doc 312, publish | ✅ |

---

## 170 Series: Writer Playbooks

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 170_ Writer Playbook - Pillar Pages.md | Doc 170 | Doc 102, Doc 104, Doc 108, Doc 121-124 | Doc 316, Doc 320, Doc 324 | ✅ |
| Doc 171_ Cluster Page Writers Playbook.md | Doc 171 | Doc 161 | Doc 316, Doc 320, Doc 324 | ✅ |
| Doc 172_ Local Page Writers Playbook.md | Doc 172 | Doc 162 | Doc 316, Doc 320, Doc 324 | ✅ |
| Doc 173_ AI Writing Prompt.md | Doc 173 | Doc 104 | — | ✅ |
| Doc 174_ B2B Writer Playbook.md | Doc 174 | — | — | ✅ |

---

## 180 Series: Writer Agents

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 180_ Writer Agent - MasterShield.md | Doc 180 | Doc 170, Doc 106, Doc 130 | Doc 328 | ✅ |
| Doc 181_ Writer Agent - Klean Gutter.md | Doc 181 | Doc 170, Doc 106, Doc 131 | Doc 328 | ✅ |
| Doc 182_ Writer Agent - MMGG.md | Doc 182 | Doc 170, Doc 106, Doc 132 | Doc 328 | ✅ |

---

## 190 Series: Publishing, Handoff & Remediation

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 190_ Publishing and Page Assembly System.md | Doc 190 | Doc 153 | Doc 328, Doc 192 | ✅ |
| Doc 192_ Canonical Page Handoff Template.md | Doc 192 | Doc 190 | Doc 316, Doc 320, Doc 324, Doc 361, Doc 328 | ✅ *v2.4, July 27, 2026 (Karen): "publish" is now a standing trigger for the Audit Gate covering already-shipped pages being re-requested, not just new drafts — closes the gap that let Klean/MMGG's pages sit "audit pending" for two weeks. v2.3, July 21: added 7A-SCHEMA (real JSON-LD required, found missing from 5 live MasterShield pages). v2.2/v2.1: Audit Gate + stage-gate made explicit. v2.0, July 10, 2026: retired the blue/black Google Doc build-sheet output format for a self-contained, styled HTML preview. v1.1: see file.* |
| Doc 193_ Canonical Execution Plan Format.md | Doc 193 | Doc 153, Doc 190 | Doc 153, Doc 154, execution-plan-writer | ✅ |

*(The June 2026 visual/handoff remediation spec is a supporting document, not pipeline doctrine — it lives in `company/`, outside the RAG folder, and is intentionally unnumbered.)*

---

## 200 Series: Workflow & Governance

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 200_ Pipeline Orchestration Overview.md | Doc 200 | — | — | ✅ |
| Doc 201_ Content Performance Rubric.md | Doc 201 | — | Doc 205, Doc 210 | ✅ |
| Doc 202_ Pipeline Metrics & Reporting.md | Doc 202 | — | Doc 210 | ✅ |
| Doc 203_ Learning Loop Protocol.md | Doc 203 | — | Doc 300, Doc 304 | ✅ |
| Doc 204_ Performance Enforcement & Optimization Protocol.md | Doc 204 | Doc 205 | Doc 230 | ✅ |
| Doc 205_ Closed-Loop Enforcement Protocol.md | Doc 205 | Doc 201 | Doc 204, Doc 230 | ✅ |
| Doc 206_ Content Decay & Freshness Protocol.md | Doc 206 | — | Doc 100 | ✅ |
| Doc 207_ Fact Nugget System.md | Doc 207 | Doc 113, Doc 328 (harvester) | Doc 114, Doc 361 | ✅ |
| Doc 208_ Change Ripple Protocol.md | Doc 208 | Document Registry (starting point, not sole source) | Any doc/skill-draft edit | ✅ *v2.8, July 27, 2026: added Worked Example #8, a fix Doc 329 made to its own trademark check (C2) never rippled to Doc 328's identical check; found only because Karen's audit request caused the check to actually run. v2.7: added Step 3D, "missing entirely" is the same ripple finding as "present but stale," not exempt. v2.6-v1.0: see file.* |

---

## 210 Series: Experimentation

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 210_ Revenue Intelligence & Prioritization Engine.md | Doc 210 | — | Doc 145, Doc 300 (loads), Doc 202 | ✅ |
| Doc 211_ Systemwide A-B Testing Protocol.md | Doc 211 | Doc 143 | Doc 230 | ✅ |

---

## 220 Series: Architecture

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 220_ URL Architecture Map.md | Doc 220 | — | Doc 312 | ✅ |
| Doc 221_ Hub-and-Spoke Linking Topology.md | Doc 221 | — | Doc 304 | ✅ |
| Doc 222_ Cluster Architecture Map.md | Doc 222 | Doc 142 | Doc 312 | ✅ |

---

## 230 Series: System Governance

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 230_ System Governor & Pipeline Orchestration Protocol.md | Doc 230 | — | All | ✅ |

---

## 240 Series: Integration

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 240_ Visby Integration Protocol.md | Doc 240 | — | — | ✅ |
| Doc 241_ KPI Tracking & Reporting System.md | Doc 241 | — | — | ✅ |
| Doc 242_ Agent System Definition.md | Doc 242 | — | — | ✅ *Updated to v7.0 with 300-series agent IDs* |

---

## 300 Series: Pipeline Agents

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 300_ Analyst Agent Instructions.md | Doc 300 | Doc 111, Doc 150, Doc 210 | Doc 304 | ✅ |
| Doc 304_ Strategist Agent Instructions.md | Doc 304 | Doc 300, Doc 307, Doc 308, Doc 314, Doc 155 (knowledge), Doc 142 (knowledge), Doc 432 (knowledge) | Doc 153 | ✅ |
| Doc 306_ Routing Agent.md | Doc 306 | — | Doc 312 | ✅ |
| Doc 307_ Collector Agent.md | Doc 307 | — | Doc 201, Doc 304 | ✅ |
| Doc 308_ SERP Intelligence Agent.md | Doc 308 | Doc 120, Doc 150 | Doc 304 | ✅ |
| Doc 309_ AEO Extraction Agent.md | Doc 309 | — | Doc 304, Doc 337 | ✅ |
| Doc 310_ Brand Voice Agent.md | Doc 310 | — | Doc 337 | ✅ |
| Doc 312_ Architect Agent Instructions.md | Doc 312 | Doc 153, Doc 222, Doc 220, Doc 221, Doc 155 | Doc 316/320/324 | ✅ |
| Doc 314_ Question & PAA Agent.md | Doc 314 | SEO data, Reddit, G2, forums, Keyword Bundle (new formal input) | Doc 304, Doc 354, Doc 355, Doc 357, Doc 164, Doc 153 (theme_clusters, new) | ✅ *v6.1, July 12, 2026: added Step 7 Topic Theme Clustering, groups keyword_variants by subject, sums real search_vol, cross-references PAA support, outputs `theme_clusters[]` for Doc 153's Keyword Bundle Mapping. Never invents a theme with no bundle backing; degrades gracefully with a human-review flag if the bundle is unavailable.* |
| Doc 316_ MasterShield Writer Agent Instructions.md | Doc 316 | Doc 180, Doc 155, Doc 317, Doc 192, Doc 114, Doc 160, Doc 316-M…316-B2B | Doc 328 | ✅ *v13.1, July 12, 2026: added mandatory Provenance bullet to Section 5, write only the plan's Step 6B FAQ set, no padding, no borrowing sibling-brand FAQs. Prior: v13.0, July 10, 2026: matched Doc 192 v2.0's new styled-HTML output format (retiring the Google Doc build sheet); updated the Your Questions Answered rule to specify the `.qa` component (a staged block, correct there). v12.0, July 10, 2026: fixed a Doc 192 mismatch (above-fold was "exactly two" full answers; Doc 192's July 4 update requires 3 truncated teasers with jump links), added the mandatory four-beat FAQ bridge and a template-repetition caution. v11.0, July 9, 2026, added Doc 192/114 as required loads, Six Questions model, corrected stats/symbol/byline/pricing.* |
| Doc 320_ Klean Gutter Writer Agent Instructions.md | Doc 320 | Doc 181, Doc 155, Doc 317, Doc 192, Doc 114, Doc 131, Doc 316-M…316-B2B | Doc 328 | ✅ *v13.1, July 12, 2026: same Provenance bullet as Doc 316, Klean-specific phrasing (don't pull FAQs from MasterShield's or MMGG's page). Prior: v13.0, July 10, 2026, same Doc 192 v2.0 format fix as Doc 316. v12.0/v11.0: see file.* |
| Doc 324_ MMGG Writer Agent Instructions.md | Doc 324 | Doc 182, Doc 155, Doc 317 (B2B register), Doc 192, Doc 114, Doc 132, Doc 316-B2B | Doc 328 | ✅ *v13.2, July 12, 2026: added a "sourced-but-reframed ≠ unsourced" clarification, a dealer-phrased FAQ traces correctly to a consumer PAA/bundle/competitor row when the underlying topic matches even if the wording doesn't, plus a structural exception for required trade-enablement/routing content. Prior: v13.1, added mandatory Provenance bullet to Section 5. v13.0/v12.0/v11.0: see file. See Doc 208 Worked Example #4 and its addendum.* |
| Doc 328_ Auditor Agent Instructions.md | Doc 328 | Doc 1710, Doc 120-122, Doc 317, Doc 430, Doc 434, Doc 164, Doc 192, Doc 153 (Step 6B, new) | Doc 316-324 (if fails), Doc 190 (if passes) | ✅ *v16.1, July 27, 2026: fixed the Trademark Symbols check, still read "Only MasterShield® is registered," a single-brand assumption Doc 329's C2 had already caught and fixed weeks earlier without the identical fix rippling here; parametrized per Doc 114/Doc 329's language. Found while running a real audit pass on the three micro-mesh pages at Karen's request. Prior: v16.0, July 26, 2026, image policy reset per Doc 190 v6.5. v14.9-v13.0: see file. See Doc 208 Worked Example #4/#8.* |
| Doc 329_ Refresh Audit (361 Light Gate).md | Doc 329 | Doc 114, Doc 141, Doc 144, Doc 190, Doc 194 | Doc 361-MS/KG/MMGG (the refresh track's actual audit gate — NOT Doc 328, which auto-fails a refresh on missing execution-plan schema) | ✅ *v1.2, July 12, 2026: parametrized C2 (trademark) and C3 (trust bar) by brand, was hardcoded to MasterShield only ("Only MasterShield® is registered" was wrong for Klean Gutter®/MicroMeshGutterGuards.com®, both separately registered); added C15 (MMGG neutrality). Companion to the new Doc 361-KG/MMGG tracks. Prior: v1.1, added C14 (FAQ Provenance) as a critical blocking gate. See Doc 208 Worked Example #4/#5.* |
| Doc 361_ MasterShield Page Refresh (Instructions).md | Doc 361-MS-I | Doc 361-K (Knowledge Pack, uploaded alongside), Doc 361-W (Workflow Reference, shared) | Refreshed MasterShield pages | ✅ *v1.2, July 12, 2026: noted this is now one of three parallel tracks (referred to as Doc 361-MS by its new siblings), no procedural change. Prior: v1.1, repaired file truncation, added FAQ source-tracking + cap. See Doc 208 Worked Example #4/#5.* |
| Doc 361_MasterShield Page (Knowledge).md | Doc 361-MS-K | Doc 114, Doc 430, Doc 142, Doc 432 | Doc 361-MS-I | ✅ *v1.2, July 12, 2026: noted Klean/MMGG now have their own sibling Knowledge Packs. Prior: v1.1, repaired file truncation, corrected a stale above-fold-count sync claim. Corrected August 4, 2026: filename in this row carried a stray space after the underscore ("Doc 361_ MasterShield") that no longer matched the file's actual on-disk name; fixed to match, per the Registry's own closing-note allowance for necessary corrections.* |
| Doc 361_ Refresh Page (Workflow).md | Doc 361-W | — | Doc 361-MS-I/K, Doc 361-KG-I/K, Doc 361-MMGG-I/K | ✅ *v1.2, July 12, 2026: declared explicitly shared across all three Doc 361 tracks; added the "which page's data" sourcing note (Klean/MMGG very often source from MasterShield's real data, cited as such) and the reframed-audience/topic-not-phrase check needed for the new MMGG track. Prior: v1.1, added the 2-per-page fallback cap. Renamed 2026-08-03 (Karen) from "Doc 361_ MasterShield Page (Workflow).md" to remove the misleading MasterShield-specific implication — this row updated to match, per the Registry's own closing-note allowance for necessary corrections.* |
| Doc 361-KG_ Klean Gutter Page Refresh (Instructions).md | Doc 361-KG-I | Doc 131, Doc 320, Doc 361-KG-K, Doc 361-W (shared) | Refreshed/new Klean Gutter pages | ✅ *Added July 12, 2026. v1.0: built as Klean's sibling to Doc 361-MS, replacing the retired KG Content Adapter. Sources demand data from MasterShield's real pull when Klean has none of its own (Step 1A mode split — confirmed by Karen that Klean has almost no independent search footprint), but always writes independently, never adapts MasterShield's prose. FAQ Provenance built in from the start. See Doc 208 Worked Example #5.* |
| Doc 361-KG_ Klean Gutter Page (Knowledge).md | Doc 361-KG-K | Doc 131, Doc 114, Doc 361-KG-I | — | ✅ *Added July 12, 2026. v1.0: Klean-specific facts/voice/CTA/attribution, sourced from Doc 131 and the built Klean micro mesh gutter guards page. Flagged one unverified claim from the retired adapter (a field-test "top-two performer" claim) rather than carrying it forward unverified.* |
| Doc 361-MMGG_ MMGG Page Refresh (Instructions).md | Doc 361-MMGG-I | Doc 132, Doc 324, Doc 361-MMGG-K, Doc 361-W (shared) | Refreshed/new MMGG pages | ✅ *Added July 12, 2026. v1.0: built as MMGG's sibling to Doc 361-MS, replacing the retired MMGG Content Adapter. Sources demand data from MasterShield's real pull (no independent B2B search corpus exists for this category), reframed for the trade, never ported as a homeowner how-to. Built with the topic-not-phrase FAQ reframe rule from the start, the exact fix Doc 153/324/328 needed retroactively after Worked Example #4's addendum — applied here before the mistake could repeat. See Doc 208 Worked Example #5.* |
| Doc 361-MMGG_ MMGG Page (Knowledge).md | Doc 361-MMGG-K | Doc 132, Doc 114, Doc 361-MMGG-I | — | ✅ *Added July 12, 2026. v1.0: MMGG-specific facts/voice/CTA/attribution, sourced from Doc 132 and the built MMGG page. Flagged an unresolved Doc 132/Doc 324 CTA wording discrepancy ("Schedule a Technical Review" vs. "Talk to a Strategist") rather than silently picking one.* |
| ~~Cross-Brand Content Adapter — Spec.md~~ | — | — | — | ⚠️ RETIRED July 12, 2026 — Moved to RETIRED folder. Replaced by Doc 361-KG + Doc 361-MMGG. Superseded the word-swap-from-MasterShield model. |
| ~~KG Content Adapter — GPT Instructions (paste-ready).md~~ | — | — | — | ⚠️ RETIRED July 12, 2026 — Moved to RETIRED folder. Replaced by Doc 361-KG. |
| ~~MMGG Content Adapter — GPT Instructions (paste-ready).md~~ | — | — | — | ⚠️ RETIRED July 12, 2026 — Moved to RETIRED folder. Replaced by Doc 361-MMGG. |
| Doc 332_ Distributor Agent Instructions.md | Doc 332 | Doc 190, Doc 113, Doc 134, Doc 130-132 | Doc 336 | ✅ |
| Doc 336_ Seeding Agent Instructions.md | Doc 336 | Doc 332, Doc 125 | — | ✅ |
| Doc 337_ Reactive Seeding Agent.md | Doc 337 | Doc 309, Doc 310, Doc 113, Doc 124 | — | ✅ |
| Doc 340_ Source Citation Hunter Agent.md | Doc 340 | Doc 112, Doc 113, Doc 151 | — | ✅ |

---

## 317 + 316-X Series: Voice Standard & Page-Type Companions

*Doc 317 is the universal voice standard loaded by all writers (316/320/324) and the auditor (328). The 316-X companions supply page-type structure + voice variants, selected by the Execution Plan's `page_subtype` (Doc 153).*

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 317_ Premium Builder Simple Science Voice Standard.md | Doc 317 | — | Doc 316, Doc 320, Doc 324, Doc 328 | ✅ |
| Doc 316-M_ Mechanism Page Structure.md | Doc 316-M | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-C_ Comparison and Category Page Structure.md | Doc 316-C | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-P_ Pricing and Value Page Structure.md | Doc 316-P | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-Sym_ Symptom and Problem Page Structure.md | Doc 316-Sym | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-Ins_ Installation Page Structure.md | Doc 316-Ins | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-L_ Local and Geographic Page Structure.md | Doc 316-L | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-G_ Guide and Pillar Page Structure.md | Doc 316-G | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-FAQ_ FAQ and Answer Page Structure.md | Doc 316-FAQ | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |
| Doc 316-B2B_ Dealer and B2B Page Structure.md | Doc 316-B2B | Doc 317 | Doc 316/320/324, Doc 328 | ✅ |

---

## 350 Series: SOT Generation

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 163_ SOT Page Type Module.md | Doc 163 | Doc 430 | Doc 354 | ✅ |
| Doc 354_ SOT Agent Instructions.md | Doc 354 | Doc 314, Doc 163, Doc 430, 431, 432, 433, 434 | Doc 357, Doc 355 | ✅ |
| Doc 355_ Local SOT Agent.md | Doc 355 | Doc 163, Doc 142, Doc 356, Doc 357, CSVs | Local Page asset, Doc 312 | ✅ |
| Doc 356_ Local Generation & Context System.md | Doc 356 | Dealer database, CSVs | Doc 355 | ✅ |
| Doc 357_ SOT QA & Question Tracking.md | Doc 357 | Doc 354, Doc 314, Question tracker | Doc 358 (pass), Doc 354 (fail) | ✅ |
| Doc 358_ Entity Consistency Gate.md | Doc 358 | Doc 130-132, Doc 142, Doc 114, Doc 430, Dealer DB | Doc 356, Doc 355 | ✅ |

---

## 400 Series: SOT & LLM Seeding System

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 430_ Canonical Entity Library.md | Doc 430 | — | Doc 431, Doc 432, Doc 164, Doc 328 | ✅ |
| Doc 431_ Answer Object Engine.md | Doc 431 | Doc 430 | Doc 432 | ✅ |
| Doc 432_ Gold Answers.md | Doc 432 | Doc 431 | Doc 433, Doc 336, Doc 337 | ✅ |
| Doc 433_ Field Doctrine.md | Doc 433 | Doc 432 | Doc 434 | ✅ |
| Doc 434_ Edge Case Library.md | Doc 434 | Doc 433 | Doc 435, Doc 164, Doc 328 | ✅ |
| Doc 435_ Seeding Support Chain Protocol.md | Doc 435 | Doc 434, Doc 125 | — | ✅ |

---

**Naming note:** Doc 125 remains the master seeding doctrine. Doc 435 is support-chain knowledge, not master doctrine.

## 500 Series: Dealer Network (Core Doctrine)

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Doc 510_ Dealer Execution SOP.md | Doc 510 | — | Doc 511 | ✅ |
| Doc 511_ Dealer Agent Architecture.md | Doc 511 | Doc 510 | Doc 512 | ✅ |
| Doc 512_ Dealer Tracking + Compliance.md | Doc 512 | Doc 511 | — | ✅ |
| Doc 520_ MasterShield Dealer Agent.md | Doc 520 | — | — | ✅ |
| Doc 521_ Klean Gutter Dealer Agent.md | Doc 521 | — | — | ✅ |
| Doc 530_ Answer Object Deployment Agent.md | Doc 530 | — | — | ✅ |

---

## Supporting Documents (Not Numbered)

| Filename | Internal ID | Pulls From (Inputs) | Pushes To (Outputs) | Status |
|----------|-------------|---------------------|---------------------|--------|
| Net-New_Topic_Research_Process.md | N/A | — | Doc 153 | ✅ |

---

## SOT Asset Registry

*Tracks SOT assets by state. Updated on publish, revalidation, and regeneration.*

### Tracking Fields

| Field | Description |
|-------|-------------|
| sot_id | Unique SOT identifier (e.g., SOT-gutter-guards-B2C-20260426-v2) |
| asset_type | base / local / B2B |
| primary_question | The main question this SOT answers |
| current_version | Current version (e.g., v2) |
| status | draft / qa_passed / published / stale / archived |
| parent_sot_id | Parent sot_id (if local child) |
| child_assets | Array of DMA/region variants |
| qa_pass_version | Last version that passed Doc 357 |
| entity_pass_version | Last version that passed Doc 358 |
| published_version | Last version published |
| seeding_version | Version currently in seeding use |
| comparison_trigger | TRUE/FALSE |
| faq_eligible | TRUE/FALSE |
| external_validation_priority | high / medium / low |
| stale_flag | TRUE/FALSE |
| last_revalidated_at | Date of last doctrine revalidation |
| publish_status | Not published / published / scheduled |
| last_seeded_at | Date of last seeding use |

### SOT Asset Table

| sot_id | asset_type | version | status | parent | child_assets | qa_pass_ver | entity_pass_ver | published_ver | stale_flag |
|--------|-----------|---------|--------|--------|-------------|------------|---------------|--------------|-----------|
| | | | | | | | | | |

*Add new assets here as they are created.*

### Update Triggers

| Event | Action |
|-------|--------|
| New SOT generated | Add row, version v1, status draft |
| QA passes (Doc 357) | Update qa_pass_ver, status qa_passed |
| Entity passes (Doc 358) | Update entity_pass_ver |
| Published (Doc 190) | Update published_ver, status published |
| Local child generated | Add child, inherit parent version |
| Parent regenerates | Increment parent version, mark children stale |
| Doctrine change (per 230) | Flag all stale, set last_revalidated_at |
| Seeding used | Update seeding_version, last_seeded_at |
| Performance drop | Flag stale, trigger rebuild |

---

## Rebuild Trigger Visibility

| Trigger Event | Action |
|--------------|--------|
| Parent SOT regenerates | Flag children STALE in registry, trigger rebuild |
| Doctrine change (Doc 230) | Flag all stale, set last_revalidated_at |
| Performance drop (Doc 203) | Flag stale, trigger rebuild |
| New PAA gaps (Doc 314) | Trigger new local generation |

**Rebuild Flow:**
```
Doc 354 (regenerates) → Flag children STALE → Doc 356 trigger → Regenerate local
```

---

## Pipeline Flow Summary (Quick Reference)

*End of Document Registry - April 27, 2026*
