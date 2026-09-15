# CI System - AI Track
**Version 1.0** | **Last Updated: April 4, 2026**
**Purpose:** Track and improve brand visibility in AI Answer Engines (ChatGPT, Perplexity, Google AI Overviews). Complement the Traditional Track with AI-specific competitive intelligence.

> **Playbook Phase Reminder:** This document governs the **AI Visibility** phase. Run AFTER the Traditional Track Mode 2-3 (data collection) is complete. Connects to Agent 2 (The Visibility Hacker).

---

## 1.0 WHY ENGINE 9B EXISTS

Traditional SEO measures Google rankings. AI competitive intelligence measures **AI citation dominance**.

| Traditional (CI Traditional) | AI (CI AI) |
| :--- | :--- |
| Rankings (position 1-10) | Citations (is your brand in the answer?) |
| Organic traffic | AI traffic (unnamed, growing) |
| SoV (click share) | AIVS (AI Visibility Score) |
| Backlinks | Brand mentions in AI responses |
| Featured Snippets | AI Overview sources |

**Run both:** CI Traditional and CI AI are parallel tracks. Neither replaces the other.

---

## 2.0 GLOSSARY

| Term | Definition |
| :--- | :--- |
| **AIVS (AI Visibility Score)** | Your % of AI Overview citations vs. competitors |
| **Citation Rate** | % of tested prompts where your brand appears in AI answer |
| **Citation Position** | Where your brand appears (1st = primary source, 2-5 = supporting) |
| **Unprompted Brand Mention** | AI mentions your brand without brand name in prompt |
| **AI Overview Source** | Domain cited in Google's AI Overview answer |
| **Prompt Category** | TOFU (problem-aware), MOFU (solution-aware), BOFU (brand-aware) |
| **LLM Pickup** | Your content is used as source by ChatGPT/Perplexity |
| **Entity Proximity** | Semantic closeness between your brand and target concepts |

---

## 3.0 MODE 0: PREREQUISITES

Before running CI AI, confirm:

| Check | Requirement |
| :--- | :--- |
| Visby.ai configured | Project set up with your domain + competitors |
| Competitor set aligned | Same 3-5 competitors as CI Traditional |
| Prompt library loaded | TOFU/MOFU/BOFU prompts entered in Visby |
| Export capability | Can export AI Visibility CSV |

**All YES → Proceed Mode 1**

---

## 4.0 MODE 1: VISBY DATA COLLECTION

### 4.1 Weekly Export from Visby.ai

| Export | Filename | Contains |
| :--- | :--- | :--- |
| Brand Visibility Report | `Visby_brand_visibility_YYYY-MM-DD.csv` | Prompt, Your Brand (Y/N), Comp1, Comp2, Comp3, Position |
| AI Overview Citations | `Visby_aio_citations_YYYY-MM-DD.csv` | Keyword, Source1, Source2, Source3, Your Site Cited (Y/N) |
| Perplexity Citations | `Visby_perplexity_YYYY-MM-DD.csv` | Prompt, Sources, Your Brand Mentioned (Y/N) |
| ChatGPT Citations | `Visby_chatgpt_YYYY-MM-DD.csv` | Prompt, Sources, Your Brand Mentioned (Y/N) |

### 4.2 Manual AI Overview Check (Backup)

If Visby export delayed, manually check:

1. Open Google incognito
2. Search 5 money terms (from CI Traditional)
3. Capture: Which sites are in AI Overview?
4. Screenshot each SERP

---

## 5.0 MODE 2: DATA VALIDATION

| Check | YES/NO |
| :--- | :--- |
| Visby export has ≥ 20 prompts tested | |
| All competitors present in export | |
| Date within 7 days | |
| AI Overview data included | |
| Perplexity/ChatGPT data included | |

**PASS → Proceed Mode 3**

**FAIL → Re-download or note manual backup**

---

## 6.0 MODE 3: AI KPI ANALYSIS

### 6.1 AI Overview Citation Dashboard

| Metric | Your Value | Comp Avg | Gap | Status | Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Total Prompts Tested | 50 | 50 | - | - | Baseline |
| Your Citations | 12 | 8 | +4 | GREEN | It's GREEN because you exceed comp avg by 4 |
| Citation Rate | 24% | 16% | +8pp | GREEN | Above 15% threshold |
| Avg Citation Position | 2.3 | 2.8 | +0.5 | GREEN | Closer to primary source (1) |
| Primary Source Rate | 20% | 12% | +8pp | GREEN | Most-cited position |

**Status Rules:**
| Status | Rule |
| :--- | :--- |
| GREEN | Citation Rate ≥ Comp Avg + 5pp OR Primary Source Rate ≥ 15% |
| YELLOW | Within ±5pp of Comp Avg |
| RED | Citation Rate < Comp Avg - 5pp OR Not cited at all |
| GRAY | < 10 prompts tested |

---

### 6.2 Perplexity/ChatGPT Dashboard

| Engine | Your Citation Rate | Comp Avg | Status | Notable Pattern |
| :--- | :--- | :--- | :--- | :--- |
| Perplexity | 18% | 10% | GREEN | Strong BOFU mentions |
| ChatGPT | 12% | 14% | YELLOW | Comp B dominant |

---

### 6.3 Funnel Breakdown

| Prompt Category | Prompts Tested | Your Citation Rate | Comp Avg | Status |
| :--- | :--- | :--- | :--- | :--- |
| TOFU (Problem Aware) | 15 | 8% | 12% | RED |
| MOFU (Solution Aware) | 20 | 22% | 18% | GREEN |
| BOFU (Brand Aware) | 15 | 40% | 25% | GREEN |

**Insight:** TOFU is RED - competitors are winning educational queries in AI. Need E4 to create AI-targeted educational content.

---

### 6.4 Unprompted Brand Mentions

| Metric | Value | Status | Meaning |
| :--- | :--- | :--- | :--- |
| Unprompted % | 8% | YELLOW | AI mentions you without brand query |
| Trend | +2% MoM | - | Improving |

**What this means:** When users ask "what are the best gutter guards?" (no brand), AI mentions you 8% of the time. This is organic authority.

---

### 6.5 Competitor AI Analysis

| Competitor | AI Citation Rate | Primary Source Rate | TOFU | MOFU | BOFU | Pattern |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Comp A | 28% | 22% | 18% | 30% | 35% | Strong BOFU, owns brand queries |
| Comp B | 22% | 15% | 25% | 20% | 20% | Strong TOFU - winning educational |
| Comp C | 8% | 4% | 5% | 10% | 10% | Weak across all stages |

**Pattern Teaching:** Comp B is winning TOFU in AI because they publish "what is..." content that AI finds authoritative. If you're RED on TOFU, study Comp B's content structure.

---

## 7.0 MODE 4: LOW-HANGING FRUIT FOR AI

### 7.1 AI Citation Opportunities (Page 2 → Citation)

| Keyword/Query | Your Status | Comp Citing | Gap | Action |
| :--- | :--- | :--- | :--- | :--- |
| "how to clean gutters" | Not cited | Comp A, Comp B | Missing from AI | Add to AI content queue |
| "best gutter guard for pine trees" | Position 3 | Comp A (pos1) | Need primary | Optimize for citation |
| "gutter guard cost" | Not in AI | Comp B | Zero presence | Create pricing FAQ |

---

### 7.2 Content Format Opportunities

AI engines prefer certain formats. Analyze what's winning:

| Format | Comp Using | AI Prefers | Your Coverage | Action |
| :--- | :--- | :--- | :--- | :--- |
| FAQ schema | Comp A, B | YES | YES | Expand |
| Step-by-step lists | Comp B | YES | NO | Add |
| Comparison tables | Comp A | YES | Partial | Enhance |
| Definition boxes | Comp B | YES | NO | Add |

---

## 8.0 MODE 5: LLM SEEDING OPPORTUNITIES

Per Doc 125 (LLM Seeding Protocol), identify where to increase AI visibility:

| Opportunity | Source | Action | Owner | ETA |
| :--- | :--- | :--- | :--- | :--- |
| TOFU citation gap | CI AI analysis | Create "what is..." educational content | E4 | 7 days |
| CI AI | Agent 2 (E5) | AI citation gaps, format opportunities | Weekly |
| CI AI | E4 | TOFU content needs | Weekly |
| CI AI | Doc 125 | LLM Seeding triggers | When RED |
| CI AI | Doc 210 | AI opportunity scores | Monthly |

---

## 10.0 MONTHLY AI DELIVERABLES (EOM+5)

### 1. AI Citation Cascade Report
| Keyword | AI Answer | Primary Source | You Cited (Y/N) | Position | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |

### 2. Competitor AI Content Audit
| Competitor | AI-Optimized Pages | Schema Usage | Format Type | What's Working |
| :--- | :--- | :--- | :--- | :--- |
| Comp A | 12 | Full | FAQ + Tables | Comparison content |

### 3. LLM Seeding Priority List
| Page | Current AI Status | Seeding Action | Expected Lift | Owner |
| :--- | :--- | :--- | :--- | :--- |
| /gutter-guards | Cited, not primary | Add 5 new facts | +10% citation rate | E4 |

### 4. AI Visibility Trend Chart
- 3-month rolling AIVS
- Citation rate by funnel stage
- Competitor comparison

---

## 11.0 INTEGRATION WITH DOC 311 (Agent 2)

CI AI feeds Agent 2 (The Visibility Hacker) data. Per Doc 311 directives:

| Agent 2 Directive | CI AI Output |
| :--- | :--- |
| Semantic Structuring Tweaks | Format opportunities, schema gaps |
| LLM Seeding Opportunities | Citation opportunities, unprompted tracking |
| Entity Proximity | TOFU/MOFU/BOFU analysis |
| Information Gain | What unique facts are you providing? |

---

## 12.0 ARTIFACTS

| Artifact | Filename |
| :--- | :--- |
| Visby Export | `visby_export_YYYY-MM-DD.csv` |
| AI Overview Screenshots | `aio_screenshot_[keyword].png` |
| Weekly Report | `Engine9B_Weekly_Report_YYYY-MM-DD.md` |
| Monthly Deliverables | `Engine9B_Monthly_YYYY-MM.md` |

---

## 13.0 CONSTRAINTS

| Scenario | Handling |
| :--- | :--- |
| No Visby API | Manual exports weekly, note in report |
| New to AI search | First 4 weeks = baseline only, no REDs |
| SERP volatility (AI changes often) | Note "AI landscape shifting" in report |
| Competitor data limited | Use available data, mark GRAY |

---

*End of CI System - AI Track v1.0*

**Next:** Create the SEO & AI Search Watch Report system.