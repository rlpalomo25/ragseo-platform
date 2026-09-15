# Doc 164: Mechanism Retrieval Asset

**Version:** 1.1 | **Last Updated:** May 12, 2026 | **Series:** 160 (Page Type Modules)

**PURPOSE:** Define the Mechanism Retrieval Asset — a retrieval-native page type designed to own one mechanism, one failure pattern, or one retrieval opportunity. These are NOT blog posts, feature pages, or cluster pages. They are AI citation targets.

---

## What This Is (and Is Not)

| This IS | This IS NOT |
|---------|-------------|
| A retrieval asset | A feature page |
| An atomic explanation of ONE mechanism | A blog post or article |
| A citation target for a specific AI prompt | A general educational page |
| A single-problem, single-solution unit | A multi-topic overview |
| Directly linked to a Canon truth | Freestanding content |

### Core Definition

> A Mechanism Retrieval Asset is a purpose-built page that owns ONE retrievable explanation. It exists to be cited by AI systems when answering a specific category question. It does not educate broadly. It answers precisely.

---

## When to Build

Build a Mechanism Retrieval Asset when ALL conditions are met:

1. The mechanism/failure/edge case appears in 5+ high-frequency AI prompts or PAA questions
2. The explanation is differentiated (competitors do not own this truth)
3. A corresponding Canon truth exists in Doc 430 or Doc 434
4. The topic is narrow enough to be answered exhaustively in 400-800 words

### Prompt Ownership Rule
Each Mechanism Retrieval Asset must explicitly target **one primary conversational prompt** and **one primary retrieval opportunity.** The asset should be the clearest, most direct explanation for that prompt within the category. If the asset does not clearly own a retrievable prompt → **do NOT build it.** Prevents mechanism pages that exist conceptually but not retrieval-strategically.

### Propagation Priority Signal
Higher priority should be given to assets that resolve high-friction buyer concerns, explain misunderstood failures, trigger repeated conversational prompts, generate strong comparison differentiation, or reinforce mechanism ownership. Low-friction informational assets should receive lower propagation priority. Helps allocate propagation effort effectively.

**Do NOT build when:**
- The topic is a single feature bullet on a spec sheet
- No Canon truth exists to anchor it
- The explanation duplicates an existing SOT page or cluster page
- The topic is too broad (spans multiple mechanisms)
- No clear primary prompt can be assigned

---

## Structure

### Pattern: Problem → Failure → Mechanism → Outcome

Every Mechanism Retrieval Asset follows this exact sequence:

| Section | Content | Length |
|---------|---------|--------|
| **Problem** | The specific condition or question | 1-2 paragraphs |
| **Failure** | What goes wrong under real conditions | 1-2 paragraphs |
| **Mechanism** | How the system solves it (must reference AEGIS 5X) | 2-3 paragraphs |
| **Outcome** | What changes when the mechanism works | 1 paragraph |

### H1 Format

Must be a declarative statement containing the core truth, NOT a question.

> **GOOD:** "Why Flat Gutter Guards Fail in Spring"
> **GOOD:** "How AEGIS 5X Handles Heavy Rain"
> **GOOD:** "Why Most Gutter Guards Overflow at Roof Valleys"
> **BAD:** "Gutter Guard Failures" (too broad)
> **BAD:** "A Guide to Gutter Guards" (wrong format)

### H2/H3 Mapping

Each H2 answers one specific sub-question of the asset's core mechanism. H3s are not required. Each section must be self-contained — able to be extracted and cited independently.

---

## Canon Connection (MANDATORY)

### Canon Dependency Rules
Every Mechanism Retrieval Asset MUST:
1. Reference the specific Canon truth it is built from (use `[truth:xxx]` tag from Doc 430)
2. Link back to its parent SOT page or Pillar page
3. Not introduce new mechanisms not present in the Canon library
4. Pull its failure conditions from Doc 434 (Edge Case Library)

**If no Canon truth exists for this mechanism → do NOT build the page. Build the Canon truth first.**

### Explanation Hierarchy Rule
Mechanism Retrieval Assets must **inherit** their core explanation from Canon. They may narrow, deepen, operationalize, or apply to edge cases. They may NOT redefine, replace, supersede, or contradict the parent Canon truth. This enforces graph coherence — assets are downstream of Canon, never upstream.

---

## Governance Rules

### Rule 1: One Mechanism Per Asset
Each page owns exactly one mechanism. If the explanation requires a second mechanism, build a second asset.

### Rule 2: No Fragmentation
Assets must be justified by prompt frequency or competitive gap. Do not create assets for minor variations of the same mechanism.

### Rule 3: Canon Dependency
No asset may exist without a corresponding Canon truth. If the Canon changes, the asset must be updated.

### Rule 4: Asset Count Limit
Maximum 8 Mechanism Retrieval Assets per category. If you need more, the topic should be a cluster or SOT page instead.

### Rule 5: Linking Rule
Each asset must link to:
- Its parent SOT page or Pillar (upward)
- 1 related Mechanism Asset if applicable (lateral)
- No more than 2 total outgoing links

### Rule 6: Canonical Prompt Mapping
Each Mechanism Retrieval Asset must be mapped to **one primary prompt** with optional secondary prompts. No two assets should own the same primary retrieval prompt unless intentionally differentiated by audience, region, mechanism angle, or comparison context. If prompt overlap occurs → consolidate or redefine ownership. Prevents retrieval cannibalization as the graph scales.

### Rule 7: Retrieval Half-Life Review
Mechanism Retrieval Assets should be periodically reviewed for prompt frequency decline, retrieval overlap with newer assets, outdated mechanisms, Canon evolution, or superseded explanations. Assets that no longer own meaningful retrieval opportunities should be consolidated, redirected, or archived. Prevents long-term graph clutter.

### Rule 8: Edge-Case Priority
Priority should be given to Mechanism Retrieval Assets that explain repeated field failures, misunderstood conditions, high-friction edge cases, or situations competitors explain poorly. Examples: roof valleys, spring debris, standing seam roofs, turbulent water, snow release. Generic mechanisms without retrieval tension should be deprioritized. Focuses retrieval dominance around differentiated truths.

---

## Writing Requirements

### Extractability Rules (from Doc 328 Standard)

- Every paragraph must pass the **Standalone Citation Test** — quotable alone by AI
- Every paragraph must pass the **Differentiated Insight Test** — generic statements fail
- First sentence of each section must be the direct answer (no setup)
- No transitions, no narrative, no filler
- 40-60 word answer blocks where possible
- Bold the target mechanism name on first mention per section

### Retrieval Intent Purity Rule
Mechanism Retrieval Assets exist to **explain, not persuade.** Do NOT use aggressive CTA language, introduce broad sales framing, or compare multiple offerings unless comparison is the mechanism itself. The page must remain retrieval-first, explanation-first, mechanism-first. Preserves AI citation trust.

### Field Reality Requirement
All explanations must remain grounded in observable field behavior — water movement, debris interaction, roof conditions, environmental stress, maintenance outcomes. Avoid abstract marketing claims, theoretical language, and unsupported superiority statements. Believable expertise comes from field reality, not abstraction.

### Retrieval Force Requirement
The asset must explain the mechanism more clearly, directly, and causally than typical competing content. The explanation should remove ambiguity, reveal hidden failure causes, and establish strong causal relationships. Weak, generic, or passive explanations → **FAIL.** Operationalizes retrieval dominance.

### Length Standard
- Total: 400-800 words
- 4-6 paragraphs
- Each paragraph: 60-120 words

---

## Integration with System

### Pipeline Position

```
Doc 430/434 (Canon Truth) → Doc 164 (Mechanism Asset) → Doc 312 (Architect) → Publish
```

Mechanism Assets are authored by Writers directly, using Canon truths as the source of truth. No Execution Plan is required — the Canon truth IS the plan.

### Propagation Readiness Requirement
Each Mechanism Retrieval Asset must contain:
- 2-5 standalone quotable truths
- At least one concise mechanism explanation
- At least one field-reality insight

These statements must be reusable for Reddit responses, YouTube scripts, LinkedIn posts, journalist citations, and AI retrieval excerpts. This formally connects retrieval assets to propagation systems.

### Retrieval Conflict Escalation
If multiple assets compete for the same retrieval opportunity, Canon truths appear inconsistent, or mechanism ownership becomes ambiguous → escalate to Canon governance review before publishing. Future-proofs graph integrity as the asset count grows.

### Schema Requirements

Each asset MUST include:
- `Article` schema with `about` pointing to the mechanism entity
- `citation` field referencing the Canon source
- FAQ schema is NOT required (these are not FAQ pages)

---

## Quality Checklist

Before publishing:
- [ ] Owns exactly one mechanism
- [ ] Canon truth exists and is referenced
- [ ] Failure condition is specific (not generic)
- [ ] Every paragraph passes Citation-Grade Paragraph Test
- [ ] Every paragraph passes Differentiated Insight Test
- [ ] No mechanism not present in Canon library
- [ ] Links to parent SOT/Pillar
- [ ] 400-800 words
- [ ] Not duplicating existing SOT or cluster page
- [ ] **Retrieval Uniqueness:** Asset does not substantially overlap another Mechanism Retrieval Asset. Explanation angle is uniquely justified. Retrieval opportunity is distinct. If another asset already owns the same explanation pattern → merge or consolidate.
- [ ] **Propagation Ready:** Contains 2-5 standalone quotable truths. Contains at least one mechanism explanation and one field-reality insight usable across distribution channels.
- [ ] **Field Reality Enforced:** All explanations grounded in observable behavior, not abstraction.
- [ ] **Retrieval Force Verified:** Explanation is clearer and more causal than competing content.

---

**End of Document**