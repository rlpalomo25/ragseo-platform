# CI System - Traditional Track
**Version 7.0** | **Last Updated: April 4, 2026**
**Purpose:** Guide novice SEO analysts through weekly competitive analysis and monthly reporting. Transform raw competitor data into actionable intelligence for E4 E5 E6. Run alongside the AI Track (CI System - AI).

> **Playbook Phase Reminder:** This document governs the **Competitive Analysis** phase of the production workflow. Part of the unified Competitive Intelligence System.

---

## GLOSSARY (Glossary-First Language)

| Term | Definition |
| :--- | :--- |
| **SoV (Share of Voice)** | Percentage of total clicks captured by your site vs. competitors. NOT "SoV" (capital V). |
| **DA** | Domain Authority (Moz) - 0-100 predictive ranking score |
| **RD** | Referring Domains - unique domains linking to a site |
| **DA40plus** | RDs with DA ≥ 40 |
| **DA60plus** | RDs with DA ≥ 60 |
| **FS** | Featured Snippet - Position zero answer box |
| **PAA** | People Also Ask - question boxes in SERP |
| **AI Overview** | Google's AI-generated answer that cites 3-5 sources |
| **Money Terms** | Keywords where YOU and competitors both rank 1-20 |
| **Low-Hanging Fruit** | Keywords where you rank 11-20 but could move to 1-10 |
| **Vanity Keywords** | High-volume, highly competitive keywords (aspirational, not immediate) |
| **RED** | Urgent item requiring action by EOM+5 |
| **MoM** | Month-over-month (last month to this month) |
| **YoY** | Year-over-year (same month last year to this month) |
| **pp** | Percentage points - absolute difference (10 to 15 = +5pp, not +50%) |
| **CWV** | Core Web Vitals - LCP, CLS, INP |
| **LCP** | Largest Contentful Paint - load time target ≤ 2.5s |
| **CLS** | Cumulative Layout Shift - stability target ≤ 0.1 |
| **INP** | Interaction to Next Paint - responsiveness target ≤ 200ms |
| **CTR** | Click-through rate - pos1 ~30%, pos10 ~2% |
| **EEAT** | Experience, Expertise, Authority, Trust |
| **AIVS** | AI Visibility Score - percentage of AI Overview citations vs. competitors |
| **Citation Rate** | Percentage of prompts where your brand is cited in AI answers |
| **Entity Proximity** | Semantic distance between your brand and target concepts in vector space |

---

## COLOR STATUS EXPLANATIONS

Traffic-light statuses are not arbitrary. Each color has a mathematical rule:

### SoV Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | Your SoV ≥ Comp Avg + 2pp | You're winning more than average. Action: Maintain. |
| **YELLOW** | Within ±2pp of Comp Avg | Parity. Action: Watch for movement. |
| **RED** | Your SoV < Comp Avg - 2pp | Losing share. Action: Investigate quickly. |
| **GRAY** | < 200 clicks (insufficient data) | Sample too small for confidence. Action: Note, exclude from averages. |

### Top-10 Coverage Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | ≥ Comp Avg + 5pp | Strong top-10 presence. |
| **YELLOW** | Within ±5pp | Adequate but not dominant. |
| **RED** | < Comp Avg - 5pp | Significant gap. |
| **GRAY** | < 10 terms | Insufficient keywords to measure. |

### FS/PAA Share Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | ≥ 15% | Dominating SERP features. |
| **YELLOW** | 5-14% | Present but not dominant. |
| **RED** | < 5% | Missing from SERP features. |
| **GRAY** | < 10 terms | Insufficient data. |

### DA Velocity Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | Gap closing MoM | Authority growing faster than competitors. |
| **YELLOW** | Stable (no significant change) | Maintaining position. |
| **RED** | Gap widening | Losing authority relative to market. |
| **GRAY** | < 3 months data | Insufficient history to measure velocity. |

### Net-New RDs Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | ≥ Comp Avg | Winning link acquisitions. |
| **YELLOW** | 50-99% of Comp Avg | Acceptable but below average. |
| **RED** | < 50% of Comp Avg | Behind in link building. |
| **GRAY** | < 3 comps | Insufficient competitor data. |

### Avg Position Delta Status
| Status | Rule | Why |
| :--- | :--- | :--- |
| **GREEN** | Improved ≥ 1 position | Ranking gains. |
| **YELLOW** | Stable (±0.5 position) | No significant change. |
| **RED** | Declined ≥ 1 position | Ranking losses. |
| **GRAY** | < 10 keywords | Insufficient data. |

---

## CONVERSION IMPACT CONTEXT

Every keyword opportunity is tied to revenue. Remind analysts of this connection:

| Metric | Current | Target | Revenue Impact |
| :--- | :--- | :--- | :--- |
| **Local Conversion Rate** | 0.5% | 3-4% | $195/appointment |
| **Dealer Sales** | - | - | $5,000-$6,500/sale |
| **Page 2 → Page 1 Move** | - | - | +20-30% traffic to that keyword |
| **Low-Hanging Fruit Volume** | - | - | New leads = volume × 3% × $195/mo × 12 |

---

## MODE 0: PREREQUISITE CHECK

> **Playbook Phase:** Foundation Validation

**Before starting competitive analysis, confirm Phase 1 is complete:**

| Check | Requirement | Action if NO |
| :--- | :--- | :--- |
| E1 - Technical SEO | Crawl errors < 5% | Stop - complete Tech SEO first |
| E2 - UX/CRO | Conversion rate 0.5% → 3-4% | Stop - optimize conversion first |
| E10 - Site Speed | CWV Pass: LCP ≤2.5s, CLS ≤0.1, INP ≤200ms | Stop - fix performance first |
| E11 - Security | HTTPS + backups | Stop - secure site first |

**All YES → Proceed to Mode 1**

**After first time, simply ask:** "Any foundation status changes since last week?"
- NO → Proceed Mode 1
- YES → Note in Dashboard, alert Head SEO

---

## MODE 1: SETUP VALIDATION

> **Playbook Phase:** Data Source Configuration

| Check | Requirement | Action if NO |
| :--- | :--- | :--- |
| Ubersuggest | Project created | Create project |
| Competitors | 3+ competitors configured | Add competitors |
| Export capability | Can export PDFs and CSVs | Verify export settings |

**All YES → Proceed to Mode 2**

**Any NO → STOP - fix gaps before proceeding**

---

## MODE 2: DATA COLLECTION

> **Playbook Phase:** Raw Data Gathering

### CRITICAL FILE NAMING

Ubersuggest uses generic filenames. **Rename by company before upload.**

### Workflow: Company-by-Company, Not Report-by-Report

Process all data for one competitor before moving to the next. This builds pattern recognition.

### Max 10 Files Per Upload | Direct Competitors Only (5 max weekly) | Informationals (monthly only)

### Per Competitor (Including Your Domain):

**1. Traffic Overview PDF**
- Path: Competitive Research → Traffic Overview
- Export: Top right down arrow
- Contains: DA, Total Backlinks, Organic Keywords, Traffic
- Filename: `CompName_Traffic_Overview.pdf`

**2. Keywords by Traffic CSV**
- Path: Competitive Research → Keywords by Traffic
- Sort: Est Visits
- Export: Square gray button "KEYWORDS" → "Export Selected"
- Contains: Keyword, Position, URL, Visits
- Filename: `CompName_Keywords_Traffic.csv`

**3. Backlinks PDF + CSV**
- Path: Link Building → Backlink Overview
- Filter: "New This Month"
- Export: PDF (top right), CSV (Backlinks section)
- Contains: New RDs, DA40plus, DA60plus
- Filename: `CompName_Backlinks_Overview.pdf`, `CompName_backlinks.csv`

**4. FS/PAA/AI Overview Manual Check**
- Open Google Search incognito
- Search 2-3 money terms
- Note: Featured Snippet owner, PAA questions, AI Overview sources (is YOUR site cited?)
- Screenshot: `Keyword_SERP_Screenshot.png`

**5. Visby.ai Export (NEW 2026)**
- Path: Brand Visibility → AI Overview Citations
- Export: CSV
- Contains: Prompt, Your Brand Cited (Y/N), Competitors Cited, Citation Position
- Filename: `CompName_AI_Visibility.csv`

---

## MODE 3: DATA VALIDATION

> **Playbook Phase:** Quality Assurance

### 6-Point Validation Checklist

| # | Check | YES/NO |
| :--- | :--- | :--- |
| 1 | Competitor Set: 3+ competitors | |
| 2 | DA & Backlinks: All domains have values | |
| 3 | New RDs: All domains have "This Month" counts | |
| 4 | Keywords: 10+ per domain with Position + URL | |
| 5 | FS/PAA/AI Overview: 2+ terms with owner + questions | |
| 6 | Date: Current within 7 days | |

**PASS → Proceed to Mode 4**

**FAIL → List gaps, re-download, fix before proceeding**

---

## MODE 4: KPI ANALYSIS

> **Playbook Phase:** Insight Generation

### 8-Section Report Structure

---

### Section 1: COMPETITIVE SNAPSHOT

2-3 sentences plain English. Summarize the market position this week.

---

### Section 2: KPI DASHBOARD

#### 2.1 Share of Voice (SoV) - Non-Branded

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your SoV | X% | COLOR | It's COLOR because [rule application]. This means [impact]. |
| Comp Avg SoV | X% | - | Average of all competitors |
| MoM Change | +Xpp / -Xpp | - | Direction and magnitude |

**Why this matters:** SoV measures your percentage of total clicks in your competitive set. If you're at 25% and competitors average 20%, you're capturing more than your fair share.

---

#### 2.2 Top-10 Coverage

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your % | X% | COLOR | It's COLOR because [rule]. This means [impact]. |
| Comp Avg % | X% | - | - |
| MoM Change | +Xpp / -Xpp | - | - |

---

#### 2.3 FS/PAA Share

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your % | X% | COLOR | It's COLOR because [rule]. This means [impact]. |
| Comp Avg % | X% | - | - |
| MoM Change | +Xpp / -Xpp | - | - |

---

#### 2.4 DA Velocity

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your DA | X | COLOR | It's COLOR because [rule]. This means [impact]. |
| Comp Avg DA | X | - | - |
| Gap | X points | - | Your DA minus Comp Avg |
| MoM Change | +X / -X | - | - |

---

#### 2.5 Net-New RDs

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your New RDs | X | COLOR | It's COLOR because [rule]. This means [impact]. |
| DA40plus | X | - | High-quality new links |
| DA60plus | X | - | High-authority new links |
| Comp Avg | X | - | - |
| MoM Change | +X / -X | - | - |

---

#### 2.6 Avg Position Delta

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| Your Avg Pos | X.X | COLOR | It's COLOR because [rule]. This means [impact]. |
| MoM Change | +X.X / -X.X | - | - |

---

#### 2.7 AI VISIBILITY (NEW 2026) - From Visby.ai

| Metric | Value | Status | Explanation |
| :--- | :--- | :--- | :--- |
| AI Overview Citation Rate | X% | COLOR | It's COLOR because [rule]. This means [impact]. |
| Competitors Cited Avg | X | - | How many competitors appear in AI Overviews |
| Perplexity Citation Rate | X% | COLOR | - |
| ChatGPT Citation Rate | X% | COLOR | - |
| Your Brand Unprompted % | X% | - | Times AI mentions you without brand query |

---

### Section 3: PER-COMPETITOR FEEDBACK

For EACH competitor (even if no change - teach pattern recognition):

| Competitor | DA | New RDs | Top Movers (Keywords ↑/↓) | Notable Actions | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Comp A | 45 | +3 | "+gutter guards" ↑5 | New FS captured | YELLOW |
| Comp B | 62 | +12 | "+best gutter guard" ↑2 | AI Overview citation | GREEN |
| Comp C | 38 | +1 | No significant moves | - | GRAY |

**Pattern teaching:** If Comp B suddenly appeared in AI Overviews, what did they publish? This is what you should learn to spot.

---

### Section 4: LOW-HANGING FRUIT (Page 2 → Page 1)

> **Important:** Low-hanging fruit is an INPUT to prioritization, not the DECISION. The Strategist Agent weighs this against traffic volume, AI visibility, and pillar alignment.

**Data-Driven Prioritization (ranked by weight):**

| Factor | Weight | Source |
|--------|--------|--------|
| **Traffic Volume** | Highest | Ubersuggest/GSC - what are people actually searching? |
| **AI Search Visibility** | High | Visby - where are competitors being cited in AI? |
| **Pillar Alignment** | High | Does this support the cluster architecture? |
| **Low-Hanging Position** | Medium | Are we 11-20? Can we move to 1-10? |
| **Competitor Gap** | Medium | Who dominates? Can we win? |

**Example (your scenario):**
- Keyword A: "gutter guards" | Pos 6 | Volume 8,100 | AI cited = YES → **PRIORITY** (pillar, high traffic, AI visible)
- Keyword B: "micro mesh gutter guard" | Pos 14 | Volume 1,200 | AI cited = NO → Consider after pillar built

**Low-Hanging Table** (informational - feed to Strategist, don't auto-prioritize):

| Keyword | Your Pos | Comp Pos | Volume | Difficulty | AI Cited? | Why You Can Win | Expected Impact |
|---------|-----------|----------|--------|------------|-----------|-----------------|-----------------|
| gutter guard installation | 14 | 8 | 1,200 | 45 | Check | You have better content structure | +240 visits/mo |

**Convert to Revenue:**
- New visitors = Volume × (Target CTR - Current CTR)
- New leads = New visitors × 3%
- Appointment revenue = New leads × $195/mo × 12
- Dealer revenue = New leads × $1,038-1,058/mo × 12

---

### Section 4B: KEYWORD BUCKETS (Page Value Maximization)

Not all keywords are equal. Categorize by strategic purpose:

| Bucket | Purpose | Example | Priority |
|--------|---------|---------|----------|
| **Original Authority** | Be first - own new angles competitors don't have | Our unique engineering (AEGIS 5X) | PRIMARY |
| **Traffic Drivers** | High volume, build authority | "gutter guards" (8,100/mo) | SECONDARY |
| **AI Visibility** | Win AI citations | Keywords triggering AI Overview | SECONDARY |
| **Conversion Capture** | Bottom-funnel, high intent | "gutter guard cost", "installers near me" | SECONDARY |
| **Competitor Follow** | Only if competitors win with it - match/beat | What LeafFilter ranks for | TERTIARY - only when proven |
| **Local Capture** | City-specific intent | "gutter guards Charlotte NC" | SECONDARY |

> **Philosophy:** Being first is PRIMARY. We create content competitors don't have - own new angles, unique data, proprietary insights. Competitor-follow is TERTIARY - only when competitors have proven a keyword type works AND we have a unique angle to do it better.

**Rule:** Every page should target at least one keyword bucket. The bucket determines content strategy.

---

### Section 4C: COMPETITOR-FOLLOWING STRATEGY (TERTIARY)

> **Important:** Being first is PRIMARY. Competitor-follow is only for keywords competitors have PROVEN work - never the default strategy.

**Philosophy:** We create content competitors don't have - own new angles, unique data, proprietary insights. Competitor-follow is TERTIARY - only when:
1. Competitors have PROVEN a keyword type works (they get traffic)
2. We have a UNIQUE ANGLE to do it better (not just copy)

**When to use competitor-follow:**
- Competitor has high traffic from a keyword type AND
- We have proprietary data, better format, or unique angle to outrank them

**When NOT to use competitor-follow:**
- Just because a competitor ranks for something doesn't mean we should copy
- We want to WIN new ground, not play catch-up on their terms

**How to identify opportunities (use sparingly):**

1. **Traffic Analysis:** What pages does LeafFilter (or competitor) get the most traffic from?
2. **Content Audit:** What content types are they winning with? (e.g., cost pages, reviews, comparisons)
3. **AI Citation Audit:** Are they being cited in AI Overviews for certain keywords?

**The Test:** Before pursuing competitor-follow, ask:
- "Is this a space where we can be FIRST on a new angle?"
- "Do we have unique data/insights competitors don't have?"
- If YES to either → Pursue ORIGINAL AUTHORITY instead
- If NO to both → THEN consider competitor-follow

**Example:**
- Competitor wins with "gutter guard cost" pages
- We could: Copy their content → TERTIARY
- Or: Create "The True Cost of Gutter Guards Over 20 Years" with proprietary 20-year cost data → PRIMARY (Original Authority)

**Note:** Competitor-follow is NOT copying. It's identifying winning patterns where we have a superior angle.

---

### Section 5: KEYWORD CLUSTER ANALYSIS

| Cluster | Comp | Theme | Keywords (5-10) | Avg Pos | Landing Page | Traffic | What's Effective | Your Coverage | Opportunity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Gutter Protection | Comp A | Product | "gutter guards", "gutter covers" | 8.2 | /gutter-guards | 450 | Word count, schema | YES | Medium |

---

### Section 6: THREE MOVES

Three priority actions this week:

| # | Action | Owner | ETA | Impact |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Optimize Page 2 → Page 1 keywords | E4 | 3 days | High |
| 2 | Fix RED SoV keyword gaps | E5 | 5 days | Medium |
| 3 | Pursue Competitor B's new RDs | E6 | 7 days | Medium |

---

### Section 7: REDs (Issues Requiring Action by EOM+5)

| Metric | Page/Query | Action | Owner | Due | Expected Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SoV RED | "gutter guard reviews" | Content refresh | E4 | EOM+5 | +2pp SoV |
| FS/PAA RED | "how to install gutter guards" | New FS-targeting content | E5 | EOM+5 | +5% FS share |

---

### Section 8: EXECUTIVE SUMMARY

2-3 lines maximum. What does the Head SEO need to know?

> "This week we gained +3pp SoV on money terms, driven by Page 2→Page 1 wins. Comp B is capturing AI Overview citations - we need E5 to analyze their content structure. Two REDs require immediate attention: SoV gap on 'gutter guard reviews' and missing FS on 'how to install.'"

---

### Artifacts to Save

| Artifact | Filename |
| :--- | :--- |
| Traffic PDFs | CompName_Traffic_Overview.pdf |
| Keywords CSVs | CompName_Keywords_Traffic.csv |
| Backlinks PDFs/CSVs | CompName_Backlinks_Overview.pdf, CompName_backlinks.csv |
| SERP Screenshots | Keyword_SERP_Screenshot.png |
| AI Visibility CSVs | CompName_AI_Visibility.csv |
| Report | Engine9_Weekly_Report_YYYY-MM-DD.md |

---

## MODE 5: QUALITY CHECK

> **Playbook Phase:** Quality Assurance

### 20-Point Rubric

| Category | Points | Criteria |
| :--- | :--- | :--- |
| **Accuracy** | 4 | Numbers match sources, Deltas correct, Lights match rules, Math correct |
| **Completeness** | 3 | All 8 sections, All KPIs, All competitors |
| **Deltas** | 3 | MoM shown in pp or positions, Explained |
| **Actionability** | 3 | Moves have owners, ETAs, Impact estimates |
| **Artifacts** | 3 | PDFs saved, CSVs saved, Screenshots saved, Report saved |
| **Handoffs** | 2 | REDs routed to correct agents, Checklist complete |
| **Major Events** | 2 | Events logged, Correlated with changes |

**Score ≥ 18/20 → PASS**

**Score < 18/20 → FAIL (list gaps, fix, re-score)**

---

## MODE 6: HANDOFF CONFIRMATION

> **Playbook Phase:** Routing

| Item | Route To | Complete? |
| :--- | :--- | :--- |
| SoV REDs | E4 (Content) | YES/NO |
| FS/PAA REDs | E5 (AEO) | YES/NO |
| Backlink REDs | E6 (Link Building) | YES/NO |
| KPIs logged (15 cols) | System | YES/NO |
| Head SEO notified | Leadership | YES/NO |

**All YES → Complete**

**Any NO → Fix before closing**

**Recurring REDs (3+ months) → Escalate to E12**

---

## CONSTRAINTS & EXCEPTIONS

| Scenario | Handling |
| :--- | :--- |
| Sample Size < 200 clicks | GRAY status, exclude from averages |
| MoM | Use weekly data, YoY only for seasonal context |
| Competitor Set | Priority to top 5 by DA, SoV; informationals monthly |
| Traffic-Light Freeze | Algorithm update = freeze 14 days |
| Data Sparsity | < 10 keywords = exclude from averages |
| Manual Overrides | Log with major events, adjust explanations |
| Seasonality | Use 3-month rolling median |
| SERP Volatility | Freeze 14 days, note in report |
| Data Sparsity | Exclude and note in report |

---

## CROSS-ENGINE HANDOVERS

| From | To | What | When |
| :--- | :--- | :--- | :--- |
| E9 | E4 | Beat Page briefs | Monthly |
| E9 | E4 | Low-hanging fruit opps | Weekly |
| E9 | E4 | New page opportunities | Weekly (if RED) |
| E9 | E5 | Snippet/PAA gaps | Monthly |
| E9 | E5 | AI Overview capture opps | Weekly (if RED) |
| E9 | E6 | Outreach list | Monthly |
| E9 | E6 | Overlap domains (2+ comps) | Monthly |
| E9 | E12 | Recurring REDs 3+ months | Immediate |
| E8 | E9 | Major Events Log | Correlate with changes |

---

## MONTHLY DELIVERABLES (EOM+5)

### 1. Beat Page Briefs (12 points)
| Target Kw | Our URL | Comp URL | SERP Map | Outline (+20%) | Title | H1 | Meta | FAQs | Schema | Internal Links | Media | EEAT | CTA | Owner | ETA | Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

### 2. Snippet & PAA Gaps
| Keyword | FS Owner | PAA Owner | Our URL | Answer (40-60w) | Title | Meta | Schema | QA Impact |

### 3. Outreach List (CSV)
| Domain | DA | Links Comp1 | Links Comp2 | Links Comp3 | Overlap | Topical Fit (0-3) | Page Type | Difficulty (0-3) | Contact | Pitch |

**Priority:** Overlap ≥ 2, DA ≥ 40, Topical Fit = 3

### 4. Cluster Opportunities
| Competitor | Theme | Keywords (5-10) | Avg Pos | Page | Traffic | Effective | Coverage | Opportunity | Impact |

---

## IS THIS ALL WORTH HAVING?

**Yes, if:**
- You have the data sources (Ubersuggest, Visby, GSC, GA4)
- You have the time (analyst needs 2-4 hours/week for weekly, 4-6 hours/month for monthly)
- You have the team (E4/E5/E6 agents to receive handoffs)

**Simplify if:**
- New site (< 6 months) → Start with Mode 0-3 only, skip monthly until you have data
- Single brand → Reduce competitor set to 3
- No Visby yet → Use manual AI Overview checks, note as "manual" in report

**The 2026 update adds:**
- AI Visibility metrics (from Visby)
- Perplexity/ChatGPT tracking
- Cross-engine handoffs to Agent 2 (E5)
- Monthly AI-specific deliverables

---

*End of CI System - Traditional Track v7.0*