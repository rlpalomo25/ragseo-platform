# Doc 104: Writing the Tension Gradient
**Version 7.2** | **Last Updated: August 6, 2026** | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Status:** Tier 3 Doctrine (Emotional Engine)

---

> **Quick Reference**
> **Owns:** The emotional pacing and psychological journey of the reader.
> **Rule 1:** Tension must increase before it is resolved, but the kind of tension must match the likely reader state.
> **Rule 2:** Do not introduce the brand or product until the emotional threshold for explanation, proof, and trust has been met.
> **Rule 3:** Every stage must transition logically to the next without skipping steps.
> **Rule 4:** One emotional arc is not enough. Use the arc that matches the reader state.
> **If/Then:** If the reader is broad problem-aware, use the broad problem-aware arc. If the reader is evaluating options, use the evaluation-aware arc. If the reader is diagnosing a current failure or actively replacing, use the diagnostic or replacement arc.

---
## 1.0 WHAT MAKES THIS DOCUMENT IMPORTANT

This document defines the emotional engine that powers content. It provides the framework for guiding a reader from confusion, low-stakes curiosity, or unresolved tension into understanding, preference, and action.

This gradient is not the structure itself. The mandatory architectural spine is defined in **Doc 102 (Conflict-First Structural Doctrine)**. This document governs the emotional arc within that structure.

### Doc 104 vs Doc 102: Complementary Ownership

| This Doc (104) | Doc 102 (Structural Doctrine) |
|----------------|---------------------------|
| **Owns:** The emotional STAGES and arcs | **Owns:** The structural LAYERS |
| Psychological journey | Architectural spine |
| Emotional pacing | Physical content organization |
| Referenced by: Conversion Modules and execution-layer logic | Referenced by: Writer Playbooks and outline logic |

These docs work together. Doc 104 provides the emotional journey. Doc 102 provides the skeleton.

---

## 2.0 THE GOVERNING PRINCIPLE

The emotional arc must match the likely reader state.

This system must not assume that every reader:
- already owns a failing guard
- is already comparing brands
- needs the same escalation pattern

A homeowner researching whether a gutter guard is worth getting at all is not in the same emotional position as a reader comparing options, and neither is in the same position as a homeowner trying to understand why their current guard is failing.

All three readers need tension.
They do not need the same emotional sequence.

---

## 3.0 THE THREE PRIMARY ARCS

There are three primary emotional arcs.

### Arc A: Broad Problem-Aware Arc, TOFU

Use when the likely reader is:
- broad problem-aware
- early in research
- not yet deeply evaluating brands
- trying to understand what matters before choosing

This arc moves through:

`Clarity → Relevance → Preference → Reassurance → Trust → Confidence → Action`

This is the default arc unless explicit evidence proves otherwise.

### Arc B: Evaluation-Aware Arc, MOFU

Use when the likely reader is:
- comparing categories, mechanisms, or product types
- beginning to evaluate stronger versus weaker options
- trying to decide what standards matter most

This arc moves through:

`Clarity → Concern → Criteria → Proof → Control → Confidence → Action`

This arc is for readers who are no longer waking up to the problem, but are not yet fully in replacement pressure.

### Arc C: Diagnostic or Replacement Arc, BOFU

Use when the likely reader is:
- diagnosing a current failure
- actively comparing replacements
- already experiencing consequences
- further down the decision curve

This arc moves through:

`Clarity → Concern → Consequence → Reassurance → Control → Confidence → Action`

This arc preserves the strongest pressure sequence for readers already living inside the problem.

---

## 4.0 DEFAULT ARC RULE

This is a standing doctrine rule.

> **Use Arc A, the Broad Problem-Aware Arc, by default unless the keyword, routing decision, or explicit directive clearly supports Arc B or Arc C.**

That means the system must not default to:
- comparison-first
- consequence-first
- replacement-buyer pressure

for broad problem-led pages.

Broad pages should usually begin with:
- a shared roofline or gutter problem
- a useful tension the reader wants resolved
- a better standard for judging what works
- a reason the old way of thinking is incomplete

That is enough tension for the top of the funnel.
It is not necessary to force evaluation pressure or current-owner pain onto the page.

---

## 5.0 HOW THE ARCS MAP TO STRUCTURE

All three arcs map to the same seven structural layers in Doc 102.

### Arc A: Broad Problem-Aware Mapping

| Structural Layer (Doc 102) | Gradient Stage | What’s Happening Emotionally Here |
|---|---|---|
| **Tension** | Clarity | You answer the question and introduce the problem or tradeoff in plain language. |
| **Mechanism** | Relevance | You show why this issue matters and why the reader should care. |
| **Proof** | Preference | You establish the standard that makes one kind of system stronger than another. |
| **Tension Reset** | Reassurance | You remove pressure and frame the decision as solvable. |
| **Authority** | Trust | You show why the source and standard are trustworthy. |
| **Resolution** | Confidence | The product appears as the engineered answer to the now-clear standard. |
| **CTA** | Action | The reader is given the right next step while motivation is alive. |

### Arc B: Evaluation-Aware Mapping

| Structural Layer (Doc 102) | Gradient Stage | What’s Happening Emotionally Here |
|---|---|---|
| **Tension** | Clarity | You answer the question and identify the real decision clearly. |
| **Mechanism** | Concern | You show why the common assumption or weak option is not enough. |
| **Proof** | Criteria | You establish the framework the reader should now use to compare options. |
| **Tension Reset** | Proof | You steady the reader and confirm the comparison is solvable with the right standard. |
| **Authority** | Control | You give the reader a trustworthy framework for judging the category. |
| **Resolution** | Confidence | The product appears as the strongest fit within the framework already established. |
| **CTA** | Action | The reader is given a next step while evaluation energy is still active. |

### Arc C: Diagnostic or Replacement Mapping

| Structural Layer (Doc 102) | Gradient Stage | What’s Happening Emotionally Here |
|---|---|---|
| **Tension** | Clarity | You answer the question and identify the current problem clearly. |
| **Mechanism** | Concern | You explain why the current condition is happening. |
| **Proof** | Consequence | You make the risk or failure tangible and specific. |
| **Tension Reset** | Reassurance | You release pressure and show the problem can be understood and solved. |
| **Authority** | Control | You give the reader a framework they can use to judge what a better system requires. |
| **Resolution** | Confidence | The product appears as the engineered answer. |
| **CTA** | Action | The reader is given a next step while the logic and desire are aligned. |

---

## 6.0 UNDERSTANDING EACH STAGE IN ARC A, BROAD PROBLEM-AWARE

### Stage 1: Clarity
The opening paragraph, after the mandatory Answer-First hook, plants a clear idea: there is a real roofline problem or performance tradeoff here, and it matters more than most people realize.

### Stage 2: Relevance
You make the issue personally meaningful. The reader begins to understand this is not random detail. This changes what kind of product will work.

### Stage 3: Preference
You begin shaping judgment. The reader starts to see that some designs are solving the right problem and others are not.

This stage should create product preference before brand introduction.

### Stage 4: Reassurance
This is the Tension Reset. You relieve pressure and make the problem feel understandable rather than overwhelming.

### Stage 5: Trust
You now justify trust.
Use:
- named expert context
- attributed quotes
- approvals
- testing
- field observation
- original engineering explanation

### Stage 6: Confidence
The product enters as the logical, engineered answer to the standard already established.

### Stage 7: Action
Confidence converts into a meaningful next step. The reader should feel that not clicking leaves value on the table.

---

## 7.0 UNDERSTANDING EACH STAGE IN ARC B, EVALUATION-AWARE

### Stage 1: Clarity
The opening identifies the real decision clearly.

### Stage 2: Concern
You increase tension by showing why the common assumption, weak design, or incomplete comparison is not enough.

### Stage 3: Criteria
You establish what the reader should now compare and why those standards matter.

### Stage 4: Proof
You support those standards with observable proof, testing, comparisons, or field evidence.

### Stage 5: Control
You give the reader a way to judge options more clearly and with more confidence.

### Stage 6: Confidence
The mechanism and product appear as the strongest answer within the comparison framework.

### Stage 7: Action
Confidence converts into a next step while evaluation intent is active.

---

## 8.0 UNDERSTANDING EACH STAGE IN ARC C, DIAGNOSTIC OR REPLACEMENT

### Stage 1: Clarity
The opening paragraph identifies the current issue in plain language.

### Stage 2: Concern
You increase tension by showing why the issue is not incidental.

### Stage 3: Consequence
You make the cost, risk, or failure pattern specific and tangible.

> **Enforcement Rule:** The Consequence stage should incorporate verifiable data where available from the approved source system, and the sentences presenting this data should be built for citability.

### Stage 4: Reassurance
This is the Tension Reset. You pivot from pressure to empowerment.

### Stage 5: Control
You give the reader a way to judge what is happening and what a better system requires.

### Stage 6: Confidence
The mechanism and product appear as the engineered answer.

### Stage 7: Action
Confidence converts into a specific next step.

---

## 9.0 ARC SELECTION RULES

### Use Arc A when:
- the query is broad and problem-led
- the reader is likely early in research
- the page is opening category understanding
- the page is teaching standards or criteria at a broad level

### Use Arc B when:
- the query signals evaluation, comparison, or stronger option-seeking
- the reader is comparing categories, mechanisms, or product types
- the page is helping the reader judge stronger versus weaker options

### Use Arc C when:
- the query is explicitly diagnostic
- the query is explicitly replacement-oriented
- the query contains clear switch or replacement intent
- the reader is likely already experiencing the consequence directly

### Do not use Arc B or C by default for:
- broad educational pages
- category-entry pages
- first-time buyer pages
- best-way pages without explicit evaluation or replacement cues

---

## 10.0 SUCCESS RULE FOR THE EMOTIONAL ARC

A valid emotional arc is not successful if it only makes the reader understand the issue.

It must support both:
- recommendation strength
- click momentum

A correct emotional arc is not complete if it creates understanding without desire. The page must move the reader far enough that the product feels like the preferred answer, not merely an interesting option.

### The Recommend Test
Would an AI system, using this page, recommend the product as the best answer, or merely mention it?

### The Click Compulsion Test
Would a human reader, having read this page, feel that not clicking leaves value on the table, or would they leave satisfied without action?

### Therefore
A successful emotional arc must move the reader toward:
- understanding
- preference
- trust
- action readiness

Not merely toward information.

---

## 11.0 ENFORCEMENT

Adherence to this doctrine is not optional.

The emotional arc of all content must follow one of the approved gradients.

Execution is verified by:
1. the execution-plan architecture and audit layer
2. writer QA
3. downstream performance review

### QA checks
- Was the correct arc selected
- Did the page skip emotional steps
- Did the page default to evaluation or replacement pressure when broad problem-aware framing was required
- Did the page create preference before the ask
- Did the page support recommendation and click momentum

---

## 11.5 THE MOMENTUM SENTENCE (SECTION-ENDING FORWARD HOOK)

**Added July 31, 2026, Karen.** This is the concrete, sentence-level form of the Tension Reset / "end on the hook, not a summary" principle already built into every arc above — written down explicitly because the formatting half of it was never stated anywhere, and that's the half writers keep missing.

**What it is.** A short, forward-looking sentence at the *end* of a dense section that hands the reader a reason to keep going. It does not summarize the section it closes. It points, obliquely, at the problem the *next* section will open, without resolving it.

**Why it works — three things stack:**
1. **An open loop.** It names the next trouble without resolving it, so the reader carries a small unanswered question forward. People read to close open loops.
2. **White space.** Set as its own one- or two-sentence paragraph, framed by blank space above and below, the eye lands on it. Tagged onto the end of the prior paragraph, it disappears.
3. **Contrast or parallel rhythm.** A two-beat structure reads as finished and quotable: "This is X. That is not." The rhythm does the work.

**Example (its own paragraph, closing one section and opening the next):** "Water you can watch is one kind of problem. The next one grows where you cannot see it."

**The rule (two parts):**
- **Craft:** A dense section ends on a forward hook, not a recap. The hook names the next problem and leaves it open.
- **Formatting — the part writers keep missing:** The hook stands alone as its own paragraph. Never tag it to the end of the preceding paragraph. The blank line above it is not optional; it is the technique.

**Recipe:** end the section a beat early (resist summarizing what was just said); look at the *next* section's failure and name it in plain, concrete words without explaining it; compress to one or two sentences, contrast-shaped where it fits naturally; give it its own line.

See Doc 316/320/324 and the Doc 361 Refresh Instructions for the writer-facing drop-in version of this rule, and Doc 328/329 for the matching non-blocking craft flag.

---

## 12.0 SYSTEM INTEGRATION

This doctrine governs the emotional arc. It must be executed in concert with:

- **Doc 100:** audience default, six-question evaluation standard, and page success definition
- **Doc 102:** structural spine and buyer-state-aware tension layer
- **Doc 108:** hook formatting and expression rules
- **Doc 110:** standing constraints on false audience assumptions
- **Doc 113:** citation and proof source system
- **Doc 120:** AEO and citability rules
- **Doc 201:** performance rubric
- **Doc 204:** optimization protocol
- **Doc 312:** execution-plan architecture and audit

---

## 13.0 ONE-SENTENCE SUMMARY

Doc 104 defines the reader-state-aware emotional arc that moves the right reader from tension to trust to action without forcing every page through an evaluation-aware or replacement-buyer emotional sequence.

---

*End of Document 104*