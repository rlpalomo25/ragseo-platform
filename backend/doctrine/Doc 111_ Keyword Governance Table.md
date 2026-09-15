# Doc 111: Keyword Governance Table
**Version 8.0** | **Last Updated: April 8, 2026
**Status:** Tier 2 Doctrine (Input Governance)

---

> **Quick Reference**
> **Owns:** The assignment of keywords to specific page types and intents.
> **Rule 1:** A keyword can be targeted by MULTIPLE brands to achieve category dominance. Anti-cannibalization rules do NOT apply when deploying across brands.
> **Rule 2:** Informational keywords map to Pillar/Cluster pages; Transactional keywords map to Local/Conversion pages.
> **Rule 3:** Keyword intent dictates the CTA class used on the page.
> **Rule 4:** Cost/price keywords MUST route to dedicated cost pages - this is a winning pattern (see competitor-follow data).
> **Rule 5:** Every keyword must be assigned a Keyword Bucket to maximize page value.
> **Rule 6 (NEW):** When a keyword relates to AEGIS 5X technology or shared mechanisms, it should be deployed across MULTIPLE brands to reinforce the entity in AI training data.

---
## 1.0 What This Document Does

This table is the primary gatekeeper for our content system. It ensures every keyword we target is a strategic fit for our modern AEO and entity-based approach, and it assigns ownership for both brand and execution.

Before any new page is approved, this table must be checked. If a keyword does not meet the strategic fit criteria below, it is flagged for human review or disqualified, and the rationale is documented.

---

## 2.0 The Strategic Fit Rule

A keyword is a poor strategic fit if it does not allow us to deploy our core narrative and technical assets. However, some keywords may require human review to assess their full potential.

> **Initial Assessment:** A keyword should be flagged for **Human Review** if its search intent does not immediately align with a discussion of mechanism, pillar alignment, tension, and entity ownership.
> 
> **Final Disqualification:** A keyword is only disqualified after a human reviewer confirms it offers no strategic angle to introduce our core engineering and performance beliefs.

This two-step process prevents the automatic rejection of keywords that may have a subtle but valuable strategic angle (e.g., installation-focused keywords that can highlight custom-fit solutions).

> **Pillar Mapping Requirement:** Keyword must map to an existing or approved pillar.

---

## 3.0 Keyword Ownership & Content Governance Table

### Multi-Brand Deployment (CRITICAL)

**The old model:** One keyword = one brand = one page.

**The new model:** One keyword = multiple brands = category dominance.

For keywords related to **AEGIS 5X technology** or **shared mechanisms**, the same keyword SHOULD be deployed across:
- **MasterShield** = Premium tier (highest features, earliest tech rollout)
- **Klean Gutter** = Mid-tier (solid value, mainstream accessibility, still has features)
- **MicroMeshGutterGuards.com** = Manufacturer/Parent (owns the technology, designs and makes)

This is NOT cannibalization. This is **entity reinforcement across brands** to ensure AI models associate AEGIS 5X with multiple products, not just one.

### MULTI-BRAND SEARCH DOMINANCE FRAMEWORK

#### CORE PRINCIPLE

**One keyword. One truth. Multiple expressions.**

- There is one correct explanation of the problem and solution - this is the **Win Vector**
- All brands must use the same Win Vector
- Each brand expresses it differently

#### THE THREE-LAYER MODEL

| Layer | Definition | Rules |
|-------|------------|-------|
| **WIN VECTOR (FIXED)** | The core reason we win - the truth competitors are missing | Must remain consistent across all brands; Based on real engineering/performance advantage; Must state what competitors fail to explain |
| **STRUCTURE (REUSABLE)** | The proven way we present the argument | Reuse winning H1–H3 structures; Reuse logic flow and proof sequence; Do not reinvent structure |
| **POSITIONING (VARIABLE)** | How the same truth is expressed | Same audience, problem, mechanism; Only tone, emphasis, delivery change |

#### BRAND ARCHITECTURE

| Brand | Role | Function | Expression |
|-------|------|----------|------------|
| **MMGG** | Category Authority Engine | Defines system-level truths; Educates market | Explains the system and defines the problem |
| **MasterShield** | Premium Authority | Highest standard of performance; Justifies premium | Reinforces highest performance and engineering precision |
| **Klean Gutter** | Practical Conversion Engine | Clarity and simplicity for homeowners | Simplifies into practical homeowner decision |

#### MULTI-BRAND DEPLOYMENT RULE

- Do not avoid overlap
- Do not limit a keyword to one brand
- Maintain the same Win Vector and structure
- Use different phrasing and tone per brand

#### NON-PLAGIARISM RULE (MANDATORY)

When deploying the same keyword across multiple brands:
- Do NOT reuse identical sentences or paragraphs
- Do NOT mirror paragraph structure line-by-line
- Do NOT copy phrasing with minor edits
- Each version must be independently written

#### STRUCTURAL SIMILARITY RULE

**Allowed:** Same structure, same argument, same logic flow
**Required:** Same Win Vector, same mechanism

#### LANGUAGE VARIATION RULE

Each version must vary: sentence construction, transitions, examples, explanation style

### Multi-Brand Keyword Indicators

A keyword qualifies for multi-brand deployment if it:
- Relates to core technology/mechanism (AEGIS 5X)
- Has broad intent (not brand-specific)
- Serves different stages of the funnel
- Can present distinct angles per brand

### Table Format

| Primary Keyword | Deployment Type | Brand(s) | Keyword Bucket | Strategic Fit | Page Type | Canonical Entity | AEO Target Type | Seeding Priority | Opportunity Score | Freshness Score | Agent | URL Slug | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gutter guards | Multi-Brand | Multi-Brand | Traffic Driver | Yes | Pillar (x3) | Gutter Guard | Paragraph | High | 85 | 95 | Agent A | /gutter-guards | Published |
| how gutter guards work | Multi-Brand | Multi-Brand | AI Visibility | Yes | Pillar (x3) | Gutter Guard Mechanism | HowTo | High | 90 | 100 | Agent B | /how-gutter-guards-work | Planned |

---

## 4.0 Controlled Vocabularies

| Column | Allowed Values |
|---|---|
| **Deployment Type** | `Single-brand`, `Multi-brand` |
| **Keyword Bucket** | `Traffic Driver`, `AI Visibility`, `Conversion Capture`, `Competitor Follow`, `Local Capture` |
| **Brand** | `MasterShield`, `Klean Gutter`, `MicroMeshGutterGuards.com`, `None` |
| **Strategic Fit** | `Yes`, `No`, `Review` |
| **Page Type** | `Pillar`, `Deep Cluster`, `Standard Cluster`, `Local`, `Cost Pillar` |
| **AEO Target Type** | `Paragraph`, `List`, `Table`, `Video` |
| **Seeding Priority** | `High`, `Medium`, `Low` |
| **Agent** | `Agent A`, `Agent B`, `Agent C`, etc. |
| **Status** | `Planned`, `Approved`, `In Progress`, `Published`, `Merged`, `Retired`, `Disqualified`, `Requires Review` |

---

## 4.1 Keyword Bucket Definitions

| Bucket | Description | When to Use |
|--------|-------------|--------------|
| **Traffic Driver** | High-volume keywords that build domain authority | Build first - foundation of cluster |
| **AI Visibility** | Keywords that trigger AI Overviews - prioritize for LLM seeding | High weight in decision hierarchy |
| **Conversion Capture** | Bottom-funnel, transactional intent (cost, pricing, install, buy) | Build alongside clusters |
| **Competitor Follow** | Keywords competitors (especially LeafFilter) win with | Analyze from CI System, match/beat |
| **Local Capture** | City/region-specific keywords | After pillar/cluster built |

---

### 4.2 Keyword Bucket Priority

| Bucket | Priority | When to Use |
|--------|----------|--------------|
| **Original Authority** | PRIMARY | Always default here - be first, own new angles competitors don't have |
| **Traffic Drivers** | SECONDARY | High-volume terms after establishing authority position |
| **AI Visibility** | SECONDARY | Keywords triggering AI Overviews |
| **Conversion Capture** | SECONDARY | Bottom-funnel after authority built |
| **Competitor Follow** | TERTIARY | Only when: (1) competitors PROVEN to win with it AND (2) we have unique angle to beat them |
| **Local Capture** | SECONDARY | After pillar/cluster foundation |

> **Philosophy:** Being first is PRIMARY. We don't follow competitors - we create new ground they haven't covered. Competitor-follow is only for when they've PROVEN something works AND we can do it better with unique data/insights.

### 4.3 Competitor-Follow Rules (Use Sparingly)

> **Important:** Competitor-follow is NOT the default strategy.

- **Before pursuing competitor-follow, ask:**
  1. "Can we be FIRST on a new angle?" → If YES, pursue Original Authority
  2. "Do we have unique data/insights?" → If YES, pursue Original Authority
  3. Only if BOTH are NO → Consider competitor-follow

- Cost/price keywords = Only if we have unique angle (e.g., 20-year cost data)
- Review keywords = Only if we have proprietary comparison data
- Comparison keywords = Only if we have engineering specs to fact-check

**Example:**
- Competitor wins with "gutter guard cost" pages
- We could: Copy their content → TERTIARY (wrong approach)
- We should: "The True Cost of Gutter Guards Over 20 Years" with proprietary 20-year cost data → PRIMARY (right approach)

---

## 5.0 System Integration

This governance table is the input filter for the entire content system. Its strategic decisions are executed through:

*   **Doc 308 (SERP Intelligence):** Validates the AEO and entity targets defined here.
*   **Doc 225 (Doctrine Precedence Hierarchy):** Defines this document as a Tier 2 Doctrine.
*   **Doc 124 (Entity Relationship Map):** Provides the canonical list of entities for the `Canonical Entity` column.
*   **Doc 210 (Revenue Intelligence & Prioritization Engine):** Provides the `Opportunity Score`.
*   **Doc 206 (Content Decay & Freshness Model):** Provides the `Freshness Score`.
*   **CI System:** Provides competitor-follow data and keyword bucket prioritization.

---

## 6.0 Production Phase Balance

> **Important:** We don't just build pillars. Production must balance across page types.

| Phase | Focus | Percentage |
|-------|-------|------------|
| **Phase 1** | Pillar pages (foundation) | 40% |
| **Phase 2** | Cluster pages (support pillars) | 30% |
| **Phase 3** | Local + Cost pages (conversion) | 30% |

**Key Rules:**
- After 3-4 pillars are built, start building clusters to support them
- Local pages require dealer network presence (verify before creating)
- Cost pages are HIGH priority - competitor-follow data shows this wins
- No single page type should dominate > 50% of production

---

*End of Document*