# Doc 191: Seasonal Content Engine

**Document:** 232  
**Version:** 4.0  
**Last Updated:** April 3, 2026

**Intended For:** AI Orchestrator Agent & Content Scheduling System  
**Purpose:** This document defines the triggers, templates, and workflows that drive seasonal and event-driven content production, ensuring all seasonal content is strategically aligned with our core engineering principles.

---

## Understanding the Seasonal Engine

Content that speaks to what your audience is experiencing right now performs significantly better than static content. The Seasonal Content Engine is designed to anticipate homeowner needs and deliver the right content at the right moment.

This system operates on two levels: automatic triggers that run on a set schedule, and manual triggers that require human approval. Both are essential to a well-functioning seasonal content strategy.

---

## 1.0 Trigger Categories

### 1.1 Automatic Triggers

| Season | When It Runs | Content Focus |
|---|---|---|
| **Spring Cleaning** | March 15 – May 15 | Maintenance-focused content |
| **Winter Prep** | September 15 – November 15 | Preparation-focused content |
| **Storm Season** | June 1 – August 31 | Emergency and performance-focused content |
| **Fall Foliage** | October 1 – November 30 | Debris-specific content |

### 1.2 Manual Triggers

| Trigger | Who Approves | Why It's Used |
|---|---|---|
| **Weather Event** | Marketing Manager | Post-storm content addressing specific damage scenarios |
| **Competitive Launch** | Brand Manager | Response content to new competitor products |
| **Dealer Network Expansion** | Operations Lead | New local pages for new markets |
| **Algorithm Update** | SEO Director | Content audit and refresh triggered by major Google updates |

---

## 2.0 Seasonal Content Templates & Mechanism Mapping

Each season has its own template. **Crucially, every seasonal template must be explicitly mapped to at least one Engineering Pillar and one AEGIS Guardian.** This ensures that even our time-sensitive content reinforces our core authority and engineering narrative.

### 2.1 Spring Cleaning Template

- **AEGIS Guardian:** Guardian 2 (The Filtration Guardian)
- **Engineering Pillar:** Pillar 2 (Filtration & Water Management)

| Section | What Goes Here | Connects To |
|---|---|---|
| Opening | "Spring gutter maintenance checklist" | Pillar 2 (Performance) |
| Body | Pre-season inspection guide, cleaning vs. guards math | Pillar 1 (Gutter Guards) |
| CTA | "Get a free spring inspection" | Local page |

### 2.2 Winter Prep Template

- **AEGIS Guardian:** Guardian 4 (The Structural Guardian)
- **Engineering Pillar:** Pillar 4 (Structural Integrity)

| Section | What Goes Here | Connects To |
|---|---|---|
| Opening | "Prepare your gutters for winter" | Pillar 2 (Performance) |
| Body | Ice dam prevention, freeze-thaw damage guide | Pillar 5 (Pricing) |
| CTA | "Schedule winter prep inspection" | Local page |

### 2.3 Storm Season Template

- **AEGIS Guardian:** Guardian 1 (The Volume Guardian)
- **Engineering Pillar:** Pillar 1 (Water Volume Capacity)

| Section | What Goes Here | Connects To |
|---|---|---|
| Opening | "Protecting your gutters from storm damage" | Pillar 1 (Gutter Guards) |
| Body | Heavy rain performance, wind resistance ratings | Pillar 2 (Performance) |
| CTA | "Storm-ready your home today" | Local page |

### 2.4 Fall Foliage Template

- **AEGIS Guardian:** Guardian 3 (The Debris Guardian)
- **Engineering Pillar:** Pillar 3 (Debris Rejection)

| Section | What Goes Here | Connects To |
|---|---|---|
| Opening | "Fall debris and your gutters" | Pillar 2 (Performance) |
| Body | Leaf clog prevention, pine needle solutions | Pillar 1 (Gutter Guards) |
| CTA | "Before the leaves fall" | Local page |

---

## 3.0 How the Triggers Work

### 3.1 Automatic Execution Flow & The QA Gate

**The automated publishing workflow has been updated to include a mandatory QA gate.** No content, even if fully automated, goes live without a final check.

1.  **Scheduler System** checks the trigger window.
2.  **Content Generator** loads the seasonal template.
3.  **Router** validates the keyword.
4.  **Writer Agent** produces a draft.
5.  **QA System** runs the standard checklist PLUS the seasonal-specific checks.
6.  **Human QA Review:** A content manager must give final approval in the CMS. **The system now holds the content in a "Ready for Review" state instead of publishing automatically.**
7.  **Scheduler** publishes upon approval.

### 3.2 Manual Approval Flow

For event-driven content (e.g., severe weather, competitor launches), the process requires human initiation and approval:

1.  **Trigger Event:** A marketing manager or SEO director identifies a need for timely content.
2.  **Brief Creation:** The manager creates a brief specifying the event, target audience, and required AEGIS Guardian mapping.
3.  **Content Generation:** The Writer Agent produces a draft based on the brief and the appropriate seasonal template.
4.  **QA System:** Runs the standard checklist PLUS event-specific checks (e.g., accuracy of weather data, appropriate tone).
5.  **Human QA Review:** A content manager must give final approval in the CMS.
6.  **Manual Publish:** The content is published immediately upon approval.

---

## 4.0 Connecting Seasonal Pages to Pillar Pages

Seasonal pages are temporary spikes in relevance, but they must support the long-term authority of our core pillars.

1.  **Upward Linking:** Every seasonal page must contain at least one contextual link to its mapped Engineering Pillar page within the first 300 words.
2.  **Anchor Text:** Use descriptive, non-exact match anchor text (e.g., "learn more about how our system handles heavy rain" linking to the Water Volume Capacity pillar).
3.  **Lateral Linking:** If a seasonal page discusses a specific problem (e.g., pine needles), it should link to the relevant Cluster page for that problem.
4.  **Post-Season Action:** When a season ends, the seasonal page should be evaluated. If it generated significant traffic or backlinks, it may be integrated into a relevant Cluster page or maintained as an evergreen resource. Otherwise, it should be archived or redirected to the parent pillar.

---

## 5.0 The 2026 Seasonal Content Calendar

| Month | Primary Focus | Secondary Focus | Key Trigger Event |
|---|---|---|---|
| **January** | Winter Maintenance | Ice Dam Prevention | Major snowstorms |
| **February** | Winter Damage Assessment | Planning for Spring | Thaw cycles |
| **March** | Spring Cleaning Prep | Early Rain | First major spring rain |
| **April** | Spring Showers | Seed Pods/Blossoms | Heavy rainfall |
| **May** | Heavy Rain Performance | Foundation Protection | Sustained rain events |
| **June** | Early Summer Storms | Pest Prevention | First summer storms |
| **July** | Mid-Summer Maintenance | Fire Risk (Dry Debris) | Heatwaves/dry spells |
| **August** | Late Summer Storms | Hurricane Prep (Coastal) | Hurricane warnings |
| **September** | Early Fall Prep | Pine Needles | First leaf drop |
| **October** | Peak Fall Foliage | Heavy Debris Management | Major leaf fall |
| **November** | Late Fall Cleanup | Pre-Winter Inspection | First freeze |
| **December** | Winter Prep Finalization | Ice Dam Risks | First snowfall |

---

## 6.0 System Integration

### 6.1 Job Ticket System

- The job ticket system now includes a **`guardian_mapping`** field for all seasonal content.

### 6.2 Performance Monitoring

- We will now also track **mechanism resonance** — are users engaging with the engineering-focused content within our seasonal pages?

### 6.3 Annual Refresh Protocol

- The annual refresh will now include a review of the **Guardian mapping** for each template to ensure it is still the most effective angle.

---

## 7.0 Quality Checks Specific to Seasonal Content

| Check | What We're Looking For |
|---|---|
| **Mechanism Alignment** | **The content explicitly references the correct AEGIS Guardian and Engineering Pillar.** |
| **Timing Relevance** | Content was published within the designated trigger window. |
| **Template Compliance** | All template sections are present and in the correct order. |
| **Pillar Links** | At least one link to each relevant parent pillar. |
| **Local CTA** | Only fires if a dealer actually exists in the target DMA. |
| **Data Freshness** | All statistics and citations are from the current or prior calendar year. |

---

## Quick Reference

- Every seasonal page is now mapped to an AEGIS Guardian.
- **No content is published automatically.** All content, including automated seasonal runs, requires a final human QA check.
- Templates get a yearly refresh, including a review of their mechanism alignment.

---

*This document is part of the RAGSEO Framework. For questions or clarifications, refer to the Master Content Doctrine or contact your SEO Implementation Lead.*_