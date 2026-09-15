# Doc 357 - Canon QA & Question Tracking System

**Version:** 1.3 | **Last Updated:** April 28, 2026

---

## Purpose

Validate SOT output quality and track question-to-coverage across the system.

---

## Pipeline Position (Aligned with Doc 125)

```
Doc 314 (Questions) → Doc 354 (SOT Build) → Doc 357 (QA) → Doc 358 (Entity Check) → Doc 356 (Eligibility) → Doc 355 (Local) → Doc 312 (Architect) → Doc 190 (Publish)
```

**Flow (Per Doc 125 Section 1.0):**
- Doc 314: Extracts PAA questions
- Doc 354: Builds ONE canonical answer set (SOT Build)
- Doc 357: QA validation (4 hard gates + scored checks)
- Doc 358: Entity consistency verification
- Doc 356: Dealer/product/region validation (eligibility gate)
- Doc 355: City/condition injection (local adaptation)
- Doc 312: URL structure, internal linking
- Doc 190: WordPress publishing, schema

**Note:** Doc 357 performs QA AFTER Doc 354 builds the SOT. There is no "Pre-QA" step - the flow is: Question → Build → QA → Next Stage.

**Note:** Doc 357 performs QA AFTER Doc 354 builds the SOT. There is no "Pre-QA" step - the flow is: Question → Build → QA → Next Stage.

---

## SECTION 1: QUESTION TRACKING

### TRACKING TABLE

| PAA_Question | SOT_ID | Status | Last_Updated | Notes |
|--------------|--------|--------|--------------|-------|-------|
| | | pending/active/retired | | |

### STATUS DEFINITIONS

| Status | Meaning |
|--------|---------|
| **pending** | Question submitted, no SOT generated |
| **active** | SOT generated and passing QA |
| **retired** | Question superseded by new SOT |

### LOGIC

When Doc 314 submits questions:
1. Check existing tracker for duplicates
2. Mark new questions as "pending"
3. After SOT generation → mark as "active"
4. If question re-ranked → mark old as "retired"

---

## SECTION 2: SOT QA CHECKPOINTS

### PRE-GENERATION CHECKS (Before Doc 354)

| Check | Requirement |
|-------|-------------|
| Question valid | PAA format, not duplicate |
| Win Vector clear | Single clear win provided (from Doc 304/Execution Plan) |
| Brand rule defined | Compatibility check only, not commitment |

### POST-GENERATION CHECKS

#### HARD GATES (All 4 must pass - no scoring, pure pass/fail)

| Check | Requirement | Fail Action |
|-------|-------------|-------------|
| First sentence rule | Sentence 1 = direct answer | Return to 354 |
| Mechanism included | At least 1 AEGIS 5X reference | Return to 354 |
| Structure lock | H2s match approved SOT structure | Return to 354 |
| Retrieval readiness | Direct answer in sentence 1, single-question blocks | Return to 354 |

**Hard gate failure → rewrite and resubmit**

#### SCORED CHECKS (4 items - 1 point each, threshold-based)

| Check | Requirement | Max Points |
|-------|-------------|-----------|
| Claim strength | Specific, not vague | 1 |
| Proof points | At least 1 data/fact | 1 |
| Quote richness | Karen Sager or proof | 1 |
| Edge-case coverage | Density of relevant cases | 1 |

> **Proof Point Validation Rule:** Proof points must be traceable to a named source in Doc 113 (Citation Resource Bank). Acceptable sources include NOAA Atlas 14, HEC-22 (FHWA), peer-reviewed filtration science, verified installation statistics from Doc 114, or a Karen Sager field observation. Fabricated statistics, unsourced percentages, and vague claims (e.g., "studies show") DO NOT pass this check.

**Pass: ALL 4 hard gates pass + ≥2 scored (total 6+ of 8)**
**Fail: Any hard gate fails → return to 354**

---

## SECTION 3: LOCAL ADAPTATION QA

### BOUNDARY RULE

- **Doc 356** owns eligibility decisions
- **Doc 357** validates completeness of 356's output, does NOT re-decide

### PRE-LOCAL CHECKS (Before Doc 355)

| Check | Requirement | Fail Action |
|-------|-------------|-------------|
| Eligibility cleared | Doc 356 gate passed | Return to 356 |
| SOT active | Status = "active" | Return to 354 |
| Region valid | In 7-region list | Return to 356 |
| Conditions valid | No conflicting conditions | Return to 356 |

### POST-LOCAL CHECKS

| Check | Requirement | Scoring |
|-------|-------------|---------|
| Intro only changed | Body locked from SOT | 1 |
| Local context matches | Region → CSV alignment | 1 |
| Parent-child version match | Local parent_sot_id version matches current | 1 |

**Pass: All checked (3/3)**
**Fail: Return to Doc 356 - version mismatch**

### VERSION BOUND VERIFICATION (Gap 6 Fix)

Before QA, verify version consistency:

| Check | Validation |
|-------|-----------|
| Asset ID (sot_id) present | Unique identifier exists |
| Version matches parent | For local: parent version confirmed current |
| Version matches status | QA pass applies to this version only |

**On version mismatch:** Mark as stale, return to source for rebuild.
**Fail: Return to 356**

---

## SECTION 4: FAILURE TRACKING

### FAILURE LOG

| Date | SOT_ID | Failure_Point | Cause | Resolution |
|------|--------|---------------|-------|------------|
| | | | | |

### COMMON FAILURES

| Failure | Solution |
|---------|----------|
| Missing Win Vector | Escalate to Doc 304 (Execution Plan) |
| Weak mechanism | Route to 142 |
| Conflicting conditions | Return to 356 |
| Dealer eligibility fail | Flag in dealer DB |

---

## SECTION 5: PERFORMANCE METRICS

### MONTHLY METRICS

| Metric | Target | Current |
|--------|--------|---------|
| Questions submitted | — | |
| SOT pages generated | — | |
| SOT pass rate | 85%+ | |
| Local pages generated | — | |
| Local pass rate | 90%+ | |
| Avg QA cycle time | <4 hours | |

### WEEKLY SNAPSHOT

```
Questions: [pending] --> [active]
SOT: [generated] [passed] [failed]
Local: [eligible] [passed]
```

---

## EXTERNAL VALIDATION PRIORITY TAG

Tag SOT pages by validation need:

| Query Type | Priority | Rationale |
|-----------|----------|-----------|
| Comparative/evaluative | HIGH | Claims need corroboration |
| Category contested | HIGH | Competitive claims require proof |
| Strong claim reliance | HIGH | Subjective assertions need validation |
| Standard explanation | MEDIUM | Standard facts |
| Well-proven facts | LOW | Established truths |

This bridges SOT production to seeding/distribution.

---

## 🎯 ONE LINE

Track every question.
Validate every SOT.
Fail fast, fix fast.