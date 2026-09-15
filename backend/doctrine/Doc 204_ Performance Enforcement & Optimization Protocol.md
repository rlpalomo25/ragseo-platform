# Doc 204: 

**Document:** 315
**Version:** 4.1 | **Last Updated:** August 6, 2026 | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).

**Intended For:** Content Manager, Auditor Agent (Doc 328), SEO Director
**Purpose:** This document provides the standardized, enforceable playbooks for fixing performance issues detected by the Content Performance Rubric (Doc 201) and prioritized by the Revenue Intelligence Engine (Doc 210). It translates the "what" (e.g., "low conversion rate") into the "how" (e.g., "execute Intro Rewrite Pattern #1").

---

## 1.0 Purpose: From Detection to Resolution

Every underperforming page has a specific failure mode. This document maps each failure mode to a specific intervention playbook. The goal is to remove guesswork and ensure every optimization is executed with precision and consistency.

No optimization is executed without first completing the Content Performance Rubric (Doc 201) for the target page. The Rubric identifies the failure mode. This document provides the fix.

---

## 2.0 Optimization Trigger Matrix

| Failure Mode | Metric Threshold | Assigned Playbook |
|---|---|---|
| **Low Organic Traffic** | < 100 sessions/month for a page ranking 1–10 | Playbook #1: Title & Meta Rewrite |
| **Low CTR** | CTR < 2% for positions 1–5 | Playbook #1: Title & Meta Rewrite |
| **High Bounce Rate** | Bounce Rate > 70% | Playbook #2: Above-the-Fold Rewrite |
| **Low Scroll Depth** | < 50% average scroll depth | Playbook #9: Visual Layer Enforcement |
| **Low Conversion Rate** | < 1% conversion on a BOFU page | Playbook #3: CTA Optimization |
| **Ranking Stall** | No ranking movement in 60+ days | Playbook #4: Content Depth Expansion |
| **AI Citation Gap** | Page not cited in Visby.ai report | Playbook #5: AEO Formatting Upgrade |
| **Internal Link Deficit** | < 3 inbound internal links | Playbook #6: Internal Link Injection |
| **Stale Content** | Citations older than 18 months | Playbook #7: Data Refresh |
| **Cannibalization** | Two pages competing for same keyword | Playbook #8: Cannibalization Resolution |
| **Search Intent Pivot** | Page fails to rank for target keyword, but generates GSC impressions for secondary queries | Playbook #10: Live Page Keyword Pivot |

---

## 3.0 The Optimization Playbooks

### Playbook #1: Title & Meta Rewrite

**Trigger:** Low CTR or low organic traffic despite good ranking position.

**Steps:**
1. Review the current title tag and meta description against the top 3 ranking competitors.
2. Identify the primary value proposition missing from the current title.
3. Rewrite the title tag using the formula: `[Primary Keyword] — [Specific Benefit] | [Brand Name]`
4. Rewrite the meta description to include a direct answer to the primary question and a clear call-to-action.
5. Monitor CTR in GSC for 14 days post-update.

---

### Playbook #2: Above-the-Fold Rewrite

**Trigger:** High bounce rate (> 70%).

**Steps:**
1. Review the above-the-fold section against the Publishing & Page Assembly System (Doc 190) requirements.
2. Verify the **Your Questions Answered** section carries the top 3 reader questions as **1-2 sentence teasers, each with the full-answer link embedded in the teaser's own closing words (never a separate "Jump to full answer" tag, per Doc 192 item 3)** — not full 40-60 word answers, which duplicate the FAQ and violate one-home-per-question.
3. Verify the primary CTA is visible without scrolling.
4. Ensure the H1 matches the primary keyword exactly.
5. Add a local trust signal or authority asset if missing.
6. Monitor bounce rate in GA4 for 14 days post-update.

---

### Playbook #3: CTA Optimization

**Trigger:** Low conversion rate (< 1%) on a BOFU page.

**Steps:**
1. Review all CTAs against the Conversion Architecture Module (Doc 140) requirements.
2. Verify CTA placement by structural milestone (Doc 144): soft after the above-the-fold block, hard before the FAQ, hard at the bottom, middle CTAs only at tension-resolving section ends — not a word-count cadence.
3. Replace any generic CTAs ("Contact Us") with contextual, benefit-driven CTAs ("Get Your Free Gutter Guard Estimate").
4. Ensure the final CTA includes the full value proposition.
5. Test one CTA variant per the A/B Testing Protocol (Doc 211).

---

### Playbook #4: Content Depth Expansion

**Trigger:** Ranking stall (no movement in 60+ days).

**Steps:**
1. Run a competitive gap analysis against the top 3 ranking pages for the target keyword.
2. Identify topics, subtopics, or FAQs covered by competitors but missing from our page.
3. Add a minimum of 500 words addressing the identified gaps.
4. Ensure all 5 Engineering Pillars are addressed if this is a Pillar page.
5. Add or update the FAQ section to include competitor-covered questions.
6. Submit the updated URL for re-indexing via Google Search Console.

---

### Playbook #5: AEO Formatting Upgrade

**Trigger:** Page not cited in Visby.ai AI citation report.

**Steps:**
1. Review the page against the Answer Formatting Doctrine (Doc 121) and the AI Writing Prompt (Doc 173).
2. Ensure the first sentence of every H2 section is a direct, standalone answer.
3. Rewrite key claims using the Claim → Source Pairing format: `"The system handles 40 inches of rain per hour (ASTM G154)."`
4. Add or expand the FAQ section with exact PAA question phrasing.
5. Verify all definition statements use the "X is..." format.
6. Re-run the Visby.ai check 30 days after update.

---

### Playbook #6: Internal Link Injection

**Trigger:** Page has fewer than 3 inbound internal links.

**Steps:**
1. Query the Keyword Governance Table (Doc 111) for all pages in the same cluster.
2. Identify 3–5 pages that are topically relevant and have high authority (traffic or backlinks).
3. Add contextual links from those pages to the target page using keyword-matched anchor text.
4. Verify no anchor text conflicts with existing links (cannibalization check).
5. Log the new links in the Cluster Architecture Map (Doc 222).

---

### Playbook #7: Data Refresh

**Trigger:** Citations older than 18 months.

**Steps:**
1. Identify all statistics, studies, and data points cited in the page.
2. Check each source for a more recent version or update.
3. Replace outdated data with current data from approved sources (Doc 112).
4. Update the "Last Updated" date in the page metadata.
5. Add a brief "Updated [Month Year]" note in the above-the-fold section.

---

### Playbook #8: Cannibalization Resolution

**Trigger:** Two pages competing for the same primary keyword.

**Steps:**
1. Identify the canonical page (higher traffic, more backlinks, better content).
2. Update the non-canonical page's H1, title tag, and meta description to target an adjacent keyword.
3. Add a canonical tag on the non-canonical page pointing to the canonical URL.
4. Update all internal links pointing to the non-canonical page to use the new, adjacent keyword anchor text.
5. Monitor both pages in GSC for 30 days to confirm resolution.

---

### Playbook #9: Visual Layer Enforcement

**Trigger:** Low scroll depth (< 50%) or high bounce rate (> 70%).

| Tactic | Instruction |
|---|---|
| **Paragraph Compression** | No paragraph may be longer than 3 lines of text on mobile. Break up longer paragraphs. |
| **Image Injection** | Add at least one relevant, high-quality image for every 400–600 words of text. |
| **Layout Variation** | Break up long sections of pure text with blockquotes, tables, or comparison lists. |
| **Subheading Granularity** | Add a new subheading for every 2–3 paragraphs to improve scannability. |

---

### Playbook #10: Live Page Keyword Pivot

**Trigger:** Page fails to rank for its primary target keyword after 60 days, but GSC query mining shows it is generating impressions for a different, secondary query.

**Steps:**
1. Open Google Search Console and inspect the specific page URL.
2. Navigate to the "Queries" tab to see what users are actually typing to find this page.
3. Identify the highest-impression, most relevant secondary query.
4. **Evaluate the Pivot:** Does this secondary query match the page's actual search intent and content? If yes, stop fighting the SERP. Pivot the page.
5. **Execute the Pivot:** 
   - Rewrite the H1 to match the new query exactly.
   - Rewrite the Title Tag to feature the new query prominently.
   - (Optional but recommended) Update the URL slug to match the new query and set up a 301 redirect from the old slug.
6. Submit the updated URL for re-indexing via GSC.
7. Log the pivot in the Keyword Governance Table (Doc 111) to release the original keyword and claim the new one.

---

## 4.0 Post-Optimization Monitoring

All optimized pages are placed on a 30-day monitoring watch. The Collector Agent (Doc 307) tracks the following metrics and reports any change greater than 10% in either direction:

- Organic sessions
- Average position (GSC)
- CTR (GSC)
- Bounce rate (GA4)
- Scroll depth (GA4)
- Conversion rate (GA4)

If no improvement is observed after 30 days, the page is escalated to the SEO Director for a full content audit.

---

*End of Document*