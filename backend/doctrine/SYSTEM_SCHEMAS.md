# System Schemas - Complete Pipeline Schema Package
*Execution Plan schema (Section 3) synced to Doc 153 v12.9 — 2026-07-18.*

**Version:** 4.3 | **Last Updated:** August 1, 2026 (Section 4 flagged stale, not resynced -- see note below)

---

## COMPLETE SCHEMA HIERARCHY

```
1. Intel Pack (Doc 300 → Doc 304)
2. Strategic Directive (Doc 304 → Doc 153)
3. Execution Plan Output (Doc 153 → Writer)
4. Writer Output (Writer → Auditor)
5. Auditor QA (Auditor → System)
6. Pipeline Tracking (System State)
```

---

# SECTION 1: INTEL PACK (Previously Defined)

See Version 3.0 for complete Intel Pack schema.

---

# SECTION 2: STRATEGIC DIRECTIVE (Previously Defined)

See Version 3.0 for complete Strategic Directive schema.

---

# SECTION 3: EXECUTION PLAN OUTPUT (Doc 153 → Writer)

### Full Execution Plan Schema — canonical (synced from Doc 153 v12.9, 2026-07-18)

This is the single home for the execution-plan output contract. Doc 153 (the generator) references this section; the Architect (Doc 312), the writers (316/320/324), and the Auditor (Doc 328) all validate against these fields.


```json
{
  "plan_id": "PLAN-[keyword]-[YYYYMMDD]-[N]",
  "directive_id": "string",
  "keyword": "string",
  "brand_deployment": {
    "mode": "multi-brand | single-brand",
    "brands": [
      {
        "name": "string",
        "role": "authority | premium | conversion"
      }
    ]
  },
  "page_type": "pillar | cluster | local",
  "page_subtype": "string — the second-level type that selects the structure/voice companion doc (Doc 316-X). REQUIRED for cluster pages, one of: mechanism | comparison | pricing | symptom | installation | faq | b2b. For pillar pages: guide_pillar (default), technology_architecture_pillar (TAP), or early_resolution_pillar (only if the page passes Doc 160's two-part qualifying test). For local pages: local_geographic. This is the routing trigger read by the Writers (Doc 316/320/324) and the Auditor (Doc 328). See 'Page Subtype — Structure & Voice Routing' below.",
  "page_classification": "source-of-truth | brand-conversion",
  "win_vector": "string",
  "content_angle": "string",

  "buyer_state": {
    "primary": "first_time_buyer | replacement_buyer | diagnostic_buyer | comparison_buyer",
    "secondary": "string — secondary buyer state if mixed audience",
    "bias_guardrail": "string — what NOT to overemphasize based on primary buyer state"
  },

  "language_translation": {
    "internal_terms_to_avoid": [
      "string — e.g. 'hydraulic behavior', 'intake resistance', 'velocity exceeds intake stability', 'debris stabilization', 'puddle dynamic'"
    ],
    "preferred_homeowner_translations": {
      "internal_term": "homeowner_phrase"
    }
  },

  "narrative_attack": {
    "reader_starting_belief": "string — what the reader believes when they arrive",
    "reader_hidden_fear": "string — the unspoken concern below the surface",
    "category_misunderstanding": "string — what the industry has taught them wrong",
    "standard_to_install": "string — the evaluation framework they should use instead",
    "what_not_to_overemphasize": "string — which edge cases or secondary conditions to deprioritize",
    "final_belief": "string — what the reader must believe when they leave"
  },

  "structure": {
    "h1": "string",
    "tldr": {
      "_intent_note": "The top-of-page block is the SKIMMER'S PAGE — the most-read real estate, for the reader who will not scroll. It must (1) open with the Pull (feeling-first, not a definition), (2) answer a couple of the highest-intent questions plainly (these double as AEO above-fold extraction), and (3) give the ready reader somewhere to act. Format is flexible (bullets optional). See Doc 317 §1.5.1.",
      "purpose": "curiosity_hook | problem_statement | decision_brief",
      "voice_direction": "string — conversational register from H2/H3 voice table (e.g. 'Knowledgeable Neighbor: explain the tension like you're standing at the roofline')",
      "bullets": [
        "string — 1-2 sentences each, max 4 bullets"
      ],
      "above_fold_faqs": [
        {
          "question": "string — exact PAA question text",
          "answer_direction": "string — 1-2 sentence answer direction"
        }
      ],
      "required_elements": [
        "core_tension | reader_problem | solution_hint | decision_trigger"
      ],
      "writing_direction": "string — how the TLDR must function (e.g. 'Hook via withheld solution — make reader need the rest of the page')"
    },
    "h2_sections": [
      {
        "h2": "string",
        "h3_subsections": ["string"],
        "purpose": "string",
        "word_count_range": "string",
        "content_direction": "string",
        "narrative_role": "hook | problem_setup | mechanism_explanation | proof | objection_handling | conversion_close",
        "structural_layer": "Tension | Mechanism | Proof | Tension Reset | Authority | Resolution | CTA",
        "emotional_stage": "Clarity | Concern | Consequence | Reassurance | Control | Confidence | Action",
        "strategic_why": "string — why this section exists in the argument progression",
        "voice_direction": "string — conversational register (e.g. 'Knowledgeable Neighbor: explain shelf metaphor without jargon')",
        "section_priority": "core | supporting | required | optional",
        "required_knowledge_graph": [
          {
            "doc": "430 | 431 | 432 | 433 | 434",
            "ref": "truth_id or edge_id or section_ref",
            "purpose": "establish_authority | provide_proof | address_objection | support_claim"
          }
        ],
        "required_media": [
          {
            "type": "comparison_diagram | mechanism_cutaway | before_after | infographic | installation_photo | chart | diagnostic_illustration",
            "count": 1,
            "purpose": "explain | prove | persuade | break_tension",
            "alt_text_direction": "string"
          }
        ],
        "competitor_handling": {
          "address_competitors": true | false,
          "approach": "describe_type_not_name | mechanism_gap | cost_comparison | omit",
          "note": "string"
        },
        "schema_applicable": ["FAQ", "HowTo", "Product", "Article", "LocalBusiness"],
        "field_story_required": {
          "homeowner_observation": "string — what the homeowner sees or experiences in real-world conditions",
          "field_reality": "string — what is actually happening mechanically or physically",
          "mechanism_translation": "string — how the mechanism connects the observation to the reality in plain language"
        }
      }
    ]
  },

  "narrative_rationale": {
    "core_argument": "string — the single sentence the entire page supports",
    "section_progression": [
      {
        "section_h2": "string",
        "role": "hook | problem_setup | mechanism_explanation | proof | objection_handling | conversion_close",
        "what_it_must_establish": "string — what the reader must believe after this section"
      }
    ]
  },

  "media_plan": {
    "image_budget": {
      "value": "number — max(ceil(target_body_words/500), ceil(competitor_avg_images*1.2), page_type_floor); see Step 14 + Doc 190",
      "target_body_words": "number",
      "competitor_avg_images": "number",
      "page_type_floor": "number"
    },
    "minimum_images": "number — DEPRECATED backstop; use image_budget. Retained for compatibility; must equal page_type_floor",
    "image_style_note": "string — consistent style guidance (e.g. technical diagram style, photo composition)",
    "images_required": [
      {
        "id": "IMG-001",
        "placement_section": "H2 text",
        "type": "comparison_diagram | mechanism_cutaway | before_after | infographic | installation_photo | chart | diagnostic_illustration",
        "count": 1,
        "purpose": "explain | prove | persuade | break_tension",
        "alt_text_direction": "string"
      }
    ]
  },

  "citation_resource_assignments": [
    {
      "assignment_id": "CRA-001",
      "section": "H2 text",
      "citation_block_id": "CIT-001",
      "doc_113_ref": "statistic_id or quote_id — the specific entry from Doc 113",
      "usage_note": "string — how to incorporate into the section"
    }
  ],

  "prebuilt_citation_blocks": [
    {
      "id": "string",
      "type": "definition | comparison | failure | mechanism",
      "placement_section": "H2 text",
      "canon_truth_ref": "Doc 430 truth_id or Doc 433 principle or Doc 434 edge_id",
      "answer_format_pattern": "Doc 431 answer_object_pattern_name",
      "exact_statement": "pre-written 2-4 sentence extractable block — AI-ready, self-contained, citation-grade",
      "doc_113_refs": ["CRA-001"],
      "brand_applies_to": "all | MasterShield | Klean Gutter | MicroMeshGutterGuards.com"
    }
  ],

  "schema_plan": {
    "required_schemas": [
      {
        "type": "FAQ | HowTo | Article | Product | LocalBusiness | BreadcrumbList | VideoObject",
        "placement": "global | section_id or H2 text",
        "key_properties": ["string — required property names"],
        "purpose": "string — why this schema type is needed"
      }
    ],
    "notes": "string — any additional schema guidance"
  },

  "citation_intent_map": {
    "blocks": [
      {
        "id": "string",
        "type": "definition | comparison | failure | mechanism",
        "location": "string",
        "plain_language_statement": "string",
        "extractable": true | false
      }
    ],
    "minimum_required": "number"
  },
  
  "trust_callout_plan": {
    "points": [
      {
        "id": "string",
        "placement": "early | mid | late",
        "purpose": "credibility | proof | myth_breaking | decision_reinforcement",
        "type": "engineering_insight | field_experience | data_backed",
        "content_direction": "string"
      }
    ],
    "minimum_required": "number"
  },
  
  "cta_plan": {
    "primary_cta": {
      "placement": "string",
      "type": "soft | medium | hard",
      "intent": "education | comparison | conversion",
      "language_direction": "string"
    },
    "secondary_ctas": [
      {
        "placement": "string",
        "type": "string",
        "intent": "string"
      }
    ]
  },
  
  "aegis_guardians": [
    {
      "name": "string",
      "problem": "string",
      "mechanism": "string",
      "outcome": "string"
    }
  ],
  
  "zero_click_element": {
    "type": "interactive_tool | hyperlocal_diagnostic | gated_data | faq_block",
    "description": "string",
    "placement": "string"
  },
  
  "multi_version_plan": {
    "required": true | false,
    "versions": [
      {
        "brand": "string",
        "role": "string",
        "tone_adjustment": "string",
        "emphasis_shift": "string"
      }
    ]
  },
  
  "execution_targets": {
    "min_citation_blocks": "number",
    "min_trust_points": "number",
    "min_ctas": "number",
    "trust_level": "low | medium | high",
    "word_count_min": "number",
    "word_count_max": "number",
    "page_type_compliance": "string — e.g. 'Pillar: FAQ count = qualifying source rows per Step 6B (do not pad to a fixed number), 4+ cluster links, brand-neutral until resolution'"
  },
  
  "internal_linking_plan": {
    "links": [
      {
        "placement": "string",
        "target_url": "string",
        "anchor_text": "string",
        "purpose": "string"
      }
    ],
    "minimum_required": 2
  },
  
  "entity_enforcement": {
    "required_entities": [
      {
        "name": "string",
        "type": "brand | product | technology | concept",
        "placement": "string",
        "reason": "string"
      }
    ]
  },
  
  "citation_priority": {
    "primary": "citation_block_id",
    "secondary": ["citation_block_ids"]
  },
  
  "prohibited_moves": ["string"],

  "honesty_constraints": [
    {
      "topic": "string — area of known vulnerability or edge condition",
      "internal_truth": "string — what is true about the limitation",
      "public_handling": "string — how to address it if needed without making it the main battlefield"
    }
  ],

  "proof_entity_ownership": {
    "target_entity": "string — the entity the page wants AI to remember (e.g. 'AEGIS 5X' on TAP pages, not 'MasterShield')",
    "preferred_stat_block": "string — the exact phrasing that ties proof to the target entity"
  },
  
  "created_date": "YYYY-MM-DD"
}
```

**page_classification rules:**
- `source-of-truth`: Apply to MMGG-site pages, educational reference pages, and category-level authority pages. Requires Doc 142 Section 2B.1 canonical language. Goal: citation stability and AI extractability.
- `brand-conversion`: Apply to MasterShield, Klean Gutter, and other brand-specific persuasion pages. Requires Doc 142 Section 2B.2 conversion language. Goal: Schwartz-level mechanism force and buyer conversion.
- **Determination rule:** If `brand_deployment.brands[].role = "authority"` → `page_classification = "source-of-truth"`. If role = `"premium"` or `"conversion"` → `page_classification = "brand-conversion"`.

---


# SECTION 4: WRITER OUTPUT (Writer → Auditor)

**Purpose:** Defined contract for what "finished content" looks like.

> **STALE (flagged August 1, 2026, Karen).** This section describes a separate JSON handoff artifact and predates Doc 192's July 10, 2026 pivot to a single self-contained HTML deliverable -- the pipeline no longer produces a distinct "Writer Output" JSON file separate from the page itself. For `extractable_blocks`, `cta_blocks`, `internal_links`, and `entity_usage` specifically, **Doc 192 v2.15's YAML front matter section is authoritative, not this section** -- Doc 328 v16.19 was corrected to point there instead. The rest of this section (content_id, metadata, article_structure, trust_blocks_included, etc.) has not been individually verified against current practice; treat as historical/unconfirmed rather than assuming it still applies. Not rewritten in this pass -- flagged in place so the next person doesn't trust it by default.

### Schema

```json
{
  "content_id": "string",
  "plan_id": "string",
  "keyword": "string",
  "brand": "string",
  "page_type": "string",
  "page_subtype": "string",
  
  "metadata": {
    "title": "string",
    "meta_title": "string",
    "meta_description": "string",
    "slug": "string",
    "canonical_url": "string"
  },
  
  "article_structure": {
    "h1": "string",
    "h2s": ["string"],
    "h3s_by_section": {
      "section_1": ["string"]
    },
    "total_word_count": "number",
    "reading_time": "number"
  },
  
  "extractable_answer_blocks": [
    {
      "id": "string",
      "h2_location": "string",
      "content": "string",
      "word_count": "number",
      "is_citation_target": "yes | no"
    }
  ],
  
  "trust_blocks_included": [
    {
      "id": "string",
      "type": "proof_point | statistic | expert_quote | guarantee",
      "location": "string",
      "content": "string",
      "source_cited": "yes | no"
    }
  ],
  
  "cta_blocks_included": [
    {
      "id": "string",
      "location": "string",
      "text": "string",
      "class": "string",
      "offer_mentioned": "yes | no"
    }
  ],
  
  "internal_links_placed": [
    {
      "url": "string",
      "anchor": "string",
      "location": "string",
      "link_text": "string"
    }
  ],
  
  "source_references": [
    {
      "name": "string",
      "url": "string",
      "used_in": "string"
    }
  ],
  
  "mechanism_mentions": {
    "aegis_5x_count": "number",
    "guardians": [
      {
        "name": "string",
        "count": "number",
        "cause_mechanism_outcome_stated": "yes | no"
      }
    ]
  },
  
  "brand_compliance": {
    "brand_mentions": "number",
    "prohibited_phrasing_found": ["string"],
    "tone_met": "yes | no",
    "persona_adhered": "yes | no"
  },
  
  "entity_usage": {
    "primary_entity": "string",
    "introduction_point": "string",
    "frequency": "number",
    "mechanism_linked": "yes | no"
  },
  
  "execution_targets_met": {
    "citation_blocks_met": "yes | no",
    "trust_points_met": "yes | no",
    "ctas_met": "yes | no",
    "word_count_met": "yes | no"
  },
  
  "prohibited_moves_check": {
    "any_found": "yes | no",
    "violations": ["string"]
  },
  
  "created_date": "date",
  "version": "string",
  "writer_notes": "string"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content_id | string | YES | Unique content ID |
| plan_id | string | YES | Links to Execution Plan |
| keyword | string | YES | Target keyword |
| brand | enum | YES | Brand written for |
| page_type | enum | YES | Page type |
| page_subtype | enum | YES (cluster) | Carried from the Execution Plan; lets the Auditor validate the page-type voice match (Doc 328 Section 2B) |
| metadata | object | YES | Title, meta, slug |
| article_structure | object | YES | H1-H3 map + word count |
| extractable_answer_blocks | array | YES | Citation blocks present |
| trust_blocks_included | array | YES | Trust points present |
| cta_blocks_included | array | YES | CTAs present |
| internal_links_placed | array | YES | Links placed |
| source_references | array | NO | Sources used |
| mechanism_mentions | object | YES | AEGIS 5X tracking |
| brand_compliance | object | YES | Brand rules followed |
| entity_usage | object | YES | Entity placement |
| execution_targets_met | object | YES | Targets achieved |
| prohibited_moves_check | object | YES | Prohibited check |
| created_date | date | YES | Creation timestamp |
| version | string | YES | Version |
| writer_notes | string | NO | Writer context |

---

# SECTION 5: AUDITOR QA (Auditor → System)

**Purpose:** Machine-readable pass/fail, not narrative QA.

### Schema

```json
{
  "audit_id": "string",
  "content_id": "string",
  "plan_id": "string",
  
  "overall_disposition": "approve | revise | reject",
  "qa_pass": "yes | no",
  
  "hard_fail_reasons": [
    {
      "category": "string",
      "issue": "string",
      "evidence": "string",
      "blocking": "yes"
    }
  ],
  
  "soft_warnings": [
    {
      "category": "string",
      "issue": "string",
      "severity": "low | medium | high",
      "recommendation": "string"
    }
  ],
  
  "required_blocks_check": {
    "citation_blocks": {
      "required": "number",
      "found": "number",
      "met": "yes | no"
    },
    "trust_points": {
      "required": "number",
      "found": "number",
      "met": "yes | no"
    },
    "ctas": {
      "required": "number",
      "found": "number",
      "met": "yes | no"
    }
  },
  
  "doctrine_conflicts": [
    {
      "doc_violated": "string",
      "rule": "string",
      "violation": "string"
    }
  ],
  
  "brand_violations": [
    {
      "rule": "string",
      "issue": "string",
      "location": "string"
    }
  ],
  
  "aead_violations": [
    {
      "rule": "string",
      "issue": "string",
      "location": "string"
    }
  ],
  
  "trust_cta_failures": [
    {
      "id": "string",
      "location": "string",
      "issue": "string"
    }
  ],
  
  "win_vector_check": {
    "stated": "yes | no",
    "reinforced": "yes | no",
    "consistent": "yes | no"
  },
  
  "aegis_5x_check": {
    "mentions_minimum": "yes | no",
    "guardians_referenced": "yes | no",
    "cause_mechanism_outcome": "yes | no"
  },
  
  "execution_targets_check": {
    "citation_blocks": "pass | fail",
    "trust_points": "pass | fail",
    "ctas": "pass | fail",
    "word_count": "pass | fail"
  },
  
  "prohibited_moves_check": {
    "any_found": "yes | no",
    "violations": ["string"]
  },
  
  "extraction_readiness": {
    "has_extractables": "yes | no",
    "extractable_quality": "low | medium | high"
  },
  
  "score_card": {
    "structure_score": "number",
    "trust_score": "number",
    "conversion_score": "number",
    "aegis_score": "number",
    "total_score": "number",
    "passing_threshold": "number"
  },
  
  "revision_required": "yes | no",
  "revision_notes": "string",
  
  "auditor_name": "string",
  "audit_date": "date"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| audit_id | string | YES | Unique audit ID |
| content_id | string | YES | Links to Writer Output |
| plan_id | string | YES | Links to Execution Plan |
| overall_disposition | enum | YES | Final decision |
| qa_pass | enum | YES | Pass/fail |
| hard_fail_reasons | array | NO | Blocking issues |
| soft_warnings | array | NO | Non-blocking issues |
| required_blocks_check | object | YES | Block counts |
| doctrine_conflicts | array | NO | Doc violations |
| brand_violations | array | NO | Brand rule violations |
| aeo_violations | array | NO | AEO violations |
| trust_cta_failures | array | NO | Trust/CTA issues |
| win_vector_check | object | YES | Win vector compliance |
| aegis_5x_check | object | YES | AEGIS compliance |
| execution_targets_check | object | YES | Target achievement |
| prohibited_moves_check | object | YES | Prohibited check |
| extraction_readiness | object | YES | AI extraction quality |
| score_card | object | YES | Numeric scoring |
| revision_required | enum | YES | Needs revision? |
| revision_notes | string | NO | Revision instructions |
| auditor_name | string | YES | Auditor ID |
| audit_date | date | YES | Audit timestamp |

### Hard Fail Conditions (Immediate Reject)

```
IF any hard_fail_reasons exist → disposition = reject
IF qa_pass = no → disposition = reject
IF win_vector_check.stated = no → reject
IF aegis_5x_check.mentions_minimum = no → reject
```

---

# SECTION 6: PIPELINE TRACKING (System State)

**Purpose:** Track status across all pipeline stages.

### Schema

```json
{
  "pipeline_id": "string",
  "keyword": "string",
  
  "current_stage": "intake | analyst | router | strategist | execution_plan | writer | auditor | published",
  
  "stage_history": [
    {
      "stage": "string",
      "owner": "string",
      "status": "pending | in_progress | complete | rejected | stalled",
      "entered_date": "date",
      "completed_date": "date",
      "version": "string",
      "output_id": "string",
      "rejection_reason": "string"
    }
  ],
  
  "current_owner": "string",
  "status": "pending | in_progress | complete | rejected | stalled",
  
  "version": "string",
  "last_updated": "date",
  
  "rejection_history": [
    {
      "stage": "string",
      "reason": "string",
      "date": "date",
      "corrective_action": "string"
    }
  ],
  
  "retry_count": "number",
  "max_retries": "number",
  
  "handoff_readiness": {
    "data_complete": "yes | no",
    "validation_passed": "yes | no",
    "ready_for_next_stage": "yes | no"
  },
  
  "publish_state": {
    "published": "yes | no",
    "publish_date": "date",
    "published_url": "string",
    "live": "yes | no"
  },
  
  "priority": "number",
  "notes": "string"
}
```

### Stage Definitions

| Stage | Owner | Output |
|-------|-------|-------|
| intake | Human | Raw data |
| analyst | Doc 300 | Intel Pack |
| router | Doc 306 | Routing decision |
| strategist | Doc 304 | Strategic Directive |
| execution_plan | Doc 153 | Execution Plan |
| writer | Doc 316/320/324 | Writer Output |
| auditor | Doc 328 | QA result |
| published | System | Live page |

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| pipeline_id | string | YES | Unique pipeline ID |
| keyword | string | YES | Target keyword |
| current_stage | enum | YES | Where it is now |
| stage_history | array | YES | All stage history |
| current_owner | string | YES | Who owns current stage |
| status | enum | YES | Current status |
| version | string | YES | Current version |
| last_updated | date | YES | Last change |
| rejection_history | array | NO | All rejections |
| retry_count | number | YES | Retry attempts |
| max_retries | number | YES | Max allowed |
| handoff_readiness | object | YES | Ready to move? |
| publish_state | object | YES | Publish tracking |
| priority | number | NO | Priority score |
| notes | string | NO | Notes |

### Stage Transition Rules

```
IF current_stage.status = rejected:
  → Retry count + 1
  → If retry_count >= max_retries → mark stalled
  → Return to previous stage for rework

IF current_stage.status = complete AND handoff_readiness.ready_for_next_stage = yes:
  → Advance to next_stage
  → Update current_owner

IF current_stage.status = stalled:
  → Alert on duty
  → Require human review
```

---

# COMPLETE PIPELINE FLOW WITH SCHEMAS

```
Doc 300 (Analyst)
    ↓
Intel Pack (Schema 1)
    ↓
Doc 306 (Router)
    ↓
Routing Decision
    ↓
Doc 304 (Strategist)
    ↓
Strategic Directive (Schema 2)
    ↓
Doc 153 (Execution Plan Generator)
    ↓
Execution Plan Output (Schema 3)
    ↓
Doc 316/320/324 (Writer)
    ↓
Writer Output (Schema 4)
    ↓
Doc 328 (Auditor)
    ↓
Auditor QA (Schema 5)
    ↓
Pipeline Tracking (Schema 6) ← Always running
    ↓
Publish
```

---

**Last Updated:** June 8, 2026
**Version:** 4.2