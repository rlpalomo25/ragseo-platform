# Doc 230: System Governor & Pipeline Orchestration Protocol

**Series:** 200 (Workflow) | **Status:** Active | **Last Updated:** April 26, 2026

---
> **Quick Reference**
> **Owns:** The routing of all tasks through production pipelines.
> 
> **Two Systems Managed:**
> 1. **Main Production Pipeline** - Standard content workflow (Stage 1 → Stage 11)
> 2. **SOT Branch** - Controlled sub-pipeline (Stage 3B: 314 → 354 → 357 → 358 → 356 → 355)
> 
> **SOT Branch Rule:** The SOT branch is an exception-controlled sub-pipeline and does NOT require Doc 153, 170, 173, or 1710 unless explicitly routed back into the main content pipeline.
> 
> **Main Pipeline Rules:**
> - No task enters without a completed Execution Plan (Doc 153)
> - Content must pass QA before publication
> - Failed content routes to specific phase where failure occurred
> 
> **If/Then:** If article fails QA for missing information gain, route back to Execution Planning, not Writing.
---

 Purpose: The System's Central Nervous System

This document defines the role of the **System Governor**, the master orchestration protocol that actively manages the entire content production and optimization pipeline from end to end. It is not a passive monitor; it is the central nervous system that ensures every stage of the process is executed in the correct sequence, to the correct standard, and in alignment with the system's revenue objectives.

Its primary functions are:

1.  **Dispatch & Orchestration:** To manage the flow of work through both pipelines.
2.  **Integrity & Enforcement:** To ensure every step adheres to the standards defined in the doctrine library.
3.  **Escalation & Resolution:** To identify failures and route them to the appropriate human or automated process for resolution.

## 2.0 The Governance Layer: The System's Brain & Nervous System

To prevent system gridlock, the governance layer operates on a strict, explicit hierarchy. This is how the system thinks, decides, and acts.

| Doc # | Document Name | Role | Key Function |
| :--- | :--- | :--- | :--- |
| **224** | Unified Advisor Doctrine | **The Brain (Why)** | Translates high-level strategy into measurable KPIs. The source of strategic intent. |
| **201** | Content Performance Rubric | **The Senses (Detect)** | Measures the performance of every asset against the KPIs defined in Doc 224. |
| **210** | Revenue Intelligence & Prioritization Engine | **The Prefrontal Cortex (Decide)** | Decides **what** is worth working on by calculating the Opportunity Score. The ultimate authority on resource allocation. |
| **205** | Closed-Loop Enforcement Protocol | **The Amygdala (Triage)** | Assigns a severity tier to every detected problem, determining the urgency of the response. |
| **211** | A/B Testing & Experimentation Protocol | **The Scientific Method (Validate)** | Determines **if** a proposed fix should be tested or implemented directly. |
| **143** | Offer Library & Version Control Protocol | **The Arsenal (Offer)** | The central, version-controlled library of all testable marketing offers. |
| **204** | Performance Enforcement & Optimization Protocol | **The Muscle Memory (Fix)** | Provides the specific, pre-approved playbooks for how to fix common problems. |
| **206** | Content Decay & Freshness Protocol | **The Lifecycle Manager (Manage)** | Actively combats content entropy by forcing re-evaluation and refresh cycles. |
| **230** | **System Governor & Pipeline Orchestration Protocol** | **The Central Nervous System (Act)** | The master controller. It receives signals from all other governance docs and routes the work to the correct stage in the pipeline. **This document you are reading now.** |

> **The Unbreakable Rule:** In any conflict, the lower-numbered document in the governance layer (18-43) wins. This document (Doc 230) is the final executor of the decisions made by the higher-ranking governance documents.

---

## MANDATORY ENFORCEMENT RULES

The following rules are **system-wide requirements** enforced at every pipeline stage:

### Win Vector Enforcement
- Every keyword must have ONE clear Win Vector
- The same Win Vector must be used across all brands
- Agents must state and anchor to Win Vector throughout

### Multi-Brand Deployment (Default)
- Same keyword can deploy across multiple brands
- Structure can be reused; language must vary
- Deployment Type (Single/Multi) must be explicitly declared

### Structure Enforcement
- Writers follow Execution Plan structure exactly
- Do not modify H1, H2, H3 headings

### AEGIS 5X Consistency
- AEGIS 5X described consistently across all content
- Minimum: 2 Guardians explained per article
- Each Guardian: problem → mechanism → outcome

### Trust Enforcement
- Every claim: Level 2+ minimum
- At least one Level 3 or 4 claim per article
- Trust flow: Early (Authority) → Mid (Transparency) → Late (Social Proof)

### Revenue Alignment
- CTA type matches Execution Plan (Hard/Soft)
- Do not soften or harden CTA language

### Zero-Click Defense
- Include deeper explanation that can't be easily summarized

---

## 2.1 Pipeline Stage Reference

This document (Doc 230) orchestrates the production pipeline. Key supporting documents referenced in pipeline:

| Stage | Agent/Doc | Reference |
|-------|-----------|-----------|
| Input | Doc 151 | Keyword Selection SOP |
| Analysis | Doc 300 | Analyst Agent |
| Strategy | Doc 304 | Strategist Agent |
| SERP | Doc 308 | SERP Intelligence Agent |
| Architecture | Doc 312 | Architect Agent |
| Writing | Doc 316/320/324 | Writer Agents |
| QA | Doc 1710 | QA Checklist |
| Publishing | Doc 190 | Publishing Guide |
| Distribution | Doc 332 | Distributor Agent |
| Seeding | Doc 336 | Seeding Agent |
| Monitoring | Doc 307 | Collector Agent |

### Supporting Core Docs Referenced

- **Doc 110**: Constraint System - time/length/format limits enforced at all phases
- **Doc 100**: Master Content Doctrine - loaded at strategy phase  
- **Doc 102**: Conflict-First Structure - loaded at writing phase
- **Doc 210**: Revenue Intelligence - loaded for prioritization decisions
- **Doc 250**: Minimum Viable Doctrine - executive summary for quick reference
- **Doc 260**: WordPress Publishing Guide - used at Stage 6-8 for assembly
- **Doc 203**: Learning Loop Protocol - captures signals to improve doctrine
- **Doc 344**: Synthesizer - quarterly strategic synthesis (Tier 1 Advisory)

---

## 3.0 System Pipelines Overview

The Governor manages two parallel systems:

### Main Production Pipeline (Stages 1-11)

*   **Stage 1: Keyword Selection** (Input: Doc 111)
*   **Stage 2: SERP & Data Validation** (Input: Doc 308)
*   **Stage 3: Question & PAA Extraction** (Input: Doc 314)
*   **Stage 3B: SOT Build** (Input: Doc 354) ← *Branch point to SOT*
*   **Stage 4: Execution Contract & Outline** (Input: Doc 170)
*   **Stage 5: First Draft Generation** (Input: Doc 173)
*   **Stage 6: Content & Narrative QA** (Input: Doc 1710)
*   **Stage 7: Visual & UX Blueprint** (Input: Doc 190)
*   **Stage 8: Technical & Schema Assembly** (Input: Doc 190)
*   **Stage 9: Final Pre-Publish QA** (Input: Doc 1710)
*   **Stage 10: Publish & Distribute** (Input: Doc 125)
*   **Stage 11: Performance Optimization & Re-Entry** (The Closed Loop)

---

## 3.1 SOT Branch (Controlled Sub-Pipeline)

The SOT branch is a **controlled sub-pipeline** that diverges from Stage 3 and operates independently from the main content pipeline.

> **SOT Branch Rule:** The SOT branch does NOT require Doc 153, 170, 173, or 1710 unless explicitly routed back into the main content pipeline.

### SOT Stage Sequence

```
Stage 3 (Questions) → Doc 314 → 
Stage 3B → Doc 354 (SOT Build) → Doc 357 (QA) → Doc 358 (Entity Check) → Doc 356 (Eligibility) → Doc 355 (Local) → Publish/Local Pages
```

### SOT Documents

| Stage | Doc | Role |
|-------|-----|------|
| 3B-1 | Doc 354 | SOT Agent - builds answer set |
| 3B-2 | Doc 357 | SOT QA - validates against hard gates |
| 3B-3 | Doc 358 | Entity Check - consistency verification |
| 3B-4 | Doc 356 | Eligibility - dealer/product/region gate |
| 3B-5 | Doc 355 | Local SOT - city/condition injection |

### Escalation Rules (SOT Branch)

| Failure Point | Route To | Action |
|--------------|---------|--------|
| Content weak | Doc 354 | Rewrite |
| Strategic ambiguity | Doc 304 | Escalate |
| Mechanism issue | Doc 142 | Route to mechanism authority |
| Entity drift | Doc 358 | Flag, return to 354 |
| Dealer eligibility fail | Doc 356 | Flag in dealer DB |
| Repeated failures (3x) | Doc 230 | Full review |

### Governance Override

When Doc 357 escalates to Doc 230:
1. Doc 230 assesses systemic vs isolated issue
2. If systemic → flag for Doc 344 quarterly review
3. If isolated → route to source doc for fix

When Doc 358 fails for entity consistency:
1. Escalate to Doc 142 (if mechanism) or Doc 130-132 (if brand)
2. Flag in Document Registry for audit

When Doc 356 eligibility shows pattern failure:
1. Flag in Dealer Database
2. Escalate to Doc 230 for data governance review
3. Document in failure log (Doc 357)

### DOCTRINE CHANGE REVALIDATION (Gap 2 Fix)

When SOT governance docs change, trigger revalidation:

| Doctrine Doc | Change Triggers | Action |
|--------------|-----------------|--------|
| Doc 163 (SOT Page Type) | Rules, retrieval readiness, structure | Flag ALL active SOT pages for review |
| Doc 142 (Mechanism) | Mechanism statements, component names | Flag ALL pages with mechanism for QA |
| Doc 358 (Entity Gate) | Naming rules, entity sources | Flag ALL pages for entity recheck |

**Revalidation Process:**
1. Flag affected pages with version_stale
2. Route through Doc 357 for gate recheck
3. Doc 357 verifies against new doctrine
4. Pass: increment version, mark fresh
5. Fail: return to Doc 354 for rewrite

**Manual Trigger:** System Governor can force revalidation on any SOT doc change.

### SOT Branch Priority

The SOT branch takes priority over standard pipeline when:
- Question is category-defining (per Doc 163)
- SOT already exists for primary question
- Local pages are required for dealer network

### SOT-to-Seeding Handoff (Gap 1 Fix)

The SOT pipeline must formally hand off to seeding. Add after Doc 355 publishes:

**SOT Output → Seeding Mapping:**

| SOT Output | Seeding Consumption | Used By |
|-----------|---------------------|--------|
| SOT answer set | Maps to Gold Answers | Doc 336, Doc 337 |
| Metadata packet | Citation Intent Map | Doc 336 |
| Comparison trigger | Flag for comparative content | Doc 336 |
| FAQ pairs | FAQ seeding blocks | Doc 336 |
| External validation priority | Seeding priority queue | Doc 230 |
| Entity definitions | Entity reinforcement | Doc 337 |

**Seeding Trigger Rules for SOT:**

| Condition | Seeding Action |
|-----------|---------------|
| New SOT published | Auto-trigger outbound seeding review |
| HIGH validation priority | Priority queue for seeding |
| Comparison trigger = TRUE | Create/comparison asset seeding |
| FAQ eligible | Add FAQ pairs to seeding corpus |

**Seeding Docs Update Needed:**
- Doc 336/337 must load SOT metadata packet as input
- Doc 125 must recognize SOT outputs as seeding source

---

## 4.0 Stage 10: The Closed-Loop Optimization Engine

This is the system's adaptive core. It is a continuous loop that connects performance back to production.

### 10.1 Triggers: The Three Gates of Optimization

The closed-loop is initiated by one of three triggers:

1.  **Performance Breach (Doc 201):** An asset fails to meet its KPI benchmarks for two consecutive months.
2.  **Distribution Gap (Doc 201):** An asset is flagged with a high Distribution Gap score, triggering a mandatory seeding cycle.
3.  **Content Decay (Doc 206):** An asset's Freshness Score drops below a threshold, forcing a re-evaluation or a mandatory refresh review.

### 10.2 Mandatory First Filter: The Doc 210 Revenue Gate

Before any action is taken, the detected issue is passed to **Doc 210 (Revenue Intelligence & Prioritization Engine)**.

1.  Doc 210 calculates the **Opportunity Score** for the asset based on its revenue potential, traffic, and conversion gap.
2.  **Decision:**
    *   If the score is **below** the "Do-Nothing" threshold, the process **stops**. The issue is logged for monitoring, and no resources are allocated.
    *   If the score is **above** the threshold, the issue is approved for action and proceeds to the next step.

### 10.3 Triage: Severity Assessment & Delegation (Doc 205)

Once an issue is filtered, the Governor applies the triage and delegation rules from **Doc 205**. This determines both the severity of the issue and who is responsible for resolving it, removing the System Steward as a single point of failure.

### 10.4 Action: Re-Entry into the Pipeline

Based on the fix prescribed by **Doc 204**, the Governor re-routes the content asset back into the main pipeline at a specific stage. This is a hard-coded, non-negotiable re-entry.

| Fix Type (Prescribed by Doc 204) | Re-Entry Stage (in Doc 230) | Description |
| :--- | :--- | :--- |
| **Title / Meta Rewrite** | **Stage 8 (Final QA)** | A minor copy change that requires a quick check before re-publishing. |
| **Intro / Hook Rewrite** | **Stage 4 (First Draft)** | Requires a partial rewrite and subsequent QA. |
| **Answer Block / Structural Change** | **Stage 3 (Outline)** | A fundamental structural change that requires a new outline and full re-generation. |
| **CTA / Offer Change (Doc 143)** | **Stage 7 (Technical Assembly)** | Requires pulling a new, version-controlled offer from the Offer Library and updating the page build. |
| **Technical Schema Fix** | **Stage 7 (Technical Assembly)** | A code-level fix that requires developer intervention. |

This protocol ensures that every performance issue is addressed with the appropriate level of rigor, and that the system's resources are always focused on the highest-impact opportunities first.