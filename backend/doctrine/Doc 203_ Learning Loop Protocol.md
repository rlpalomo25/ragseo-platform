# Doc 203: Learning Loop Protocol

**Document:** 203
**Version:** 3.1
**Last Updated:** April 28, 2026

**Intended For:** Content Manager, SEO Director, All Agents
**Purpose:** This document defines how the system learns from its own outputs. Every piece of content we produce generates data. This protocol ensures that data flows back into the system to improve the next production cycle — closing the loop between what we publish and what we know.

---

## Understanding the Learning Loop

Most content systems are one-directional: produce, publish, forget. This system is different. Every article we publish is a data point. Every ranking change, every CTR shift, every engagement signal tells us something about what works and what doesn't.

The Learning Loop Protocol is the mechanism that captures those signals and converts them into actionable improvements to our doctrine, our templates, and our agent instructions.

---

## 1.0 The Four Learning Inputs

| Input | Source | Frequency |
|---|---|---|
| **Ranking Signals** | Google Search Console, Ahrefs | Weekly |
| **Engagement Signals** | GA4 (Time on Page, Scroll Depth, Bounce Rate) | Weekly |
| **Conversion Signals** | GA4 (Form Fills, Phone Calls, Quote Requests) | Weekly |
| **AI Citation Signals** | Visby.ai (Doc 240) — is our content being cited by AI search? | Bi-weekly |

---

## 2.0 The Learning Loop Cycle

The Learning Loop runs on a 4-week cycle:

### Week 1: Data Collection
The Collector Agent (Doc 307) aggregates all four input signals and produces a Performance Summary. The summary flags any page that has moved more than 3 positions in either direction, or that has changed by more than 20% in CTR or engagement.

### Week 2: Pattern Analysis
The Content Manager reviews the flagged pages and identifies patterns. Questions to answer:
- Which page types are outperforming? (Pillar, Cluster, Local)
- Which AEGIS Guardian references are generating the most engagement?
- Which FAQ structures are being cited by AI search engines?
- Which CTAs are converting at the highest rate?

### Week 3: Doctrine Update
If a consistent pattern is identified (minimum 3 data points), the Content Manager proposes a doctrine update. Doctrine updates require approval from the SEO Director before implementation. Updates are logged in the Doctrine Precedence Hierarchy (Doc 225).

### Week 4: Agent Instruction Update
Once a doctrine update is approved, the relevant agent instructions are updated to reflect the new learning. The Auditor Agent (Doc 328) is updated first, as it is the quality gate for all new content.

---

## SOT FEEDBACK LOOP (Gap Fix)

Performance and engagement data from SOT assets flow back into the system:

| Source | Feeds Back To | Purpose |
|--------|---------------|---------|
| Doc 190 (Publish) | Doc 203, Doc 230 | Performance metrics |
| Doc 336 (Outbound Seeding) | Doc 203, Doc 304, Doc 314 | Citation success patterns |
| Doc 337 (Reactive Seeding) | Doc 203, Doc 304, Doc 354, Doc 357 | Engagement + model training patterns |
| Visby.ai (Doc 240) | Doc 230, Doc 309 | AI citation tracking |

**Trigger:** Monthly review of SOT asset performance → feed winning patterns into Doc 304 (Strategist), Doc 314 (PAA), Doc 354 (SOT Build), Doc 357 (QA).

**Rebuild Trigger:** Parent SOT version change → mark all children stale → return to Doc 356 → regeneration path.

---

## 3.0 Learning Loop Triggers

In addition to the regular 4-week cycle, the Learning Loop can be triggered by:

| Trigger | Who Initiates | Action |
|---|---|---|
| **Major Algorithm Update** | SEO Director | Immediate audit of top 20 pages; pattern analysis within 7 days |
| **Competitor Outranks a Pillar** | Analyst Agent (Doc 300) | Competitive gap analysis; doctrine review within 14 days |
| **AI Citation Rate Drops** | Visby.ai Report | AEO formatting review; update Answer Formatting Doctrine (Doc 121) |
| **Conversion Rate Drops 20%+** | GA4 Alert | CTA and offer review; update Conversion Architecture Module (Doc 140) |

---

## 4.0 What Can and Cannot Be Updated

| Can Be Updated | Cannot Be Updated Without Full Review |
|---|---|
| Agent prompt instructions | Core Belief System (Doc 100) |
| FAQ templates | 5 Engineering Pillars (Doc 100) |
| CTA copy and placement | Brand Voice Guide (Doc 226) |
| AEO formatting rules | Doctrine Precedence Hierarchy (Doc 225) |
| Seasonal content templates | Keyword Governance Table (Doc 111) |

Any update to a "Cannot Be Updated" document requires a formal review meeting with the SEO Director and Brand Manager before implementation.

---

## 5.0 The Learning Log

Every learning is documented in the Learning Log, maintained in the KPI Dashboard (Doc 241). Each entry includes:

- **Date** of the learning
- **Source** (which data input triggered it)
- **Observation** (what the data showed)
- **Action Taken** (what was updated)
- **Result** (measured 30 days after the update)

This log is reviewed quarterly to identify meta-patterns — learnings about our learnings.

---

## 6.0 System Integration

- **Input:** Collector Agent (Doc 307) weekly report, Visby.ai bi-weekly report, GA4 data.
- **Output:** Doctrine updates, agent instruction updates, Learning Log entries.
- **Reviewed By:** Content Manager (weekly), SEO Director (monthly).
- **Escalated To:** SEO Director for any update to a "Cannot Be Updated" document.

---

## 7.0 SIMPLE PERFORMANCE RECORD (MINIMAL VERSION)

**Start here. Do NOT overbuild.**

### Performance Record Per Article

| Field | Source | Notes |
|-------|--------|-------|
| **article_id** | plan_id from Execution Plan | Unique identifier |
| **keyword** | From Execution Plan | Primary target keyword |
| **publish_date** | Publisher | When went live |
| **ranking_position** | GSC/Ahrefs | Current position for target keyword |
| **movement** | Week-over-week | +/– positions |
| **ai_citation** | Visby.ai | Is content cited in AI answers? (yes/no) |
| **top_extracted_section** | Manual review | Which section got pulled by AI |
| **conversions** | GA4 | Did user take action? (yes/no/count) |

**Store in:** Airtable or simple spreadsheet. No dashboard needed yet.

### What to Do With This Data

| Feed Back To | What It Improves |
|--------------|------------------|
| **Doc 300 (Analyst)** | Which topics perform, which don't |
| **Doc 304 (Strategist)** | Which win vectors win, which angles fail |
| **Doc 153 (Execution)** | Which structures get citations, which formats ignored |
| **Doc 316/320/324 (Writer)** | Which blocks get extracted, which don't |

### When This Becomes Powerful

After **20-50 articles**, you'll see:
- Patterns in what wins
- Repeat wins and repeat failures
- Clear signals for upgrade

### When to Upgrade

Only after volume data exists, add:
- Citation pattern tracking
- Win vector performance by brand
- Structure performance by page type

---

## 8.0 EXCEPTION PATH FOR LEARNING

If the system produces content that cannot be measured (e.g., no ranking data, no AI citation possible):
1. Flag as "UNMEASURABLE"
2. Note reason (thin SERP, new keyword, etc.)
3. Do NOT force metrics - some content serves awareness

---

*End of Document*

**Version 3.0 (April 10, 2026):**
- Added Section 7.0: Simple Performance Record (minimal version)
- Added Performance Record per article (plan_id, keyword, publish_date, ranking, movement, ai_citation, top_extracted_section, conversions)
- Added "What to Do With This Data" mapping
- Added When This Becomes Powerful (20-50 articles)
- Added When to Upgrade (after volume data)
- Added Section 8.0: Exception Path for Learning (unmeasurable content)