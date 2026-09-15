# Doc 153-EX: Worked Example — Execution Plan

**Version:** 1.0 | **Last Updated:** July 18, 2026 | **Companion to:** Doc 153 (Execution Plan Generator).

A full worked example of a conformant execution plan. Extracted from Doc 153 to keep the generator procedure lean; Doc 153 references this file. Model new plans on it (or on a conformant guardian plan such as the HydroVortex execution plan).

---

## EXAMPLE OUTPUT

```json
{
  "plan_id": "PLAN-gutter-guard-cost-20260410-001",
  "directive_id": "DIR-gutter-guard-cost-20260410-001",
  "keyword": "gutter guard cost",
  "brand_deployment": {
    "mode": "multi-brand",
    "brands": [
      {
        "name": "MicroMeshGutterGuards.com",
        "role": "authority"
      },
      {
        "name": "MasterShield",
        "role": "premium"
      },
      {
        "name": "Klean Gutter",
        "role": "conversion"
      }
    ]
  },
  "page_type": "pillar",
  "win_vector": "Competitors list prices but ignore upfront-cost-to-failure correlation. This creates hidden long-term expenses for homeowners. We solve with engineered durability that eliminates repeat costs.",
  "content_angle": "Cost-focused failure analysis - expose hidden costs of cheap alternatives, position engineered systems as smarter investment",
  
  "structure": {
    "h1": "Gutter Guard Cost: The Real Price of Cheap Protection",
    "tldr": {
      "purpose": "curiosity_hook",
      "voice_direction": "Knowledgeable Neighbor — explain cost-to-failure like you're talking to a homeowner across the fence, not a financial analyst",
      "bullets": [
        "Most gutter guard pricing comparisons ignore the one factor that determines real cost: how often they fail and what that failure does to your home.",
        "A $200 DIY guard that lasts 3 years and causes $15,000 in fascia rot is more expensive than an engineered system that lasts 25.",
        "The difference isn't material thickness or brand name — it's whether the guard manages water behavior or just filters debris."
      ],
      "above_fold_faqs": [
        {"question": "How much do gutter guards cost?", "answer_direction": "Answer with range but immediately introduce cost-to-failure framing — upfront price is misleading without failure economics"},
        {"question": "Are expensive gutter guards worth it?", "answer_direction": "Yes — but only if the engineering addresses real failure modes. Price correlates with surface tension management, not material."}
      ],
      "required_elements": ["core_tension", "reader_problem", "solution_hint"],
      "writing_direction": "Hook via withheld solution — make reader need the cost analysis in the rest of the page"
    },
    "h2_sections": [
      {
        "h2": "The True Cost of Gutter Protection",
        "h3_subsections": ["Why upfront price misleads", "The failure cost equation"],
        "purpose": "Establish win_vector immediately",
        "word_count_range": "600-800",
        "content_direction": "Lead with cost-to-failure correlation",
        "narrative_role": "hook",
        "strategic_why": "Must reframe 'cost' from upfront price to total cost-of-ownership before reader can evaluate any competitor offering",
        "section_priority": "core",
        "required_knowledge_graph": [
          {"doc": "432", "ref": "Gold Answer: cost-to-failure", "purpose": "establish_authority"},
          {"doc": "433", "ref": "Field Doctrine: puddle dynamic", "purpose": "support_claim"}
        ],
        "required_media": [
          {"type": "chart", "count": 1, "purpose": "prove", "alt_text_direction": "Cost comparison over 10 years: cheap guard replacement cycle vs. engineered system single installation"}
        ],
        "competitor_handling": {"address_competitors": true, "approach": "describe_type_not_name", "note": "Reference 'budget guards' generically — do not name brands"},
        "schema_applicable": ["Article"]
      },
      {
        "h2": "What Cheap Gutter Guards Actually Cost You",
        "h3_subsections": ["Common failure modes", "Installation damage risks", "Long-term repair costs"],
        "purpose": "Support win_vector with specific failures",
        "word_count_range": "600-800",
        "content_direction": "Problem-focused, quantify impact",
        "narrative_role": "problem_setup",
        "strategic_why": "Reader must feel the pain of cheap alternatives before they value the engineered solution",
        "section_priority": "core",
        "required_knowledge_graph": [
          {"doc": "434", "ref": "EC-01 through EC-07 (valley overshoot, intake geometry)", "purpose": "provide_proof"},
          {"doc": "433", "ref": "Field Doctrine: diagnostic signals (delayed drainage, isolated clean zones)", "purpose": "provide_proof"}
        ],
        "required_media": [
          {"type": "diagnostic_illustration", "count": 1, "purpose": "explain", "alt_text_direction": "Side-by-side: cheap guard failure progression vs. engineered surface tension management"},
          {"type": "before_after", "count": 1, "purpose": "persuade", "alt_text_direction": "Fascia rot damage from 3-year-old budget guard vs. clean condition of 10-year engineered system"}
        ],
        "competitor_handling": {"address_competitors": true, "approach": "mechanism_gap", "note": "Explain cheap guards lack surface tension engineering — attribute to design philosophy, not brand"},
        "schema_applicable": ["Article"]
      },
      {
        "h2": "Engineered vs. Budget: The Real Comparison",
        "h3_subsections": ["Material differences", "Engineering vs. commodity", "Lifetime value"],
        "purpose": "Comparison block - win the contrast",
        "word_count_range": "500-700",
        "content_direction": "Side-by-side, highlight mechanism gap",
        "narrative_role": "mechanism_explanation",
        "strategic_why": "Reader must understand what engineering actually changes physically — surface tension, flow management — not just trust brand claims",
        "section_priority": "core",
        "required_knowledge_graph": [
          {"doc": "430", "ref": "Primary Canon 3.1-3.2 (root requirement, root failure)", "purpose": "establish_authority"},
          {"doc": "433", "ref": "Field Doctrine: shelf metaphor, misleading zones", "purpose": "support_claim"},
          {"doc": "432", "ref": "Gold Answer: comparison block", "purpose": "address_objection"}
        ],
        "required_media": [
          {"type": "comparison_diagram", "count": 1, "purpose": "explain", "alt_text_direction": "Cross-section: cheap mesh vs. engineered surface tension — showing where water goes in each"}
        ],
        "competitor_handling": {"address_competitors": true, "approach": "mechanism_gap", "note": "Contrast 'surface tension engineering' vs. 'simple filtering' — never name competitors"},
        "schema_applicable": ["Article", "Product"]
      }
    ]
  },

  "narrative_rationale": {
    "core_argument": "The real cost of gutter protection is determined by failure frequency and repair expense, not upfront price — engineered systems outperform commodities over any relevant timeframe.",
    "section_progression": [
      {"section_h2": "The True Cost of Gutter Protection", "role": "hook", "what_it_must_establish": "Cost must be measured over time, not at purchase"},
      {"section_h2": "What Cheap Gutter Guards Actually Cost You", "role": "problem_setup", "what_it_must_establish": "Cheap alternatives create predictable, expensive failures"},
      {"section_h2": "Engineered vs. Budget: The Real Comparison", "role": "mechanism_explanation", "what_it_must_establish": "Engineering changes the physical outcome — surface tension vs. filtering is the real difference"}
    ]
  },

  "media_plan": {
    "minimum_images": 3,
    "image_style_note": "Technical diagram style for mechanism illustrations, real installation photos for proof images — consistent blue/white color palette",
    "images_required": [
      {"id": "IMG-001", "placement_section": "The True Cost", "type": "chart", "count": 1, "purpose": "prove", "alt_text_direction": "10-year cost comparison: cheap guard replacement cycle vs. engineered system single installation"},
      {"id": "IMG-002", "placement_section": "What Cheap Guards Actually Cost", "type": "diagnostic_illustration", "count": 1, "purpose": "explain", "alt_text_direction": "Failure progression of budget guard: clog → overflow → fascia damage over 3-year cycle"},
      {"id": "IMG-003", "placement_section": "Engineered vs. Budget", "type": "comparison_diagram", "count": 1, "purpose": "explain", "alt_text_direction": "Cross-section comparison: surface tension capture vs. passive mesh filtration under heavy flow"}
    ]
  },

  "citation_resource_assignments": [
    {"assignment_id": "CRA-001", "section": "What Cheap Guards Actually Cost", "citation_block_id": "CIT-002", "doc_113_ref": "Section 4.1: water damage claim average $15,400", "usage_note": "Use to quantify the financial risk of cheap guard failure leading to fascia/water damage"},
    {"assignment_id": "CRA-002", "section": "What Cheap Guards Actually Cost", "citation_block_id": "CIT-002", "doc_113_ref": "Section 4.1: 23% of all homeowners claims are water damage", "usage_note": "Anchor the prevalence argument — this is not rare"}
  ],

  "prebuilt_citation_blocks": [
    {
      "id": "CIT-001",
      "type": "definition",
      "placement_section": "The True Cost",
      "canon_truth_ref": "Doc 432 — Gold Answer: cost-to-failure correlation",
      "answer_format_pattern": "Doc 431 — Bridge Layer: observation-first, mechanism-last",
      "exact_statement": "The real cost of gutter protection isn't the purchase price — it's the total cost over time including repairs, replacements, and hidden damage. Engineered systems that manage water behavior rather than simply filtering debris eliminate the repeat-replacement cycle that makes cheap guards expensive.",
      "doc_113_refs": [],
      "brand_applies_to": "all"
    },
    {
      "id": "CIT-002",
      "type": "failure",
      "placement_section": "What Cheap Guards Actually Cost",
      "canon_truth_ref": "Doc 434 — EC-01 (valley overshoot), EC-02 (intake geometry bottleneck)",
      "answer_format_pattern": "Doc 431 — AO-FAIL-001 (hidden-state failure explanation)",
      "exact_statement": "Budget gutter guards fail because they rely on filtration instead of surface tension engineering. During heavy rain, water sheets over the guard surface rather than channeling inward — causing overflow that rots fascia, saturates foundations, and creates repair costs averaging $15,400 per claim. This is not a manufacturing defect; it is a physics limitation of passive mesh designs.",
      "doc_113_refs": ["CRA-001", "CRA-002"],
      "brand_applies_to": "all"
    },
    {
      "id": "CIT-003",
      "type": "comparison",
      "placement_section": "Engineered vs. Budget",
      "canon_truth_ref": "Doc 430 — Primary Canon 3.1-3.2 (root requirement: control both debris and water simultaneously)",
      "answer_format_pattern": "Doc 431 — Bridge Layer: failure transition → mechanism installation → canon exit",
      "exact_statement": "Engineered gutter protection systems using AEGIS 5X technology manage water through surface tension capture, not filtration. This means they handle heavy flow without overflow, shed debris without clogging, and last 25+ years — compared to the 3-5 year replacement cycle of commodity mesh guards that can't control water behavior under real conditions.",
      "doc_113_refs": [],
      "brand_applies_to": "all"
    }
  ],

  "schema_plan": {
    "required_schemas": [
      {"type": "Article", "placement": "global", "key_properties": ["headline", "author", "datePublished", "dateModified"], "purpose": "Core page schema for all content"},
      {"type": "FAQ", "placement": "zero_click_element", "key_properties": ["mainEntity — array of Question/Answer pairs from PAA data"], "purpose": "AI extraction target for PAA questions"},
      {"type": "Product", "placement": "H2: Engineered vs. Budget", "key_properties": ["name", "description", "offers"], "purpose": "Schema markup for comparison content"}
    ],
    "notes": "FAQ schema maps to the zero-click element only. Product schema covers the engineered system as a product category, not individual brand SKUs."
  },
  
  "citation_intent_map": {
    "blocks": [
      {
        "id": "CIT-001",
        "type": "definition",
        "location": "H2: The True Cost",
        "plain_language_statement": "Cheap gutter guards create hidden costs through frequent failure, fascia damage, and repeat replacement that exceed upfront savings.",
        "extractable": true
      },
      {
        "id": "CIT-002",
        "type": "failure",
        "location": "H2: What Cheap Guards Actually Cost",
        "plain_language_statement": "Budget guards fail in heavy rain because they lack surface tension engineering, causing overflow and fascia rot.",
        "extractable": true
      },
      {
        "id": "CIT-003",
        "type": "comparison",
        "location": "H2: Engineered vs. Budget",
        "plain_language_statement": "Engineered systems with AEGIS 5X technology last 25+ years vs. 3-5 year replacement cycle for commodity guards.",
        "extractable": true
      }
    ],
    "minimum_required": 4
  },
  
  "trust_callout_plan": {
    "points": [
      {
        "id": "TRUST-001",
        "placement": "early",
        "purpose": "credibility",
        "type": "engineering_insight",
        "content_direction": "Reference surface tension physics"
      },
      {
        "id": "TRUST-002",
        "placement": "mid",
        "purpose": "proof",
        "type": "data_backed",
        "content_direction": "Quantify failure rates by guard type"
      },
      {
        "id": "TRUST-003",
        "placement": "late",
        "purpose": "decision_reinforcement",
        "type": "field_experience",
        "content_direction": "Long-term owner testimonials"
      }
    ],
    "minimum_required": 3
  },
  
  "cta_plan": {
    "primary_cta": {
      "placement": "late",
      "type": "hard",
      "intent": "conversion",
      "language_direction": "Get professional quote - see exact 25-year cost"
    },
    "secondary_ctas": [
      {
        "placement": "mid",
        "type": "soft",
        "intent": "education",
        "language_direction": "Compare your options"
      }
    ]
  },
  
  "aegis_guardians": [
    {
      "name": "HydroVortex",
      "problem": "Heavy rain causes overflow on standard mesh",
      "mechanism": "Surface tension capture channels water inward",
      "outcome": "Handles 3 inches/hour - outperforms standard mesh"
    },
    {
      "name": "ShingleSafe",
      "problem": "Installation damages fascia and shingles",
      "mechanism": "Zero-screw installation distributes weight evenly",
      "outcome": "No fascia rot, no shingle damage"
    }
  ],
  
  "zero_click_element": {
    "type": "faq_block",
    "description": "Top 3 PAA questions answered above fold",
    "placement": "Immediately after introduction"
  },
  
  "internal_linking_plan": {
    "links": [
      {
        "placement": "H2: The True Cost",
        "target_url": "/gutter-protection-pillar",
        "anchor_text": "gutter protection system",
        "purpose": "link to pillar for authority"
      },
      {
        "placement": "H2: Engineered vs Budget",
        "target_url": "/aegis-5x-technology",
        "anchor_text": "AEGIS 5X technology",
        "purpose": "link to mechanism page"
      }
    ],
    "minimum_required": 2
  },
  
  "entity_enforcement": {
    "required_entities": [
      {
        "name": "AEGIS 5X",
        "type": "technology",
        "placement": "Introduction + Definition block",
        "reason": "Capture AI citation for technology"
      },
      {
        "name": "surface tension",
        "type": "concept",
        "placement": "Failure explanation block",
        "reason": "Fill AI citation gap"
      }
    ]
  },
  
  "citation_priority": {
    "primary": "CIT-001",
    "secondary": ["CIT-002", "CIT-003"]
  },
  
  "multi_version_plan": {
    "required": true,
    "versions": [
      {
        "brand": "MMGG",
        "role": "authority",
        "tone_adjustment": "System-level explanation, engineering principles",
        "emphasis_shift": "How the technology works, category education"
      },
      {
        "brand": "MasterShield",
        "role": "premium",
        "tone_adjustment": "Precision engineering, performance superiority",
        "emphasis_shift": "Highest performance, engineering excellence"
      },
      {
        "brand": "Klean Gutter",
        "role": "conversion",
        "tone_adjustment": "Practical clarity, smart decisions",
        "emphasis_shift": "Long-term value, smart investment"
      }
    ]
  },
  
  "execution_targets": {
    "min_citation_blocks": 4,
    "min_trust_points": 3,
    "min_ctas": 2,
    "trust_level": "high",
    "word_count_min": 2000,
    "word_count_max": 3000
  },
  
  "prohibited_moves": [
    "Do not list specific competitor prices",
    "Do not lead with price",
    "Do not use soft CTA - revenue intent is high"
  ],
  
  "created_date": "2026-04-10"
}
```

---

**End of Document**

**Version 12.9 (July 15, 2026):** Added Step 6C (SOT Handoff & Hold): dispatches Step 6B's sourced question list to Doc 354 with its evidence, holds the plan at `status: pending_sot` until answers return, blocks writer handoff until then. Companion fix in Doc 354 v4.2.

**Version 12.8 (July 14, 2026):**
- Root cause: building the Gutter Guard Complaints plan, no live Perplexity.ai connection was available to satisfy the mandatory pillar-page requirement, and there was no documented fallback — the plan would have either stalled indefinitely or silently skipped a required input. Karen's direction: build the fallback and write it into the instructions rather than treat it as a one-off workaround.
- Added the **WebSearch Compound-Constraint Harvesting** substitute method (full procedure at Doc 314 Step 2B; referenced here). Used only when direct Perplexity access is unavailable. Same minimum (3+ harvested items) and same grounding discipline as real Perplexity harvesting — every item must trace to something actually found (a URL, a real forum thread, a real PAA-style box for the compound query), never invented. Tagged `source: "websearch_substitute"` to stay distinguishable from `"perplexity"` in the record.
- Companion changes: Doc 314 Step 2B (new), Doc 361 (MasterShield Page Workflow) Section 7B (new Perplexity/AI-follow-up pull instruction, brand-agnostic so it also applies to Doc 361-KG/MMGG).

**Version 12.7 (July 14, 2026):**
- Root cause: building the Gutter Guard Complaints (MasterShield) execution plan surfaced that "Selected Archetype & Decision Axis" — required Execution Plan intake per Doc 316/320/324 and referenced by several page-type modules — was never actually defined or generated anywhere in this document. The field existed only as an expectation on the writer side.
- Added **Argument Archetype & Decision Axis Selection (MANDATORY)** section (after Keyword Bundle Mapping): the 12-archetype table (Explainer, Diagnostic, Myth-Buster, Comparison, Buyer Guide, Problem Escalation, Mechanism Deep Dive, Scenario Narrative, Framework, Data Breakdown, Failure Analysis, Evolution Story), a primary + optional secondary selection rule, and a reject rule for Pillar/Cluster/Local pages missing `archetype.primary`.
- `decision_axis` is flagged undefined pending Karen's confirmation — deliberately not guessed at, to avoid a wrong definition becoming silent canon.
- Fixed Step 8 word count: previously a flat page_type floor with no reconciliation against Doc 160's "beat competitor by 15-20%" rule (noted as a known gap in v12.5's changelog). Added the existing-content test: net-new pages with nothing to benchmark against use the page_type floor; pages rebuilding existing content or with real competitor SERP data use Doc 160's competitor-beat rule instead, even where that exceeds the floor.

**Version 12.3 (July 8, 2026):**
- Restored the Doc 193 citations cut in v12.1 (System Role output format, Step 5 CTA lens); they didn't actually conflict with the page's H2 limit, that was a misread. Doc 193 stays required, keyword→heading map and CTA lens included.

**Version 12.2 (July 6, 2026):**
- Added `early_resolution_pillar` as a third valid pillar `page_subtype`, alongside `guide_pillar` and `technology_architecture_pillar`. Companion change to Doc 160 v3.1, which added the "Exception: Early-Resolution Pillars" section (a documented alternative to the default brand-at-the-end pillar sequence, gated by a two-part qualifying test: real evaluation-stage signal in the SERP/PAA data, and page length/depth where the linear "teach then reveal" build costs completion). Updated the page_subtype routing table and the JSON schema field description to include it.

**Version 12.1 (July 6, 2026):**
- Removed erroneous Doc 193 references (the Output Format mandate in the System Role section, and the CTA-lens citation in Step 5). Doc 193 doesn't exist in this pipeline and contradicted the existing JSON schema / Phase 1–2 output process and the Structure Complexity Limit (10 max H2s for pillar, 6 for cluster) — it described a fixed 15-section YAML front matter that nothing else in this doc implements. Output format now points back to the Execution Plan Output Schema directly; the Eugene Schwartz CTA-voice guidance in Step 5 is kept, just without the fabricated doc citation.
- Corrected the Guardian Proof Layer Rule (Step 4) citation from "Doc 114 Section 4.2.1" to Doc 155 — Proof Entity Ownership Rule. Doc 114 was never in Required Inputs, and proof entity ownership is already governed by Doc 155 elsewhere in this document.

**Version 12.0 (June 8, 2026):**
- Added `page_subtype` field to output schema — the second-level taxonomy under `page_type`. Required for cluster pages; for pillar pages it is guide_pillar (default) or technology_architecture_pillar (TAP); for local it is local_geographic. This is the routing trigger that tells the Writers (Doc 316/320/324) and the Auditor (Doc 328) which 316-X structure/voice companion doc to load.
- Added "Page Subtype — Structure & Voice Routing" section: the full companion-doc routing table, the "unresolved" fallback rule, and the verbatim New Subtype Notification the system emits when a cluster page fits no subtype (names the two artifacts the reviewer must create — a new page_subtype row and a matching 316-X companion).
- Added 3 rejection rules: missing subtype on cluster pages, invalid subtype value, and "unresolved" with no notification raised.
- Clarifies the two-dimension model: `page_type` = architecture; `page_subtype` = structure & voice. Pairs with Doc 317 and the writer agents (316/320/324) and auditor (328).

**Version 10.3 (May 15, 2026):**
- Added H1 naming precision rule: TAP pages must not mislabel AEGIS 5X as a brand or product
- Added TL/DR bullet progression enforcement: [what's promised] → [hidden tension] → [consequence] → [solution hint]
- Added pillar tension enforcement: H2 sections must follow Doc 160's 5-Layer Consumer Journey order
- Added tension plateau prevention: no two consecutive H2 sections with same narrative_role
- Added voice_direction field to TL/DR and H2 section schemas
- Added prime narrative hook extraction rule for problem_setup and mechanism_explanation sections
- Added Perplexity follow-up data as required input for Pillar and TAP pages
- Updated rejection rules for all new constraints
- Updated structure complexity limit by page type
- Enriched H2 section schema: narrative_role, strategic_why, section_priority, required_knowledge_graph, required_media, competitor_handling, schema_applicable
- Added top-level fields: narrative_rationale, media_plan, citation_resource_assignments, prebuilt_citation_blocks, schema_plan
- Added 6 new generation steps (12-17): Narrative Rationale, Knowledge Graph Assignment, Media Plan, Citation Resource Assignment, Citation Block Pre-Build, Schema Placement Planning
- Added 11 new rejection rules for enriched fields
- Updated example output with new fields