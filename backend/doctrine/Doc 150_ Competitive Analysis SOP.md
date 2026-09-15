# Doc 150: Competitive Analysis SOP
**Version:** 3.1 | **Last Updated:** June 13, 2026 | **Series:** 150 (Workflow Input)

---

## 1. PURPOSE

This system identifies:

- What drives traffic in the market
- What gets cited by AI systems
- Where competitors win and why
- What we build next (pillars, clusters, local)

This is not research.

This is decision intelligence for ranking, citation, and revenue.

---

## 2. GOVERNANCE OVERRIDE RULE

**Keyword selection and deployment decisions are owned by the Analyst Agent (Doc 300).**

This document provides inputs, not final decisions.

The competitive analysis done here feeds into Doc 300 and Doc 304, but the final keyword selection authority rests with the Analyst Agent per the Multi-Brand Search Dominance Doctrine.

---

## 3. REQUIRED INPUTS

Must collect before proceeding:

| Input | Tool |
|-------|------|
| Traffic + Top Pages | Ubersuggest or Ahrefs |
| AI Citations | Visby.ai |
| Current Queries | GSC |
| Engagement | GA4 |
| SERP Screenshots | Manual (top 5 results per keyword) |

**If any missing → STOP**

---

## 3. COMPETITOR CLASSIFICATION (MANDATORY)

### COMMERCIAL COMPETITORS

| Example | Analyze For |
|---------|-------------|
| LeafFilter | Revenue pages, pricing strategy, conversion structure |
| Gutter Helmet | Product updates, dealer messaging |
| HomeCraft | Content strategy, SEO moves, service areas |
| Raptor Gutter Guard | Pricing, positioning |

### INFORMATIONAL COMPETITORS

| Example | Analyze For |
|---------|-------------|
| This Old House | Ranking structure, answer formatting, citation patterns |

---

## 4. CORE ANALYSIS

### 4.1 TRAFFIC DRIVER ANALYSIS

For each competitor:

- Top pages
- Page type: Pricing | Comparison | Informational | Local
- Primary traffic driver
- Secondary drivers

### 4.2 PAGE STRATEGY PATTERNS

Identify:

- Repeated page types
- Cluster depth
- Topic coverage

**Output:** What they scale → What they ignore

### 4.3 KEYWORD DOMINANCE

- Where competitors rank
- Where they are weak

**Output:** Opportunity zones

---

## 5. AI VISIBILITY ENGINE (AGENT 2 CORE)

This section is mandatory.

### 5.1 ENTITY PROXIMITY

**Output:**

- Competitors associated with: [topics]
- We are NOT associated with: [topics]
- Priority gaps

### 5.2 FACT DENSITY

For top pages:

- Number of extractable facts
- Format: lists | tables | direct answers

**Output:** Required density to compete

### 5.3 ANSWER STRUCTURE

Check:

- Direct answers present?
- Lists used?
- Sections clearly chunked?

**Output:** Required structure

### 5.4 CITATION TRIGGERS AND HIJACK OPPORTUNITIES

Identify why content is cited:

- definition
- comparison
- steps
- stats

**Citation Hijack List (MANDATORY):**
- Identify high-DR third-party sources (e.g., listicles, forums, review sites) where competitors (like LeafFilter) are cited by AI answers, but our brands are excluded.
- List specific domains and URLs to target for outbound seeding (Doc 125).

**Output:** Top 2-3 triggers + Citation Hijack Target List

### 5.5 INFORMATION GAIN

**Output:**

- What competitors say
- What is missing
- What we can add

### 5.6 PARSABILITY CHECK

Must confirm:

- [ ] Short answers
- [ ] Lists
- [ ] Tables

**If missing → required for execution**

---

## 6. CONVERSION SIGNAL ANALYSIS

Identify which pages push:

- pricing
- quotes
- comparisons

**Output:** Revenue-driving topics

---

## 7. COMPETITIVE POSITION OUTPUT (MANDATORY)

### 7.1 CURRENT POSITION

| We are winning in: | [list] |
|-------------------|--------|
| We are losing in: | [list] |
| Competitors dominating: | [list] |

### 7.2 TRAFFIC REALITY

| Primary driver: | [topic] |
|-----------------|---------|
| Secondary drivers: | [list] |

### 7.3 PILLAR OPPORTUNITY MAP

Define **3-5 pillars only.** Each includes:

| Topic | Traffic Value | Conversion Value | Why We Can Win |
|-------|---------------|-------------------|-----------------|
| [topic] | [value] | [value] | [reason] |

### 7.4 CLUSTER SIGNALS

For each pillar: 3-5 supporting topics

### 7.5 KEYWORD DIRECTION

**Output:** 3 primary keywords, 5-10 secondary

Each:

| Keyword | Intent | B2C or B2B | Brand Deployment Strategy |
|---------|--------|-----------|---------------------------|
| [kw] | [intent] | [type] | [Single-brand OR Multi-brand + which brands] |

**Multi-Brand Assignment Rule (MANDATORY)**

Each keyword must define whether it is:
- **Single-brand** OR **Multi-brand**

If multi-brand:
- Specify which brands will deploy
- Explain why this strengthens total search presence

Do not default to single-brand assignment.

### 7.6 CITATION STRATEGY

- What formats to use
- What must be beaten
- Which third-party domains to hijack from competitors (from Section 5.4)

### 7.7 BUILD PHASE DECISION

| If... | Then... |
|-------|---------|
| No pillar published, No ranking presence | Stay in **PILLAR MODE** |
| Pillar exists, 3+ related queries | Move to **CLUSTER MODE** |
| Local pack present, Competitors dominate local | Move to **LOCAL MODE** |
| Competitor traffic proves it, Conversion intent exists, We lack coverage | **ADD NEW PILLAR** |

### 7.8 REQUIRED NEXT STEP

Choose ONE:

- [ ] Keyword Selection & Prioritization SOP
- [ ] Re-run analysis
- [ ] Escalate to Advisory Agents

---

## 8. WEEKLY EXECUTION CONSTRAINTS

| Limit | Rule |
|-------|------|
| Max 3 primary keywords | Reject if exceeded |
| Max 9 pages | Reject if exceeded |
| Max 3 active pillars | Reject if exceeded |

---

## 9. OUTPUT RULES

- Max 500 words
- Bullet-based
- No opinions
- No fluff

---

## 10. VALIDATION

Must confirm:

- [ ] Data complete
- [ ] Patterns identified
- [ ] Pillars defined
- [ ] Keywords selected
- [ ] AI visibility signals present

**If not → FAIL**

---

**FINAL TRUTH**

This document now does 3 things:

1. Shows where you stand
2. Shows what is winning
3. Forces what to do next