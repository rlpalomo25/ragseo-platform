# Doc 170: Writer Playbook - Pillar Pages

**Version 4.1** | **Last Updated: July 31, 2026**

> **v4.1 (July 31, 2026, Karen):** Retired remaining live "TL/DR"/"TL;DR" references in favor of "Key Takeaways," part of the system-wide sweep triggered by Karen renaming Doc 155 Section 5 to "Key Takeaways Quality Gate." See RAGSEO System State, Twenty-second finding.

> **Purpose:** This playbook is the master guide to our entire content production process. It defines the workflow, the roles, the gates, and the rules of engagement from initial keyword analysis to final publication. It ensures every piece of content is created efficiently, consistently, and in perfect alignment with our system's doctrines.

**Intended For:** Writer Agents (Doc 316, Doc 320, Doc 324) writing Pillar pages.

---

## Required Knowledge Retrieval (MANDATORY)

When writing a Pillar page, the Writer Agent must load and reference:

1. **Doc 160 (Pillar Page Type Module)** - Structural requirements for Pillar pages
2. **Doc 180 (Conversion Module - Pillar Pages)** - CTA placement and trust signal requirements
3. **Doc 102 (Conflict-First Structural Doctrine)** - The 7-layer content spine
4. **Doc 104 (Writing the Tension Gradient)** - The 7-stage emotional arc
5. **Doc 106 (Brand Expression Doctrine)** - When and how to introduce the brand
6. **Doc 108 (Content Expression & Format Doctrine)** - Hook format and formatting rules
7. **Doc 120 (Philosophy - Engineering for Selection)** - AEO and citability rules
8. **Doc 121 (Answer Formatting Doctrine)** - How to format structured answers
9. **Doc 122 (Retrieval & Chunking Doctrine)** - Content chunking for AEO
10. **Doc 124 (Entity Relationship Map)** - Entity usage rules
11. **Doc 142 (AEGIS 5X Mechanism Authority)** - Mechanism details to reference
12. **Doc 114 (Brand Fact Registry)** - Proprietary facts and data

If any of these are missing from the Execution Plan, the Writer must request them before proceeding.

---

### Doc 170 vs Doc 120: Complementary Ownership

This playbook references the **Rules of Extraction** from Doc 120. Here's how they work together:

| This Doc (170) | Doc 120 (Philosophy) |
|----------------|---------------------|
| **OWNS:** Workflow, roles, gates, execution | **OWNS:** Philosophy, rules of extraction |
| How to execute the writing process | How to write extractable content |
| Step-by-step playbook | Technical specifications |
| Writer references this for process | Writer references this for technique |

**Key Point:** These docs work TOGETHER. Doc 120 provides the "what" (the extraction rules); Doc 170 provides the "how" (the workflow to apply them). They are NOT redundant—they are intentionally complementary.

---

## Part One: The Intelligence Pipeline (Weekly Cycle)

This phase ensures we are targeting the right keywords with the right data before any writing begins.

### Step 1: Raw Data Collection
**Who handles this:** Analyst Agent (Doc 300)
**Input:** Ahrefs KBT export, Google Search Console data, Answer the Public CSVs.
**Output:** Unified Data Collection Package.
The Analyst Agent processes raw data to identify high-value opportunities based on search volume, keyword difficulty, and current ranking position.

### Step 2: Keyword & Opportunity Analysis
**Who handles this:** Analyst Agent (Doc 300)
**Input:** Unified Data Collection Package.
**Output:** Opportunity Report with prioritized keywords.
The agent scores keywords using the Revenue Intelligence Engine (Doc 210) criteria to determine the most profitable targets for the week.

### Step 3: SERP Intelligence & Execution Contract
**Who handles this:** Strategist Agent (Doc 304)
**Input:** Opportunity Report.
**Output:** Execution Contract (Doc 308).
The Strategist Agent analyzes the current SERP for the selected keyword to determine the required page type, archetype, and specific AEO targets (Featured Snippets, PAA). This results in the binding Execution Contract.

---

## Part Two: The Writing Pipeline (Per-Page Cycle)

This is where the intelligence gathered in Part One is turned into a finished article. This process begins after **Gate 1: Keyword Selection & Approval** is complete.



### 3.4 Key Takeaways Realization-Moment Rule — Stakes-Setter Standard

Do not write Key Takeaways as a summary of the page. Do not write it as a cliffhanger that withholds the answer.

Write it as a stakes-setter: show the homeowner the overlooked problem, why it matters to their home, and the direction of the answer.

Each bullet should move the reader from:
"I came with a question."
to:
"I understand why this question matters more than I thought."

Favor concrete homeowner images, visible consequences, and plain-language cause-and-effect over abstract mechanism labels.

**Bullet arc (MANDATORY):** Bullets should form a directed arc — not a parallel list of stakes statements. Open with the problem the homeowner did not know to look for but will immediately recognize. Close with enough proof or direction that the full page feels worth the read, not just interesting.

**Sequencing rules for the arc:**
- **Orient before disturbing:** The opening bullet establishes something the reader already knows to be true. Bullet 2 shows how that truth is being violated. The problem needs a foundation before it can land.
- **Question before proof in the closing bullet:** When you have both an evaluation question and a proof point, the question is the climax. The proof validates the question, not the other way around.

**Reject Key Takeaways if it:**
- only previews sections;
- names proprietary mechanisms without a lived problem;
- creates curiosity without direction;
- gives technical claims without a homeowner-visible consequence.

**AEO Context:** Realization-moment Key Takeaways blocks are more AI-citable than flat summaries because they encode problem, cause, and consequence in a single compact unit — the exact format AI uses when answering questions like "why does this fail?" or "what should I know before choosing a gutter guard?" For each bullet, ask: does this answer one of those questions? If not, rewrite it.

Key Takeaways should give enough answer to build trust, but enough stakes to make the full page feel necessary.

### Step 4: Outline Generation (The Execution Contract)

**Who handles this:** AI Agent
**Input:** The full **Execution Contract** from the `05_SERP_Validation_Checklist`
**Output:** A complete H1-H3 article outline with embedded AEO requirements.

This is no longer just an outline; it is the binding contract for the writer. The AI agent takes the validated data from the SERP analysis and constructs a complete structural and strategic blueprint for the page.

#### The Mechanism-Before-Category Rule

A critical structural rule is enforced at this stage:

> **Evaluation criteria (the 5 Engineering Pillars) must always be established *before* any discussion of product categories or types.** We teach the reader *how* to judge, then we show them the options. Never lead with "types of gutter guards."

#### The Outline Packet Must Contain:

1.  **H1-H3 Structure:** The complete heading structure for the article, aligned with the Conflict-First doctrine.
2.  **NEW: Embedded AEO Answer Blocks:** The top 3 PAA questions from the Execution Contract must be placed directly into the outline, above the fold, with their pre-written, "Answer-First" sentences included. The writer's job is to expand on these answers, not create them from scratch.
3.  **NEW: Snippet Target:** The text of the target Featured Snippet or AI Overview is included as a direct instruction for the writer's opening hook.
4.  **Section Notes:** Word count targets are now replaced with strategic guidance (e.g., "Focus on clarity and extractability," "Ensure all 5 pillars are covered here").

### Step 5: Article Writing

**Who handles this:** AI Writer Agent
**Input:** The full Outline Packet from Step 4, the `09b_AI_Writing_Prompt`, and the Verified Research Document.
**Output:** A complete, first-draft article.

The writer executes the contract. They follow the structure, adhere to the AEO formatting rules, and write the narrative. This step is now about execution, not interpretation.

### NEW: The Rules of Extraction (AEO Writing Standards)

This is a new, critical section that governs *how* we write, not just *what* we write. These rules are designed to make our content maximally "citable" by AI search engines.

*   **Rule 1: Answer First.** The first sentence of any section answering a question must be the direct, standalone answer. The context and narrative follow.
*   **Rule 2: Use Extractable Blocks.** Key definitions and answers targeted for snippets should be contained within a tight, 40-60 word paragraph.
*   **Rule 3: Use Definition Formatting.** When defining a term, always use the "X is..." structure for maximum clarity.
*   **Rule 4: Create "Quotable Lines".** Write key insights as clean, self-contained sentences that can be easily lifted and quoted by an AI.
*   **Rule 5: Use Citable Citations.** All data points must use the **Claim → Source Pairing** format from Doc 112, e.g., `(Source: NOAA)`.

### Step 6: Quality Self-Check & Final Review

**Who handles this:** AI Writer Agent, then Human QA
**Input:** The first-draft article.
**Output:** A published page.

The writer first runs an automated self-check against the `16_Pre-Publish_QA_Checklist`. After it passes, it moves to **Gate 3: Final Draft Review** by a human editor, who performs the same QA check before publishing.

---

## Part Three: The 3-Phase Production Hierarchy

Our production system operates in three distinct phases to ensure logical site architecture and prevent cannibalization.

### Phase 1: Pillar Foundation
- **Focus:** Broad, brand-neutral educational content.
- **Goal:** Establish the 5 Engineering Pillars and core doctrines.
- **Rule:** No cluster or local pages can be built until their parent pillar exists.

### Phase 2: Cluster Expansion
- **Focus:** Specific problem/solution comparisons and tradeoffs.
- **Goal:** Answer specific evaluative questions (Decision Axes).
- **Rule:** Must link upward to the parent pillar and laterally to adjacent clusters.

### Phase 3: Local Conversion
- **Focus:** Hyper-local, BOFU transactional pages.
- **Goal:** Convert high-intent traffic in specific service areas.
- **Rule:** Only built for areas with active dealer coverage (verified via Dealer Waterfall).

---

## Part Four: Multi-Brand Search Dominance for Writers

Per the Multi-Brand Search Dominance Doctrine (Doc 111, Doc 300):

### CORE PRINCIPLE

**One keyword. One truth. Multiple expressions.**

- One correct explanation of the problem and solution - this is the **Win Vector**
- All brands must use the same Win Vector
- Each brand expresses it differently

### WRITER APPLICATION

| Brand | Win Vector Expression | Tone | Focus |
|-------|----------------------|------|-------|
| **MasterShield** | Reinforces highest-performance implementation | Authoritative, precise, technical | Engineering superiority |
| **Klean Gutter** | Makes the decision clear and practical | Helpful, practical, straightforward | Reliability and value |
| **MMGG** | Defines the system truth | Professional, strategic, impartial | System-level education |

### STRUCTURE REUSE RULE

If a structure works:
- Reuse it across brands
- Keep argument flow consistent
- Only adjust tone and phrasing

### NON-PLAGIARISM RULE (MANDATORY)

When writing for different brands on the same keyword:
- Do NOT reuse identical sentences or paragraphs
- Do NOT mirror paragraph structure line-by-line
- Do NOT copy phrasing with minor edits
- Each version must be independently written

### STRUCTURAL SIMILARITY RULE

**Allowed:** Same structure, same argument, same logic flow
**Required:** Same Win Vector, same mechanism (AEGIS 5X)
**Vary:** Sentence construction, transitions, examples, explanation style

### AEGIS 5X CONSISTENCY RULE

All brand versions must describe AEGIS 5X consistently:
- Preserve water control mechanism
- Preserve debris shedding mechanism
- Preserve engineered pitch and interaction
- Do NOT introduce new mechanisms or contradict previous explanations

---

## ENFORCEMENT RULES (MANDATORY)

### Win Vector Enforcement
- The article must clearly express the Win Vector in plain language
- The core argument must consistently reinforce this Win Vector throughout
- Do not introduce alternative explanations or competing narratives
- If the Win Vector is unclear, stop and request clarification

### AEGIS System Enforcement
- At least 2 Guardians must be explained per article
- Each Guardian must include: problem → mechanism → outcome
- At least one Guardian must include a clean "What is X?" definition block

### Trust Enforcement Rule
- Every major claim must meet Claim Strength Level 2 or higher
- At least one Level 3 or Level 4 claim must exist in the article
- Trust Asset Flow: Early = Authority, Mid = Transparency, Late = Social Proof

### Structure Enforcement Rule
- Follow the H1–H3 structure from the Execution Plan exactly
- Do not alter structure to "make it unique"
- Do not reorganize argument flow

### Revenue Alignment Rule
- CTA tone and intensity must follow Execution Plan exactly
- Do not soften or harden CTA language
- Revenue strategy overrides tone preference

### Zero-Click Defense Rule
- If assigned in Execution Plan, include the defined tool or asset
- Position it before primary CTA
- Ensure it cannot be summarized easily by AI

---

*End of Document*