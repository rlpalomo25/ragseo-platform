# Doc 221: Hub-and-Spoke Linking Topology

**Series:** 400 (Architecture) | **Status:** Active | **Last Updated:** July 31, 2026
**Version:** 5.6

> **v5.6 (July 31, 2026, Karen):** Added Section 3.3, Link Discipline — Never Announce the Destination. Karen's craft notes (from a real page build) named a recurring habit: sentences whose only job is to send the reader to another page ("see our compare page," "read more about X over here"), which read as stage directions and waste the reader's attention on navigation instead of a point. This doc already governed *where* links go (upward/lateral, anchor text by page type); it never said a link may not be announced. Fixed. Rippled the same day to Doc 316/320/324 and the three Doc 361 Refresh Instructions (writer-facing drop-in) and Doc 328/329 (non-blocking craft flag).

---

> **Quick Reference**
> **Owns:** The architectural backbone that connects content and the protocol for pruning dead links.
> **Rule 1:** Every piece of content must link upward to its Authority Parent (e.g., Cluster to Pillar).
> **Rule 2:** Content at the same level must link laterally to related content (e.g., Cluster to Cluster).
> **Rule 3:** When a page is deleted or consolidated, all inbound internal links must be pruned or redirected within 48 hours.
> **If/Then:** If a page's Opportunity Score drops below 2.5 and it is marked for deletion, the SEO Agent must execute the Internal Link Pruning Protocol before the page is removed.

---

## 1.0 Understanding the Content Hub System

Think of your website as a well-organized city. The **hubs** are your main districts, and the **spokes** are the roads connecting them. Every piece of content belongs to a district, and every district connects to others in predictable, meaningful ways.

### 1.1 The Six Hub Categories

Your system uses six distinct hub types, each serving a different strategic purpose:

| Hub Type | What It Does | Real-World Example |
|----------|--------------|-------------------|
| **Brand Hub** | The main headquarters for an entire brand | MasterShield.com domain |
| **Problem Hub** | The main landing page for a core homeowner need | "Best Gutter Guards" pillar page |
| **Geography Hub** | Content organized by city or metro area | Charlotte metro local pages |
| **Category Hub** | Content grouped by product type | Gutter protection category |
| **Solution Hub** | Content grouped by a specific use case | "For Pine Needles" cluster pages |
| **Seasonal Hub** | Content triggered by time of year | Spring maintenance content |

---

## 2.0 How the Hub Architecture Works

### 2.1 Visualizing the Structure

Here's how everything connects — from the brand level down to individual local pages:

```
                        [BRAND HUB]
                             |
          ___________________|___________________
         /                   |                   \
    [PROBLEM 1]        [PROBLEM 2]        [PROBLEM 3]
    (Pillar Page)      (Pillar Page)      (Pillar Page)
         |                   |                   |
    __________         __________         __________
   /          \       /          \       /          \
[Cluster A] [Cluster B] [Cluster C] [Cluster D]
   |          |       |          |       |          |
[Local]    [Local] [Local]    [Local] [Local]    [Local]
```

### 2.2 How Hubs Connect to Each Other

Every hub type has a specific relationship with other hubs:

| Hub Type | Looks Up To | Connects Sideways To | Points Down To |
|----------|-------------|---------------------|----------------|
| Brand Hub | (None — it's the root) | Other Brand Hubs | All Problem Hubs |
| Problem Hub (Pillar) | Brand Hub | Other Problem Hubs | Child Clusters |
| Category Hub | Brand Hub | Other Category Hubs | Related Problem Hubs |
| Solution Hub (Cluster) | Problem Hub | Other Solution Hubs | Local Pages |
| Geography Hub | Problem Hub or Solution Hub | Other Geography Hubs | Neighborhood Pages |
| Seasonal Hub | Problem Hub | Other Seasonal Hubs | Seasonal Cluster Pages |

---

## 3.0 The Linking Rules That Hold It All Together

### 3.1 Upward Links — Building From the Bottom

**The Rule:** Every piece of content links back to its parent hub (what we call the "Authority Parent").

| Page Type | Authority Parent | Where to Link | Best Anchor Text |
|-----------|------------------|---------------|------------------|
| Cluster Page | Parent Pillar | First paragraph | Primary keyword of the Pillar |
| Local Page | Parent Cluster or Pillar | First paragraph | Primary keyword of the Authority |
| Seasonal Cluster | Parent Pillar | Body section | Pillar keyword variant |

### 3.2 Lateral Links — Connecting Equals

**The Rule:** Content at the same level links to related content at that same level.

| Starting Point | Links To | Minimum Required | Example |
|----------------|----------|------------------|---------|
| Cluster | Related Cluster | 2 links | "For Pine Needles" → "For Heavy Rain" |
| Local | Neighbor City | 2 links | "Charlotte" → "Raleigh" |
| Seasonal | Related Season | 1 link | "Spring Cleaning" → "Winter Prep" |

### 3.3 Link Discipline — Never Announce the Destination

**Added July 31, 2026, Karen.**

**The problem.** Sentences like "You can find a fuller comparison on our compare page" or "this has its own answer on our X page" read like stage directions. They also spend the reader's attention pointing at navigation instead of making a point.

**The rule.** If a topic is worth mentioning, it is worth a link — but the link goes *under a natural noun phrase* inside a sentence that already earns its place. The reader never gets told to go somewhere; they get a normal sentence, and the relevant words happen to be a link.

**Before → after:**
- Before: "Your roof's specific shingle-warranty question has a fuller answer on our [gutter covers and shingles] page." After: "The [shingle warranty on your specific roof] turns on your shingles and their manufacturer, so get that named in writing too." *(link under "shingle warranty on your specific roof"; the sentence makes a real point on its own)*
- Before: "That is the short version; there is a fuller side-by-side of the types on our compare page." After: "Whatever [type you are weighing], the questions you bring to the estimate are the same." *(link under "type you are weighing"; no announcement at all)*

**Rule text (drop-in for writer agents):** Never write a sentence whose job is to send the reader to another page ("see our ___ page," "you can find ___ over here," "read more about ___ on our ___ page"). Instead, place the internal link under a natural noun phrase inside a sentence that stands on its own without the link — it must still make sense and carry a point if the link were removed. If you cannot embed the link naturally, cut the reference; do not announce it.

This adds a "no announcing" constraint on top of the hub/spoke placement rules above — it does not change where links point, only how they're written into the sentence.

### Guardian Lateral Link Rules

Lateral links between guardian cluster pages must follow approved bridge logic. Do not force guardian links where the content context does not naturally produce the bridge.

#### Approved Bridge: PitchPerfect™ → CopperCare™

**Trigger condition:** Link from PitchPerfect™ to CopperCare™ ONLY when the section discusses:
- Seasonal buildup on the guard surface
- Debris staying damp between rain events
- Moss, algae, or biological growth conditions at the roof edge
- Moisture retained by a shelf or debris ledge

**Bridge language:** "When debris sits and stays damp, it creates the conditions where moss, algae, and other biological growth become part of the roof-edge problem."

**Do NOT force:** Do not link PitchPerfect™ to CopperCare™ in pitch-only sections, mechanism-explanation sections, or sections that do not touch moisture retention or biological growth.

#### Guardian Pair Bridge Status (All 10 Pairs)

The following table tracks approved bridge logic for all guardian-to-guardian lateral links. Pairs marked PENDING need bridge rules written before those guardian cluster pages can be completed.

| Guardian A | Guardian B | Bridge Status | Natural Bridge Condition |
|-----------|-----------|--------------|---------------------------|
| PitchPerfect™ | CopperCare™ | APPROVED | Seasonal buildup + damp debris → growth conditions |
| PitchPerfect™ | HydroVortex™ | PENDING | Likely: pitch preserves movement; HydroVortex captures at intake |
| PitchPerfect™ | SelfClean Mesh™ | PENDING | Likely: pitch + mesh work together on fine debris |
| PitchPerfect™ | ShingleSafe™ | PENDING | Likely: pitch alignment enables consistent shingle contact |
| HydroVortex™ | CopperCare™ | PENDING | Likely: moisture at intake zone → growth conditions |
| HydroVortex™ | SelfClean Mesh™ | PENDING | Likely: water movement across mesh |
| HydroVortex™ | ShingleSafe™ | PENDING | Likely: intake zone and shingle edge interaction |
| CopperCare™ | SelfClean Mesh™ | PENDING | Likely: growth resistance extends into mesh surface |
| CopperCare™ | ShingleSafe™ | PENDING | Likely: moisture at roof edge affects both |
| SelfClean Mesh™ | ShingleSafe™ | PENDING | Likely: debris clearance and shingle-edge moisture |

**Rule:** As each guardian cluster page is written, the writer must identify the natural bridge condition to adjacent guardians and propose bridge language. Doc 222 and this document must be updated with approved bridge logic before that guardian page publishes.

### 3.3 Downward Links — Pointing the Way

**The Rule:** Hub pages link to everything below them.

| Hub | Points To | How Many |
|-----|-----------|----------|
| Pillar | All child Clusters | Every available cluster (minimum 4) |
| Cluster | All child Locals | All locals in the same DMA |
| Geography Hub | All neighborhoods | Every neighborhood in that metro area |

---

## 4.0 The Internal Link Pruning Protocol (The Indig Rule)

As the system scales, pages will inevitably be deleted, consolidated, or moved based on the **Content Decay & Freshness Protocol (Doc 206)**. If internal links pointing to those dead pages are not pruned, the Hub & Spoke architecture will collapse into a tangled web of 404 errors and redirect chains, destroying crawl budget and user experience.

> **The Rule: No page can be deleted or redirected until its inbound internal links have been pruned.**

### 4.1 The Pruning Workflow

When a page is marked for deletion or consolidation:

1. **Identify Inbound Links:** The SEO Agent must run a crawl (e.g., using Ahrefs or Screaming Frog) to identify every internal page that links to the target page.
2. **Evaluate the Links:**
   *   If the target page is being **consolidated** into a new page, update the inbound links to point directly to the new page (do not rely on the 301 redirect).
   *   If the target page is being **deleted** entirely, remove the inbound links and rewrite the surrounding sentence so it still makes sense.
3. **Execute the Redirect:** Only after the internal links have been updated or removed can the 301 redirect be implemented or the page deleted.
4. **Verify:** Run a follow-up crawl to ensure no internal links point to the 404 or the 301 redirect.

### 4.2 The Quarterly Link Audit

To catch any links that slip through the cracks, the Strategy Team must conduct a full internal link audit every quarter.

*   **Target 1:** Eliminate all internal links pointing to 404 pages.
*   **Target 2:** Eliminate all internal links pointing to 301 redirects (update them to point to the final destination).
*   **Target 3:** Identify and fix any "orphan pages" (pages with no inbound internal links).

---

## 5.0 Hub Setup by Brand

### 5.1 MasterShield

| Hub | URL Structure | What's Under It |
|-----|---------------|-----------------|
| Problem Hub 1 | `/gutter-guards/best-gutter-guards` | 6 clusters, 12 local pages |
| Problem Hub 2 | `/gutter-guards/how-they-work` | 4 clusters, 8 local pages |
| Problem Hub 3 | `/gutter-cleaning/alternatives` | 3 clusters, 6 local pages |

### 5.2 Klean Gutter

| Hub | URL Structure | What's Under It |
|-----|---------------|-----------------|
| Problem Hub 1 | `/gutter-guards/best` | 5 clusters, 10 local pages |
| Problem Hub 2 | `/gutter-guards/guides` | 4 clusters, 8 local pages |

### 5.3 MMGG (MicroMeshGutterGuards.com)

| Hub | URL Structure | What's Under It |
|-----|---------------|-----------------|
| Problem Hub 1 | `/reviews/best-guards` | 4 clusters (no local pages — affiliate model) |

---

## 6.0 How People Actually Navigate Your Site

### 6.1 The Primary Journey

Most visitors follow this path — and your linking should make it effortless:

```
[Research Mode] Pillar Page (Hub)
       ↓
[Comparison Mode] Cluster Page (Spoke)
       ↓
[Action Mode] Local Page (Spoke)
```

### 6.2 Alternative Routes Visitors Take

| Visitor Goal | Their Path | Example |
|--------------|------------|---------|
| Explore a specific brand | Brand → Pillar | MasterShield home → "Best Gutter Guards" |
| Find local options | City → Cluster | "Charlotte gutter guards" → "For Pine Needles" |
| Compare solutions | Pillar → Cluster | "Best Gutter Guards" → "For Heavy Rain" |
| Seasonal research | Season → Pillar | Spring Cleaning → "How Gutter Guards Work" |

---

## 7.0 How Authority Flows Through Your Hub System

### 7.1 The Authority Path

Think of "authority" (or link equity) as a river that flows downhill — from the highest-level content down to the most specific:

1. **Brand Hub** → distributes authority to every Problem Hub
2. **Problem Hub (Pillar)** → passes it to its child Clusters
3. **Cluster** → passes it to its child Local pages
4. **Geography Hub** → distributes authority to all Local pages in that region

### 7.2 Protecting Your Authority

A few rules to keep your link equity strong:

- **No orphan pages** — Every page needs at least one incoming link from somewhere
- **No circular linking** — Don't link back to the hub you came from
- **No link leakage** — Keep outbound links to external sites to 3–5 per page max

---

## 8.0 Required Link Placements by Page Type

### 8.1 Pillar (Hub) Pages

| Section | What Goes There |
|---------|-----------------|
| **Above the Fold** | Navigation CTA pointing back to Brand Hub |
| **Mid-Page** | Contextual links to 2–3 key clusters |
| **Bottom** | Full list of all clusters (minimum 4) + link to Brand Hub |

### 8.2 Cluster (Spoke) Pages

| Section | What Goes There |
|---------|-----------------|
| **First Paragraph** | Upward link to parent Pillar |
| **Body Text** | 1–2 contextual links to related clusters |
| **Link Block** | At least 2 lateral links to other clusters |
| **Bottom** | CTA pointing to a Local page (if a dealer exists in that area) |

### 8.3 Local (Spoke) Pages

| Section | What Goes There |
|---------|-----------------|
| **First Paragraph** | Upward link to parent Cluster or Pillar |
| **Service Area Section** | Lateral links to 2–3 nearby cities |
| **Bottom** | Transactional CTA + fallback option (if no local dealer is available) |

---

*This document is part of the RAGSEO Framework. For questions or clarifications, refer to the System Governor (Doc 230) or contact your Content Manager.*