# Doc 356 - Local Generation & Context System

**Version:** 1.3 | **Last Updated:** April 28, 2026

---

## Purpose

Control when and how local SOT pages are generated using dealer data, product validation, and region-based condition + context selection.

---

## OWNERSHIP RULE

**Doc 356 is the only eligibility authority in the local branch.**
Doc 357 validates completeness of Doc 356's output - it does NOT re-decide eligibility.

---

## Pipeline Position

```
Doc 358 (Entity Check) → Doc 356 (Eligibility Gate) → Doc 355 (Local SOT) → Local Pages
```

**Pulls From:**
- Dealer database (Google Sheets)
- local_data/weather.csv
- local_data/trees.csv
- local_data/house_styles.csv
- local_data/roofing.csv

**Pushes To:**
- Doc 355 (Local SOT Agent) - eligibility decision passed
- Dealer database - flag rows that fail eligibility

---

## 🔥 CORE PRINCIPLE

Local pages are NOT generated freely.

They require:
- Valid dealer
- Correct product
- Controlled, realistic local context

---

## SECTION 1: LOCAL ELIGIBILITY LOGIC (HARD GATE)

### RULE

A local page is created ONLY if BOTH conditions are met:

**CONDITION 1: DEALER EXISTS**
- Column D (Dealer) is NOT blank

**CONDITION 2: PRODUCT MATCHES DATABASE**

| Database | Product Value |
|----------|-------------|
| MasterShield | "MasterShield" |
| Klean Gutter | "Klean Gutter" |

### BOOLEAN LOGIC

```
IF Dealer ≠ blank AND Product = MasterShield → Generate MasterShield local page
IF Dealer ≠ blank AND Product = Klean Gutter → Generate Klean Gutter local page
```

### FAIL-SAFE RULE

IF Dealer exists BUT product does NOT match database → SKIP and FLAG row

---

## SECTION 2: REQUIRED DATA STRUCTURE

### DATABASE COLUMNS

| Column | Content |
|--------|---------|
| Column C | DMA (City / Area) |
| Column D | Dealer |
| Column G | Main Product |
| Column H | Region (SOURCE OF TRUTH) |

### REGION VALUES (STANDARDIZED)

- Northeast
- Southeast
- Midwest
- Southwest
- Mountain
- Pacific Northwest
- West Coast

---

## SECTION 3: LOCAL CONTEXT ENGINE

### STEP 1: LOCATION INPUT

From dealer database:
- DMA → city
- Region (Column H) → climate filter

### STEP 2: REGION FILTER (MANDATORY)

Filter ALL CSV datasets by Region before selection:
- weather conditions
- tree types
- roof types
- house types

### STEP 3: COMPATIBILITY RULE (CRITICAL)

Do NOT mix conflicting condition types:

**INVALID COMBINATIONS:**
- humidity + snow/ice
- desert + moss/algae
- tropical + freezing conditions

**VALID CLUSTERS:**

Each intro must stay within ONE cluster:
- wet / humid
- cold / snow
- dry / arid

### STEP 4: CONDITION + CONTEXT SELECTION

**REQUIRED (SELECT 1–2):**
1. Primary condition (weather or environment)
2. Optional supporting condition

**OPTIONAL (SELECT MAX 1):**
- Roof type OR house type

**USAGE RULES:**
- Conditions drive realism
- Context adds specificity
- Do NOT overload

**EXAMPLES:**

Charlotte (Southeast):
> "In Charlotte, where heavy rain and tree debris are common around large suburban rooflines…"

Denver (Mountain):
> "In Denver, where snow and rapid melt put pressure on steeper rooflines…"

Seattle (Pacific Northwest):
> "In Seattle, where constant moisture leads to moss buildup on shaded roofs…"

### HARD RULES

- Max 2 conditions
- Max 1 context detail
- Context never leads the sentence
- Context must match region

---

## SECTION 4: ROTATION (ANTI-REPETITION)

### RULE

Avoid repeating the same condition + context combination for the same DMA.

### IMPLEMENTATION

This must be handled OUTSIDE the LLM.

### EXTERNAL TRACKING TABLE

| DMA | Condition 1 | Condition 2 | Context |
|-----|-------------|--------------|---------|

### LOGIC

Before generating:
1. Check previous combination
2. Select a different valid combination

### FALLBACK (IF NO TRACKING)

Prefer unused combinations when possible.

---

## SECTION 5: LOCAL INSERTION RULE

### MODIFY ONLY THE INTRO

Local adaptation applies ONLY to Section 1 (Opening):

**FORMAT:**
> "In [City], where [condition 1] and [condition 2] are common…"
> "…around [roof/house context]"

### DO NOT

- Modify SOT answers
- Modify headings
- Insert local details into body

---

## SECTION 6: TRANSFORMATION ORDER (MANDATORY)

Apply in this exact order:

1. Base SOT
2. Product Insert (MS or KG)
3. Local Intro Injection

### DO NOT

- Apply local before product
- Rewrite content during transformation
- Modify SOT structure

---

## SECTION 7: QUALITY CONTROL

### CHECKLIST

| Check | Requirement |
|-------|-------------|
| Eligibility | Dealer not blank + Product matches database |
| Location | DMA pulled correctly + Region (Column H) present |
| Conditions | 1–2 conditions selected + Region match confirmed |
| No conflicting conditions | |
| Context | Max 1 (roof OR house type) + Supporting detail only + Matches region |
| Content | Only intro modified + SOT body unchanged + Mechanism preserved |

---

## Parent-Child Dependency Rule (Gap 5 Fix) - OWNERSHIP: Doc 356

**Doc 356 OWNS stale detection and rebuild triggering.**

| Check | Action |
|-------|--------|
| Parent SOT version matches | Proceed with local generation |
| Parent SOT version stale | DO NOT PROCEED - flag for rebuild |
| Parent SOT not found | REJECT - cannot generate local without parent |

**Local page output includes:**
- parent_sot_id (from input)
- parent_version (must match)
- local_status: fresh|stale|rebuild_needed

**Stale trigger:** If parent SOT increments version, existing local pages marked stale.

**On rebuild:** Regenerate local page against current parent version.

**Ownership Summary:**
- Doc 354: Signals version changes, outputs version fields
- Doc 356: ENFORCES version check at eligibility gate (this doc)
- Doc 355: Passive - receives version from Doc 356, no independent check

---

## 🎯 FINAL MODEL

You are not generating new content.

You are:
- Anchoring a fixed SOT in a controlled, believable local environment

---

## ⚡ ONE LINE

Conditions make it real.
Context makes it believable.
Control keeps it consistent.