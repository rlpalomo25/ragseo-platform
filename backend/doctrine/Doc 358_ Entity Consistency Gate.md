# Doc 358 - Entity Consistency Gate

**Version:** 1.0 | **Last Updated:** April 26, 2026

---

## Purpose

Verify cross-property entity consistency before publication. Prevents entity confusion from brand, mechanism, product, dealer, or company naming drift.

---

## Pipeline Position

```
Doc 357 (SOT QA) --> Doc 358 (Entity Check) --> Doc 356 (Eligibility) --> Doc 355 (Local) --> Publish
```

---

## HARD GATE CHECKS

| Check | Source of Truth | Fail Action |
|-------|-----------------|-------------|
| Brand names | Doc 130, 131, 132 | Return to 354 |
| Mechanism naming | Doc 142 (AEGIS 5X) | Return to 354 |
| Product naming | Doc 114 (Brand Fact Registry) | Return to 354 |
| Company description | Doc 430 (Entity Library) | Return to 354 |
| Dealer naming pattern | Dealer DB schema | Return to 356 |

---

## PASS RULE

**All 5 hard gates must pass.** Scored checks are quality enhancers only - does not gate pass/fail but flags quality issues in output.

---

## SCORED CHECKS

| Check | Scoring | Notes |
|-------|---------|-------|
| Local page glossary alignment | 1-3 | Matches central entity definitions? |
| Product ID consistency | 1-3 | SKU/ID match? |
| Proof object flags | 1-3 | Review/references valid? |

---

## OUTPUT: METADATA PACKET

Every approved SOT outputs:

```
{
  primary_question: string,
  entity_definitions: [string],
  product_identifiers: [string],
  mechanism: string,
  faq_pairs: [string],
  comparison_fields: [string],
  external_validation_priority: high/medium/low,
  schema_data: { ... }
}
```

---

## EXTERNAL VALIDATION PRIORITY(TAG)

Tag SOT pages by validation need:

| Query Type | Priority |
|-----------|-----------|
| Comparative/evaluative | HIGH |
| Category contested | HIGH |
| Strong claim reliance | HIGH |
| Standard explanation | MEDIUM |
| Well-proven facts | LOW |

This bridges SOT production to seeding/distribution.