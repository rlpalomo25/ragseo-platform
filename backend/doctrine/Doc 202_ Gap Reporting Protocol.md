# Doc 202: 

**Document:** 308
**Version:** 1.1
**Last Updated:** August 6, 2026 | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).

**Intended For:** Collector Agent (Doc 307), Content Manager, SEO Director
**Purpose:** This document defines how content gaps — missing pages, underperforming pages, and uncovered keywords — are identified, documented, and escalated for production.

---

## Understanding the Gap Reporting System

A gap is any place where a user's question goes unanswered by our content. Gaps are not failures — they are opportunities. This protocol ensures every gap is captured, categorized, and routed to the correct production queue before a competitor fills it.

The Gap Reporting Protocol runs on a weekly cadence and feeds directly into the Analyst Agent (Doc 300) and the Revenue Intelligence Engine (Doc 210).

---

## 1.0 Gap Categories

| Gap Type | Definition | Priority |
|---|---|---|
| **Missing Pillar** | A high-volume keyword cluster has no parent pillar page | Critical |
| **Missing Cluster** | A Decision Axis keyword has no dedicated cluster page | High |
| **Missing Local** | A market with active dealer coverage has no local page | High |
| **Underperforming Page** | A page ranking in positions 11–30 with no recent optimization | Medium |
| **Cannibalization Risk** | Two pages competing for the same keyword | Medium |
| **Stale Content** | A page with citations older than 18 months | Low |
| **Orphaned Page** | A page with zero inbound internal links | Low |

---

## 2.0 Gap Detection Sources

Gaps are identified from four data sources, checked weekly:

1. **Google Search Console (GSC):** Queries with impressions but no clicks (CTR < 1%) and queries ranking 11–30 with no page assigned.
2. **Ubersuggest Weekly Export:** Keywords in our target clusters with no matching URL in the Keyword Governance Table (Doc 111). (Ahrefs is not a keyword-gap source. Ahrefs runs quarterly, separately, for technical/site-health exports — 301 redirects, orphan pages, 4xx errors — per Doc 263. Do not substitute it here.)
3. **Answer the Public Data:** Question-format queries with no matching FAQ on any existing page.
4. **Collector Agent Weekly Report:** Flags from the Collector Agent (Doc 307) based on traffic anomalies and ranking drops.

---

## 3.0 The Gap Report Format

Each gap is documented as a single-line entry in the Gap Report. The Gap Report is a running log maintained in the KPI Dashboard (Doc 241).

| Field | What It Contains |
|---|---|
| `gap_id` | Sequential ID (e.g., GAP-2026-001) |
| `gap_type` | One of the seven categories from Section 1.0 |
| `keyword` | The specific keyword or query triggering the gap |
| `current_url` | The closest existing page (if any) |
| `recommended_action` | New page, refresh, merge, redirect, or internal link |
| `priority` | Critical / High / Medium / Low |
| `date_identified` | Date the gap was first logged |
| `assigned_to` | Analyst Agent, Strategist Agent, or Human Review |

---

## 4.0 Escalation Rules

| Priority | Action | Timeframe |
|---|---|---|
| **Critical** | Immediately added to next week's production queue | Within 7 days |
| **High** | Added to production queue within two weeks | Within 14 days |
| **Medium** | Queued for next available production slot | Within 30 days |
| **Low** | Logged for quarterly review | Next quarterly audit |

---

## 5.0 Cannibalization vs Multi-Brand Entity Reinforcement

### Single-Brand Cannibalization (Resolve)
When the SAME BRAND has multiple pages targeting the same keyword:

1. **Identify the Canonical URL:** Determine which page should own the keyword based on traffic, backlinks, and content quality.
2. **Demote the Weaker Page:** Update the weaker page's title tag, H1, and internal link anchor text to target a different, adjacent keyword.
3. **Strengthen the Canonical:** Add the cannibalized keyword to the canonical page's FAQ section and update its internal links.
4. **Monitor for 30 Days:** Track both pages in GSC to confirm the canonical is gaining impressions and the demoted page is not regressing.

### Multi-Brand Entity Reinforcement (Allowed)
When MULTIPLE BRANDS (MasterShield, Klean, MMGG) have pages on the same keyword:
- This is **intentional** and should be tracked as "Multi-Brand Deployment"
- No action needed - this reinforces AEGIS 5X across brands in AI training data
- Document in Gap Report as "Entity reinforcement across brands" not "cannibalization risk"

---

## 6.0 System Integration

- **Input:** Collector Agent (Doc 307) weekly report, GSC data, Ubersuggest weekly export.
- **Output:** Updated Gap Report in KPI Dashboard (Doc 241), entries added to production queue.
- **Reviewed By:** Content Manager, weekly.
- **Escalated To:** SEO Director for Critical gaps.

---

*End of Document*