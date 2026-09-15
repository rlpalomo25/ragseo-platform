# Net-New Topic Research Process (Supporting Document)

**Version:** 1.0 | **Last Updated:** May 19, 2026
**Purpose:** A supporting workflow for generating execution-plan-ready research packages for net-new topics (e.g., new AEGIS 5X Guardians, proprietary materials, or category-defining concepts) that lack existing search volume or standard SEO data.

---

## 1.0 When to Use This Process

This process is used **only** when starting from scratch on a proprietary topic that does not have existing search volume or standard competitor data (e.g., PitchPerfect™, ShingleSafe™, CopperCare™). 

It bypasses the standard Analyst Agent (Doc 300) workflow because there is no historical data to analyze. Instead, it relies on mining community conversations and adjacent problem-aware queries to build relevance for the net-new topic.

## 2.0 The Research Workflow

To build a complete, execution-plan-ready research package, follow these five steps:

### Step 1: Question Mining (The Foundation)
You cannot research a proprietary term that doesn't exist yet. Instead, research the **problem** the proprietary term solves.
*   **Sources:** Reddit (e.g., r/HomeImprovement, r/Roofing), Quora, YouTube comments, and Google People Also Ask (PAA) for adjacent topics.
*   **Goal:** Extract 15-25 verbatim questions that homeowners and contractors are asking about the failure mode or the mechanism.
*   **Output:** A consolidated FAQ list, noting the source type for each question.

### Step 2: Cross-Guardian Link Mapping
For AEGIS 5X Guardian pages, map how the new topic connects to the other four Guardians.
*   **Action:** Review the extracted FAQs. Identify which questions naturally lead to a discussion of another Guardian (e.g., a question about overflow on a PitchPerfect page naturally links to HydroVortex).
*   **Output:** A linking map pairing specific FAQs to target Guardians, including suggested anchor text.
*   *Note: Ensure any proposed links align with the approved bridge logic in Doc 221 (Hub-and-Spoke Linking Topology). If a bridge is marked PENDING in Doc 221, flag it for approval before publishing.*

### Step 3: Keyword Bundling by Intent Stage
Organize the gathered keywords and phrases into distinct bundles based on the user's awareness level. Do this separately for B2C (Homeowner) and B2B (Dealer) audiences.

**B2C Bundles:**
*   **Stage 1 (Problem-Aware):** High-volume queries describing the failure (e.g., "flat gutter guard overflow"). Used above the fold.
*   **Stage 2 (Solution-Aware):** Queries comparing solutions or mechanisms (e.g., "gutter guard roof pitch"). Used in mechanism sections.
*   **Stage 3 (Brand-Recognition):** The proprietary terms (e.g., "PitchPerfect installation"). Used to build entity association.

**B2B Bundles:**
*   **Stage 1 (Dealer Problem-Aware):** Queries about business friction (e.g., "gutter guard installation callbacks").
*   **Stage 2 (Dealer Solution-Aware):** Queries about methodology (e.g., "correct angle for gutter guard installation").
*   **Stage 3 (Brand/Partnership):** Queries about training and dealer programs.

### Step 4: External Citation Pre-Approval
Identify and pre-approve 1-3 highly credible, third-party sources that validate the *problem* (not the product).
*   **Acceptable Sources:** Government agencies (.gov), university extensions (.edu), or recognized industry authorities (e.g., National Weather Service for ice dam risks).
*   **Output:** Source name, URL, the specific citable passage, and a brief explanation of why it supports the narrative.

### Step 5: Architecture Recommendation
Based on the intent mapping and FAQs, draft a recommended H1-H2 structure for the page.
*   **Action:** Map the keyword bundles and FAQs to specific H2 sections to ensure the page flows logically from Problem → Mechanism → Solution.

---

## 3.0 Handoff

Once the research package is complete, it serves as the foundational input for the **Execution Plan Generator (Doc 153)**, utilizing the `intake_override_used: true` flag to bypass the standard data requirements.