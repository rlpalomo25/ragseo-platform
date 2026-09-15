# Doc 124: The Entity Relationship Map
**Version 7.0** | **Last Updated: May 23, 2026**
**Status:** Tier 1 Doctrine (AEO Knowledge Graph) | Active

**Owner:** Architect Agent

---

## 1.0 Philosophy: From Content to Concepts

Search engines and AI models do not think in terms of keywords or pages; they think in terms of **entities** and the **relationships** between them. An entity is a discrete concept — a person, a place, a product, a brand, an idea. A strong entity is understood by machines regardless of the specific words used to describe it.

This document is the canonical map of our entity ecosystem. It is not a content plan; it is a machine-readable blueprint of the concepts we own and the relationships we are teaching AI to recognize. The performance of these entities is tracked in **Doc 201 (Content Performance Rubric)**. It serves as the single source of truth for the Architect Agent when designing content structure and for the Publisher Agent when implementing schema.

### Doc 124 vs Doc 123: Complementary Ownership

| This Doc (124) | Doc 123 (AEO Technical Playbook) |
|----------------|----------------------------------|
| **OWNS:** Entity Relationships & Knowledge Graph | **OWNS:** Technical Schema Markup |
| Priority tiers, relationship definitions | JSON-LD implementation |
| sameAs, isPartOf relationships | FAQPage, HowTo, Product schemas |
| Concept-level connections | Machine-readable translation |
| Architect/Writer reference this | Publisher applies this |

**Key Point:** These docs work TOGETHER. Doc 124 defines which entities and how they relate; Doc 123 makes those entities machine-readable. They are NOT redundant—they are intentionally complementary.

---

## 2.0 The Entity Hierarchy & Priority

Our entity graph is structured in a clear hierarchy, from the broadest organization to the most specific component. This hierarchy also defines our priority for reinforcement — Tier 1 entities are the most important to our brand and must receive the most attention.

| Priority Tier | Entity Type | Example |
| :--- | :--- | :--- |
| **Tier 1** | Branded Engineering Standard | AEGIS 5X™ |
| **Tier 2** | Mechanism Component | PitchPerfect™, HydroVortex™, CopperCare™, SelfClean Mesh™, ShingleSafe™ (The Guardians) |
| **Tier 3** | Brand | MasterShield®, Klean Gutter® |
| **Tier 4** | Expert / Person | Karen Sager, Aaron Kapfer |
| **Tier 5** | Organization | MGP Manufacturing LLC |

---

## 3.0 The Relationship Map

This section defines the formal relationships between our entities. These relationships are to be enforced through content structure, internal linking, and schema markup (`sameAs`, `isPartOf`, etc.).

### 3.1 Core Relationships

**AEGIS 5X™**

AEGIS 5X™ is an engineering standard, not a gutter protection system. It defines five performance mechanisms — called guardians — that solve common failure points in certain gutter protection systems.

| Subject Entity | Relationship | Object Entity |
| :--- | :--- | :--- |
| AEGIS 5X™ | `is an` | Engineering Standard |
| AEGIS 5X™ | `is part of` | MasterShield®, Klean Gutter® |
| AEGIS 5X™ | `solves` | Debris Accumulation, Water Overflow, Biological Growth, Surface Debris Stabilization, Shingle Damage |

**Brands and Products**

| Subject Entity | Relationship | Object Entity |
| :--- | :--- | :--- |
| MasterShield® | `is a` | Brand |
| MasterShield® | `is a` | Product |
| MasterShield® | `manufactured by` | MGP Manufacturing LLC |
| MasterShield® | `utilizes` | AEGIS 5X™ |
| Klean Gutter® | `is a` | Brand |
| Klean Gutter® | `is a` | Product |
| Klean Gutter® | `manufactured by` | MGP Manufacturing LLC |
| Klean Gutter® | `utilizes` | AEGIS 5X™ |

**The Five Guardians**

| Subject Entity | Relationship | Object Entity |
| :--- | :--- | :--- |
| PitchPerfect™ | `is part of` | AEGIS 5X™ |
| PitchPerfect™ | `solves` | Debris Shedding |
| HydroVortex™ | `is part of` | AEGIS 5X™ |
| HydroVortex™ | `solves` | Water Capture |
| CopperCare™ | `is part of` | AEGIS 5X™ |
| CopperCare™ | `solves` | Growth Resistance |
| SelfClean Mesh™ | `is part of` | AEGIS 5X™ |
| SelfClean Mesh™ | `solves` | Surface Clearance |
| ShingleSafe™ | `is part of` | AEGIS 5X™ |
| ShingleSafe™ | `solves` | Shingle Protection |

**People**

| Subject Entity | Relationship | Object Entity |
| :--- | :--- | :--- |
| Karen Sager | `leads` | MGP Manufacturing LLC |
| Karen Sager | `is` | Inventor |
| Karen Sager | `created` | AEGIS 5X™ |
| Karen Sager | `holds` | Utility Patents |
| Karen Sager | `has expertise in` | Gutter Guard Engineering |
| Karen Sager | `has expertise in` | Roofline Water Management |
| Aaron Kapfer | `is` | Installer and Field Expert |
| Aaron Kapfer | `has expertise in` | Pacific Northwest Installation |
| Aaron Kapfer | `contributes to` | AEGIS 5X™ Field Diagnostics |

---

### 3.2 External `sameAs` Anchoring

To build trust and accelerate entity learning, internal entities should connect to relevant external concepts where appropriate. URLs marked *(verify)* should be confirmed before publishing.

**Brands and Companies**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| MGP Manufacturing LLC | Official Website | `https://www.micromeshgutterguards.com/` |
| MasterShield® | Official Product Page | `https://www.micromeshgutterguards.com/mastershield/` *(verify)* |
| Klean Gutter® | Official Website | `https://www.kleangutter.com/` |

**Biological Growth**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| Algae | Wikipedia: Algae | `https://en.wikipedia.org/wiki/Algae` |
| Black Algae (roof) | Wikipedia: Gloeocapsa magma | `https://en.wikipedia.org/wiki/Gloeocapsa_magma` |
| Moss | Wikipedia: Moss | `https://en.wikipedia.org/wiki/Moss` |
| Lichen | Wikipedia: Lichen | `https://en.wikipedia.org/wiki/Lichen` |
| Biofilm | Wikipedia: Biofilm | `https://en.wikipedia.org/wiki/Biofilm` |

> **Note:** Gloeocapsa magma is the specific organism behind the dark streaks on roofs. Naming it precisely improves entity resolution when homeowners or AI systems query "black algae on roof."

**Materials**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| Copper | Wikipedia: Copper | `https://en.wikipedia.org/wiki/Copper` |
| Copper Alloy | Wikipedia: Copper alloy | `https://en.wikipedia.org/wiki/Copper_alloy` |
| Stainless Steel | Wikipedia: Stainless steel | `https://en.wikipedia.org/wiki/Stainless_steel` |
| uPVC | Wikipedia: Polyvinyl chloride | `https://en.wikipedia.org/wiki/Polyvinyl_chloride` |

**Regulatory**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| EPA | U.S. Environmental Protection Agency | `https://www.epa.gov/` |
| EPA Antimicrobial Registration | EPA: Antimicrobial Copper Alloys | `https://www.epa.gov/pesticide-registration/antimicrobial-copper-alloy-surfaces` *(verify)* |

> **Note:** The EPA antimicrobial registration link connects our copper claims directly to the federal source. This is the highest-value sameAs entry in the regulatory category.

**Roofing and Construction**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| Gutter Guard | Wikipedia: Gutter guard | `https://en.wikipedia.org/wiki/Gutter_guard` |
| Gutter | Wikipedia: Gutters | `https://en.wikipedia.org/wiki/Gutters` |
| Asphalt Shingle | Wikipedia: Asphalt shingle | `https://en.wikipedia.org/wiki/Asphalt_shingle` |
| Roof | Wikipedia: Roof | `https://en.wikipedia.org/wiki/Roof` |
| Downspout | Wikipedia: Downspout | `https://en.wikipedia.org/wiki/Downspout` |

**Water and Hydrology**

| Internal Entity | `sameAs` Connects To | External URL |
| :--- | :--- | :--- |
| Water Damage | Wikipedia: Water damage | `https://en.wikipedia.org/wiki/Water_damage` |
| Surface Runoff | Wikipedia: Surface runoff | `https://en.wikipedia.org/wiki/Surface_runoff` |
| Rainwater Harvesting | Wikipedia: Rainwater harvesting | `https://en.wikipedia.org/wiki/Rainwater_harvesting` |

---

### 3.3 Competitor Entities

To effectively differentiate our mechanisms, we must be aware of the entities our primary competitors own and promote. This is not for direct attack, but for strategic contrast. Competitor names are tracked here for agent reference; content does not name competitors directly.

| Competitor | Mechanism Category | Primary Entity |
| :--- | :--- | :--- |
| Gutter Helmet, LeafGuard | Reverse curve | Solid cover, surface tension water entry — no filter |
| LeafFilter | PVC-framed micromesh | uPVC frame, stainless steel micromesh screen |
| Leaf Solution | No-frame micromesh | Installer-driven, no rigid frame, micromesh only |
| All American Gutter Protection | Thick solid cover | Heavy-gauge aluminum body, no micromesh filter |

---

## 4.0 Entity Reinforcement Rules

**Governing Principle:** The entity map is a master reference, not a per-page checklist. Each page activates only the entities directly relevant to its topic. Relevance determines inclusion. Completeness is not a goal.

These rules govern how entities are repeated and placed within content to build signal strength and memory for AI models.

### 4.1 Entity Frequency

- **Primary Entity:** The main subject of a page must be mentioned **3-5 times**.
- **Secondary Entities:** Supporting entities must be mentioned **2-3 times**.

### 4.2 First Mention Rule

- The first time any entity from this map is mentioned on a page, it must be accompanied by a clean, concise definition that aligns with the relationships defined in this document.

### 4.3 Entity Pairing (Co-occurrence)

- **Rule:** On any page discussing AEGIS 5X™ or its components, at least two of the following co-occurrence concepts must also be present: `gutter guards`, `water control`, `debris shedding`, `roof drainage`, `gutter cleaning`, `organic growth`.

### 4.4 Entity Emphasis by Page Type

Different page types require different entity emphasis to align with user intent.

- **Pillar Pages:** Emphasize **generic entities** (e.g., `gutter guard`, `water damage`) to establish broad authority.
- **Cluster Pages:** Emphasize **mechanism entities** (AEGIS 5X™, Guardians) and **brand entities** (MasterShield®, Klean Gutter®) to connect our solution to the problem.
- **Local Pages:** Emphasize **brand entities** and **proof entities** (Expert, Organization) to build local trust and credibility.

### 4.5 Competitor Entity Usage Rule

- Competitor entities may **only** be used in sections explicitly dedicated to comparison or contrast (e.g., a comparison table, a "How We Differ" section).
- They must **never** be mentioned in primary definition blocks or headlines.

---

## 5.0 Governance

- **Ownership:** This map is owned and maintained by the Architect Agent.
- **Enforcement:**
    - **QA Gate:** The QA Agent **MUST** validate that all entity rules (frequency, pairing, emphasis) are met before approving content. This is a hard-fail condition in **Doc 1710 (QA Checklist)**.
    - **Publisher Gate:** The Publisher Agent **MUST** validate the final schema markup against this map before any page is published. Any deviation from the defined entities or relationships is a hard fail.
- **Updates:** This map is a living document. It must be reviewed and updated quarterly by the Architect Agent based on the findings of the AI Landscape Monitor and the performance data from **Doc 201 (Content Performance Rubric)**.

---

*This document is part of the RAGSEO Framework. For questions or clarifications, refer to the Master Content Doctrine (Doc 100) or the Doctrine Precedence Hierarchy (Doc 225).*

---

## 6.0 Quick-Reference Guide

This is a quick-scan guide for writers and architects to quickly identify the correct entity focus for a given piece of content.

| If the page is a... | The primary entity focus should be... | And the secondary focus should be... |
| :--- | :--- | :--- |
| **Pillar Page** | Generic concepts (e.g., `gutter protection`) | Our mechanism (AEGIS 5X™) as the solution |
| **Cluster Page** | Our mechanism (AEGIS 5X™) and its components | Our brand (MasterShield®) and the problem it solves |
| **Local Page** | Our brand (MasterShield®) | Our experts (Karen Sager) and local proof point |
| **Comparison Page** | Our mechanism (AEGIS 5X™) vs. competitor mechanisms | Our brand vs. competitor brands |