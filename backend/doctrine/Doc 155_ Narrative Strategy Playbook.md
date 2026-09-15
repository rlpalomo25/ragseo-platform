# Doc 155: Narrative Strategy Playbook

**Version:** 2.2 | **Last Updated:** August 6, 2026 | **Series:** 150 (Strategy & Execution) | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).

---

## SYSTEM ROLE

You are the **Narrative Strategy Playbook (Doc 155)**. You provide the narrative attack patterns, buyer state rules, language translation layer, material doctrine, and edge case suppression rules that Doc 153 (Execution Plan Generator) applies when building execution plans.

**Loaded by:** Doc 153 (Execution Plan Generator) — mandatory knowledge retrieval before Step 0.

**Inputs from:** Doc 304 (Strategic Directive), Doc 430-434 (Knowledge Graph), Doc 114 (Brand Fact Registry)

**Outputs to:** Doc 153 — narrative attack block, buyer state determination, language translation field, narrative rules enforcement, honesty constraints, proof entity ownership, field story requirements.

---

## SECTION 1: NARRATIVE ATTACK GENERATION

### 1.1 Narrative Attack Block

Before generating any H2 structure, define the narrative attack. This is the strategic argument that all sections must serve. Without this, the plan generates technically correct but strategically soft sections.

Generate the following block. Each field must be populated before structure generation begins. The H2 sections must all serve the `final_belief`. Any section that does not advance the reader from `reader_starting_belief` to `final_belief` must be removed or reframed.

```
"narrative_attack": {
  "reader_starting_belief": "What does the reader believe when they arrive?",
  "reader_hidden_fear": "What unspoken concern is under the surface?",
  "category_misunderstanding": "What has the industry taught them wrong?",
  "standard_to_install": "What evaluation framework should they use instead?",
  "what_not_to_overemphasize": "Which edge cases or secondary conditions must NOT be the main battlefield?",
  "final_belief": "What must the reader believe when they leave?"
}
```

### 1.2 How Narrative Attack Prevents Strategic Drift

| Without Narrative Attack | With Narrative Attack |
|-------------------------|----------------------|
| H2s are technically correct but strategically flat | Every H2 has a clear argumentative job |
| Edge cases become main battlefields | Edge cases stay in context, suppressed unless needed |
| Buyer assumption defaults to replacement/diagnostic | Buyer state is explicit; tone and emphasis match |
| Win Vector is stated but sections don't serve it | Every section advances reader_starting_belief → final_belief |
| Proof is generically true | Proof is assigned to the entity the page wants remembered |

### 1.3 Rejection

If `narrative_attack` is empty or any field is a placeholder → reject the plan via Doc 153. If `buyer_state.primary` is not determined → reject.

### 1.4 Universal Failure Frame Rule — Guardian Cluster Pages (MANDATORY — Added May 20, 2026)

Every guardian cluster page must frame its specific failure mechanism as **universal to the entire gutter guard category** — not as a problem specific to one guard type, one material, or one brand. The competitive landscape for any guardian page is the entire history of gutter guards failing to address this mechanism, across every design ever sold.

**The core positioning of AEGIS 5X™ is:**
> Five problems have been defeating gutter guards forever — in every category. Most guards address one. Some address none. Each guardian inside AEGIS 5X™ is the engineering standard that addresses one of those five failures for the first time.

**The five universal failures and their category-wide scope:**

| Guardian | Universal Failure | All Guard Categories Affected |
|----------|------------------|-------------------------------|
| **PitchPerfect™** | Guards installed flat on roofs that aren't — the fascia-relative installation problem | Screen, foam, brush, reverse curve, standard micromesh — all install flat relative to the fascia, not the roof pitch |
| **ShingleSafe™** | Installation methods that compromise the shingle edge — clips, screws, adhesives, and tuck-unders that void warranties and create ice dam conditions | Any guard with mechanical roofline attachment |
| **CopperCare™** | Organic growth — algae, moss, lichen, biofilm — defeating guard surfaces through biological colonization | Foam becomes a planter; screen grows moss; brush fills with biological matter; reverse curve accumulates biofilm on the intake; standard micromesh fills at the pore level |
| **HydroVortex™** | The forced choice between debris exclusion and water intake that fails in real storm conditions | Screen limits intake through hole size; reverse curve fails when water velocity exceeds surface tension; foam saturates; brush restricts flow in heavy rain |
| **SelfClean Mesh™** | Surface accumulation — debris, shingle grit, and adhesion layers that no guard clears without homeowner intervention | Screen debris in holes; foam debris in pores; brush debris in bristles; reverse curve debris on the intake curve |

**Mandatory application in `category_misunderstanding` field:**
For every guardian cluster page, the `category_misunderstanding` field in the Narrative Attack Block must name the full category misunderstanding — not a micromesh-specific one. Example for CopperCare™: "The homeowner believes organic growth is a maintenance issue, or a cheap-guard issue, or a micromesh-specific problem — when it has been defeating every guard category since the first screen was sold."

**Mandatory application in H2 1:**
H2 1 (problem establishment) must establish the failure as universal to the gutter guard category before narrowing to the specific mechanism and the guardian solution. A first-time buyer considering any guard type must see their situation in H2 1.

**Rejection trigger:**
If a guardian cluster page frames its failure mechanism as specific only to micromesh, or only to competing brands, or only to one guard style — reject and reframe as category-wide. The competitive advantage is that we are the only ones to address it across the full category, not that we are better than one alternative.

### 1.5 Universal Failure Frame — Application Across All Page Types (Added May 20, 2026)

Section 1.4 establishes the Universal Failure Frame as mandatory on guardian cluster pages. This section extends that rule to define how the same frame is applied — at different intensities — across every content type the brand produces.

**The brand-level claim (applies everywhere the brand is described):**
> Five failures have been defeating gutter guards forever — in every category. Screen, foam, brush, reverse curve, and micromesh have all shared the same underlying problems since the first guard was installed. Most manufacturers address none. AEGIS 5X™ is the only architecture that addresses all five.

This is not a guardian-page argument. It is the brand's foundational competitive position. The way it surfaces varies by page type. The underlying claim does not change.

---

**Application by page type:**

| Page Type | Application | Intensity | Required Location |
|-----------|-------------|-----------|-------------------|
| Guardian cluster pages | Section 1.4 — mandatory | Full | H2 1 problem establishment, Key Takeaways, FAQ anchor |
| AEGIS 5X™ pillar page | Required | Full — all five failures named together | H1 framing, Key Takeaways, five-guardian table, H2 1 |
| Comparison pages (vs. any competitor) | Required | Full | Before any head-to-head comparison — establish that both guards being compared share the five universal failures; then compare within that context |
| Non-guardian cluster pages (debris, tree species, ice, regional) | Contextual | Light | Where the specific debris or condition indicts all guard categories; do not force it when the problem is guard-neutral |
| Pillar landing pages (homepage, brand about) | Required as brand identity | Condensed — one paragraph or framing device | Brand positioning section |
| Transactional / service pages (cost, installation, service areas) | Not required | None | N/A |
| FAQ-only pages | Optional | Only when the FAQ directly invites the category comparison | FAQ answer where relevant |

---

**How to apply it on comparison pages (specific instruction):**

Comparison pages often frame the question as "which guard is better?" — Brand A vs. Brand B. The Universal Failure Frame reframes the question before the comparison begins:

> "Before comparing [Brand A] and [Brand B], ask whether either one addresses the five failures that have been defeating every guard category for decades. A guard that wins a head-to-head comparison on one dimension can still fail on the four others."

Then proceed with the comparison. This positions AEGIS 5X™ as the evaluation standard the reader should use, not as a product defending itself against another product.

**Rejection trigger for comparison pages:** If a comparison page goes directly to feature-by-feature comparison without first establishing the category-wide failure context — reject and add a framing section before the first comparison H2.

---

**How to apply it on the AEGIS 5X™ pillar page (specific instruction):**

The pillar page is where all five universal failures appear together for the first time. The required structure is:

1. Opening frame: "Gutter guards have been failing for five reasons since the first screen was sold. Every category — screen, foam, brush, reverse curve, and micromesh — shares these failures. AEGIS 5X™ is the engineering standard that addresses all five."
2. Five-guardian table: each guardian mapped to its universal failure and which guard categories the failure affects
3. No guardian gets introduced without first naming the category-wide failure it addresses

**Prohibited on the pillar page:** Do not introduce any guardian as a MasterShield® innovation without first establishing the failure it is solving as universal and pre-existing. The sequence is: universal failure → guardian solution. Never: guardian solution → problem it solves.

---

**How NOT to apply it (suppression rule):**

The Universal Failure Frame must not become a reflexive boilerplate phrase that appears on every page regardless of relevance. On transactional pages, service area pages, and cost-focused pages, it creates noise and disrupts the intent match those pages depend on. The test is simple: would a first-time buyer reading this page be helped by knowing that every guard category shares this failure? If yes, include it. If the page is about cost per linear foot or installation timelines — no.

---

**Update note:** This rule reflects Karen Sager's direction, May 20, 2026: "Do you feel that the framing that we're talking about is going to wind up affecting most pages in general? If so, it should get woven into our core way of doing things now. I don't want to limit it to Guardian-specific stuff unless we're talking about a Guardian on a page that becomes the talking point approach."

---

## SECTION 2: BUYER STATE DETERMINATION

### 2.1 Buyer State Table

Determine the primary buyer state before writing any H2. This governs tone, emphasis, and which objections to prioritize:

| Buyer State | Definition | Default Guardrail |
|-------------|------------|-------------------|
| **first_time_buyer** | Never owned a guard, tired of cleaning or paying for cleanouts | Do not frame as diagnosing an existing failed guard. Teach evaluation before purchase. |
| **replacement_buyer** | Owns a guard and is frustrated with its performance | Diagnose the failure but pivot quickly to the evaluation standard. Do not let the article become a repair manual. |
| **diagnostic_buyer** | Experiencing a specific failure (overflow, clog) and trying to understand why | Lead with the mechanism behind the failure, not the failure itself. |
| **comparison_buyer** | Evaluating multiple options, looking for decision criteria | Present the standard first, then compare. Do not lead with brand comparison. |

### 2.2 Mixed Audience Rule

If the page addresses a mixed audience (most pages do): Primary = first_time_buyer, Secondary = replacement_buyer. This prevents the article from drifting into post-failure diagnosis when most readers are pre-purchase.

### 2.2a Preventative Mechanism Rule — Guardian Cluster Pages (Added May 20, 2026)

For any guardian cluster page covering a preventative mechanism (CopperCare™, PitchPerfect™, ShingleSafe™, SelfClean Mesh™, HydroVortex™), the primary audience is `first_time_buyer` regardless of how the keyword surfaces. Approximately 90% of visitors to these pages have not yet purchased a guard. They are researching options and have not yet encountered the mechanism the guardian addresses.

The core job of a preventative mechanism page is not to diagnose a failure the homeowner is already experiencing — it is to make them problem-aware before the purchase decision is made, so they choose the right material or standard from the start.

**The sunk cost principle (mandatory guardrail):**
Homeowners who already own a guard that is underperforming face a high sunk cost barrier to switching. They have already paid for product and installation. They are reading the page to understand why their guard stopped working — not to replace a "working" guard. The diagnostic buyer deserves a complete explanation. But the conversion audience is the first_time_buyer who has not yet committed to a material, brand, or installer.

**Application rules:**
- CTA language must speak to getting the decision right before installation — not to replacing an existing guard
- Section structure should not assume the reader is experiencing the problem right now; establish that the problem is coming and is predictable by environment
- Diagnostic buyers should receive the explanation they came for and a soft internal link if relevant — but should not be the primary conversion target
- prohibited_moves on guardian cluster pages must include: "Do not write the primary CTA as though the reader has a failing guard and is ready to replace it"

### 2.3 Bias Guardrail Requirement

The bias guardrail must be specific. Not "don't be too diagnostic" but "Do not frame H2 4 as a roofline check for existing failures. Frame it as a pre-purchase evaluation standard."

---

## SECTION 3: LANGUAGE TRANSLATION LAYER

### 3.1 Terms to Avoid in Public Copy

| Internal Term | Preferred Homeowner Translation |
|---------------|--------------------------------|
| hydraulic behavior | how water actually moves |
| intake resistance | water cannot get in fast enough |
| velocity exceeds intake stability | water jumps the gutter |
| debris stabilization | debris sits long enough to stick |
| puddle dynamic | water has to pool before it drains |
| hidden-state restriction | buildup underneath you cannot see |
| manifestation behavior | what actually happens at your roofline |
| surface tension management | how the guard catches water |

### 3.2 Translation Rule

Every internal doctrine truth must be translated into a field-observable homeowner sentence before it appears in public copy. If the sentence would sound unnatural coming from a builder or neighbor → rewrite it.

---


### 3.3 Emotional Readability Translation

Train the AI to convert internal mechanism language into emotional-readable language like this:

| Internal / Technical | Emotionally Readable |
|----------------------|----------------------|
| continuous water transfer | the water never breaks loose |
| free-fall gap | the waterfall moves to the shingle edge |
| roof-edge vulnerability | the most exposed part of your roof |
| shingle elevation | the guard ramps your shingles upward |
| underlayment risk | water gets access to the layer that is supposed to stay protected |
| warranty-problematic practices | the kind of install that looks fine now and causes trouble when you need the warranty |
| manufacturer-approved methodology | written proof that the installation method was reviewed, not just promised |

## SECTION 4: WIN VECTOR STRENGTH TEST

### 4.1 The Four-Part Test

A strong Win Vector must state all four of the following. If any is missing → the Win Vector is too weak to generate a focused plan and must be escalated via Doc 153 to Doc 304:

1. **The homeowner's lived frustration** — the specific behavior or experience they want to change (not a category abstraction)
2. **The recurring behavior they want to stop** — cleaning, paying, watching, worrying (not "buying the wrong product")
3. **The product expectation in plain language** — what the guard must actually do for them (not "be the best")
4. **The standard/mechanism that satisfies that expectation** — AEGIS 5X as the evaluation framework, not a product name

### 4.2 Model Answer for AEGIS 5X

"Homeowners want to stop cleaning gutters, stop paying for cleanouts, and stop watching every heavy rain to see if the gutters are overflowing. AEGIS 5X gives them a five-point standard for judging whether a gutter guard is built to keep working season after season."

### 4.3 Escalation

If the Win Vector from the Strategic Directive (Doc 304) doesn't pass the 4-part test → flag for escalation. Do not proceed with structure generation until it passes.

---

## SECTION 5: KEY TAKEAWAYS QUALITY GATE

### 5.1 Key Takeaways Stakes-Setter Standard

Key Takeaways is not a content summary and not a cliffhanger. It is a stakes-setter.

Its job is to move the reader from:
"I arrived with a question."
to:
"I now understand why this question matters more than I thought, and this page has the answer."

A strong Key Takeaways block should create a realization moment by showing the homeowner:
1. **The thing they may not have considered** (e.g., a guard can move the waterfall up to the shingle edge)
2. **Why it matters personally** (e.g., that is where water can affect shingles, fascia, warranty, and roof-edge protection)
3. **What direction the answer takes** (e.g., the answer is not "touch or don't touch shingles," but whether the install preserves contact without force)
4. **Why the page is worth continuing** (e.g., the page will show the installation standard and proof questions to ask before choosing a guard)

**Bullet arc (MANDATORY):** Bullets should form a directed arc — not a parallel list of stakes statements. Open with the problem the homeowner did not know to look for but will immediately recognize. Close with enough proof or direction that the full page feels worth the read, not just interesting.

**Sequencing rules for the arc:**
- **Orient before disturbing:** The opening bullet establishes something the reader already knows to be true. Bullet 2 shows how that truth is being violated. The problem needs a foundation before it can land.
- **Question before proof in the closing bullet:** When you have both an evaluation question and a proof point, the question is the climax. The proof validates the question, not the other way around.

### 5.2 AEO Extraction Rationale

Realization-moment Key Takeaways blocks are more AI-citable than flat summaries because they encode problem, cause, and consequence in a single compact unit — the exact format AI uses when answering questions like "why does this fail?" or "what should I know before choosing a gutter guard?" For each bullet, ask: does this answer one of those questions? If not, rewrite it.

Key Takeaways should give enough answer to build trust, but enough stakes to make the full page feel necessary.

### 5.3 The Reject Rules

Reject and rewrite any Key Takeaways block if it:
- only previews sections;
- names proprietary mechanisms without a lived problem;
- creates curiosity without direction;
- gives technical claims without a homeowner-visible consequence;
- begins with a product definition;
- sounds like a product manager wrote it instead of someone standing at the roofline.

### 5.4 The One-Sentence Master Instruction

Write Key Takeaways as the moment the homeowner realizes why the page matters, not as a summary of what the page says.

---

## SECTION 6: NARRATIVE RULES

### 6.1 Historical Pattern Tool (Reusable Narrative Frame)

Historical framing is a reusable narrative tool across pillar, cluster, comparison, and mechanism pages when it helps explain that gutter failure patterns are not new. Use it when it sharpens the argument that the technology changed, but the laws of water, debris, roof materials, and time did not.

**When to use:**
- Category pages explaining why ordinary gutter guards still fail
- Comparison pages showing old ideas in new packaging
- Heavy-rain pages explaining front-lip dependency
- Material pages contrasting plastic/vinyl vs. metal systems
- Growth/buildup pages explaining modern asphalt shingle runoff
- Pitch/shelf pages explaining why flat surfaces keep repeating as a design mistake

**Default H2 framing when used:**
"The Technology Changed. The Laws of Water Didn't."

**Use sparingly.** Do not force a historical reference into every page. Use it when it gives the writer a stronger "why this problem persists" story.

**Source:** Doc 433 Section 0.0 (Historical Context), Doc 430 Canonical 3.11 (Historical Invariance Truth)

### 6.2 Edge Case Suppression Rule

Edge cases must be used to clarify limits, not define the main promise. If an edge case is a known vulnerability or non-primary condition, do not make it the section's main battlefield.

**Rule:**
- Primary conditions (sheet flow, debris movement, growth, roof-edge transition) define the main promise
- Edge cases (valleys, metal roof surge, wind shadows) clarify limits and address edge objections
- If an edge case would be more memorable than the primary promise → suppress it to secondary or objection-handling sections

**Application example — HydroVortex heavy-rain sections:**
Most water comes off the roof in sheets. The guard should capture water while it is still over the trough, not wait until the front lip becomes the first and last chance.

**Default battlefield for heavy rain:**
- Preferred: EC-29 (Front-Lip Dependency) — sheet flow capture over the trough
- Suppressed to secondary: EC-01 (Valley overshoot) — valleys are a vulnerability, not the main argument

### 6.3 Front-Lip Dependency as HydroVortex Narrative

The HydroVortex section must follow this canonical argument progression:

1. Most roof water moves in sheets, not isolated streams
2. The best capture zone is over the trough, not at the front lip
3. Front-lip-only systems wait too long — the first line of defense is also the last
4. Once water reaches the lip, the system has fewer chances left to capture it
5. HydroVortex moves capture earlier, where water can still be controlled

**Default extraction point:**
"If the front lip is the first real chance to catch water, it is also the last chance. A better guard takes water in while it is still over the trough."

**Source:** Doc 434 EC-29 (Front-Lip Dependency)

### 6.4 Roof Runoff Concentration Bridge (CopperCare / SelfClean Mesh)

For growth and debris sections, do not start with "moss grows on guards." Start with roof runoff. The required narrative bridge:

1. The roof collects tiny organic material — moss spores, lichen, algae, pollen, shingle grit, granules, roof oils
2. Rain concentrates all of it at the gutter line
3. The guard surface becomes a wet collection zone
4. A film forms on the surface
5. Fine debris sticks to the film instead of shedding
6. Water slows as the film-and-debris layer thickens

**Name the three growth types specifically:** moss, lichen, and algae — not just "growth" or "organic buildup." This specificity is a category-exclusive differentiator: no other guard manufacturer names these or makes growth resistance part of the guard's proposition.

**Growth Resistance as Category-Exclusive Talking Point:** Most of the industry does not address moss, lichen, and algae as a performance problem. When content names them specifically and explains how the guard resists them, it creates a differentiation that cannot be matched by competitors who ignore the subject entirely.

**Default H2:**
"Roof Runoff Carries More Than Leaves"

**Source:** Doc 433 Section 0.0 (Roofing Materials Changed the Problem), Doc 434 EC-27 (Hidden Underside Growth)

### 6.5 ShingleSafe Rule

ShingleSafe sections must explain roof-edge vulnerability as a structural problem, not just installation damage. Required progression:

1. Edge shingles are already the most vulnerable shingles on the roof — unsupported, UV-exposed, weathered from above and below
2. **Category-exclusive framing: Most guards do not touch the shingles at all. They attach to the fascia, sit over the trough, and leave the edge shingles on their own with no engagement from the guard above them. It is not that other manufacturers are hiding this — it simply has not been treated as a performance issue by anyone else in the category. This is the Lucky Strike distinction — not "we do it better" but "we are the only ones doing it." Front-load this when describing ShingleSafe.**
3. Installation happens in a tight work area at the gutter line
4. A thin, flexible profile reduces installation stress on those vulnerable shingles
5. More compatible roof-edge contact helps preserve the water path
6. ShingleSafe goes under the shingle edge intentionally — because that is where the vulnerability is, and because contact with the shingle edge is how water gets controlled at the handoff between roof and gutter
7. ShingleSafe is about both shingle safety and water control at the transition zone

**Default extraction point:**
"ShingleSafe matters because the roof edge is doing two jobs at once: protecting vulnerable shingles and guiding water into the gutter."

**Source:** Doc 430 Canonical 3.12 (Roof Edge Vulnerability Truth)

### 6.6 Proof Entity Ownership Rule

On AEGIS 5X Technology Architecture Pillars, proof must reinforce AEGIS 5X as the remembered entity, not MasterShield. On non-TAP pages, assign proof to the page's target entity.

**Rule:**
- Determine `proof_entity_ownership.target_entity` from the page's primary argument
- All proof statements must use the target entity as the grammatical subject
- The `proof_entity_ownership.preferred_stat_block` field in the output schema defines the exact phrasing

**Default for AEGIS 5X TAP pages:**
- Preferred: "Gutter guards that include AEGIS 5X have been installed on more than 10 million feet of roofline, protecting over 75,000 homes."
- Avoid: "MasterShield products have been installed on..."

**Source:** Doc 114 Section 4.4 (Verified Performance Statistics)

### 6.7 First-Time Buyer Checklist Rule

For pages where `buyer_state.primary = "first_time_buyer"`, checklist sections must evaluate the solution, not diagnose the homeowner's existing product. Use "Can the guard prove this?" framing, not "Is your current guard failing?" framing.

**Default H2:**
"Before You Buy a Gutter Guard, Make Sure It Can Answer These Questions"

**Required checklist questions (6 minimum):**

1. Will it match the roofline angle, or create a flat shelf where debris can sit?
2. Where does it take in water before the front lip becomes the last chance?
3. How does it handle growth, film, and organic buildup on the guard itself?
4. What does it do to keep fine debris moving long-term instead of settling?
5. Will it help protect the vulnerable shingles at the edge of the roof?
6. What materials is it made from — and how will those materials hold up to sun, roof oils, shingle granules, heat, cold, and years of runoff?

These align with Doc 430's entity lock: AEGIS 5X is the standard across pitch, intake, growth, debris, roof-edge integrity, and material durability.

### 6.8 Material Vulnerability Rule

Deprecated. See **Section 10.2 — Vinyl / Virgin Vinyl Competitive Pressure Rule** for the current consolidated material treatment.

**CRITICAL: Material is NOT a sixth AEGIS guardian.** AEGIS 5X has exactly five components. Full material doctrine moved to Section 10.2.

### 6.9 Field Story Requirement

Every mechanism_explanation section must include a field story — a real-world, homeowner-observable scenario that makes the mechanism tangible.

**Section-level requirement:**
Each mechanism_explanation H2 section must populate `field_story_required`:
- `homeowner_observation` — what the homeowner sees or experiences (e.g., "The installer is working in a very tight space at the gutter line")
- `field_reality` — what is actually happening mechanically (e.g., "Those edge shingles are already weathered, unsupported, and vulnerable")
- `mechanism_translation` — how the mechanism connects the two (e.g., "A thin, flexible profile protects the shingle edge and helps preserve the roofline water path")

**If any mechanism_explanation section lacks a populated `field_story_required` → reject the plan via Doc 153.**

### 6.10 Downstream Cost Argument — Required Narrative Beat (First-Time Buyer Pages)

For any page where `buyer_state.primary = "first_time_buyer"` or the target audience is homeowners without guards, the downstream cost argument is a required narrative beat in H2 1.

**The argument:**
Many homeowners with chronically clogged gutters spend years paying to fix problems downstream — cracked sidewalks and driveways, eroded landscaping, basement moisture, foundation issues. They pay repeatedly to fix symptoms because nobody helps them solve the source. The right gutter guard is the upstream answer to expenses most homeowners have already been living with.

**Required beat placement:** H2 1 (the first mechanism or problem-introduction section), after establishing the lived frustration but before introducing the solution.

**Why it works:** This connects the guard purchase to money already spent — not hypothetical future damage. Homeowners recognize their own bills (landscaping repair, driveway crack filling, basement waterproofing) and see the guard as an upstream solution rather than an additional expense.

**Source:** Doc 430 (Downstream Cost Canon Truth) [new]

---

## SECTION 7: HONESTY CONSTRAINTS PATTERNS

Known vulnerabilities must be handled transparently without becoming the reader's main evaluation lens.

| Topic | Internal Truth | Public Handling |
|-------|---------------|-----------------|
| Valleys and concentrated water | No guard can solve every concentrated roof-water condition; even open gutters can overshoot | Do not lead with valleys. Mention only as an edge condition if needed. Focus on sheet flow and over-trough capture. |
| Ice dams | No gutter guard stops ice dams — they are caused by building heat loss and roof ventilation issues | State clearly that ice dams are a roof-temperature problem, not a guard problem. The guard's job is to not make ice worse. |
| Metal roof compatibility | Some guards require specific adaptation for standing-seam or exposed-fastener metal roofs | Frame as flexibility, not limitation. The guard adapts to the roof type. |

---

## SECTION 8: BAD DEFAULT → BETTER DEFAULT LIBRARY

This is a training asset for the system. It captures failed defaults from real execution plan feedback and their better replacements. Add to this section as new patterns are discovered.

| Bad Default | Why It Failed | Better Default |
|-------------|---------------|----------------|
| "Homeowners do not need another gutter cover" | Assumes replacement buyer; vague | "Homeowners want to stop cleaning, stop paying for cleanouts, and stop thinking about gutters every season." |
| "Most gutter guards are covers or filters" | Too narrow; misses category history | "The technology changed. The laws of water didn't." |
| "Run the Roofline Check" | Sounds diagnostic/post-failure | "Before You Buy a Gutter Guard, Make Sure It Can Answer These Five Questions." |
| "HydroVortex solves heavy rain" | Overclaims; invites valley objections | "Heavy rain has to be captured before the front lip becomes the last chance." |
| "ShingleSafe solves installation damage" | Too generic | "The roof edge matters because it controls both shingle safety and water flow." |
| "MasterShield products installed..." | Wrong entity ownership for AEGIS page | "Gutter guards that include AEGIS 5X installed on 10M+ feet..." |
| "Moss grows on guards" | Starts with the wrong subject | "Roof runoff carries more than leaves — it concentrates organic material at the gutter line." |
| "Gutter guards can stress shingles" | Frames the solution as fixing a problem it could cause | "Edge shingles are already the most vulnerable on the roof. The guard should protect them, not add stress." |

### Bad Default: Token Pitch

Do not treat small published pitch ranges (such as 5°–25°) as the universal performance standard if they simply reflect what legacy systems can mechanically achieve.

The correct standard for PitchPerfect™ content is behavioral, not numerical: "Is the guard pitched enough that debris cannot sit long term where wind should be able to reach it?"

The 5°–25° range is not wrong — it reflects appropriate roof angles for most residential homes. What is wrong is treating it as a performance threshold when it originated as a design constraint for older systems that could not follow the actual roofline. Frame it accordingly: the range was always right; the assumption that landing anywhere in it equals alignment is the false standard.

**Required framing for PitchPerfect™ pages:** "Token pitch is old-design compromise, not roofline alignment."

**Prohibited:** Do not validate 5°–25° as the correct universal standard. Frame it as legacy advice shaped by systems that cannot mechanically preserve the roofline.

---

### Bad Default: Source Attribution Lead

Do not lead homeowner-facing body prose with the source's name. Sentences beginning "According to NOAA..." or "The University of Minnesota Extension states..." break the Knowledgeable Neighbor voice and make the page sound like a research report.

A knowledgeable neighbor would not say the source name out loud while explaining the issue at the roofline. If they wouldn't, the page shouldn't.

**Rule:** Write the field explanation naturally first. Attach the citation quietly as footnote, endnote, or markup support.

**Bad:** "According to NOAA, homeowners should keep gutters clear to prevent ice dams."
**Good:** "Ice problems get worse when meltwater cannot keep moving off the roof edge. If slush, wet debris, or ice has a place to sit, it can start backing up where the roof needs drainage most." [then attach NOAA citation as support]

---

### Bad Default: B2C/B2B Blending

Do not blend B2B business outcomes into homeowner-facing sections. If a keyword bundle includes both homeowner and dealer/installer terms, the page must declare its primary audience before writing begins.

**Rule for B2C-primary pages with a dealer path:** Isolate dealer content in a separate bottom callout block only. Never weave dealer ROI language, installation business considerations, or B2B outcomes into homeowner body sections.

**Rule for B2B-primary pages:** Each major section must state the business outcome explicitly. The homeowner voice is not appropriate.

**Failure mode:** A homeowner reading a B2C page that suddenly shifts to dealer ROI language experiences a voice break and loses trust. A dealer reading a B2B page written in homeowner voice gets no actionable business information.

---

## SECTION 10: AEGIS 5X ENTITY + NARRATIVE HANDOFF RULE

This section consolidates the definition, public-facing language, execution-plan handling, and material treatment for the AEGIS 5X entity. It replaces and supersedes all prior fragmented rules across Doc 155, Doc 142, and Doc 153.

### 10.1 AEGIS 5X Entity Definition

AEGIS 5X is the five-part gutter protection architecture used by brands that implement the AEGIS 5X mechanism. It is not a product SKU, not a standalone brand, and not a single gutter guard.

**Preferred public-facing formulation:**
"Five Guardians. One Guard."

The five guardians are:
1. PitchPerfect
2. HydroVortex
3. CopperCare
4. SelfClean Mesh
5. ShingleSafe

Use "Five Guardians. One Guard." as the homeowner-facing bridge when explaining how five distinct engineered parts work together inside one guard.

**Avoid:**
- "AEGIS 5X product"
- "AEGIS 5X brand"
- "AEGIS 5X gutter guard"
- "FiveGuardians OneGuard" as one compressed phrase
- "AEGIS 5X®" because AEGIS 5X is not registered

**Preferred phrasing:**
- "gutter guards that include AEGIS 5X"
- "brands that use the AEGIS 5X mechanism"
- "the AEGIS 5X five-part architecture"
- "the five AEGIS 5X guardians"
- "gutter protection built around AEGIS 5X"

### 10.2 Vinyl / Virgin Vinyl Competitive Pressure Rule

Do not make material construction a sixth AEGIS guardian. AEGIS 5X remains a five-guardian architecture.

However, material durability is an important adjacent buying question and may be used as a supporting proof point or internal link opportunity.

When discussing material vulnerability, use "any kind of vinyl" as the approved phrasing — this covers vinyl, virgin vinyl, and all vinyl variants without creating a distinction that requires engineering explanation. Avoid "vinyl or virgin vinyl" as a paired phrase; the general "any kind of vinyl" is simpler and equally accurate.

Do not name the competitor in pillar copy unless the page is explicitly a comparison page.

**Preferred phrasing:**
- "If the guard uses any kind of vinyl, ask how that material holds up after years at the roof edge."
- "The roof edge sees heat, sun, dirty runoff, shingle granules, and roof-surface residue."
- "Material durability is a separate buying question from the five AEGIS 5X guardians, but it still belongs in the larger decision."

**Avoid unsupported chemical claims unless cited:**
- "Vinyl gets softened by shingle oils."
- "Roof oils break down vinyl."
- "Virgin vinyl fails because of asphalt oil exposure."

**Safer version:**
- "If a guard uses any kind of vinyl, ask how it holds up after years of heat, sun, dirty runoff, shingle granules, and roof-surface residue."

### 10.3 Execution Plan Handoff Protocol

The execution plan must follow a two-phase output structure:

**Phase 1 — Human-Readable Brief:**
- Generated first
- Contains narrative attack, buyer state, structure outline, Key Takeaways, citation blocks, field stories
- Reviewed and approved by human

**Phase 2 — Structured JSON:**
- Created only after human review / quality check and before writer handoff
- Contains the full structured output schema

**Intake Override Rule:**
If the page is net-new and prior SERP/PAA/Perplexity analysis is unavailable, the agent may proceed with doctrine and human-supplied strategic context, but must:
- Mark `intake_override_used: true` in the output
- Ask the human to confirm the intake override before writer handoff

**Source:** Doc 153 Section 8 (Human Review Prompts), Doc 304 (Strategic Directive)

---

## SECTION 9: DOC 153 INTEGRATION REFERENCE

Doc 153 (Execution Plan Generator) loads this document as a required knowledge retrieval. The mapping between this doc's sections and Doc 153's steps:

| Doc 155 Section | Doc 153 Step |
|-----------------|--------------|
| Section 1 (Narrative Attack) | Step 0 — Narrative Attack Generation |
| Section 1.4 (Universal Failure Frame — Guardian Pages) | Step 0 — category_misunderstanding field; Step 1 — H2 1 problem establishment; Key Takeaways |
| Section 1.5 (Universal Failure Frame — All Page Types) | Step 0 — page type classification; applied in pillar, comparison, and brand identity pages |
| Section 2 (Buyer State) | Step 0 — Buyer State Determination |
| Section 3 (Language Translation) | Applied during Step 1 (Structure), Step 16 (Citation Blocks), and Key Takeaways Generation |
| Section 4 (Win Vector Test) | Step 2 — Win Vector Enforcement |
| Section 5 (Key Takeaways Quality Gate) | Key Takeaways Generation in Step 1 |
| Section 6.1 (Historical Pattern) | Step 13 — Knowledge Graph Assignment |
| Section 6.2 (Edge Case Suppression) | Step 13 — Knowledge Graph Assignment |
| Section 6.3 (Front-Lip Narrative) | Step 4 — AEGIS Guardian Assignment |
| Section 6.4 (Roof Runoff Bridge) | Step 13 — Knowledge Graph Assignment |
| Section 6.5 (ShingleSafe Rule) | Step 13 — Knowledge Graph Assignment |
| Section 6.6 (Proof Ownership) | Step 4 — Trust & Mechanism Assignment |
| Section 6.7 (First-Time Checklist) | Step 1 — H2/H3 Generation |
| Section 6.8 (Material Rule — deprecated) | See Section 10.2 — moved to consolidated rule |
| Section 6.9 (Field Story) | Step 1 — H2 section field_story_required |
| Section 6.10 (Downstream Cost) | Step 1 — Required narrative beat in H2 1 for first_time_buyer pages |
| Section 7 (Honesty Constraints) | Populates `honesty_constraints` field in output schema |
| Section 8 (Bad Default Library) | Training reference — consulted during Step 0 and all H2 generation |
| Section 10.1 (AEGIS 5X Entity Definition) | Step 0 — Narrative Attack, Step 4 — Guardian Assignment |
| Section 10.2 (Vinyl Competitive Pressure) | Step 13 — Knowledge Graph Assignment, proof/trust sections |
| Section 10.3 (Execution Plan Handoff) | Steps 0–17 — governs output structure and intake decisions |

---

**End of Document**