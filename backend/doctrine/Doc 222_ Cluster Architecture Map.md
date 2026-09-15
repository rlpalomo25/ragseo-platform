# Doc 222: Cluster Architecture Map

**Last Updated: May 16, 2026
**Doctrine Tier:** Core Architecture  
**Version: 5.7

---

## Purpose & Audience

This document serves as the single source of truth for how our engineering excellence framework translates into content architecture. It's designed for use by the AI Writer Agent, Content Managers, and SEO Strategists who need to understand how pages connect and why.

**What you'll find here:**
- The relationship between our five core engineering pillars and the cluster pages that support them
- The mandatory linking structure that ties everything together
- Integration requirements with other system documents

---

> **Quick Reference**
> **Owns:** The mapping of the AEGIS 5X entity to its five guardian cluster pages.
> **Rule 1:** The AEGIS 5X entity page must link directly to each of the five guardian cluster pages.
> **Rule 2:** Every guardian cluster page must link up to the AEGIS 5X entity within the first two paragraphs.
> **Rule 3:** Every guardian cluster page must link to at least two other relevant guardian cluster pages.
> **Rule 4:** Every guardian cluster page must include `entity_parent: aegis-5x` in its execution contract.
> **If/Then:** If building the core engineering content, the architecture must fully map to the five AEGIS 5X guardians.

---

## Section 1: Core Doctrine — Architecture Follows Engineering

Here's the underlying principle that drives everything we do: **the content architecture must fully map to the core engineering framework of the product.**

This isn't about chasing keyword search volume. It's about building genuine, comprehensive authority around the problems our products solve. Each of the five pillars in our Engineering Evaluation Framework (taken from the Master Content Doctrine) deserves its own dedicated cluster page—not because we're guessing what might rank, but because each pillar represents a real engineering challenge that homeowners need to understand.

> **Why this matters:** If a core engineering pillar of our product lacks a dedicated content home, our authority is incomplete. We're leaving a gap that our competitors can exploit.

Think of this map as the blueprint. It's a subset of the full site architecture, which is documented elsewhere. But this document specifically defines how the five pillars connect to their mandatory cluster pages.

---

## Section 2: The Master Pillar & Cluster Map

This section defines how the AEGIS 5X technology entity maps to its five component guardians and their respective cluster pages. The architecture follows a two-level hierarchy: the AEGIS 5X entity at the top, with the five guardian cluster pages beneath it.

This structure applies to both **MasterShield®** and **Klean Gutter®** brands.

### 2.1 Entity Architecture — AEGIS 5X

AEGIS 5X is the five-component integrated gutter protection system. It serves as the parent entity for all guardian content. The entity page explains how the five engineered parts work together as one integrated system.

| Entity | Description | Example URL |
|--------|-------------|-------------|
| AEGIS 5X | Five-component integrated gutter protection system | `/entity/aegis-5x` |

All five guardians below are components of the AEGIS 5X system. Each guardian cluster page inherits AEGIS 5X as its entity parent.

### 2.2 Pillar-to-Cluster Reference Table

| Engineering Pillar | AEGIS 5X™ Guardian | Mandatory Cluster Page Title | Decision Axis | Parent Pillar |
|---|---|---|---|---|
| Alignment & Flow Control | HydroVortex™ | Why Gutter Guards Fail in Heavy Rain | Water Velocity | How Gutter Guards Work |
| Edge & Roofline Protection | ShingleSafe™ | How Improper Gutter Guard Installation Damages Your Roof | Risk & Damage Prevention | How Gutter Guards Work |
| Organic & Oil Resistance | CopperCare™ | Why Most Gutter Guards Clog (And How to Prevent It) | Long-Term Performance | How Gutter Guards Work |
| Debris Shedding & Self-Cleaning | SelfClean Mesh™ | The Truth About "Self-Cleaning" Gutter Guards | Maintenance & Upkeep | How Gutter Guards Work |
| Structural Durability | PitchPerfect™ | Why Gutter Guards Fail Over Time (Thermal Expansion) | Weather & Environment | How Gutter Guards Work |

### Important Notes on Usage

The **Parent Pillar "How Gutter Guards Work"** is the designated Master Pillar for all engineering-related content. These cluster page titles are foundational—they establish the core topic and frame the decision the reader needs to make.

### Title Adaptation Rules

| Condition | Action |
|-----------|--------|
| **SERP analysis shows different query pattern** | Router CAN adapt title to match search intent |
| **Local variant (e.g., "in [City]")** | Router CAN add geo-modifier |
| **Core topic or Decision Axis changes** | Router CANNOT adapt - violates architecture |
| **Brand-specific variant** | Router CAN adapt for MasterShield vs Klean Gutter |

**The Rule:** The Decision Axis and core topic are **mandatory, non-negotiable**. Title wording around them can adapt based on SERP analysis.

---

## Section 3: Linking Hierarchy & Rules
> **Cross-Reference — Guardian Lateral Links:** Doc 221 (Hub-and-Spoke Linking Topology) contains the Guardian Lateral Link Rules table, including approved bridge logic for all 10 guardian-to-guardian lateral link pairs. Before any guardian cluster page publishes, the writer must confirm the bridge condition to adjacent guardians with Doc 221 and update that document with approved bridge language.



Now for the practical part: how these pages link to each other. These rules are mandatory and must be implemented by the AI Writer Agent during content generation.

### Rule 1: Pillar to Cluster (Downward Linking)

The Master Pillar ("How Gutter Guards Work") must contain a dedicated section that introduces the five core engineering challenges and links directly to each of the five mandatory Engineering Cluster Pages.

### Rule 2: Cluster to Pillar (Upward Linking)

Every Engineering Cluster Page must link up to the Master Pillar within the first two paragraphs. This establishes the page's position within the hierarchy and helps the reader understand where they are in the content ecosystem.

### Rule 3: Cluster to Cluster (Lateral Linking)

Every Engineering Cluster Page must link to at least **two** other relevant Engineering Cluster Pages.

Why? Because the five pillars aren't isolated topics—they're part of an integrated system. A page about gutter guard pitch (Alignment & Flow Control) naturally connects to a page about heavy rain performance (also Alignment & Flow Control). A page about installation damage (Edge & Roofline Protection) connects to a page about structural failure over time (Structural Durability).

These lateral links reinforce the concept that understanding one pillar helps you understand them all.

### Rule 4: Cluster to Local (Downward Linking)

The Engineering Cluster Pages serve as the primary entry point to the local conversion funnel. Each cluster page must include a transactional CTA that routes the user to the appropriate Local Page or dealer locator, as defined in the **Conversion Architecture Module (Doc 140)**.

This is where research turns into action. After a homeowner understands the engineering behind why pitch matters, they should have a clear, low-friction path to finding a professional who can install the right system for their home.

### Rule 5: Entity Linking (AEGIS 5X)

The AEGIS 5X entity page serves as the authority parent for all five guardian cluster pages.

- Every guardian cluster page MUST link to the AEGIS 5X entity page within the first two paragraphs as a proof reference
- The AEGIS 5X entity page MUST link to all five guardian cluster pages
- Brand pillar pages that reference the AEGIS 5X system MUST link to the entity page as the technical proof source
- The entity page at `/entity/aegis-5x` uses a self-referencing canonical and is not subject to canonical pass-up

---

## Section 4: System Integration Mandates

This section outlines how this architecture connects with the rest of the system. Each mandate ensures that the architectural intent translates into actual execution.

### Mandate 1: Router Logic

The **Router Logic Module** must recognize these five Engineering Cluster Pages as a mandatory, non-negotiable part of the site architecture.

**Key requirements:**
- Execution plans for these pages must be created and prioritized
- Build order is sequential: the Master Pillar must be complete before the five Engineering Cluster Pages are built
- The Router must contain logic to route users from a cluster page to the geographically correct Local Page based on user data or a location selector

### Mandate 2: Execution Contract

The **Execution Contract** for each of the five Engineering Cluster Pages must explicitly load the **AEGIS 5X™ Mechanism Authority (Doc 142)** and include the following fields:

- **`primary_guardian`**: Must match the Guardian defined in the map above
- **`decision_axis`**: Must match the Decision Axis defined in the map above
- **`entity_parent`**: Must be set to `aegis-5x` for all five guardian cluster pages

These fields ensure that every piece of content stays true to its engineering foundation.

### Mandate 3: Keyword Governance

The five Engineering Cluster Page titles and their corresponding URLs must be added to the **Keyword Governance Table** to prevent keyword cannibalization and ensure architectural integrity.

**Important:** These pages are considered foundational. They are not subject to removal based on keyword volume fluctuations. Their existence is driven by engineering relevance, not search demand.

### Mandate 4: QA Checklist

The **QA Checklist** must be updated to include specific checks for:

- The linking hierarchy defined in Section 3.0
- The presence and correct usage of the `decision_axis` as the core framing of the article
- The explicit connection in the body copy between the cluster topic and the `primary_guardian`
- Each guardian cluster page links to the AEGIS 5X entity page within the first two paragraphs
- The `entity_parent` field is set to `aegis-5x` in the execution contract

### Mandate 5: Cluster Page Type Module

The **Cluster Page Type Module (Doc 161)** must be updated to include minimum content depth requirements for these five Engineering Cluster Pages.

Specifically, these pages must contain:
- Required comparison elements
- Mechanism depth
- Proof types relevant to their Decision Axis

---

## Section 5: How This Fits With Other Documents

This document defines the **site architecture** for the core engineering content. It's the blueprint for how pages connect and relate to each other.

The **AEGIS 5X™ Mechanism Authority (Doc 142)** defines the **product mechanism logic** that populates this architecture. It's the "what makes our products work" layer that gives these pages their technical credibility.

Together, these two documents are complementary. They don't overlap in function—one handles the structure, the other handles the substance. Both are essential to building content that serves homeowners and establishes genuine authority.

---

*End of Document*