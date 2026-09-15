# Doc 161: 

**Document:** 214b  
**Last Updated:** April 3, 2026
**Version:** 4.0  

*For use by the AI Writer Agent (Modular Pipeline) — Loaded when Page Type is set to Cluster*

---

## What This Module Does

The Cluster Page Type Module tells the AI writer exactly how to build a middle-of-the-funnel page that helps homeowners compare their options and make a specific decision. Think of it as the blueprint for pages that answer questions like "Which gutter guard handles pine needles best?" or "What happens if my gutters clog in winter?"

Cluster pages sit between your broad pillar content (the "how do gutter guards work" pages) and your transactional local pages (the "get a quote near me" pages). They're where people go when they've moved past general curiosity and into active comparison mode.

---

## 1.0 Core Doctrine Rules

Before diving into structure, here are the foundational rules that govern every cluster page:

### 1.1 Brand Expression Guidelines

Following the Brand Expression Doctrine (Doc 106), cluster pages operate using **Belief Layers 1, 2, and 3**. Here's what that means:

- **Layers 1 & 2** (Category Beliefs + Solution Beliefs) can appear throughout most of the page
- **Layer 3** (Product Beliefs) — that's where specific brands come in — are permitted *only* in the Engineered Resolution section, and only at the very end

This keeps the comparison fair and neutral. The reader should feel like they're getting honest information, not a sales pitch.

### 1.2 Archetype Rotation

Cluster pages use archetype rotation, meaning the page tone and framing approach change based on what the search results already show. The Router Logic Module (Doc 174) selects the appropriate archetype based on:

- The current SERP format
- The keyword intent
- The rotation protocol

This prevents every cluster page from feeling exactly the same.

### 1.3 The Decision Axis Rule

Every cluster page exists to answer one specific question or own one specific decision axis. This must be explicit in your execution plan, and it must fall into one of these four categories:

| Decision Axis Type | Examples |
|---|---|
| **Failure mode** | What happens when fine debris causes clogging? Ice damming? |
| **Environmental condition** | How do these handle heavy rainfall? Pine needle density? Freeze-thaw cycles? |
| **Installation variable** | What about roof pitch? Fascia condition? |
| **Cost/lifecycle dimension** | What's the 20-year cost of ownership? How often does it need maintenance? |

### 1.4 Tension Gradient Entry Point

Cluster pages skip the broad orientation that pillar pages use. Instead, they enter at **Stage 2 (Concern)** — opening directly with a specific tradeoff or failure mode relevant to the cluster keyword.

The full emotional arc follows: **Concern → Consequence → Control → Confidence**

### 1.5 Brand Timing

Brand mentions are allowed — but not where you'd expect. Specifically:

- Brand may appear in the *final paragraph* of the optional Engineered Resolution section
- Brand should **never** appear in the comparison section

The comparison stays neutral. The brand show up only at the very end, if at all.

---

## 2.0 How the Psychology Maps to Structure

Every cluster page follows a four-layer psychological sequence. This isn't arbitrary — it's designed to match how homeowners actually think when they're comparing options.

| Psychological Layer | Tension Gradient Stage | Where It Appears | What It Does |
|---|---|---|---|
| **1. Specific Problem** | Concern | H1 and above-the-fold copy | States the exact problem the page solves |
| **2. Mechanism Comparison** | Consequence + Control | The core of the article | Neutral, evidence-based comparison of how different mechanisms perform |
| **3. Tradeoff Analysis** | Control | Dedicated section | Explains what each solution gives up in exchange |
| **4. Logical Routing** | Confidence | Conclusion | Routes the reader based on their likely next question |

This structure respects the reader's intelligence. They came to compare, so you compare. They want tradeoffs, so you show tradeoffs. They're ready for next steps, so you guide them there.

---

## 3.0 Structural Requirements (In Order)

Here's the complete anatomy of a cluster page, from top to bottom:

### 3.1 Above-the-Fold Section

The first thing readers see sets the tone for everything. This section includes:

- **H1 Title:** Must use the primary keyword exactly — no variations, no creative rewrites
- **Early FAQs:** The top 2-3 questions people ask about this topic should be addressed early in the article
- **CTA:** Must be a **navigational CTA** at this stage. Examples:
  - "Compare all gutter guard types"
  - "See how [problem] compares across options"
  
  This matches the Stage 2 entry point of the Tension Gradient — the reader isn't ready to buy yet; they want to understand their options.
  
- **Upward Pillar Link:** The first paragraph must contain a contextual link back to the parent pillar page. This maintains the site architecture and helps readers who need broader context.

### 3.2 Body Content

The body follows a specific sequence:

#### Problem Section

Elaborate on the specific problem from the Decision Axis. This section must include:

- A **Failure Consequence** subsection that quantifies the risk — timelines, cost implications, and physics-based outcomes. Don't vague-box the consequences. Tell them exactly what happens, how long it takes, and what it costs.

#### Mechanism Comparison Section

This is the heart of the cluster page. Before presenting any comparison table:

1. Restate the core tradeoff from the parent pillar page — this frames the comparison and gives readers anchor context
2. Then present a detailed, neutral analysis of how different gutter guard types perform against the specific problem

**Critical requirements:**

- At least one comparison table with required columns (see Section 6.0)
- Meet evidence standards (Section 6.0)
- The **primary guardian** (the main solution being recommended) is the dominant reference throughout this section
- **Secondary guardian(s)** appear in the Tradeoff Analysis section, providing engineering context without overshadowing the primary

#### Tradeoff Analysis Section

Explain what each solution gives up. Every option has costs — this section names them honestly. Secondary guardians are referenced here to add engineering depth.

- **Category economics** are allowed (e.g., "screen guards typically cost $X per linear foot")
- **Brand-specific pricing** is not allowed

#### Engineered Resolution Section (Conditional)

This section is optional. It appears *after* Tradeoff Analysis and *before* the Internal Linking Block.

- May be included **only** if the cluster topic maps directly to one of the five engineering pillars
- This is the **only section** where Layer 3 (Product Beliefs) are permitted
- Brand can appear here, in the final paragraph only

#### Real Experience Section (Required)

This section establishes E-E-A-T through documented field experience. It belongs in the Authority Layer (after Tradeoff Analysis, before Internal Linking Block).

**Required elements:**

- At least one **named installer quote** with job date and location
- A **problem/solution narrative** describing a specific installation challenge and how it was resolved
- A **case study template** including: homeowner name (or "a homeowner in [city]"), installation date, property type, specific problem addressed, and outcome

This is where you prove you've actually done this work — not just written about it.

#### Internal Linking Block (Required)

A dedicated section titled "Next Steps" or "Related Reading." Must contain a minimum of 2-3 lateral cluster links — pages that cover adjacent problems or comparison angles.

### 3.3 FAQ Section

- **Minimum:** 10 FAQs
- **Target:** 15-20 FAQs
- The AI agent must check Engine 4 SERP benchmarks and scale to 20+ if competitors have high FAQ counts
- **Do not duplicate pillar FAQs** — these should be new questions specific to the cluster topic

### 3.4 Bottom of Page

The footer section wraps up the page with trust and conversion elements:

- **Expert Bio:** Load from the assigned Brand Module (211/b/c). Place in the Authority Layer — not just as a byline. Include credentials, years of experience, and relevant expertise.

- **Trust Assets:** Load required trust assets from the Trust Layer System (Doc 141):
  - Minimum 1 authority asset
  - Minimum 1 social proof asset

- **Educational CTA:** Placed mid-page after the comparison section. This is a lead magnet (e.g., downloadable guide, checklist) that deepens engagement. Per the Conversion Architecture Module (Doc 140).

- **Transactional CTA:** Placed at the bottom of the page. By this point, the reader has completed the full tension arc. Examples:
  - "Schedule Your Free Diagnostic"
  - "Request a Quote"
  - "Find a Dealer Near You"
  
  Per the Conversion Architecture Module (Doc 140).

---

## 7.0 Explicit Routing Logic

The final section of a cluster page must route the reader logically based on their next likely question. This isn't about pushing toward a sale — it's about being genuinely helpful by pointing them to what they actually need next.

| If the reader's state is... | Then route them to... | Example |
|---|---|---|
| Concept confused or needs broader context | The **Parent Pillar** page | "How do gutter guards work in the first place?" → links to Pillar 3 |
| Ready to explore an adjacent problem | An **Adjacent Cluster** page | "How do these guards handle pine needles vs. leaves?" → links to a different cluster |
| Evaluation complete, considering installation | A **Local Page** or Dealer Locator | "Who can install this near me?" → links to dealer locator |

---

## 8.0 Dynamic Conversion Paths (Next Best Action)

Cluster pages should present "Next Best Action" CTAs that route users based on where they are in their decision journey:

| Current State | Next Best Action CTA | Destination |
|---|---|---|
| User needs local solution | "Get specific for [your location]" | Local page (if dealer exists in DMA) |
| User wants broader comparison | "Explore other gutter guard types" | Related Cluster page |
| User is not in service area | "Not in [city]? [brand] serves [region]" | Fallback to nearest active Local or Brand landing page |

### CTA Placement

- **Mid-Page (after comparison):** Educational CTA to adjacent Cluster
- **Bottom of Page:** Transactional CTA to Local page (conditional on dealer availability)

### Fallback Logic

If no local dealer exists in the target DMA, the Cluster page must display: *"Not in [city]? [brand] serves the [region] area"* — linking to the nearest active Local page or Brand landing page.

This ensures every reader gets a path forward, even if they're outside your current service footprint.

---

## 9.0 System Integration & Enforcement

### How This Module Connects to the Pipeline

- **Router (Doc 174):** Loads this module automatically when `page_type=Cluster`. The Router output packet for Cluster pages specifies:
  - `CTA_class=Educational (mid-page) + Transactional (bottom)`
  - `guardian_mode=named`
  - `archetype=selected`
  - `primary_guardian`
  - `secondary_guardians`
  
  Belief layer is determined implicitly by page type per the Brand Expression Doctrine (Doc 106).

- **Execution Contract:** Your execution plan must specify:
  - `page_type=Cluster`
  - `decision_axis`
  - `primary_guardian`
  - `secondary_guardians`
  
  These come from the Router's job ticket output.

- **QA Checklist (Doc 140):** Must validate structural, content, belief layer, and linking requirements defined in this module before publication.

### Dependencies

This module requires and loads rules from:

- Brand Expression Doctrine (Doc 106)
- Conversion Architecture Module (Doc 140)
- Trust Layer System (Doc 141)
- AEGIS 5X Mechanism Authority (Doc 142)
- Cluster Architecture Map (Doc 222)
- The assigned Brand Module (211 or 216)

---

*End of Cluster Page Type Module*