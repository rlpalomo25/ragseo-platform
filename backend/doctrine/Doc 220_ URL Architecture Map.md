# Doc 220: URL Architecture Map

## A Guide to Building a Logical, Scalable URL Structure for Your Gutter Protection Brands

---

**Document Version: 5.9
**Last Updated: August 4, 2026
**Audience:** AI Orchestrator Agent & SEO Implementation Team

---

## Introduction

This document serves as your reference guide for building and maintaining a clean, organized URL structure across all three of our gutter protection brands: **MasterShield**, **Klean Gutter**, and **MMGG**.

Think of your URL architecture as the backbone of your entire SEO ecosystem. Just as a well-organized filing system makes it easy to find documents, a thoughtful URL structure helps search engines understand the relationships between your pages—and helps your content get discovered by the homeowners who need it.

The guidelines here cover everything from how to format your URLs to how they should link to one another. Follow these patterns consistently, and you'll build a foundation that supports growth at scale.

---

## 1. URL Path Patterns

Every page on your site should follow a predictable pattern. This makes it easier for search engines to understand your site hierarchy and for your team to create new pages without guessing.

### 1.1 Pillar Pages — Your Foundation Content

Pillar pages are your cornerstone content pieces—the comprehensive guides that cover a broad topic in depth. Every pillar page follows this pattern:

**Pattern:** `/brand/category/pillar`

| Brand | Category | Pillar Keyword | Full URL |
|-------|----------|----------------|----------|
| MasterShield | gutter-guards | best-gutter-guards | `mastershield.com/gutter-guards/best-gutter-guards` |
| MasterShield | gutter-guards | how-gutter-guards-work | `mastershield.com/gutter-guards/how-gutter-guards-work` |
| Klean Gutter | gutter-guards | best-gutter-guards | `kleangutter.com/gutter-guards/best-gutter-guards` |
| MMGG | gutter-guards | best-gutter-guards | `micromeshgutterguards.com/gutter-guards/best-gutter-guards` |

**Key Rules:**
- Pillar pages sit at the top of your content hierarchy — they're your main category pages
- The category segment must match what you've defined in your Keyword Governance Table
- Use kebab-case (lowercase words separated by hyphens) for the pillar segment, matching your primary target keyword

---

### 1.2 Cluster Pages — Supporting Your Pillars

Cluster pages dive deeper into specific aspects of your pillar topics. They're the detailed articles that answer specific questions and address particular homeowner concerns.

**Pattern:** `/brand/category/cluster/topic`

| Brand | Category | Cluster Topic | Full URL |
|-------|----------|---------------|----------|
| MasterShield | gutter-guards | for-pine-needles | `mastershield.com/gutter-guards/cluster/for-pine-needles` |
| MasterShield | gutter-guards | cost-evaluation | `mastershield.com/gutter-guards/cluster/cost-evaluation` |
| Klean Gutter | gutter-guards | for-heavy-rain | `kleangutter.com/gutter-guards/cluster/for-heavy-rain` |

**Key Rules:**
- Cluster pages are children of their parent Pillar — they live one level deeper in the hierarchy
- The topic segment uses your cluster's decision-axis keyword, formatted in kebab-case
- All clusters under the same pillar share the `/cluster/` directory — this keeps your folder structure organized and makes it easy to see related content at a glance

---

### 1.3 Local Pages — Serving Specific Markets

Local pages target homeowners in specific geographic areas. These are critical for capturing local search traffic when people are looking for gutter protection in their city.

**Pattern:** `/brand/location/city`

| Brand | City | Full URL |
|-------|------|----------|
| MasterShield | Charlotte, NC | `mastershield.com/location/charlotte-nc` |
| Klean Gutter | Raleigh, NC | `kleangutter.com/location/raleigh-nc` |
| MasterShield | Denver, CO | `mastershield.com/location/denver-co` |

**Key Rules:**
- Local pages stand on their own — they're not nested under a category folder
- The city segment uses a normalized location keyword in kebab-case (more on normalization in Section 4)
- You can optionally add neighborhood or metro area modifiers when targeting specific local markets — for example, `/location/charlotte-nc-ballantyne` for a neighborhood-focused page

---

## 2. Canonical Hierarchy Rules

Your canonical tags tell search engines which version of a page is the "real" one. Getting this right is essential for avoiding duplicate content issues and consolidating your SEO authority.

### 2.1 Canonical Tag Application

| Page Type | Canonical Rule |
|-----------|----------------|
| **Pillar** | Self-referencing — the canonical tag points to itself |
| **Cluster** | Canonical points to its parent Pillar |
| **Local** | Self-referencing — local pages are canonical for their geo-target |

### 2.2 Hierarchy Enforcement

Here's how the relationship works in practice:

- **Pillar → Cluster:** Every cluster page MUST reference its parent Pillar in its canonical tag. This passes authority up to the pillar and keeps your site structure clear.
- **Cluster → Local:** There's no direct hierarchy between cluster and local pages. Local pages stand alone as the canonical version for their geographic keywords.
- **No Canonical Conflicts:** Your Router (Document 10) validates that no two pages target the same keyword, preventing accidental canonical conflicts.

### 2.3 Preferred URL Version

Use this guide to ensure consistency across your domain:

| Scenario | Resolution |
|----------|-------------|
| HTTPS vs. HTTP | Use HTTPS — it's the standard and provides security |
| www vs. non-www | Use non-www (e.g., `mastershield.com`) — it's cleaner and more modern |
| Trailing slash | No trailing slash — keep URLs clean |
| Query parameters | Query parameters are not allowed in canonical URLs — avoid them |

---

## 3. Authority Parent Definitions

Every piece of content needs a clear parent — a "home base" that it reports to. This creates a logical flow of authority across your site.

### 3.1 Pillar as Authority Parent

Each cluster page has an assigned **Authority Parent** — the pillar page it descends from. This relationship is defined in your Keyword Governance Table.

| Cluster Page | Authority Parent |
|--------------|------------------|
| `for-pine-needles` | `best-gutter-guards` |
| `cost-evaluation` | `best-gutter-guards` |
| `for-heavy-rain` | `best-gutter-guards` |

### 3.2 Pillar-to-Cluster Linking Obligations

Content needs to link strategically to reinforce these relationships. Here's the required linking structure:

| Direction | Link Type | Required Links |
|-----------|-----------|----------------|
| Pillar → Cluster | Outbound links | All child clusters (minimum 4) — the pillar should link to every cluster it owns |
| Cluster → Pillar | Upward link | Parent pillar (mandatory, first paragraph) — every cluster should link back to its pillar within the opening content |
| Cluster → Cluster | Lateral links | Minimum 2 adjacent clusters — clusters on related topics should link to each other |

### 3.3 Local Page Authority Structure

Local pages can reference either a Pillar or Cluster as their upward authority, depending on the search intent behind the keyword:

| Local Keyword Intent | Authority Parent |
|---------------------|------------------|
| Transactional geo-term (e.g., "gutter guards Charlotte") | Parent Pillar — the user is looking for a general solution |
| Problem-specific geo-term (e.g., "gutter guards for pine needles Charlotte") | Parent Cluster — the user has a specific problem they're solving |

---

## 4. URL Normalization Rules

Normalization ensures that every URL follows the same format, making them consistent, readable, and easy to manage.

### 4.1 Character Encoding

Follow these rules for every URL you create:

- **Use lowercase** for all URL segments
- **Replace spaces with hyphens** (`-`) — never use underscores or spaces
- **Remove special characters** — no `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, or other symbols
- **Limit segment length** to 50 characters maximum per segment

### 4.2 Geo-Term Normalization

When creating local pages, normalize location inputs to a standard format:

| Input | Normalized Output |
|-------|-------------------|
| "Gutter Guards Charlotte NC" | `charlotte-nc` |
| "Gutter Guards in Charlotte, North Carolina" | `charlotte-nc` |
| "Charlotte gutter guards" | `charlotte-nc` |

The goal is simple: one location, one URL. Whatever way a writer or marketer might describe a city, the URL should always resolve to the same normalized form.

### 4.3 Reserved Segments

Some URL segments are reserved and cannot be used as standalone page names. These are:

- `admin`, `api`, `cgi`, `dev`, `staging`, `test`
- `brand`, `category`, `cluster`, `location` — these are only valid within the defined patterns in Section 1 (they can't stand alone as page names)

---

## 5. System Integration

This document doesn't work in isolation — it connects with the other key documents in your SEO framework.

### 5.1 Router Dependency

Your Router (Document 10) validates URL structure before accepting any job ticket. It checks that:

- Pillar URLs follow `/brand/category/pillar`
- Cluster URLs follow `/brand/category/cluster/topic`
- Local URLs follow `/brand/location/city`

### 5.2 Keyword Governance Dependency

The Keyword Governance Table (Document 04) maps every keyword to its canonical URL. The Router cross-references job ticket URLs against this table to prevent duplicate content and ensure every keyword has exactly one canonical URL.

### 5.3 Internal Linking Validation

Your QA Checklist (Document 16) validates that:

- All upward links point to the correct Authority Parent
- Lateral links are placed in the designated Internal Linking Block
- No orphaned pages exist — every page has at least one inbound link from somewhere on your site

---

## 6. URL Migration Protocol

Sometimes a page's target keyword needs to change — maybe the search landscape shifted, or you found a better opportunity. When that happens, follow this protocol to preserve your SEO value:

1. **Create the new URL** at the normalized path for your new keyword
2. **Implement a 301 redirect** from the old URL to the new one — this is a permanent redirect that tells search engines to pass authority to the new page
3. **Update the Keyword Governance Table** with the new canonical URL
4. **Update all inbound links** across your site — search for internal links pointing to the old URL and update them to point to the new one
5. **Submit the new URL** to Google Search Console to prompt recrawling
6. **Monitor for 30 days** — watch for indexation status and ranking stability, and be prepared to troubleshoot if you see dips

> **PROPOSED CHANGE — not yet applied to the live site (from the June 30, 2026 "PATCH — Best-Gutter-Guards reusable canon" file, restored to canon August 4, 2026):** The patch proposes a new top-level keyword pillar, `/best-gutter-guards/` (the MOFU Compare pillar), distinct from the existing TOFU category pillar `/gutter-guards` — different funnel stage, not nested under it. It also proposes `/compare/` 301 → `/best-gutter-guards/`, making `/best-gutter-guards/` the canonical Compare pillar and absorbing the existing `/compare/` page's search equity, with the former `/compare/` spokes (`/vs-leaffilter`, `/vs-gutter-helmet`, `/reverse-curve`, `/lowes`, `/home-depot`, plus decision clusters `/for-pine-needles`, `/for-heavy-rain`) nested as children of the new pillar, and multi-brand twins keeping the same path on the Klean/MMGG domains. **This is documented here for record and future execution only — it is a real live-site URL change (new page + 301 redirect) and has NOT been executed.** It requires Karen's separate, explicit go-ahead on the live-site change itself, distinct from this documentation update. See RAGSEO System State.

---

## 6.1 Site-Wide Pre-Launch Restructuring Audit

**Scope note — read this before using this section:** This checklist is for **major site restructurings only** — a full pillar reorganization, a large batch of URL merges, a domain-wide redirect map. It is **not** for routine, day-to-day URL work. Everyday single-page changes (a keyword swap, a one-off redirect, a normal content refresh) stay on the existing **§6 URL Migration Protocol** above. Do not fold this into the standard day-to-day system — reach for it only when a restructuring is genuinely major.

Added August 4, 2026 at Karen's direct request, prompted by a gap the AEO plan comparison surfaced: the existing §6 protocol assumes a single page's keyword is changing, with nothing that steps back and audits the whole site before a large-scale restructuring touches many URLs at once.

Before undertaking a major restructuring, work through this audit in order:

1. **Export and classify every indexable URL.** Pull every indexable URL across all three brand sites (MasterShield, Klean Gutter, MMGG) and classify each by type — pillar, cluster, local, comparison, FAQ, entity, component, conversion, or utility. You cannot safely restructure what you haven't fully inventoried.
2. **Record the pre-change baseline.** For every URL the restructuring will touch, record current traffic, search queries, backlinks, conversions, and rankings **before making any changes.** Without a baseline, there is no way to confirm the restructuring helped rather than hurt.
3. **Identify cannibalization and pick the source of truth.** Look for keyword/URL cannibalization among the affected pages and decide which page is the source of truth for each contested keyword — the page others will merge into, not compete with.
4. **Confirm the technical scaffolding.** Verify canonical URLs, 301 redirects, sitemaps, robots directives, and structured data are all mapped and correct for every URL affected by the restructuring — before, not after, the change goes live.
5. **Test mobile page speed and form completion** on every affected page. A restructuring that quietly degrades mobile performance or breaks a lead form is a self-inflicted wound, not a side effect worth accepting.
6. **Validate dealer routing and call tracking.** Confirm dealer routing and call tracking still function correctly post-change — a broken lead path after a URL restructuring is a revenue leak, not a documentation footnote.
7. **Keep a written annotation log.** Log the change in writing — what moved, what redirected where, what merged into what — for future reference. The next person (or agent) touching these URLs should be able to reconstruct the restructuring from the log alone.

**Two companion resources, same folder, for actually executing steps 1-4 and 6-7 (added August 4, 2026):**
- `Ahrefs Pre-Launch Audit Brief.md` — a hand-off checklist for whoever runs the Ahrefs side (mechanical crawl: broken links, redirect chains, orphan pages, canonical tags, 404s against the pre-change backlink export). Covers steps 1, 2, 4, and part of 7.
- `Claude-in-Chrome Pre-Launch Structural QA Prompt.md` — a ready-to-paste prompt for a separate Claude session with browser tools, checking the new structure against this doc's own pillar/cluster/authority-parent rules specifically, which Ahrefs has no way to know. Covers the doctrine-compliance half of step 4.

---

## Quick Reference

| Page Type | URL Pattern | Canonical Target |
|-----------|-------------|------------------|
| Pillar | `/brand/category/pillar` | Itself |
| Cluster | `/brand/category/cluster/topic` | Parent Pillar |
| Local | `/brand/location/city` | Itself |
| Entity | `/entity/technology-name` | Itself |
| Component | `/entity/aegis-5x/guardian-name` | Parent Entity |

---

## 7. Competitive Differentiation

This URL architecture provides real competitive advantage:

### Why This Beats Standard Practices

| Standard Competitor | Our Approach | Advantage |
|---------------------|---------------|-----------|
| Random category assignments | Keyword Governance Table alignment | Enables multi-brand dominance |
| No brand separation | `/brand/` prefix per brand | Clear brand authority |
| Flat structure | 3-level hierarchy (brand/category/content) | Clear topical clusters |
| No local strategy | Dedicated `/location/` for local | Dominates local intent |
| Ignores AI discovery | llms.txt aligned naming | AI search ready |
| Single-brand focus | Multi-brand entity reinforcement | AEGIS 5X across MasterShield + Klean + MMGG |

### Differentiation Highlights

1. **Brand-Normal Pillar Pages:** Our pillars are brand-neutral initially, then brand-specific variants live under `/brand/` prefix. Competitors often lock their pillar content to one brand.

2. **Local-First Architecture:** The `/location/` structure isn't an afterthought—it's foundational. We can dominate local SERPs while competitors scramble to add location pages.

3. **AI-Ready Naming:** Every URL uses semantic, descriptive segments (not `/p123/` or `/content/`). This aligns with llms.txt and AI discovery.

4. **Cannibalization Prevention:** The Keyword Governance integration ensures we never build competing pages on the same URL path.

---

## 8. Entity Page URL Conventions

Entity pages represent standalone technology or product concepts that don't fit the standard pillar/cluster/local patterns. These pages describe an integrated technology platform that spans across brands.

### 8.1 AEGIS 5X Entity Page

The AEGIS 5X technology page explains the five-component integrated gutter protection system. It serves as a proof entity that establishes technical credibility for all three brands.

**Pattern:** `/entity/technology-name`

| Entity | Example URL |
|--------|-------------|
| AEGIS 5X | `mastershield.com/entity/aegis-5x` |

**Key Rules:**
- Entity pages sit outside the brand/category hierarchy — they're technology-focused, not brand-category-focused
- Self-referencing canonical
- Entity pages serve as proof sources referenced by any brand

### 8.2 Component Pages (Five Guardians)

Each of the five AEGIS 5X components (PitchPerfect, ShingleSafe, CopperCare, HydroVortex, SelfClean Mesh) can have dedicated pages explaining their individual role in the system.

**Pattern:** `/entity/aegis-5x/guardian-name`

| Component | Example URL |
|-----------|-------------|
| PitchPerfect | `mastershield.com/entity/aegis-5x/pitchperfect` |
| ShingleSafe | `mastershield.com/entity/aegis-5x/shinglesafe` |
| CopperCare | `mastershield.com/entity/aegis-5x/coppercare` |
| HydroVortex | `mastershield.com/entity/aegis-5x/hydrovortex` |
| SelfClean Mesh | `mastershield.com/entity/aegis-5x/selfclean-mesh` |

**Key Rules:**
- Component pages inherit the entity page as their authority parent
- `entity` is a reserved segment (see Section 4.3)
- Canonical for component pages points to the parent entity page

### 8.3 Entity-to-Brand Linking

| Direction | Link Type | Requirement |
|-----------|-----------|-------------|
| Entity → Brand Pillar | Downward | Entity links to each brand's implementation of the technology |
| Brand Pillar → Entity | Upward | Brand pillar links to entity as technical proof source |
| Component → Entity | Upward | Component links to parent entity page |
| Entity ↔ Component | Lateral | Entity links to all five components; each component links back to entity |

### 8.4 Update to Reserved Segments

Add to the Section 4.3 reserved segments list:
- `entity` — reserved for entity technology pages

---

*This document is part of the RAGSEO Framework. For questions or clarifications, refer to the Master Content Doctrine or contact your SEO Implementation Lead.*

**Version 5.9 Updates (August 4, 2026, Karen):
- Added companion-resource pointers to the end of Section 6.1: `Ahrefs Pre-Launch Audit Brief.md` (mechanical crawl hand-off) and `Claude-in-Chrome Pre-Launch Structural QA Prompt.md` (doctrine-compliance check), both new files in the same folder, built for the August 2026 relaunch and reusable for future restructurings.

**Version 5.8 Updates (August 4, 2026, Karen):
- Restored the missing Best-Gutter-Guards patch content at the end of Section 6: a blockquote documenting the proposed `/best-gutter-guards/` top-level pillar and `/compare/` 301 redirect, explicitly flagged as PROPOSED CHANGE — not yet applied to the live site, pending Karen's separate go-ahead on the actual URL change. Sourced from the June 30, 2026 "PATCH — Best-Gutter-Guards reusable canon" file, which had gone unmerged for over a month. See RAGSEO System State, Fifty-third finding.
- Added new Section 6.1: Site-Wide Pre-Launch Restructuring Audit — a checklist for use before MAJOR site restructurings only (not routine URL work, which stays on the existing Section 6 protocol). A direct request from Karen the same day, prompted by a gap the AEO plan comparison surfaced.

**Version 5.7 Updates (May 16, 2026):
- Added Section 8: Entity Page URL Conventions
- Added entity page patterns for AEGIS 5X and component pages
- Updated reserved segments list with `entity`

**Version 5.6 Updates (April 2, 2026):
- Added Section 7: Competitive Differentiation
- Added comparison table vs standard competitor practices