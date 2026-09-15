# Doc 355 - Local SOT Agent

**Version:** 2.1 | **Last Updated:** April 28, 2026

---

## Purpose

Creates local-market adaptations from SOT pages by injecting location-specific context.

**Scope:**
- Doc 354 = local-ready structure only
- Doc 355 = actual city/condition injection only

**Clarification:** Doc 355 creates the local page asset from approved SOT parent plus approved local context. It does not decide eligibility.

---

## Pipeline Position

```
Doc 356 (Eligibility Gate) → Doc 355 (Local SOT) → Local Pages
```

**Doc 356 Role:** Validates dealer exists + product matches + conditions valid BEFORE generation

**Doc 354 Scope:** Produces local-ready structure (intro + body template)