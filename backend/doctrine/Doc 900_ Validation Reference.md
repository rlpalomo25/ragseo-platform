# Doc 900: Validation Reference — Content & Execution Plan Review

**Purpose:** Quick-reference checklist for validating any content or execution plan against the RAG system.
**Usage:** Load this doc first, then load the specific docs listed for the page type being validated.

---

## 1. PAGE TYPE — Which Doc Set to Load

| Page Type | Primary Spec | Conversion Module | Writer Playbook | Notes |
|-----------|-------------|-------------------|-----------------|-------|
| **Pillar** | Doc 160 | Doc 180 | Doc 170 | Also verify subtype: neutral pillar vs. technology pillar vs. brand pillar |
| **Cluster** | Doc 161 | Doc 181 | Doc 171 | Cluster Arch Map (Doc 222) for mandatory Engineering Clusters |
| **Local** | Doc 162 | Doc 182 | Doc 172 | Local SOT (Doc 355) + Local Gen (Doc 356) |
| **SOT** | Doc 163 | — | — | SOT Agent (Doc 354) + QA (Doc 357) + Entity (Doc 358) |

---

## 2. UNIVERSAL DOCS (Load for EVERY Validation)

| Priority | Doc | What to Check |
|----------|-----|---------------|
| **P0** | **Doc 142 (AEGIS 5X Mechanism Authority)** | Core mechanism phrasing, component definitions, cause→mechanism→outcome, prohibited claims, competitive comparison table, §11A PitchPerfect framing (shelf metaphor, evaluation close, patent precision, pitch terminology) |
| **P0** | **Doc 114 (Brand Fact Registry)** | Patent counts, verified statistics (0.00001% warranty, 10M+ ft, ASTM), trademarks, E-E-A-T credentials. Cross-check all factual claims against this. |
| **P0** | **Doc 130 (MasterShield Brand Module)** | Brand voice (Knowledgeable Neighbor), argument posture, prohibited phrases, pricing rule, author bio requirements, archetype selection |
| **P1** | **Doc 102 (Conflict-First Structural Doctrine)** | 7-layer spine (Tension→Mechanism→Proof→Tension Reset→Authority→Resolution→CTA), Answer-First Hook requirement |
| **P1** | **Doc 104 (Writing the Tension Gradient)** | 7-stage emotional arc (Clarity→Concern→Consequence→Reassurance→Control→Confidence→Action), ensure Reassurance/Tension Reset is present |
| **P1** | **Doc 106 (Brand Expression Doctrine)** | Decision Threshold (brand follows proof), BAIO Brand-Mechanism repetition (2-3x/page), Beliefs Before Brands |
| **P1** | **Doc 108 (Content Expression & Format)** | Answer-First hybrid hook (Line 1=answer, Lines 2-4=tension), paragraph whitespace, em dash limit (1), trademark first mention only, 6th grade reading level, pitch terminology rule (no ratios in homeowner content) |
| **P1** | **Doc 120 (AEO Philosophy)** | Answer-First always, 40-60 word extractable blocks, citable answer criteria (standalone/complete/specific/context-independent), FAQ construction (5-8 Qs, PAA-first), BAIO rules, evaluation-standaard close pattern |
| **P2** | **Doc 110 (Constraint System)** | Word count (Pillar: 1,800-2,500, Cluster: 800-1,200, Local: 800-1,200), time limits, output length constraints — but note Doc 153 may override for clusters (1,200-1,800) |
| **P2** | **Doc 140 (Conversion Architecture)** | CTA types by funnel stage (TOFU=Navigational, MOFU=Educational, BOFU=Transactional), CTA-Trust pairing, placement per page type |
| **P2** | **Doc 141 (Trust Layer System)** | Trust assets (Authority/Social Proof/Transparency), trust escalation (early/mid/late), Claim Strength Hierarchy (min Level 2, at least 1 Level 3-4), trust asset placement per page type |
| **P2** | **Doc 100 (Master Content Doctrine)** | 5 Pillars, core belief, Information Gain mandate (proprietary data, first-hand methodologies, expert anecdotes), B2B vs B2C delivery rule |
| **P3** | **Doc 220 (URL Architecture)** | URL pattern (Pillar: /brand/category/pillar, Cluster: /brand/category/cluster/topic), canonical rules, internal linking hierarchy |
| **P3** | **Doc 222 (Cluster Architecture Map)** | For clusters: mandatory Engineering Cluster Pages, Decision Axis, linking hierarchy (upward/downward/lateral) |
| **P3** | **Doc 225 (Doctrine Precedence)** | Resolve any conflicts between docs using tier system. Tier 0 > 1 > 2 > 3 > 4. Same tier = lower number wins. |
| **P3** | **Doc 1710 (Pre-Publish QA Checklist)** | FAQ count (20 for schema), author bio, trust assets, CTA alignment, generic content filter, "Does This Win?" check |

---

## 3. AGENT-SPECIFIC CHECKS (For Written Content, Not Plans)

| Agent Doc | When to Load | What to Check |
|-----------|-------------|---------------|
| **Doc 316 (MasterShield Writer)** | MS content | Output schema, trust enforcement, AEGIS Guardian min 2, CTA type match, Win Vector enforcement, prohibited moves |
| **Doc 328 (Auditor Agent)** | After writing | Critical fails (structure deviation, prohibited moves, Win Vector weak, competing narratives), scored checks, Final Question Test |
| **Doc 308 (Trust & Conversion Agent)** | CRO-heavy pages | Trust asset flow, claim strength, objection handling |
| **Doc 310 (Brand Voice Agent)** | Voice consistency | Tone anchor compliance, archetype rotation, forbidden phrases |

---

## 4. 400s/SOT CHECKS (For SOT Content Only)

| Doc | What to Check |
|-----|-----------------|
| **Doc 430 (Entity Library)** | Primary canonicals match, no internal conflict, First Sentence Rule (no metaphor, no brand-first) |
| **Doc 354 (SOT Agent)** | Mechanism phrasing exact from Doc 142, bridge structure (belief→failure→mechanism→outcome) |
| **Doc 357 (Canon QA)** | Hard gates: first sentence rule, mechanism included, structure lock |
| **Doc 358 (Entity Gate)** | Naming against Doc 142 and Doc 114 |

---

## 5. VALIDATION SEQUENCE — Branching by Page Type

### 5.1 COMMON BASE (Every Validation)

```
STEP 1: Identify page_type from content header or execution plan
STEP 2: Load page-type spec from Section 1
STEP 3: Load P0-P1 universal docs (142, 114, 130, 102, 104, 106, 108, 120)
STEP 4: Load P2-P3 docs as needed (140, 141, 100, 110)
```

### 5.2 PILLAR PAGE PATH (Doc 160)

```
STEP 5:  Doc 160 first — Brand Neutrality rule (Part 1). Is this a neutral pillar or branded technology pillar?
STEP 6:  Doc 160 — 5-Layer Consumer Journey present? (Simple Desire → Hidden Friction → Root Cause → Engineering Frame → Generic Mechanism)
STEP 7:  Doc 160 — Body sequence correct? (Core Belief → 5 Pillars → Types → Pros/Limitations → DIY → Cost → Complaints → Engineered Resolution)
STEP 8:  Doc 160 — Real Experience Section present? (installer quote + problem/solution narrative + case study)
STEP 9:  Doc 160 — FAQ count 20+, organized by category?
STEP 10: Doc 160 — 4+ internal links to cluster pages?
STEP 11: Doc 160 — H1 uses primary keyword?
STEP 12: Doc 100 — Information Gain present?
STEP 13: Doc 102/104 — 7-layer spine + 7-stage tension gradient complete?
STEP 14: Doc 108 — Answer-First hybrid hook in first 4 lines?
STEP 15: Doc 142 — Mechanism accuracy, locked phrasing, prohibited language
STEP 16: Doc 114 — All factual claims in registry?
STEP 17: Doc 130 — Brand voice, pricing rule, author bio
STEP 18: Docs 140/141 — CTA placement correct for TOFU (Navigational), trust flow
STEP 19: Doc 120 — Extractable blocks, BAIO repetition, FAQ construction
```

### 5.3 CLUSTER PAGE PATH (Doc 161)

```
STEP 5:  Doc 161 first — Decision Axis declared?
STEP 6:  Doc 161 — Real Experience Section present? (REQUIRED — installer quote + narrative + case study)
STEP 7:  Doc 161 — Upward pillar link in first paragraph?
STEP 8:  Doc 161 — Problem section with Failure Consequence?
STEP 9:  Doc 161 — Mechanism Comparison with table?
STEP 10: Doc 161 — Tradeoff Analysis?
STEP 11: Doc 161 — Engineered Resolution present?
STEP 12: Doc 161 — FAQ minimum 10 (or 20 if schema required)?
STEP 13: Doc 161 — Internal linking block with 2-3 lateral cluster links?
STEP 14: Doc 222 — If engineering cluster, does Decision Axis and Guardian match the Cluster Architecture Map?
STEP 15: Doc 181 — CTA gradient (Hard-to-Hard for clusters)?
STEP 16: Do 102-108-120-130-142-114 checks (same as pillar steps 13-19 above)
```

### 5.4 LOCAL PAGE PATH (Doc 162)

```
STEP 5:  Doc 162 first — Local data populated (region, climate, debris types)?
STEP 6:  Doc 162 — Dealer info present? (name, photo, service area)
STEP 7:  Doc 162 — Local trust signals? (installations in county, local testimonials)
STEP 8:  Doc 182 — CTA = Transactional (Schedule Free Diagnostic)?
STEP 9:  Doc 141 — Above-fold social proof, mid-page authority + social, bottom testimonial
STEP 10: Do 102-108-120-130-142-114 checks (same as pillar steps 13-19 above)
```

### 5.5 SOT PATH (Doc 163, 354, 357, 358, 430)

```
STEP 5:  Doc 430 — Primary canonicals match query? First Sentence Rule?
STEP 6:  Doc 354 — Bridge structure: belief → failure → mechanism → outcome?
STEP 7:  Doc 354 — Mechanism phrasing exact from Doc 142?
STEP 8:  Doc 357 — Hard gates: first sentence rule, mechanism included, structure lock?
STEP 9:  Doc 358 — Entity naming against Doc 142 and Doc 114?
STEP 10: Doc 163 — SOT answer-writing rules followed? (SOT is a writing sub-pipeline, not a page type)
STEP 11: Doc 120 — Extractable blocks, standalone citable answers
```

### 5.6 EXECUTION PLAN PATH (Doc 153)

```
STEP 5:  Validate plan schema against Doc 153 rejection rules:
        - Win Vector enforced in structure?
        - Citation blocks ≥ minimum?
        - Trust points ≥ minimum?
        - CTA aligned with offer_type?
        - Multi-brand has version plan?
        - Internal linking ≥ 2 links?
        - Entity enforcement from AI layer?
        - ≤ 6 H2 sections?
        - Single content angle?
STEP 6:  Simulate Human Review (formerly Doc 154):
        - Win Vector validation (specific competitor gap?)
        - Content angle (different from competitors?)
        - Structure (real-world customer logic?)
        - Industry accuracy
        - CTA alignment
        - Information Gain
        - Real-world gap identification
STEP 7:  Run remaining content checks from the page-type path above
        (Docs 102-108-120-130-142-114, etc.)
```

### 5.7 WRITTEN CONTENT PATH (Post-Writing Check)

```
Run the page-type path above, PLUS:
STEP 20: Doc 316 (or 320/324) — Writer output schema validation
STEP 21: Doc 328 — Auditor checks:
        - Structure deviation from Execution Plan (auto-fail)
        - Prohibited moves violated (auto-fail)
        - Win Vector diluted (auto-fail)
        - Competing narratives (auto-fail)
        - Generic content (auto-fail)
        - Final Question Test: "Would this make a reader choose this brand?"
STEP 22: Doc 1710 — Pre-Publish QA Checklist verification
```

---

## 6. MOST COMMON FAILURE PATTERNS (Historical)

1. **Answer-First Hook missing** — First line of body is narrative tension, not a direct answer
2. **Real Experience Section missing** — Required by Doc 160/161, often confused with expert quote
3. **FAQ count below 20** — Schema minimum, consistently under-shot
4. **Tension Reset missing** — Stage 4 of tension gradient, single-paragraph pivot
5. **Decision Axis not declared** — Required for cluster pages (Doc 161/222)
6. **Patent count wrong** — Must match Doc 114 §4.2: author/reviewer bios use Karen's personal **"nine utility patents"**; the **trust bar (all brands)** uses the shared **"17+ patents insured by IPISC"** corporate portfolio. "9"/"nine patents" in a trust bar, or "17+" cast as Karen's personal count, = wrong.
7. **CTA gradient too soft** — Cluster pages need Hard-to-Hard per Doc 181
8. **Doc 160 pillar-type ambiguity** — AEGIS 5X technology pillar doesn't fit cleanly into Doc 160's neutral-pillar model
9. **Brand introduced too early on pillar pages** — Doc 160 says Engineered Resolution only
10. **BAIO repetition missing** — 2-3 Brand+Mechanism pairings per page

---

## 7. Version Tracking

Version, date, and status for every doc now live in **`System_Documentation_Spreadsheet.csv`** (the single source of truth — columns `Version`, `Last Updated`, `Status`). The static table that used to sit here drifted stale — it still listed Doc 153 at v11.5 and Doc 328 at v8.0 — which is exactly the duplication this system is removing. Check the spreadsheet, not a copy.