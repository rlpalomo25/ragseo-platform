# Doc 123: The AEO Technical Playbook
**Version:** 8.3 | **Last Updated:** August 6, 2026 | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Status:** Tier 1 Doctrine (AEO Execution)

**Owner:** Publisher Agent

---

## 1.0 Philosophy: Machine Translation

This is the technical execution playbook for Answer Engine Optimization.

Its purpose is to translate content, credibility, and entity relationships into technical signals that machines can parse cleanly.

This document governs:
- schema implementation
- machine-readable translation
- validation discipline
- agentic-readiness support at the technical layer

### Clarification

Technical translation helps machines understand the page.
It does not replace:
- strong content
- clear page structure
- useful answers
- people-first relevance

Google’s current guidance says generative AI optimization still rests on SEO fundamentals, helpful non-commodity content, and clear technical structure. Google also says there is no special schema or special AI-only file required for generative AI search visibility

So this document should not be read as:
- “schema creates AI visibility by itself”
- “technical markup can substitute for content quality”
- “there is a special AI markup layer Google requires”

It should be read as the machine-translation layer that supports strong content.

### Doc 123 vs Doc 124: Complementary Ownership

| This Doc (123) | Doc 124 |
|----------------|---------|
| **Owns:** Technical schema markup | **Owns:** Entity relationships and knowledge graph logic |
| JSON-LD implementation | sameAs, isPartOf, conceptual relationships |
| FAQPage, HowTo, Product, Article schema | priority tiers and relationship definitions |
| machine-readable translation | concept-level connections |

---

## 2.0 The AEO Tiering System

| Tier | Content Type | Technical Requirements |
| :--- | :--- | :--- |
| **Tier 1** | Pillar Pages | Full appropriate technical stack |
| **Tier 2** | Standard Cluster Pages | Partial appropriate technical stack |
| **Tier 3** | Local and Supporting | Minimal appropriate technical stack |

### Clarification

“Full stack” does not mean “use every possible schema.”
It means use the right schema types for the page honestly and cleanly.

Google’s guidance says structured data is not required for generative AI search and there is no special schema.org markup needed just for that purpose. It remains useful as part of overall SEO and eligibility for rich results

Therefore:
- use schema where it is genuinely appropriate
- do not over-schema pages
- do not invent AI-only markup strategies

---

## 3.0 Schema Decision Matrix — mechanical, so no one has to know schema

**Two lists: what every page always gets, and what to add only if the page has a specific feature. The writer picks by looking at the page — no schema knowledge required. Generate the JSON-LD code for every type that applies.**

### Always on — every page (no judgment call)
- **`Article`** — the page itself (headline = H1, author, publisher, datePublished + dateModified, primary image). **Also add `reviewedBy` when a named field/technical expert (e.g., Aaron Kapfer) genuinely reviewed the page's technical accuracy** — reference their Person entity below, don't inline a bare name string. **Also add explicit `citation` entries** for the page's Technical Sources (Doc 113/Doc 192 item 6A) where the page carries them — this schema field has existed unused; the citations themselves already live in the visible Technical Sources block, this just marks them up.
- **`Organization`** — the publishing company (MasterShield® / Klean Gutter® / MicroMeshGutterGuards®) as `publisher`; canonical name, URL, logo per Doc 114, plus `sameAs` (official social/profile links per Doc 114) and, where a page's context calls for it, the parent/manufacturer relationship (MicroMeshGutterGuards.com as the parent company — see Doc 114 §"shared corporate facts").
- **`BreadcrumbList`** — the on-page breadcrumb trail (Home › Pillar › This Page), on every indexable page.
- **`FAQPage`** — include whenever the page carries a visible FAQ block (the standard on these pages). Kept for AI extraction, not rich results (see FAQ status below). Skip only if the page genuinely has no FAQ.
- **`Person`** (added August 4, 2026, Karen): standalone, reusable entity profiles for Karen Sager and Aaron Kapfer — credentials, role, and `sameAs` (LinkedIn/official bio links) — built once, referenced by `@id` from every page's Article `author` or `reviewedBy` field rather than re-inlined as a bare name string each time. Stronger E-E-A-T signal than a per-page string, and keeps the two credentialed entities consistent across every brand. Build the two profiles once (source: `E-E-A-T Author Bios.md` / Doc 113 §3.3) and reference them everywhere, don't regenerate per page.

### Add only if the page has this feature (mechanical trigger — look at the page)
| If the page has… | Add |
| :--- | :--- |
| a head-to-head / ranked comparison (a "best" or "vs" page) | `ItemList` |
| a specific product it describes and sells | `Product` — **plus `Review`/`AggregateRating` ONLY if real, first-party reviews/ratings exist** |
| genuine step-by-step instructions | `HowTo` |
| an embedded video (mechanism demo, install video, field test) | `VideoObject` |
| an original diagram or field photograph with a descriptive caption | `ImageObject` (added August 4, 2026 — was already in the §7.0 priority tier but missing from this actionable table; reconciled) |
| a physical location / local/dealer page with real business details | `LocalBusiness`, or **`HomeAndConstructionBusiness`** where the more specific subtype fits (added August 4, 2026 — a sharper fit for a home-improvement contractor than generic `LocalBusiness`; use whichever the page's actual content supports) |
| an installation or service-area page (not tied to one physical location) | `Service` (added August 4, 2026 — real gap, this type didn't exist in the matrix before) |

### The one hard rule (honesty)
Never mark up content the page does not truly contain. In particular: **do not add `Review` or `AggregateRating` unless the page shows real reviews or ratings of *your* product.** A page that merely *discusses* complaints or competitor reviews (e.g., the Gutter Guard Complaints page) is **not** a review page — it gets `Article` + `FAQPage` + `Organization` + `BreadcrumbList`, and never `Review`/`AggregateRating`. Marking up ratings you don't have is a Google violation.

### Failure condition


A schema block fails if it:
- misrepresents the page
- marks up content the page does not truly contain
- creates technical clutter without clear relevance

### FAQ schema status (June 18, 2026)

FAQ rich results were deprecated by Google on May 7, 2026. FAQPage is still a valid type and Google still parses it, but it no longer produces a SERP feature. Use FAQPage only where the page has genuine, visible FAQ content; keep it for AI extraction and entity clarity, not for rich results. Do not chase "20 FAQ questions for a featured snippet" — that guidance is retired. Reconcile any older reference to this rule (e.g., the System Documentation Spreadsheet line describing Doc 123 as "FAQ schema, 20 PAA questions, eligible for featured snippets").

---

## 4.0 Entity Priority: Mechanism-First

When schema includes entity hierarchy, prioritize the mechanism or product entity when that is the true subject of the page.

### Hierarchy
1. Product or mechanism when page intent supports it
2. Organization as context
3. Person as supporting authority where relevant

### Clarification

Mechanism-first does not mean force the mechanism into every schema block.
It means the primary schema entity should reflect the real answer object of the page.

---

## 5.0 Implementation and Validation

- Validate with the Rich Results Test where relevant
- Aim for zero critical errors
- Keep JSON-LD clean and minimal
- Store validation artifacts where your production system requires them

### Rule

Custom schema must not conflict with platform-generated schema.
If a plugin auto-generates conflicting markup, resolve the conflict instead of stacking incompatible blocks.

---

## 6.0 Advanced Technical Execution

### 6.1 Retrieval Integrity Support
Each FAQ answer, HowTo step, or answer-support block must remain self-contained enough to survive extraction.

**Placement matters as much as structure.** The page's primary extractable answer must sit in the first ~30% of the page (in or just under Key Takeaways), because AI systems pull most citations from the opening of a document. A perfectly structured answer buried low is a missed citation. (Content ownership of this rule is Doc 120/121; this is the technical reinforcement.)

This section supports Docs 120, 121, and 122.
It does not replace them.

### 6.2 AI Crawlability

Google’s guidance makes several things clear:
- llms.txt is not required
- there is no special AI-only file needed
- core technical accessibility still matters
- pages must be crawlable, indexable, and eligible to show a snippet in Google Search

### Current guidance

- Do not treat llms.txt as a meaningful Google AI requirement
- robots.txt remains the authoritative crawl-control mechanism
- crawlability, indexability, snippet eligibility, and technical cleanliness remain the real foundation

### What actually matters for AI crawlability

- content is accessible to Google Search
- page is indexable and snippet-eligible
- HTML is clean and readable
- heading hierarchy is intact
- alt text is descriptive where needed
- page loads properly
- schema is valid where used

### 6.3 External Entity Anchoring

Use sameAs and related external anchors where appropriate.

These may include:
- authoritative profiles
- publications
- patents
- other legitimate external identity references

Do not add weak or irrelevant sameAs targets.

### 6.4 Freshness Signals

Update `dateModified` when meaningful content changes occur.

Do not update freshness signals for trivial edits only to simulate recency.

### 6.5 Agentic Readiness

Google’s current guidance highlights agentic experiences where browser agents may analyze rendered pages, DOM structure, and accessibility-related structures when interacting with sites

This means technical readiness should include:
- clean heading hierarchy
- descriptive alt text
- static accessibility of core content where possible
- load integrity
- title and H1 alignment where appropriate

### Required for pillar pages and important cluster pages

| Check | Requirement | Why |
|-------|-------------|-----|
| **Heading hierarchy** | H1 once, H2 and H3 nested logically, no skipped levels | supports accessibility and structured navigation |
| **Alt text** | descriptive and specific where images matter | supports accessibility tree and image understanding |
| **Static content access** | core content should not depend on hidden JS states to exist | supports reliable access by crawlers and agents |
| **Page load integrity** | avoid broken loads and blocked essentials | agents and crawlers may fail degraded pages |
| **Title / H1 alignment** | semantically aligned subject signals | reduces ambiguity about page subject |

---

## 7.0 Schema Priority Tiers

| Priority | Schema Types | Why |
| :--- | :--- | :--- |
| P0 | Product, FAQPage, HowTo where truly relevant | direct answer support |
| P1 | Article, VideoObject, ImageObject | support understanding and eligibility |
| P2 | LocalBusiness, Review | local and trust support |
| P3 | BreadcrumbList | crawl and navigation support |

### Clarification

Priority does not mean obligation on every page.
It means order of usefulness when the page legitimately qualifies.

---

## 8.0 Open Graph and Social Tags

Open Graph tags support social previews.
They do not function as special generative AI markup.

| Property | Purpose | Notes |
| :--- | :--- | :--- |
| og:title | Social title | may differ from meta title |
| og:description | Social snippet | concise and social-facing |
| og:image | Social image | appropriate minimum size |
| og:url | Canonical URL | must match page |
| og:type | Content type | usually article |
| og:site_name | Brand name | display use |
| twitter:card | X card type | typically summary_large_image |

### Requirements

- important pillar and cluster pages should have custom OG tags
- images should meet practical preview standards
- OG description may differ from meta description
- include twitter:card where relevant

---

## 9.0 Technical Myths to Ignore

In light of Google’s current guidance, do not build doctrine around these ideas:
- special AI-only files are required
- special AI-only schema is required
- chunking pages into tiny pieces is required
- structured data alone improves generative AI visibility

Google explicitly says you do not need special AI files or special schema, and that structured data is not required for generative AI search, though it remains useful within broader SEO

---

## 10.0 Enforcement

Compliance with this doctrine is enforced through technical QA and publishing validation.

### Automatic failure triggers

- invalid or conflicting schema
- schema that misrepresents page content
- inaccessible or blocked core content
- broken heading structure on pages requiring agentic readiness
- technical implementation that assumes unsupported AI-only requirements

---

## 11.0 One-Sentence Summary

Doc 123 governs the technical machine-translation layer so strong pages are crawlable, parsable, and technically legible to search systems and agents without pretending that schema, llms.txt, or AI-only markup can replace people-first SEO fundamentals.

---

*End of Document 123*