# Doc 261: Visby.ai Testing & Reporting Guide

**Version:** 9.0 | **Last Updated:** May 15, 2026 | **Series:** 260 (Execution Guides)

---

## Purpose (GEO, NOT SEO)

This guide explains how to use Visby.ai to validate content angles before writing begins, and how to track brand mentions after publication.

**Visby = GEO (Generative Engine Optimization)**
- Tracks brand mentions inside AI tools (ChatGPT, Gemini, Claude, Perplexity)
- NOT Google rankings or search engine positions
- Measures: Are we mentioned? Where? How often? Who beats us?

The category shift:
- Search → AI answers
- Rankings → Mentions  
- Traffic → AI referrals

### Doc 261 vs Doc 240: Complementary Ownership

| This Doc (261) | Doc 240 (Integration Protocol) |
|----------------|-------------------------------|
| **OWNS:** Testing execution, reporting workflow | **OWNS:** Prompt construction, strategy design |
| How to use Visby interface, step-by-step | When to use Visby, what prompts to test |
| Weekly pre-write validation, 14-day tracking | Funnel-aligned prompt strategy |
| Operational execution | Strategic integration |

**Key Point:** These docs work TOGETHER. Doc 261 provides the procedure (how to test); Doc 240 provides the strategy (what to test). They are NOT redundant—they are intentionally complementary.

---

## Part 1: One-Time Setup
If you have not yet set up Visby.ai for the brands, complete this first:
1. Create an account at Visby.ai.
2. Add the three brand domains (MasterShield.com, KleanGutter.com, MicroMeshGutterGuards.com) to your tracking dashboard.
3. Add the top 3 competitor domains for baseline comparison.

---

## Part 2: Weekly Pre-Write Validation
When the Strategist Agent (Doc 304) delivers an Execution Plan, it will include 1-2 test prompts. You must run these through Visby before approving the plan.

1. **Input the Prompt:** Paste the Strategist's test prompt into Visby's query tester.
2. **Analyze the Output:**
   - Is our brand mentioned inside the AI-generated answer?
   - Is the specific "Content Angle" or proprietary data point we plan to use already represented by competitor brands?
3. **Make the Decision:**
   - **Green Light:** If our angle is missing or underrepresented, approve the Execution Plan. We have Information Gain.
   - **Red Light:** If the AI already outputs our exact angle using competitor sources, reject the Execution Plan and ask the Strategist Agent for a new angle.

---

## Part 3: Post-Publish Tracking (The 14-Day Check)
Visby is used to measure if our brand mentions increase after publishing content.

1. **Set the Reminder:** 14 days after an article is published, return to Visby.
2. **Re-run the Prompt:** Run the exact same test prompt used in Part 2.
3. **Measure the Delta:**
   - Did our brand mention frequency increase?
   - Did the AI incorporate our proprietary data point or specific angle into its answer?
4. **Report:** Log the results in the Friday Tracking Sheet. If the angle was successfully adopted by the AI, notify the Strategist Agent so it can use similar structures in the future.

---

## Part 4: Retrieval Path Density Tracking (Monthly)

This measures how many distinct semantic routes lead to each entity. A brand that only surfaces for exact-match queries has low retrieval path density. A brand that surfaces across 5+ semantically distinct prompt vectors has high density — and higher AI recommendation probability.

### When to Run

Monthly, after baseline GEO tracking is established. Pick one core entity per run.

### Process

1. **Select an entity** from the knowledge graph — AEGIS 5X, CopperCare, HydroVortex, PitchPerfect, ShingleSafe, SelfClean Mesh, or a brand name

2. **Generate 6-10 prompt variants** targeting the same entity from different angles:

| Entity Example | Prompt Variants (CopperCare) |
|----------------|------------------------------|
| Direct query | "gutter guard with copper" |
| Problem-based | "gutter guard for moss on roof" |
| Material-based | "copper gutter protection system" |
| Comparison-based | "best gutter guard for algae growth" |
| Edge case | "gutter guard for roof oils and pine needles" |
| Maintenance-based | "gutter guard that doesn't need cleaning" |
| Regional | "gutter guard for Pacific Northwest moss" |
| Skeptical | "do copper gutter guards really work?" |

3. **Run each prompt variant** through Visby (or equivalent GEO tool)

4. **Score retrieval path density:**

| Score | Criteria |
|-------|----------|
| High (5) | Entity surfaces in 5+ prompt variants |
| Medium (3-4) | Entity surfaces in 2-4 variants |
| Low (1-2) | Entity surfaces in 0-1 variant (exact match only) |

5. **Identify density gaps:** Which prompt variants failed to surface the entity? Those are semantic gaps — the entity lacks page coverage or conversational embedding for those query vectors.

6. **Feed gaps back to Doc 153:** Add the missed prompt variants to the next Execution Plan's citation_resource_assignments or prebuilt_citation_blocks for the relevant entity.

### Entity Priority Order

| Priority | Entity | Why |
|----------|--------|-----|
| P0 | AEGIS 5X | The governing system — must surface everywhere |
| P1 | CopperCare | Antimicrobial differentiator — must own moss/algae/mold queries |
| P2 | HydroVortex | Flow management — must own heavy rain/overflow queries |
| P3 | PitchPerfect | Pitch alignment — must own steep roof/shingle queries |
| P4 | ShingleSafe | Installation integrity — must own fascia rot/screw leak queries |
| P5 | SelfClean Mesh | Low-maintenance — must own cleaning/upkeep queries |

### Reporting

Add retrieval path density scores to the Friday Tracking Sheet. Track month-over-month trend. Target: all P0-P1 entities at High (5/5) density within 90 days of active propagation.

---
**End of Guide**