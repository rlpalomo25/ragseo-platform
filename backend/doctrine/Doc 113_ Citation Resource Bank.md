# Doc 113: The Citation Resource Bank
**Version 8.9** | **Last Updated: August 5, 2026** | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 5, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).
**Status:** Tier 2 Doctrine (Resource Bank)

## 1.0 Purpose & Philosophy

This document is the central, canonical source for all factual claims, statistics, and expert credentials used in our content. It is a **resource bank**, not a strategy guide. The quality of sources in this bank directly impacts our performance scores in **Doc 201 (Content Performance Rubric)**. Its purpose is to ensure every factual claim we make is accurate, verifiable, and legally sound.

> This document operates under the **Engineering for Selection** doctrine. It provides the credible, factual ammunition required by Doc 120 (Philosophy - Engineering for Selection) and Doc 123 (The AEO Technical Playbook).

## 2.0 Governance

-   **Rule of First Resort:** All factual and data-driven claims in new content **must** originate from a source listed in this document.
-   **Update Cadence:** This document is reviewed and updated quarterly by the **Source Citation Hunter (Doc 340)** to incorporate new research and retire outdated claims.
-   **Freshness Enforcement:** All sources in this bank must be reviewed annually. Any source older than 3 years must be re-validated or replaced. This process is a direct input to the **Doc 206 (Content Decay & Freshness Model)**.
-   **Scope Note required on every Approved Claim (MANDATORY):** An approved claim is not usable until it states its own limits. Every claim in §4.0/§5.0 must carry a one-line **Scope Note** with four parts: **(1) what was actually measured**, **(2) the population and sample it was measured on**, **(3) when**, and **(4) what the claim does NOT say.** A bare percentage with no scope reads as clean, authoritative, and general — which is precisely how an ambiguous figure reaches a page looking verified. The number isn't the claim; the number plus its scope is the claim.
    -   *Worked example — the failure this prevents:* "78% of gutter guard failures on non-MGP products were traced back to incorrect pitch alignment" (§4.5). Read alone it implies 78% of all gutter guard failures, everywhere. Its real scope is narrower: failures **our installers were called to inspect**, on **competitor products**, as **diagnosed by our own field team**. That is a legitimate, useful, defensible first-party claim — but only when its scope travels with it.
    -   **First-party data carries a higher bar, not a lower one.** A first-party claim must name who collected it, on what population, and why that population is not the general population. Self-selected samples (service calls, warranty claims, inspections we were invited to) are never representative of the category by construction — say so in the note rather than letting the reader assume otherwise.
    -   **Enforcement:** a claim with no Scope Note is **not approved for use** — treat it as unverified and hold the page. Any claim cited in a plan or page must carry its Scope Note into the `citation_intent_map` so the writer and the auditor can both see the limits. Existing claims in this bank that predate this rule are grandfathered as *unverified* until a Scope Note is added.

### Citation Discipline Standards (June 8, 2026)

**Two types of citations. Different purposes. Different formats.**

**Type 1 — External Proof Citations** (academic, government, manufacturer, testing sources)
Use for: science claims, safety statistics, warranty/approval claims, material/fire/code claims, anything measurable or legally sensitive.
Format: Quiet inline superscripts or endnotes. Never lead a paragraph with the source name.
Quota per guardian cluster page: **3–5 external citations maximum** in body or endnotes.

**Type 2 — Internal Expert Assertions** (Karen Sager or Aaron Kapfer statements)
Use for: core mechanism takeaway, field-observable reality, buyer evaluation question, memorable proof of concept.
Format: One or two sentences. Plainspoken. Specific. Attribution after the statement, not before.
Quota per guardian cluster page: **2–4 internal expert assertions required**.

**Proof Notes Format (preferred for most pages)**
Rather than inline footnotes for every citation, collect external proof sources at the end of the article under a brief section — **as a numbered list, each entry anchor-targeted, so the body can actually link to it**:

> **Technical Sources**
> 1. Ladder safety: CDC/NIOSH ladder safety data.
> 2. Filter behavior: Filtration mechanics and particle behavior research.
> 3. Surface weathering: Roof material weathering and surface soiling research.
> 4. Manufacturer approvals: MasterShield approval letters from GAF, CertainTeed, Malarkey, IKO, and Owens Corning.

**HTML wiring (added August 3, 2026, Karen — root cause of pages shipping with no working footnote links):** the list above renders as `<ol>` with each `<li id="src-N">`. Every sentence that draws on one of these sources gets a quiet superscript **at the point of use** in the body, wired as a real anchor, not a decorative character: `<sup><a href="#src-N">N</a></sup>`. Doc 317 §4.1's "put a superscript number at the end of the relevant sentence" is this markup, not a bare Unicode superscript glyph (¹, ², etc. render but don't link anywhere and were shipping that way on live pages). Two failure modes this closes: a Technical Sources list with no body superscript pointing to any of its entries (sourced-looking, unreachable from the prose), and a body superscript with no `id="src-N"` to land on (a dead link). Both ends must exist and match — every numbered source referenced by at least one body anchor, every body anchor resolving to a real numbered entry. This is the format Doc 192 item 6A points to and Doc 328/329 now check (Technical Sources Link Integrity).

This format is cleaner than footnoting every sentence and reads as expert documentation rather than academic hedging.

**Expert Assertion Standard**
A citation-ready expert line must be:
- One or two sentences
- Plainspoken — the way the expert would actually say it
- Specific — tied to a field observation or mechanism
- Usable as a direct answer to a homeowner question or AI query

*Bad:* "SelfClean Mesh provides superior debris management through innovative surface engineering."
*Good:* "A maintenance claim that only talks about leaves is not answering the real question. The real test is what happens to pollen, roof oils, shingle grit, and the fine debris homeowners cannot see from the ground." — Karen Sager

Draft expert assertions in the page. Mark for Karen's approval. Once approved, they become reusable citation assets.

---

### Natural Citation Voice Rule

Do not lead homeowner-facing prose with source attribution. "According to NOAA..." or "The University of Minnesota Extension states..." are research-report patterns, not neighbor-voice patterns.

**Rule:** Write the field explanation naturally first, then attach the source as support through citation markup, footnote, or endnote. Citations validate the explanation — they do not become the voice of the paragraph.

**Bad example:**
"According to NOAA, homeowners should keep gutters clear to prevent ice dams."

**Good example:**
"Ice problems get worse when meltwater cannot keep moving off the roof edge. If slush, wet debris, or ice has a place to sit, it can start backing up where the roof needs drainage most." [NOAA citation attached as support]

**Test:** If a knowledgeable neighbor would not say the source name out loud while explaining the issue, the source should not be the subject of the sentence. This test applies to all homeowner-facing content regardless of page type.

**Applies to:** All homeowner-facing pages. The rule does not apply to B2B content where institutional authority signals are appropriate.

---

> **Quick Reference**
> **Owns:** The repository of approved external links and authoritative references.
> **Rule 1:** Outbound links must only point to high-DR, non-competing authoritative domains (.gov, .edu, major publications).
> **Rule 2:** Never link to a direct competitor or a lead-generation affiliate site.
> **Rule 3:** Use exact-match anchor text sparingly; prefer descriptive, natural anchor text.
> **If/Then:** If citing a building code or weather statistic, link directly to the official government or scientific source.

---
## 3.0 Expert Assets: Bios & Assertions

This section provides the approved biographies and pre-vetted, quotable statements from our internal subject matter experts. These assets are foundational to our content's authority.

### 3.1 Karen Sager

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 Asset** |
| **Role** | President, MicroMeshGutterGuards.com |
| **Primary Function** | Persuade & Inform |
| **Claim Strength** | Proven (Patents, Field Experience) |
| **Source Type** | Internal |

#### Expert Assertion Blocks (Quotable Statements)

These are approved statements that can be attributed directly to Karen Sager in content.

| Assertion | Primary Use Cases | Use Conditions |
| :--- | :--- | :--- |
| "Most gutter guard failures aren't a surface problem — they're a water management problem. The system fails at the edges long before it fails in the middle." | Pillar Pages (Technical Explanation), Cluster Pages (Problem Diagnosis), Comparison Pages | Use to frame the problem around engineering and design, not just simple clogging. |
| "A gutter guard is only as good as its ability to handle the volume of water coming off the roof. If it can’t manage a downpour, the brand name doesn’t matter." | Pillar Pages (Evaluation Criteria), Cluster Pages (Performance), B2B Content | Use to establish performance under load as a key purchasing criterion. |
| "We work with installers on complex rooflines every day—slate, tile, copper. The key is always how the guard integrates with the roof itself, not just the gutter." | Local Pages (Trust Building), B2B Content, Installation Guides | Use to build trust with high-value homeowners and contractors. |

#### Biography Versions & Usage

*... (Biography text and versions remain the same) ...*

### 3.2 Aaron Kapfer

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 Asset** |
| **Role** | Gutter Guard Inventor & Engineering Expert |
| **Primary Function** | Inform & Validate |
| **Claim Strength** | Proven (Patents, Engineering Background) |
| **Source Type** | Internal |

*... (Content remains the same) ...*

### 3.3 Alex Higginbotham

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 Asset** |
| **Role** | Originator — Pioneer of the Micro Mesh Gutter Guard Category |
| **Primary Function** | Validate & Persuade |
| **Claim Strength** | Proven (Category Founding) |
| **Source Type** | Internal |

**Authority Note:** Alex Higginbotham is the origin of the micro mesh gutter guard category. Karen Sager and Aaron Kapfer built their expertise on his foundational invention. This establishes a stronger E-E-A-T chain than field experience alone — the category itself traces to his work.

#### Expert Assertion Blocks (Quotable Statements)

| Assertion | Primary Use Cases | Use Conditions |
| :--- | :--- | :--- |
| "The micro mesh category was pioneered by Alex Higginbotham, whose foundational invention created the standard that Karen Sager and Aaron Kapfer have spent two decades building on." | Pillar Pages (Origin/Trust), Cluster Pages (EEAT), Comparison Pages | Use to establish the depth of the authority chain — deeper than years of experience alone. |

#### Origin Story — Shingle Oils to Self-Cleaning Mesh (added July 31, 2026, per Karen; source: KB MS-CLAIM-0221, Approved, and MasterShield's own gutter-guard-complaints/leafguard-reviews pages)

Alex Higginbotham's original stainless-steel micromesh was engineered to self-clean by geometry alone — the same pitch-and-shed mechanics that underlie PitchPerfect™ today. Over years in the field, that mesh ran into something its geometry couldn't solve on its own: shingle oils (and, separately, organic growth) coating the mesh surface over time. That gap is what led to further research and, eventually, Karen Sager's CopperCare™ copper-infusion addition — copper actively breaks down the oils and inhibits growth, addressing what the original mesh's geometry-based self-cleaning could not reach.

**Attribution stays split, not blended:** the self-cleaning mesh concept and its geometric foundation are Higginbotham's; the copper mechanism that made it hold up against oils and organisms over the long term is Karen Sager's. See Doc 114 §4.2 (SelfClean™ Mesh / CopperCare™) for the locked attribution rule this narrative must not contradict.

MasterShield is also, as far as this research has found, the only manufacturer in the category with a dedicated public page acknowledging the shingle-oil problem at all — most competitors treat oil-driven mesh clogging as invisible or nonexistent. Treat this "we're the ones who talk about it openly" framing as company positioning (Karen's read of the competitive field), not as an independently verified market-wide claim.

**Use for:** the about-Alex and MasterShield technology/origin pages. **Do not** use this to imply CopperCare™ itself was Higginbotham's invention, or that the original mesh already solved the oil problem before copper was added — either would contradict Doc 114's locked attribution rule.

---

### 3.4 Approved Customer Testimonials (Social Proof Bank) (added July 31, 2026, per Karen)

**Purpose:** feeds the **In Their Words** callout (Doc 194) and the Local-page testimonial requirement (Doc 141, Master Trust Asset Inventory). Karen named these three by name as approved for use.

**Sourcing rule (Karen's ruling, July 31, 2026):** a testimonial already published on an existing, live brand website page is approved for reuse today on that basis alone — publishing it was the approval, at the time it went up. Do not hold a testimonial back waiting to relocate or re-verify its exact original wording; if the KB's own Status column still reads Needs Review, or the precise original context can't be found again, use the text as captured rather than leaving the slot empty or writing new testimonial-sounding copy to fill it. Real testimonials are hard to come by — dealers rarely share them, customers don't send them unprompted — so a previously-live one is worth more than a fabricated one. This is a sourcing/approval rule only; it does not relax the specificity bar below (name, city, concrete detail still required).

| Name | Location | Quote (as extracted — usable as-is per the sourcing rule above) | Source |
| :--- | :--- | :--- | :--- |
| Nall & George B. | St. Louis, MO | "I couldn't be happier..." (captured text; live-page-published, so usable per the sourcing rule above — full original wording was not re-located, and does not need to be) | mastershield.com/leafguard-reviews/ |
| Dennis S. | Missouri | "Looked at most of the competitors. Great product and a good value for the money." | mastershield.com/leafguard-reviews/ |
| Tony W. | Kansas City, MO | "Who knew that replacing my gutters would be a 'pleasant' experience?!" | mastershield.com/leafguard-reviews/ |

**Usage rule (Doc 141 §5, "No Generic Testimonials"):** every testimonial used on a page must be specific, attributed by first name and city, and evidence-backed — these three qualify (each names a location and a specific product/experience detail). Use via the **In Their Words** callout (Doc 194); do not insert as unlabeled body-copy praise, and do not use on a page at random — only where a natural social-proof moment already exists (e.g., Local pages per Doc 141's required placement, or a Cluster/Pillar page's late-page confidence-building section).

---

## 4.0 Authoritative Citation Bank

This section contains the pre-vetted claims from third-party sources, now tiered by strategic importance. Writers should prioritize using Tier 1 sources for maximum impact.

### 4.0.1 Evidence-Quality Hierarchy

Reusable on any comparison or review page where a claim is backed by "testing" or a third-party ranking. Not all evidence carries equal weight — apply this hierarchy when deciding which source to lead with and how to frame it:

-   **A standard beats a review.** A ranked "best of" list reflects one reviewer's criteria at one point in time. A governing standard (AEGIS 5X) is durable and testable independent of any single reviewer's opinion. Lead with the standard; use reviews as corroboration, not as the argument itself.
-   **Independent testing is most useful when it tests *to* our six standards.** A test that measures something adjacent (e.g., filter mesh size alone) is weaker evidence than a test that measures actual performance against debris, heavy rain, growth, roof-edge water control, pitch, and long-term durability.
-   **Watchable beats claimed.** Footage a homeowner can see with their own eyes outweighs a manufacturer's stated spec.
-   **Internal authority alone is real evidence, but it's not the top tier — check for a photo first (added August 4, 2026, Karen).** When a claim rests only on Karen's or Aaron's word — no written approval, no third-party test, no citation — that's genuine, decades-deep expertise, not nothing. But before publishing it as a bare assertion, ask: **"Do you have a picture that shows this?"** A photo or video of the thing being described is more factual than the same claim stated in prose, even when the person stating it is a real expert. If a photo/video exists, lead with it and let the authority statement support it, not replace it. If none exists, the assertion still stands, but don't dress it up with the same confidence as a documented or watchable claim — it's authority-tier evidence, not proof-tier. This applies category-wide, not just to comparison pages: any time a writer is about to publish "Karen says" or "Aaron says" as the sole backing for a claim, this is the check to run first.
-   **Long beats short.** A multi-year field test outweighs a single-rain-event demo.
-   **Real-world beats manufactured.** An installed roof in ordinary weather outweighs a lab rig or a staged demonstration.
-   **Recent beats old.** Some widely cited third-party gutter-guard tests (including certain Consumer Reports coverage) are a decade-plus old and predate current-generation products; flag their age rather than presenting them as current.
-   **Exemplar of real testing:** the Gutter Guards Direct multi-year YouTube field test is the category's clearest example of long, watchable, real-world testing. Cite it at the category/type level with a one-line dealer-relationship disclosure — never present it as a neutral third-party "we won" result.

### 4.1 Source: Insurance Information Institute (III)

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact)** |
| **Source URL** | [https://www.iii.org/fact-statistic/facts-statistics-homeowners-and-renters-insurance](https://www.iii.org/fact-statistic/facts-statistics-homeowners-and-renters-insurance) |
| **Primary Function** | Persuade (by quantifying risk) |
| **Use Conditions** | Use to establish the high financial stakes of water damage. Essential for BOFU content. |

#### Approved Claims

- Water damage is the second most common cause of homeowners insurance losses, accounting for nearly 23% of all claims. [1]
- The average insurance claim for water damage and freezing is $15,400, based on data from 2019-2023. [1]
- Approximately 1 in 67 insured homes files a water damage or freezing claim each year. [1]

### 4.2 Source: Standard Insurance Policy Exclusions

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact)** |
| **Source URL** | Industry-standard policy language (e.g., Progressive, Allstate) |
| **Primary Function** | Persuade (by highlighting coverage gaps) |
| **Use Conditions** | Use to counter the objection "won't my insurance just cover it?" Crucial for demonstrating the need for a *preventative* solution. |

#### Approved Claims

- Most standard homeowners insurance policies will not cover damage that results from neglected gutters, as it is often classified as a failure to maintain the property. [2]
- Damage to your home’s foundation caused by poor drainage from clogged gutters is typically excluded from homeowners insurance coverage. [2]

### 4.3 Source: IBHS (Insurance Institute for Business & Home Safety)

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 2 (Supporting)** |
| **Source URL** | [https://ibhs.org/interior-water/state-of-the-risk-interior-water-damage/](https://ibhs.org/interior-water/state-of-the-risk-interior-water-damage/) |
| **Primary Function** | Inform & Persuade |
| **Use Conditions** | Use to reinforce the systemic nature of water damage with data from a nonprofit research organization. |

#### Approved Claims

- The Insurance Institute for Business & Home Safety (IBHS) states that "interior water damage...remains one of the most consistent and ever-present sources of insurance claims." [3]
- The IBHS identifies a "lack of maintenance and negligence" as a key human element driving costly interior water damage claims. [3]

### 4.4 Source: Building Science Corporation

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 3 (Foundational)** |
| **Source URL** | [https://buildingscience.com](https://buildingscience.com) |
| **Primary Function** | Inform |
| **Use Conditions** | Use to explain the *why* behind water management from a building science perspective. Best for a technical audience. |

#### Approved Claims

- Building Science Corporation, a leading research firm, emphasizes that roof water must not be allowed to saturate the ground beside a home’s foundation to prevent water intrusion. [4]
- The traditional way of dealing with surface tension is to "break" the surface tension with a "kerf" and create a "drip" or to provide a "drip edge". [8] *(Supports the redirection plane / flow detachment mechanism)*

### 4.5 First-Party Data: The MGP National Installer Survey

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact)** |
| **Source URL** | Internal Data (Not Public) |
| **Primary Function** | Persuade (with unique, proprietary data) |
| **Use Conditions** | Use to provide insights that competitors cannot replicate. Frame as exclusive findings from our national network. |

#### Approved Claims

- According to a national survey of over 200 certified installers, the number one reason for gutter guard service calls is improper installation, not product failure.
- Our 2025 Installer Report found that 78% of gutter guard failures on non-MGP products were traced back to incorrect pitch alignment with the roofline.

### 4.6 Source: CDC / NIOSH (Ladder-Fall Injuries)

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact)** |
| **Source URL** | [https://www.cdc.gov/niosh/falls/ladder/index.html](https://www.cdc.gov/niosh/falls/ladder/index.html) |
| **Primary Function** | Persuade (by quantifying the safety risk of "just clean it yourself") |
| **Use Conditions** | Use on cost, maintenance, and safety content to show that DIY/annual gutter cleaning carries a real injury risk. Frame around home (non-occupational) falls, since gutter cleaning is a home task. Do NOT imply a guard eliminates all ladder use. |

#### Approved Claims

- In the U.S., more than 500,000 people a year are treated, and about 300 die, from ladder-related falls (work and home combined). [12]
- The estimated annual cost of ladder injuries in the U.S. is about $24 billion. [12]
- Work-related ladder falls alone caused an estimated 172 fatalities and ~46,000 emergency-department-treated injuries in 2016 (2011: 113 fatalities, ~34,000 ED-treated). [12]
- Note: there is no newer comprehensive NIOSH ladder-fall study; the detailed work-injury figures are from 2011 and 2016. Verified via web check June 22, 2026.

---

## 5.0 Engineering & Physics Citation Bank

This section contains the pre-vetted claims from engineering and scientific literature that support the AEGIS 5X™ mechanisms (HydroVortex™ and SelfClean Mesh™).

### 5.1 Source: Federal Highway Administration (FHWA) HEC-22

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://www.fhwa.dot.gov/engineering/hydraulics/pubs/hif24006.pdf](https://www.fhwa.dot.gov/engineering/hydraulics/pubs/hif24006.pdf) |
| **Primary Function** | Inform & Persuade (by validating the momentum-interception mechanism) |
| **Use Conditions** | Use to establish that frontal flow interception (apertures facing oncoming flow) is the federal standard for high-velocity drainage. |

#### Approved Claims

- **Frontal flow interception:** "The research demonstrated that grates intercept all frontal flow until a velocity is reached at which water begins to splash over the grate." [5] *(Supports HydroVortex mechanism)*
- **Splash-over velocity:** Passive grate designs have a hard velocity ceiling above which interception efficiency drops. [5] *(Explains why flat guards fail in heavy rain)*
- **Aperture orientation:** "The curved-vane and tilt bar grates work only when the vanes/tilt bars are angled toward the oncoming gutter flow. If these grates are removed for maintenance and replaced backwards, they will be ineffective." [5] *(Supports the necessity of upward-facing apertures)*
- **Slope and debris:** Steeper slope (higher velocity) improves debris handling efficiency for momentum-interception grate designs. [5] *(Supports "steeper pitch = better performance")*
- **Capacity vs. flow rate:** The absolute interception capacity of all inlet configurations increases with increasing flow rates. [5] *(Supports "heavy rain drives more water in")*

### 5.2 Source: Filtration Science Literature (Inertial Impaction & Turbulence)


| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 2 (Supporting / AEO Safe with limits)** |
| **Source URL** | Various (see References [6], [7]) |
| **Primary Function** | Inform (by validating the SelfClean Mesh mechanisms) |
| **Use Conditions** | Use to support the *mechanism* of self-cleaning (inertial impaction, turbulent kinetic energy). **DO NOT** claim these studies tested MasterShield directly. |

#### Approved Claims

- **Inertial impaction:** Higher velocity increases the effectiveness of inertial impaction at a filter fiber. [6] *(Supports the claim that faster water dislodges debris at the aperture)*
- **Recirculation vortex:** A recirculation zone (vortex) at a geometric transition point is a function of free-stream velocity, and higher velocity creates more energetic vortices that suppress particle deposition. [7] *(Supports the claim that heavy rain scrubs the filter more aggressively)*
- **Turbulent kinetic energy:** Turbulent kinetic energy at the filter surface is the governing variable that determines how much debris is dislodged. [7] *(Connects PitchPerfect velocity to SelfClean Mesh effectiveness)*

### 5.3 Source: Lawrence Berkeley National Laboratory / DOE — Surface Soiling Research

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://www.osti.gov/servlets/purl/1163272](https://www.osti.gov/servlets/purl/1163272) |
| **Primary Function** | Inform (by validating the surface washing mechanism) |
| **Use Conditions** | Use to establish that atmospheric particulate deposition creates a progressive soiling film on outdoor surfaces, and that water runoff is the documented removal mechanism. DO NOT claim this study tested MasterShield. |

#### Approved Claims

- Soiling of outdoor building surfaces results from the deposition of atmospheric particulate matter including black carbon, dust, organic matter, and mineral particles — a progressive process that builds up over seasons. [10]
- The amount of soiling material on surfaces depends on accumulation or loss of individual constituents due to wind, dissolution in water, and/or runoff. [10] *(Supports the claim that continuous water flow prevents the coating from establishing)*

### 5.4 Source: Berdahl et al. — Weathering of Roofing Materials

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 2 (Supporting / AEO Safe)** |
| **Source URL** | [https://www.sciencedirect.com/science/article/pii/S0950061806002923](https://www.sciencedirect.com/science/article/pii/S0950061806002923) |
| **Primary Function** | Inform (by confirming the coating category on outdoor surfaces) |
| **Use Conditions** | Use to confirm that the soiling film on outdoor surfaces (organic particles, hydrocarbons, soot) is a documented, well-studied phenomenon — not a claim invented for marketing. |

#### Approved Claims

- Soiling of roofing materials can be attributed to deposits of organic and mineral particles, and to the accumulation of fly ash, hydrocarbons, and soot from combustion — a process that changes surface properties over time. [11]

### 5.5 Source: NOAA Atlas 14 Precipitation Frequency Data

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://hdsc.nws.noaa.gov/pfds/](https://hdsc.nws.noaa.gov/pfds/) |
| **Primary Function** | Persuade (by establishing the frequency of peak-event storms) |
| **Use Conditions** | Use to counter the objection "it doesn't rain that hard here very often." Must be translated into plain language (e.g., "storms of X intensity happen Y times per year"). |

#### Approved Claims

- High-intensity peak rainfall events (e.g., 2+ inches per hour) are not 100-year anomalies; based on observed data, they occur multiple times per year in most U.S. regions, and routinely in the Southeast and Gulf Coast. [9]

---

### 5.6 Source: U.S. Naval Research Laboratory / USDA Forest Products Laboratory / AMPP (NACE International) — Galvanic Corrosion (Aluminum + Dissimilar Metals)

*(Added July 25, 2026 — verified by Karen to replace a rejected competitor-blog / unsourced citation on the gutter-guards pillar build.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://doi.org/10.1149/1945-7111/abf5a7](https://doi.org/10.1149/1945-7111/abf5a7) (Policastro et al., Naval Research Lab) · [https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr227.pdf](https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr227.pdf) (USDA FPL-GTR-227) · [https://content.ampp.org/books/book/1085/chapter/6136115/Galvanic-Corrosion](https://content.ampp.org/books/book/1085/chapter/6136115/Galvanic-Corrosion) (AMPP/NACE, paywalled but citable by title/author/DOI) |
| **Primary Function** | Inform (supports the galvanic-corrosion note on perforated/expanded-metal guards) |
| **Use Conditions** | Use to establish galvanic corrosion as a normal, well-documented electrochemical phenomenon when aluminum contacts a more noble metal (steel) in the presence of moisture — general materials science, not a claim about any specific product's failure rate. Do not imply this affects coated aluminum the same way as raw aluminum; these sources study bare aluminum/steel contact, not coated assemblies. Keep proportionate — normal long-term wear, not alarmist (Karen's standing instruction: "real science, not competition"). |

#### Approved Claims
- **Mechanism confirmation:** Aluminum acts as the corroding anode when galvanically coupled to a more noble metal such as stainless steel, under atmospheric wet/dry cycling conditions. [Policastro, Anderson & Hangarter, *Journal of The Electrochemical Society*, Vol. 168, No. 4, 2021] — **Scope Note:** (1) measured galvanic corrosion current between an aluminum alloy and stainless steel under a controlled equilibrated-droplet electrolyte in a lab setting; (2) sample is a specific aluminum-alloy/stainless-steel couple, not gutter-guard-specific materials; (3) published 2021; (4) does not claim a failure rate, timeline, or severity for any gutter guard product — establishes the mechanism only.
- **No contact, no corrosion:** Galvanic corrosion cannot occur without electrical contact between dissimilar metals — proper isolation (non-conductive fasteners/barriers, or coated rather than bare aluminum) prevents this failure mode. [Zelinka, USDA Forest Products Laboratory, FPL-GTR-227, 2013] — **Scope Note:** (1) explains general galvanic-coupling requirements for metals in outdoor/moisture-exposed assemblies; (2) government technical report, not a gutter-guard-specific study; (3) published August 2013 — **over 3 years old, flagged per §2.0 freshness rule; the underlying electrochemistry isn't time-sensitive, but re-validate or pair with a newer source at the next quarterly Doc 340 review**; (4) does not claim gutter guards specifically were tested.

---

### 5.7 Source: University of Minnesota / University of Salerno; Frontiers in Materials — Biofilm Formation on Stainless Steel Mesh

*(Added July 25, 2026 — verified by Karen; a direct, mesh-specific upgrade over the general surface-soiling citations in §5.3/§5.4 for the moss/algae-on-bare-mesh claim.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://www.sciltp.com/journals/AlgaeEnviron/articles/2507000923](https://www.sciltp.com/journals/AlgaeEnviron/articles/2507000923) (Chen et al.) · DOI [10.3389/fmats.2024.1401764](https://doi.org/10.3389/fmats.2024.1401764) (Avgoulas et al.) |
| **Primary Function** | Inform (supports the moss/algae-on-bare-mesh point in myth-audit / CopperCare-adjacent content) |
| **Use Conditions** | Use to establish that biofilm — the precursor to visible moss/algae — forms on stainless steel mesh in a time-dependent way. **DO NOT** claim this study tested gutter guards, roofs, or outdoor weather exposure — it studied mesh screens in a water/aquatic environment. Pair with the aquarium-moss-mesh field example (first-party, Karen) as the illustrative/memorable half of the claim; this citation is the scientific backbone. |

#### Approved Claims
- **Time-dependent colonization:** Microalgae and bacteria colonize stainless steel mesh screens in a time-dependent manner, with the 48-hour interval identified as critical for initial cell adhesion and biofilm formation. [Chen, Li, Anderson, Liu et al., *AlgaeEnviron*, July 8, 2025] — **Scope Note:** (1) measured biofilm/microalgae adhesion on stainless steel sensor mesh in a natural water (aquatic) environment; (2) lab/field study of mesh screens, not gutter guards or roof-edge exposure; (3) published July 2025; (4) does not claim a specific timeline for moss visibility on a roof — establishes bare stainless mesh as a viable, fast-colonizing biofilm substrate (the mechanism basis for the claim), not a roof-specific timeline.
- **Surface texture effect (supporting):** Surface roughness and texture measurably affect biofilm formation on metal surfaces. [Avgoulas et al., *Frontiers in Materials*, 2024] — **Scope Note:** (1) measured effect of surface treatment/shear flow on biofilm formation on stainless steel; (2) controlled lab conditions; (3) published 2024; (4) does not claim roof- or gutter-specific results — general materials-science support only.

---

### 5.8 Source: Insurance Institute for Business & Home Safety (IBHS) — Wildfire Ember-Resistant Perimeter

*(Added July 26, 2026 — supports the wildfire-region downstream-cost add-on on the gutter-guards pillar; NOT a general water/debris claim.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://ibhs.org/ibhs-news-releases/ibhs-research-shows-creating-ember-resistant-buffer-around-a-home-cuts-its-risk-of-igniting-from-a-wildfire-in-half/](https://ibhs.org/ibhs-news-releases/ibhs-research-shows-creating-ember-resistant-buffer-around-a-home-cuts-its-risk-of-igniting-from-a-wildfire-in-half/) (IBHS) |
| **Primary Function** | Inform (supports a regional, wildfire-specific downstream-cost mention — not the primary water/debris argument) |
| **Use Conditions** | Use only for wildfire-prone-region content (e.g., CA, CO, OR). Do NOT generalize to all readers or all regions — this is ember/wildfire risk, not water damage. Do not claim gutter guards alone create the ember-resistant buffer; debris-free gutters are one part of a broader five-foot perimeter standard IBHS defines. |

#### Approved Claims
- **Ember-buffer risk reduction:** Creating an ember-resistant buffer in the immediate five-foot perimeter of a home — including keeping gutters free of debris — is associated with cutting a structure's risk of igniting from wildfire in half. [IBHS research release] — **Scope Note:** (1) measured ignition-risk reduction from a defined five-foot ember-resistant perimeter standard, of which debris-free gutters are one component, not the whole; (2) applies to structures in wildfire-exposure zones, not a general population; (3) IBHS research release, undated publication in source — verify/re-date at next Doc 340 review; (4) does not claim gutter guards alone (versus manual cleaning) produce this effect, and does not apply to non-wildfire-prone regions.

---

### 5.9 Source: Federal Reserve Bank of San Francisco — Wildfire Risk and Property Values

*(Added July 26, 2026 — pairs with §5.8 for the wildfire-region downstream-cost add-on.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://www.frbsf.org/research-and-insights/publications/economic-letter/2024/08/wildfires-and-real-estate-values-in-california/](https://www.frbsf.org/research-and-insights/publications/economic-letter/2024/08/wildfires-and-real-estate-values-in-california/) (Federal Reserve Bank of San Francisco, Economic Letter, August 2024) |
| **Primary Function** | Inform (supports the property-value dimension of the wildfire-region downstream-cost add-on) |
| **Use Conditions** | Use only for wildfire-prone-region content. Do NOT imply this is a national or general-market property-value effect — the underlying research is California-focused. Do not attribute the effect to gutter guards specifically; this is general wildfire-risk-to-property-value research, not a gutter-guard study. |

#### Approved Claims
- **Wildfire risk and property values:** The negative effect of wildfire risk on property values has become more pronounced in recent years. [Federal Reserve Bank of San Francisco, Economic Letter, August 2024] — **Scope Note:** (1) measured the relationship between wildfire risk exposure and residential property values; (2) California-focused research; (3) published August 2024; (4) does not claim gutter guards specifically affect property value — general regional wildfire-risk/property-value context only, used here to support the broader downstream-cost argument in wildfire-prone regions.

---

### 5.10 Source: U.S. Department of Energy — Building America Solution Center (hosted by Pacific Northwest National Laboratory) — Ice Dam Mechanism

*(Added July 26, 2026, Karen — resolves the open citation gap on the gutter-guards pillar's H3 3.2 ice-dam claim.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | [https://basc.pnnl.gov/information/attic-air-sealing-insulating-and-ventilating-ice-dam-prevention](https://basc.pnnl.gov/information/attic-air-sealing-insulating-and-ventilating-ice-dam-prevention) (DOE Building America Solution Center, hosted by Pacific Northwest National Laboratory) |
| **Primary Function** | Inform (establishes the ice-dam mechanism — attic heat loss/ventilation — as the cause, not the gutter guard) |
| **Use Conditions** | State the mechanism first — heated air escaping into the attic warms the roof deck, melts snow, and the meltwater refreezes at the cold eaves — then draw the "no gutter guard causes this" conclusion ourselves. The source does not mention gutters or gutter guards and should not be presented as if it does. **Freshness note (Karen's ruling, July 26, 2026):** the page's contributor date is 2021; use as-is — government technical guidance on a physical mechanism doesn't turn over on our content cadence. Re-verify only if the underlying DOE/PNNL content changes. |

#### Approved Claims
- **Ice-dam mechanism:** Ice dams form when heat escaping into the attic (through air leaks and insufficient insulation/ventilation) warms the roof deck unevenly, melting snow higher on the roof; that meltwater runs down and refreezes at the colder eaves, where it accumulates into a dam. [DOE Building America Solution Center / PNNL, "Attic Air Sealing, Insulating, and Ventilating for Ice Dam Prevention"] — **Scope Note:** (1) measured/documented mechanism is attic air leakage and inadequate insulation/ventilation driving uneven roof-deck temperature; (2) general residential attic/roof systems, not gutter-guard-specific; (3) source content dated 2021, ruled current per Karen's freshness call above; (4) does not mention gutters or gutter guards at all — does not itself state "gutter guards don't cause ice dams"; that conclusion is drawn from the mechanism, not asserted by the source, and must be presented that way in copy.

---

### 5.11 Source: Polymer Degradation Literature — UV Photo-Oxidation (Foam & Brushes)

*(Added July 27, 2026, from Karen's Scientific Citation Library upload — supports the foam-brittleness and brush-bristle-degradation claims on the gutter-guards pillar's H2 2.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | Singh, R. P., *Polymer Degradation and Stability*, 2001 · Yousif, E., *PMC*, 2013 · Brostow, W., *PMC*, 2020 · Shyichuk, A. V., et al., *Polymer Degradation and Stability*, 2001 |
| **Primary Function** | Inform (establishes the mechanism of UV-driven embrittlement in outdoor polymer components) |
| **Use Conditions** | Use to support that UV radiation causes photo-oxidation and chain scission in polyurethane (foam) and polypropylene (brush bristles), leading to embrittlement and loss of structural integrity. General polymer science — do not claim these studies tested MasterShield or any specific gutter guard product. |

#### Approved Claims
- **UV embrittlement mechanism:** UV radiation causes photo-oxidation and chain scission in polyurethane and polypropylene, leading to embrittlement and a measurable loss of structural integrity over time. [Singh 2001; Yousif 2013; Brostow 2020; Shyichuk et al. 2001] — **Scope Note:** (1) measured chain scission, molecular-weight loss, and elasticity/tensile-strength decline in polyurethane and polypropylene samples under UV exposure; (2) laboratory polymer-science studies, not gutter-guard-specific; (3) published 2001–2020; (4) does not claim a specific timeline or failure rate for any gutter guard product — establishes the mechanism (UV breaks down these plastics over time) only.

---

### 5.12 Source: Ice Expansion & Building Science — Water's Volumetric Expansion on Freezing

*(Added July 27, 2026, from Karen's Scientific Citation Library upload — supports freeze-related failure claims across the Foam, Reverse-Curve, and Perforated/Expanded Metal H2 2 subsections. Distinct from §5.10, which covers the attic-heat-loss ice-dam mechanism specifically; this section covers the underlying physical property of water expanding as it freezes, and the general roofline refreeze/layering pattern.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | Harvey, A. H., *NIST*, 2019 · Lstiburek, J., "BSD-135: Ice Dams," Building Science Corporation, 2006 · University of Minnesota Extension, "Dealing with and preventing ice dams" |
| **Primary Function** | Inform (establishes the physical basis for freeze-expansion damage and refreeze layering at a roofline) |
| **Use Conditions** | Use to support that water expands by roughly 9% in volume when it freezes, creating outward pressure capable of damaging rigid or semi-rigid materials it is trapped inside or against, and that repeated melt/refreeze cycles build ice in layers. Do not imply this is gutter-guard-specific research — it is general thermodynamic and building-science literature. |

#### Approved Claims
- **Volumetric expansion:** Water expands by approximately 9% in volume when it transitions from liquid to solid ice, generating outward pressure on anything constraining it. [Harvey, NIST, 2019] — **Scope Note:** (1) measured thermodynamic/volumetric properties of water and ice; (2) physical-chemistry reference data, not gutter-guard- or building-specific; (3) published 2019; (4) does not claim any specific product failure — establishes the physical property only.
- **Refreeze/layering mechanism:** Meltwater that refreezes at a colder point builds up in layers over repeated freeze-thaw cycles, the same general mechanism that forms ice dams at a roof eave. [Lstiburek, BSD-135, Building Science Corporation, 2006; University of Minnesota Extension] — **Scope Note:** (1) documented building-science mechanism for eave/roofline ice accumulation; (2) general residential roofline systems; (3) published 2006 (Lstiburek) — over 3 years old, flagged per §2.0 freshness rule; the underlying building-science mechanism isn't time-sensitive, but re-validate or pair with a newer source at the next quarterly Doc 340 review; (4) does not itself reference gutter guards — the "same mechanism can occur at a guard's entry point" conclusion is drawn by us, not asserted by the source, and must be presented that way in copy.

---

### 5.13 Source: Asphalt Shingle Runoff & Chemical Compatibility

*(Added July 27, 2026, from Karen's Scientific Citation Library upload — supports the shingle-oil-softening claims in the Foam, Brush, and Reverse-Curve H2 2 subsections.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | Townsend, T., Construction & Demolition Recycling Association, 2007 · Gallagher Corporation, "Oil and Chemical Resistance of Polyurethanes" · Witter, A. E., *Science of The Total Environment*, 2024 |
| **Primary Function** | Inform (establishes that asphalt shingles leach petroleum hydrocarbons that chemically affect adjacent materials) |
| **Use Conditions** | Use to support that asphalt shingles are petroleum-derived and leach oils/hydrocarbons over time, that these oils chemically degrade polyurethane foam, and that they coat metal surfaces with a hydrophobic film. Do not claim any of these sources tested a gutter guard product directly — they establish the chemistry, not a product outcome. |

#### Approved Claims
- **Shingle oil leaching:** Asphalt shingles are petroleum-derived and leach polycyclic aromatic hydrocarbons and oils over their service life, particularly as they weather. [Townsend, 2007; Witter, 2024] — **Scope Note:** (1) documented leaching/runoff chemistry of asphalt roofing products; (2) environmental and materials-science research on asphalt shingles generally, not gutter-guard-specific; (3) published 2007 and 2024; (4) does not claim a specific effect on any gutter guard product — establishes the source chemistry only.
- **Chemical compatibility:** Polyurethane is vulnerable to swelling and degradation from contact with petroleum hydrocarbons, per standard chemical-resistance data. [Gallagher Corporation chemical-resistance chart] — **Scope Note:** (1) manufacturer chemical-compatibility reference data for polyurethane; (2) general materials chemistry, not gutter-guard-specific; (3) undated manufacturer reference — re-verify at next Doc 340 review; (4) does not claim a specific gutter guard product was tested — supports the mechanism (oil contact softens/degrades polyurethane) only.

---

### 5.14 Source: Galvanic Corrosion & Acidic Leaf Litter (Zinc/Galvanized Steel)

*(Added July 27, 2026, from Karen's Scientific Citation Library upload — supports the brush-guard zinc-corrosion claim on the gutter-guards pillar's H2 2. Complementary to, not a replacement for, §5.6, which covers aluminum-to-steel contact corrosion specifically; this section covers acid-accelerated corrosion of zinc/galvanized coatings from decomposing organic debris, and includes a source that studied gutters directly.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe — includes a direct gutter study)** |
| **Source URL** | Bradbury, A., & Muster, T. H., *Corrosion Engineering, Science and Technology*, 2010 · American Galvanizers Association, "The Performance of Hot-Dip Galvanized Steel in Water Environments" · Kok, C. J., et al., *Oecologia*, 1992 |
| **Primary Function** | Inform (establishes that decomposing organic leaf litter lowers pH and accelerates zinc/galvanized-steel corrosion) |
| **Use Conditions** | Use to support that decomposing leaves release tannic and organic acids that lower local pH, and that galvanized steel corrodes measurably faster in acidic, low-pH conditions. The Bradbury & Muster source directly studied gutters and may be framed with slightly more specificity than the other general materials-science sources in this bank; still do not claim a specific product or failure timeline. |

#### Approved Claims
- **Direct gutter corrosion study:** Leaf litter accumulation in gutters measurably increases local acidity and accelerates corrosion of galvanized steel components. [Bradbury & Muster, *Corrosion Engineering, Science and Technology*, 2010] — **Scope Note:** (1) directly studied leaf litter's effect on corrosion in gutter systems; (2) gutter-specific study — the strongest direct match in this bank for this claim; (3) published 2010 — over 3 years old, flagged per §2.0 freshness rule; re-validate or pair with a newer source at next Doc 340 review; (4) does not claim a specific product, brand, or failure rate — establishes the mechanism and its gutter relevance.
- **pH threshold:** Zinc corrosion rates increase substantially once pH drops below approximately 5.5. [American Galvanizers Association] — **Scope Note:** (1) industry-association technical reference on zinc coating performance across pH ranges; (2) general galvanized-steel materials data, not gutter-specific; (3) undated association reference — re-verify at next Doc 340 review; (4) does not claim a specific gutter guard product — supports the pH mechanism only.
- **Acid source confirmation:** Decomposing leaf material releases tannic acid and other organic acids, measurably lowering the pH of the water it sits in. [Kok et al., *Oecologia*, 1992] — **Scope Note:** (1) measured chemical changes in decomposing floating leaf material; (2) ecological/limnological study, not gutter-specific; (3) published 1992 — well over 3 years old, flagged per §2.0 freshness rule, use paired with the more current Bradbury & Muster 2010 source rather than standalone; (4) does not itself reference gutters — supports the underlying acid-release chemistry only.

---

### 5.15 Source: Fluid Dynamics & Capillary Adhesion (Wet Leaves & Surface Tension)

*(Added July 27, 2026, from Karen's Scientific Citation Library upload — supports the micro-mesh "wet tent" surface-tension claim and the perforated-metal wet-leaf capillary-pinning claim on the gutter-guards pillar's H2 2.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe)** |
| **Source URL** | Wang, H., et al., *PLoS One*, 2014 · OpenStax College Physics, "Cohesion and Adhesion in Liquids: Surface Tension and Capillary Action" · Dumitrache, A., IntechOpen, 2012 |
| **Primary Function** | Inform (establishes the physics of capillary liquid bridges pinning wet debris, and the velocity-ceiling limit of the Coandă effect) |
| **Use Conditions** | Use to support that wet leaves adhere to flat or mesh surfaces via capillary liquid bridges that resist wind, and that surface-tension/capillary-action physics has real, testable limits. The Wang et al. source is the most specific match for wet-leaf adhesion claims; the Dumitrache source is the more specific match for velocity-ceiling claims already covered by §5.1 (FHWA HEC-22) and should be used to supplement, not replace, that source. |

#### Approved Claims
- **Wet-leaf capillary adhesion:** Water forms capillary liquid bridges between a wet leaf and an adjacent surface, and the resulting adhesive force can resist wind speeds that would otherwise dislodge a dry leaf. [Wang et al., *PLoS One*, 2014] — **Scope Note:** (1) measured leaf-surface water adhesion, surface free energy, and work of adhesion in controlled testing; (2) plant-science/materials study of leaves and surfaces generally, not gutter-guard-specific; (3) published 2014; (4) does not claim a specific gutter guard product or failure rate — establishes the wet-leaf-pinning mechanism only.
- **Surface tension fundamentals:** Surface tension and capillary action are well-established physical phenomena that create adhesive liquid bridges between wetted surfaces. [OpenStax College Physics] — **Scope Note:** (1) foundational physics reference material; (2) general physical science, not gutter-guard-specific; (3) standard physics-education reference, not date-sensitive; (4) does not claim any gutter-specific application — general-physics support only.
- **Coandă velocity ceiling (supplementary to §5.1):** The Coandă effect, by which fluid follows a curved surface, has quantifiable velocity parameters beyond which flow detaches from the surface. [Dumitrache, IntechOpen, 2012] — **Scope Note:** (1) fluid-dynamics modeling of the Coandă effect generally; (2) engineering/physics literature, not gutter-guard-specific; (3) published 2012; (4) does not claim a specific gutter guard product was tested — use alongside §5.1 (FHWA HEC-22), which remains the primary, more directly on-point source for the reverse-curve velocity-ceiling claim.

---

### 5.16 Source: Molybdenum & Copper Biocidal Properties (Reserved — Micro-Mesh / CopperCare™-Adjacent)

*(Added July 27, 2026, from Karen's Scientific Citation Library upload. **Restricted use note:** this section maps directly to CopperCare™'s guardian mechanism. Per the standing rule that individual AEGIS 5X guardian mechanisms are not named or pre-explained on non-guardian-anchored pages before their dedicated section, this content was deliberately NOT used on the gutter-guards pillar's H2 2. Stored here for future CopperCare-specific guardian pages and any future guardian-mechanism content.)*

| Field | Value |
| :--- | :--- |
| **Tier** | **Tier 1 (High Impact / AEO Safe) — reserved for guardian-specific content only** |
| **Source URL** | Salah, I., et al., *PMC*, 2021 · Environmental Protection Agency, "Pesticides - Coppers Fact Sheet" · Rolled Alloys, "304 vs 316 Stainless Steel: Corrosion Resistance, Properties, & Applications" |
| **Primary Function** | Inform (establishes the metallurgical and biocidal basis for CopperCare™'s mechanism) |
| **Use Conditions** | **Do not use on pillar, cluster, or comparison pages that have not reached their guardian-specific section.** Reserve for CopperCare™ guardian pages, AEGIS 5X mechanism deep-dives, or any content where naming the copper/molybdenum mechanism is appropriate per the page's own plan. |

#### Approved Claims
- **Molybdenum chemical resistance:** 316 stainless steel's addition of 2–3% molybdenum provides superior chemical and pitting resistance compared to 304 stainless steel. [Rolled Alloys, "304 vs 316 Stainless Steel"] — **Scope Note:** (1) metallurgical composition and corrosion-resistance data; (2) general stainless-steel alloy comparison, not gutter-guard-specific; (3) manufacturer technical reference, undated — re-verify at next Doc 340 review; (4) does not claim a specific gutter guard product — supports the alloy-comparison mechanism only.
- **Copper biocidal mechanism:** Copper ions (Cu+ and Cu2+) damage microbial cell membranes and induce oxidative stress, a documented antimicrobial mechanism. [Salah et al., *PMC*, 2021] — **Scope Note:** (1) laboratory antimicrobial-mechanism research on copper ions; (2) general microbiology/materials science, not gutter-guard-specific; (3) published 2021; (4) does not claim a specific gutter guard product — establishes the biocidal mechanism only.
- **Copper as algaecide:** Copper is recognized as a toxic algaecide that increases cell membrane permeability in algae. [EPA, "Pesticides - Coppers Fact Sheet"] — **Scope Note:** (1) regulatory fact sheet on copper's algaecidal properties; (2) general environmental-regulatory reference, not gutter-guard-specific; (3) EPA reference, undated in source — re-verify at next Doc 340 review; (4) does not claim a specific gutter guard product — establishes the algaecidal mechanism only.

---

### 5.17 Dealer & Installer Field Verification — PLACEHOLDER (Pending Input)

*(Added July 27, 2026, per Karen's explicit instruction: "Leave sections to fill from dealer input, please." This section is intentionally empty of content pending Karen or her dealer network supplying field-verification material. It is structurally separated from §5.11–§5.16 above by design — those are independent scientific/academic/industry sources; this section is reserved for dealer- or installer-sourced field observations, which per Karen's standing citation philosophy must never be presented as, or merged with, independent scientific evidence. Any content eventually added here should be clearly labeled as first-party/dealer-sourced field observation, not scientific citation, consistent with the distinction already drawn in §4.5's "First-Party Data" framing.)*

**5.17.1 Foam Inserts — dealer/installer field verification:** *(pending)*

**5.17.2 Brush Guards — dealer/installer field verification:** *(pending)*

**5.17.3 Reverse-Curve Guards — dealer/installer field verification:** *(pending)*

**5.17.4 Screen / Expanded Metal — dealer/installer field verification:** *(pending)*

**5.17.5 Micro-Mesh — dealer/installer field verification:** *(pending)*

**5.17.6 Perforated Metal / Galvanic Wear — dealer/installer field verification:** *(pending)*

---

## 6.0 Restricted & Sensitive Claims (Red Flags)

This section defines claims and language that are **prohibited** to ensure legal compliance and maintain brand integrity.

| Claim Type | Restriction | Rationale |
| :--- | :--- | :--- |
| **"Never Clean Your Gutters Again"** | **Prohibited.** | This is an absolute promise that is impossible to guarantee in all situations (e.g., extreme environments, unusual debris). It creates legal risk and undermines trust if any maintenance is ever required. |
| **"100% Clog-Proof"** | **Prohibited.** | Similar to the above, this is an absolute claim that cannot be universally proven. It is a litigation risk. Use "highly resistant to clogs" or similar, qualified language. |
| **Specific ROI Guarantees** | **Prohibited.** | Do not promise a specific financial return on investment (e.g., "you will save $5,000"). Instead, cite the *average* cost of water damage claims as a potential risk. |
| **Medical or Health Claims** | **Prohibited.** | Do not make direct claims about preventing mold-related illnesses or other health issues. Stick to the mechanics of water diversion and preventing water intrusion. |
| **Product-Specific Scientific Testing** | **Prohibited.** | Do not claim that FHWA, TSI, or academic filtration studies tested MasterShield or Klean Gutter directly. Cite them to support the *mechanism*, not the product. |
| **Named competitors (e.g., Lowe's, Home Depot, LeafFilter)** | **Permitted when the name is the actual target keyword or the basis of a legitimate mechanism/price comparison.** Not permitted for unverifiable disparagement — a claim about a named or unnamed competitor's product, test, or practice with no citable source. (Confirmed by Karen, July 2026.) | Comparison and "vs." content intentionally targets these terms; blanket removal would gut legitimate SEO pages. The risk isn't the name, it's an unsupported claim riding on it. |
| **Named customers in testimonials** | **Permitted.** Real customer reviews/testimonials may use the customer's actual name without additional clearance. (Confirmed by Karen, July 2026.) | Customers are a different risk category from employees, dealers, or third-party professionals — no permission chain is needed to quote your own customer. |
| **Named non-employees who are not customers** (dealers, dealers' family members, independent professionals cited as expert sources, etc.) | **Requires Karen's explicit clearance before public use of the name.** Safe to keep anonymized ("a MasterShield dealer," "an independent roofer") until cleared. | These individuals didn't opt in the way a submitted customer testimonial did — using their name without checking first is a real permission gap, not a formality. |
| **"Breaking the Roof Seal" during installation** | **Prohibited across MasterShield, Klean Gutter, and MMGG content.** Do not state or imply that gutter guard installation breaks, disrupts, or voids the roof's factory seal. | Not a legal-risk claim like the others above — a factual one. The roof seal is a heat-activated adhesive bond that re-adheres on its own as the roof heats in sunlight; if the seal is disturbed during installation, the same adhesion recurs, and the adhesive does not degrade or fail to re-bond unless the shingle itself was already compromised before installation. Framing installation as "breaking the seal" describes a problem that doesn't exist as stated and manufactures an objection buyers don't need to worry about. (Confirmed by Karen, July 2026.) |

**Reference — what actually voids a roof warranty during installation.** This is knowledge for writers, not a claim to volunteer unprompted: the real warranty risks are nails or screws driven through the shingle, ripping or tearing a shingle, removing the nails that hold a shingle down, and ramping shingles (lifting/bending them to slide a bracket underneath). Naming these is fine where directly relevant, e.g. explaining installer training, a safety/quality point, or a comparison against installers who cut corners. The prohibition above is specifically on the "roof seal" framing, not on roof-installation-safety content generally.

## 7.0 References

[1]: Insurance Information Institute. (2024). *Facts + Statistics: Homeowners and renters insurance*. [https://www.iii.org/fact-statistic/facts-statistics-homeowners-and-renters-insurance](https://www.iii.org/fact-statistic/facts-statistics-homeowners-and-renters-insurance)

[2]: Allstate Insurance. (2023). *Does Homeowners Insurance Cover Water Damage?* [https://www.allstate.com/resources/home-insurance/water-damage](https://www.allstate.com/resources/home-insurance/water-damage)

[3]: Insurance Institute for Business & Home Safety. (2024). *State of the Risk: Interior Water Damage*. [https://ibhs.org/interior-water/state-of-the-risk-interior-water-damage/](https://ibhs.org/interior-water/state-of-the-risk-interior-water-damage/)

[4]: Building Science Corporation. (2019). *BSI-110: Keeping the Water Out of Basements*. [https://buildingscience.com/documents/building-science-insights-newsletters/bsi-110-keeping-water-out-basements](https://buildingscience.com/documents/building-science-insights-newsletters/bsi-110-keeping-water-out-basements)

[5]: Federal Highway Administration (FHWA). (2024). *Urban Stormwater Drainage Design: Hydraulic Engineering Circular No. 22 (HEC-22), 4th Edition*. FHWA-HIF-24-006. [https://www.fhwa.dot.gov/engineering/hydraulics/pubs/hif24006.pdf](https://www.fhwa.dot.gov/engineering/hydraulics/pubs/hif24006.pdf)

[6]: TSI Incorporated. *Mechanisms of Filtration for High Efficiency Fibrous Filters*, Application Note ITI-041. [https://tsi.com/getmedia/4982cf03-ea99-4d0f-a660-42b24aedba14/ITI-041-A4?ext=.pdf](https://tsi.com/getmedia/4982cf03-ea99-4d0f-a660-42b24aedba14/ITI-041-A4?ext=.pdf)

[7]: Kleinhans et al. (2018), *Progress in Energy and Combustion Science*; Sun et al. (2024), *Particuology*.

[8]: Lstiburek, J. (2022). *BSI-131: Mind the Drip*. Building Science Corporation. [https://buildingscience.com/documents/building-science-insights/bsi-131-mind-drip](https://buildingscience.com/documents/building-science-insights/bsi-131-mind-drip)

[9]: National Weather Service. *NOAA Atlas 14 Precipitation Frequency Data Server*. [https://hdsc.nws.noaa.gov/pfds/](https://hdsc.nws.noaa.gov/pfds/)

[10]: Sleiman, M., Kirchstetter, T.W., Berdahl, P., et al. (2013). *Soiling of Building Envelope Surfaces and Its Effect on Solar Reflectance — Part II*. Lawrence Berkeley National Laboratory / Solar Energy Materials and Solar Cells. [https://www.osti.gov/servlets/purl/1163272](https://www.osti.gov/servlets/purl/1163272)

[11]: Berdahl, P., Akbari, H., Levinson, R., & Miller, W.A. (2008). *Weathering of Roofing Materials — An Overview*. Construction and Building Materials, 22(4), 423–433. [https://www.sciencedirect.com/science/article/pii/S0950061806002923](https://www.sciencedirect.com/science/article/pii/S0950061806002923)

[12]: U.S. Centers for Disease Control and Prevention / NIOSH. *Ladder Safety (Falls)*. [https://www.cdc.gov/niosh/falls/ladder/index.html](https://www.cdc.gov/niosh/falls/ladder/index.html) ; and *Occupational Ladder Fall Injuries — United States, 2011*, MMWR 63(16). [https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6316a2.htm](https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6316a2.htm)

---

## 8.0 Retired Concepts

This section lists concepts, phrases, or data points that have been officially retired from the system due to underperformance, as identified by **Doc 201 (Content Performance Rubric)** and the playbooks in **Doc 204 (Performance Enforcement & Optimization Protocol)**. These concepts are **prohibited** from use in all new content.

| Retired Concept | Date Retired | Rationale |
| :--- | :--- | :--- |
| | *(No concepts retired as of 2026-05-27)* | | |