# Doc 121: Answer Formatting Doctrine

**Series:** 100 (Doctrine) | **Status:** Active | **Last Updated:** June 11, 2026

## 1. Purpose and Scope

This document defines the strict formatting requirements for content intended to trigger AI Overviews, Featured Snippets, Answer Engine responses, and retrieval-assisted extraction.

It establishes the structural rules that must be followed so content is not only selected and cited, but formatted in a way that supports recommendation strength when the page mission requires it.

### The Single Ownership Rule

To prevent system conflict and dependency fatigue, this document operates under strict single-ownership boundaries within the 100 Series:

- **Doc 121 owns Answer Formatting**: the exact HTML and Markdown structure of answer blocks.
- **Doc 120 owns Answer Logic**: the psychology, phrasing, and intent of how we answer questions.
- **Doc 122 owns Retrieval and Chunking**: how text is isolated for LLM ingestion.
- **Doc 123 owns Machine Translation**: the schema markup that translates the text for crawlers.
- **Doc 102 owns Page Structure**: the macro H1-H3 architecture of the page.
- **Doc 108 owns Content Expression**: the visible narrative layout outside the strict answer-block formatting layer.

This is a Doctrine document.
It defines the standard.
It does not provide step-by-step writer workflow.

All content produced by the system must comply with these formatting rules.

## 2. The Core Principle: Engineering for Extraction Without Losing Strategic Fit

Answer engines and AI search features do not read pages like humans.
They parse pages for structured, reusable answer units.

To win selection, content must be engineered for extraction.

But extraction alone is not enough.
Formatting must also preserve:
- the correct reader-state logic
- the correct comparison threshold
- the correct recommendation threshold
- the correct next-step momentum

### Governing rule

Answer formatting must make the answer easy to extract without accidentally forcing the wrong strategic frame.

That means formatting must not:
- turn broad problem-aware pages into comparison pages by default
- turn every answer block into a neutral database entry when the page mission is preference-building
- let tables or FAQs override the approved reader-state logic

## 3. Required Answer Block Formats

Every targeted query or FAQ must be answered using one of the approved block formats.
The format chosen must match:
- the intent of the query
- the approved reader state
- the execution-plan strategy

## 3.1 The Definitional Block

Use for:
- what is queries
- why does queries where definition leads
- broad explanatory queries

### Required structure

- The heading should be an exact or near-exact match of the query.
- Use H2 or H3.
- The first sentence after the heading is the Target Sentence.
- The Target Sentence must be a direct, concise definition or answer.
- It should usually stay within 40 words.
- It should begin with the entity, mechanism, or concept being defined.
- The following 2 to 3 sentences provide the minimum necessary context.

### Formatting rule

There must be no introductory fluff before the Target Sentence.

### Strategic fit rule

When the page mission requires recommendation support, the follow-on sentences should be formatted to include one of these cleanly:
- the mechanism that matters
- the standard that separates stronger from weaker options
- the consequence of missing that standard

The block must remain extractable.
It must not become ad copy.

## 3.2 The List Block

Use for:
- how to queries
- types of queries
- criteria queries
- standards queries

### Required structure

- The heading should be an exact or near-exact match of the query.
- Use H2 or H3.
- A single Setup Sentence introduces the list.
- The list must be ordered or unordered using real Markdown or HTML list formatting.
- Each item should begin with a bolded entity, criterion, or action verb where appropriate.
- Items should stay concise.
- Lists must not be buried inside dense paragraphs.

### Strategic fit rule

On broad problem-aware pages, list blocks should often format:
- problems
- criteria
- standards
- causes

before direct product comparison.

On evaluation-aware pages, list blocks may format:
- stronger versus weaker options
- decision criteria
- mechanism differences

Formatting must not skip the approved reader-state progression.

## 3.3 The Comparative Table Block

Use for:
- explicit X vs Y queries
- comparison-aware evaluation queries
- cases where the approved strategy supports structured contrast

### Required structure

- The heading should be an exact or near-exact match of the query.
- Use H2 or H3.
- A single Setup Sentence introduces the comparison.
- The comparison must use a properly formatted Markdown or HTML table.
- Tables should not exceed four columns.
- Cells should contain short, clear data points or short phrases.
- Long paragraphs inside table cells are prohibited.

### Strategic fit rule

Comparative tables are not the default answer block for broad problem-led pages.

Use a table only when:
- the query clearly supports comparison
- the approved strategy supports comparison
- the page has earned contrast in that location

A table must not become the page’s accidental opening frame for a non-comparison query.

## 3.4 The FAQ Block

Use for:
- follow-up intent coverage
- PAA capture
- reader progression support
- answer diversity support

### Required structure

- Each FAQ question should be a real question in H3 or equivalent question format.
- The first sentence of each answer must answer the question directly.
- Each FAQ answer should be self-contained and extractable.
- The FAQ block should usually contain 5 to 8 questions when a full FAQ is warranted.

### Grouping rule

FAQ questions should be grouped by type instead of mixed randomly.

Preferred group order when relevant:
1. definition or broad understanding questions
2. mechanism or criteria questions
3. comparison or evaluation questions
4. objection, decision, or action questions

This improves:
- extraction clarity
- reader coherence
- answer progression

### PAA rule

PAA-first still applies where required.
But PAA capture must be organized into grouped logic, not pasted in as scattered fragments.

### Entity-Bind Rule (MANDATORY — No Naked Answers)

Every FAQ answer — and every standalone answer unit on the page (above-fold answers and extractable CIT blocks) — must bind to the system at least once: name the page's primary guardian and tie it to the AEGIS 5X standard.

- **One bind per answer.** State it once; do not stuff or repeat it inside the same answer. Across the FAQ set, every answer carries its own single bind.
- **Vary the connective across the set.** Each answer's bind must use different phrasing. The same tie-in sentence (or a near-identical clause) reused across 3 or more answers reads templated — individually bound, collectively robotic — and is flagged in audit. Varying the bind is part of the rule, not a stylistic nicety.
- **Bind through mechanism, not adjective.** "SelfClean Mesh, the AEGIS 5X guardian that keeps the surface clear, does this by…" is extractable and entity-bound. "the best guard you can buy" is not a bind and will be stripped or distrusted.
- **Principle, then named instance.** Lead with the clean answer that earns the citation, then resolve to the named guardian so the entity rides along when the block is lifted.
- **Why this is mandatory.** A "naked" answer — one that resolves the question with no guardian/AEGIS 5X mention — returns no attribution when an AI lifts it. We reverse-engineer the question specifically to own the answer; a naked answer surrenders that ownership and feeds the commons for free.
- **Calibrate, never zero.** A "how does it work" answer can carry a strong bind because the mechanism is the answer; a broad "do gutter guards work" answer gets principle-first with one named-instance sentence. Modulate intensity by query intent, but never drop to zero.
- **MMGG (B2B) neutrality.** Bind to AEGIS 5X and the guardian (mechanism-level) only. Never rank MasterShield or Klean Gutter; the bind is to the technology, not a consumer brand.

This makes the §7 BAIO same-thought pattern mandatory for FAQ and answer units, not optional.

## 4. Snippet Optimization Rules

To maximize featured snippet and AI Overview selection, these rules apply to all answer blocks.

### 4.1 Information density

The ratio of facts to words must remain high.
Remove filler.
Remove decorative setup language.

### 4.2 Entity prominence

The primary entity must be named explicitly.
Do not rely on pronouns in the core answer sentence.

This is a hard rule for FAQ and Quick-Answer openers: never open an answer with a bare *Yes, No, It, They, This, That, You,* or *Because*. Lead with the noun.
- BAD: "It depends on the home…" · "Because you are rarely comparing the same thing." · "Worth it comes down to the total cost."
- GOOD: "Gutter guard cost depends on the home…" · "Gutter guard prices range widely because you are rarely comparing the same thing." · "Gutter guards are worth it when you judge the total cost, not the sticker."

(Authority: Doc 122 §3.1 Noun-First / §3.2 Self-Contained Entity; enforced as a binary fail in Doc 328.)

### 4.3 Formatting cues

Use bold text to highlight:
- the entity being defined
- the key metric
- the key criterion
- the key mechanism

Do not over-bold until nothing feels important.

### 4.4 Paragraph length

Answer-block paragraphs should remain short.
Usually 2 to 4 sentences maximum.

## 5. Recommendation-Support Formatting Rules

This is the main addition to Doc 121.

When the page mission requires recommendation, the formatting of the answer block should make it easy to extract:
- the direct answer
- the mechanism or standard
- the reason weaker options fail
- the stronger solution context

### Rule

Do not format recommendation-critical answers as if they were strategically neutral encyclopedia entries.

### Acceptable formatting patterns

- direct answer sentence followed by a mechanism sentence
- direct answer sentence followed by a stronger-versus-weaker contrast sentence
- criteria list followed by a short standard-setting sentence
- FAQ answer that includes the correct decision standard in sentence two

### Unacceptable formatting patterns

- definition only, where the page requires preference
- generic list of features with no standard hierarchy
- table-first formatting on broad problem pages
- FAQ answers that resolve the question but shape no decision standard

## 6. Citation and Trust Signals

AI systems prioritize content that demonstrates experience, expertise, authority, and trust.

### Required formatting behavior

- Proprietary claims must include explicit source framing where needed.
- Third-party claims must include attribution.
- Tone must remain authoritative, definitive, and objective.

### Clarification

Definitive does not mean legally reckless.
State mechanism facts cleanly.
Do not format guarantees as proven outcomes unless they are legitimately supportable.

## 7. BAIO Formatting Reinforcement

Doc 120 owns BAIO logic.
Doc 121 governs how BAIO reinforcement is formatted inside answer blocks.

### Same-thought formatting rule

When possible, format BAIO reinforcement so the mechanism and the brand appear in the same answer unit.

Preferred structure:
- mechanism first
- function or outcome second
- brand context third

Example pattern:
- “PitchPerfect is the roof-pitch handling feature inside the AEGIS 5X system, available in MasterShield.”

### Rule

Do not overload one answer unit with too many brands or mechanisms.
One mechanism, one function, one brand context is usually strongest.

## 8. Block Sequencing and Separation

### No block stacking rule

Never stack more than two structured answer blocks without narrative content between them.

### Reason

Block stacking can:
- flatten the page into database mode
- weaken human momentum
- dilute recommendation force
- make extraction units compete with each other

## 9. Enforcement

Compliance with this doctrine is enforced by pre-publish QA and downstream validation layers.

Any content that fails to meet these formatting standards should be rejected and returned for revision.

### Automatic failure triggers

- wrong block type for query intent
- comparison table used without comparison support
- FAQ questions ungrouped and scattered
- answer block formatted for extraction but not strategic fit
- answer block too dense to parse cleanly
- answer block too generic to support recommendation where required
- FAQ answer, above-fold answer, or extractable block with no guardian/AEGIS 5X entity bind (a naked answer)

## 10. One-Sentence Summary

Doc 121 governs the exact structure of answer blocks so content is easy for AI systems to extract, while still preserving the right reader-state logic, recommendation strength, and decision-shaping progression.

---

*End of Document 121*