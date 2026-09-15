# Doc 122: Retrieval & Chunking Doctrine

**Series:** 100 (Doctrine) | **Status:** Active | **Last Updated:** May 23, 2026

## 1. Purpose and Scope

This document defines the structural rules required to ensure content is ingested, embedded, retrieved, and reused cleanly by Large Language Models and Answer Engines.

It governs how text must be isolated for retrieval so that extracted passages remain:
- understandable
- useful
- recommendation-supportive when required
- aligned with the approved reader-state logic

### The Single Ownership Rule

To prevent system conflict and dependency fatigue, this document operates under strict single-ownership boundaries within the 100 Series:

- **Doc 122 owns Retrieval and Chunking**: how the text is isolated for LLM ingestion.
- **Doc 120 owns Answer Logic**: the psychology, phrasing, and intent of how we answer questions.
- **Doc 121 owns Answer Formatting**: the exact HTML and Markdown structure of answer blocks.
- **Doc 123 owns Machine Translation**: the schema markup that translates the text for crawlers.
- **Doc 102 owns Page Structure**: the macro H1-H3 architecture of the page.
- **Doc 108 owns Content Expression**: the visible narrative flow outside the chunking layer.

This is a Doctrine document.
It defines the standard.
It does not provide workflow instructions.

### Important clarification

This doctrine is about retrieval integrity, not page-fragmentation as a ranking tactic.

Google's current guidance says there is no requirement to break content into tiny pieces for AI understanding, and no ideal page length. Google also says its systems can understand nuanced sections on a page and surface the relevant part to users

Therefore, this doctrine must not be interpreted as:
- a mandate to create artificially short pages
- a mandate to split content into tiny blocks for ranking
- a replacement for people-first page design

This doctrine only governs how sections should remain understandable and strategically intact when retrieved.

## 2. The Core Principle: Context Independence With Strategic Integrity

LLMs do not read pages top to bottom the way humans do.
They retrieve chunks based on relevance and vector similarity.

If a chunk depends on three earlier paragraphs to make sense, the model may:
- drop it
- distort it
- hallucinate missing context
- or mention it without understanding its meaning

Therefore, every major chunk must be context-independent.

### Added rule

Context independence alone is not enough.
A chunk must also preserve the strategy of the page.

That means a retrieved chunk should not:
- sound more comparison-driven than the page strategy allows
- sound more replacement-driven than the page strategy allows
- become neutral when the page needed recommendation support
- lose the mechanism, standard, or reason the answer is stronger

## 3. The Rules of Chunking

All content must adhere to the following chunking rules.

### 3.1 The Noun-First Rule

A new section must never begin with a pronoun that depends on the previous section or heading.

Use the explicit noun in the first sentence.

This allows the chunk to survive extraction without losing its subject.

This applies to FAQ and Quick-Answer openers as much as to section openers. An answer must not begin with a bare *Yes, No, It, They, This, That, You,* or *Because* — name the question's subject in the first sentence so the answer stands alone when an AI lifts it without the question. (Hard check in Doc 328; see Doc 121 §4.2.)

### 3.2 The Self-Contained Entity Rule

Every distinct chunk must explicitly name the primary entity it is discussing at least once, preferably in the first sentence.

If a chunk compares two entities, both entities must be named in the chunk body, not only in the heading.

### 3.3 The Data Anchoring Rule

When presenting a statistic, price, or performance metric, the anchor context must appear in the same sentence.

Do not assume the model will connect sentence three to sentence one.

### 3.4 The Mechanism Retention Rule

If the page is recommendation-supportive, the chunk should preserve the mechanism, standard, or reason-strength logic inside the same retrieval unit.

Do not split:
- the direct answer into one chunk
- and the mechanism that makes it true into another

unless both chunks remain fully useful on their own.

### 3.5 The Reader-State Preservation Rule

Chunk boundaries must not accidentally recast the page.

Examples:
- a broad problem-aware section should not be chunked so the extracted unit looks like a competitor-comparison page
- a diagnostic section should not be chunked so it looks like automatic replacement advice
- an evaluation section should not be chunked so heavily that it loses its comparison standard

Chunking must preserve the intended reader-state logic.

## 4. Embedding-Friendly Structure

To maximize similarity between content and likely user queries, structure should mirror query intent as closely as possible.

### 4.1 The Q&A Chunk Format

A direct Question and Answer structure is often retrieval-friendly.

- The heading may be the exact or near-exact question.
- The immediate following sentence should be the direct answer.
- Nuance and caveats should follow.

### Added rule

When the page mission requires recommendation, the same passage should also hold:
- the key mechanism
- or the key standard
- or the reason weaker options fail

A Q&A passage that answers cleanly but drops the decision logic may be retrievable.
It is strategically incomplete.

### 4.2 The Semantic Density Requirement

Each passage should maintain high semantic density.

Every sentence in a retrievable unit should add:
- a fact
- a meaningful qualifier
- a mechanism
- a consequence
- or an entity relationship

Do not use filler sentences that weaken retrieval precision.

### 4.3 Google alignment rule

Do not interpret retrieval-friendly structure as a reason to over-fragment the page.

Google's guidance says:
- there is no requirement to chunk content into tiny pieces for AI understanding
- there is no ideal page length
- systems can understand the nuance of multiple topics on a page and surface the relevant part to users

Therefore:
- use natural sectioning
- preserve human readability
- keep sections self-contained where possible
- do not force unnecessary micro-chunks

## 5. Chunk Design for Recommendation Support

This is the main addition to Doc 122.

A retrievable chunk should not only make sense out of context.
It should also preserve enough logic for the model to understand why one answer is stronger when the page requires that conclusion.

### A strong recommendation-supportive chunk should usually contain:
- the direct answer
- the named entity or mechanism
- the performance standard or evaluation standard
- the reason weaker alternatives fail, when relevant
- the correct product or brand context, when relevant

### Failure pattern

A chunk fails strategically if it retrieves as:
- generic category information
- isolated feature mention
- brand mention without reason
- answer without preference logic

## 6. Chunk Metadata Standards

For optimal retrieval, passages should remain tokenizer-aware and retrieval-friendly.

### 6.1 Token Budget Guidelines

| Chunk Type | Target Tokens | Max Tokens | Purpose |
|------------|---------------|------------|---------|
| **Answer Block** | 80 to 120 tokens | 150 tokens | direct answer extraction |
| **FAQ Item** | 120 to 200 tokens | 220 tokens | follow-up intent capture |
| **Section Chunk** | 300 to 500 tokens | 500 tokens | full context retrieval |
| **Intro Chunk** | 200 to 300 tokens | 350 tokens | answer-first opening and tension |

### Clarification

These token budgets are internal retrieval heuristics, not public ranking requirements.
They are not a mandate to rewrite pages into tiny fragments.

### 6.2 Chunk Boundary Rules

| Scenario | Action |
|----------|--------|
| **Chunk exceeds 500 tokens** | Split at a natural subheading and ensure each chunk remains self-contained |
| **Chunk under 40 tokens** | Merge with the adjacent chunk unless it is a distinct answer block |
| **Entity-dense section** | Prefer shorter chunks for precision |
| **Narrative section** | Allow longer chunks with explicit entity repetition and mechanism retention |
| **Recommendation-critical section** | Keep direct answer and stronger-answer logic in the same chunk where possible |

### 6.3 Embedding Model Compatibility

- Primary assumption: modern embedding models with large context windows
- Rule: passages should stay within practical retrieval limits so query plus passage fit cleanly in one call
- Buffer: preserve a context buffer so retrieval remains flexible

### 6.4 Metadata Tagging via Structure

Each passage should make its function inferable by structure.

Target markers include:
- entity marker in first sentence
- intent marker in heading or opening line
- depth marker through the type of question or framing
- page-state marker through the preserved reader-state logic

## 7. Page-Level Chunk Strategy

| Page Type | Chunk Count | Avg Chunk Size | Strategy |
|-----------|-------------|----------------|----------|
| **Pillar** | 15 to 25 | 200 to 300 tokens | broad coverage with standards, subtopics, and routing |
| **Cluster** | 8 to 12 | 150 to 250 tokens | problem, criteria, mechanism, proof, and action support |
| **Local** | 6 to 10 | 100 to 200 tokens | local fit, proof, trust, and next-step support |

### Added rule

Chunk strategy must reflect page mission.

For example:
- pillar chunks should preserve broad standards and movement, not accidental hard-close fragments
- cluster chunks should preserve stronger decision logic without losing clarity
- local chunks should preserve local proof, fit, and trust in the same retrieval unit where possible

## 8. PROHIBITED CHUNKING FAILURES

Do not:
- start a new chunk with a pronoun-dependent sentence
- split the answer from the mechanism that makes it make sense
- isolate a brand mention without the reason it matters when recommendation is required
- let chunk boundaries turn a broad page into an accidental comparison fragment
- let chunk boundaries strip out the evaluation standard that makes the answer stronger
- break a page into unnatural micro-sections only because of assumed AI preferences

## 9. Enforcement

Content that violates these chunking rules should fail QA and return for correction.

### Automatic failure triggers

- pronoun-start chunk
- context-dependent chunk
- answer and mechanism split into separately weak chunks
- chunk retrievable but strategically neutral where recommendation is required
- chunk boundary changes reader-state meaning

## 10. One-Sentence Summary

Doc 122 governs how content is chunked for retrieval so extracted text stays understandable, strategically faithful, and strong enough to preserve recommendation logic when the page requires more than citation.

---

*End of Document 122*