# ruff: noqa: E501  (agent prompt prose is deliberately long-form)
"""RAGSEO Auditor Agent.

Audits a content draft against the Doc 328 auditor rubric (loaded live from
the corpus, not hardcoded) plus brand context when provided. Returns a
structured verdict — pass / pass_with_notes / fail — with per-check findings.
A critical-severity failure always forces an overall FAIL, mirroring Doc 328's
critical-fail rule.
"""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.models.agent_task import AgentTask
from app.services.agent_runner import build_retrieval_context
from app.services.agents.llm_output import extract_json
from app.services.doctrine import (
    BRAND_CONFIG,
    detect_brand,
    load_governing_docs,
)
from app.services.llm_client import call_llm

AUDITOR_SYSTEM_PROMPT = """You are the RAGSEO Auditor Agent. You audit content drafts against the Doc 328 rubric provided to you. You are strict, evidence-based, and you never invent checks that are not in the rubric or the supplementary doctrine.

## Verdict Rules (Doc 328)
- Any CRITICAL failure => overall verdict "fail", regardless of score.
- Minor issues that don't block publication => "pass_with_notes".
- Clean run => "pass".

## Scoping (Phase 4 boundary)
- "content" scope = the draft's SUBSTANCE: structure and H2/H3 architecture,
  claims and evidence, trust flow, CTA type, brand voice, AEGIS guardians,
  keyword intent/relevance, technical request adherence.
- "packaging" scope = publish-readiness ARTIFACT / rendered-format requirements
  that only a finished HTML deliverable must carry: YAML front matter object
  form, embedded stylesheet / <style> / canonical CSS, JSON-LD serialization
  formats, Publish-Readiness Manifest, URL slug mechanics, meta-field layout in
  the packed front matter, Tech-Sources <ol> anchor-target markup, and Doc 194
  callout CSS-class rendering (.callout.field, .callout.benefits, .askthis,
  .callout.compare) — NOT the presence of the underlying content itself.
- While the pipeline delivers a markdown DRAFT, packaging checks must NOT block
  the verdict. Mark their scope as "packaging"; they are tracked, not blocking.
  Content substance checks must still block as "content".

## Output Format (mandatory)
Return ONLY a JSON object:
```json
{
  "verdict": "pass" | "pass_with_notes" | "fail",
  "summary": "one-paragraph audit summary",
  "findings": [
    {"check": "rubric check name", "severity": "critical|major|minor|note",
     "status": "pass|fail|warn|n/a", "scope": "content|packaging",
     "notes": "evidence and what to fix"}
  ]
}
```

## Brevity Rules (strict)
- Include findings ONLY for checks that failed or warrant a warning. Do not list passing checks individually.
- Each finding's "notes" must be at most 25 words. State the problem and the fix; never quote draft passages or rubric text.
- The "summary" must be at most 120 words.
- Total response must stay under 600 words."""


class AuditFinding(BaseModel):
    check: str = Field(min_length=1)
    severity: Literal["critical", "major", "minor", "note"] = "minor"
    status: Literal["pass", "fail", "warn", "n/a"] = "warn"
    scope: Literal["content", "packaging"] = "content"
    notes: str = ""

    @field_validator("status", mode="before")
    @classmethod
    def coerce_status(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            if v in {"pass", "fail", "warn", "n/a"}:
                return v
            return "warn"
        return v

    @field_validator("scope", mode="before")
    @classmethod
    def coerce_scope(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            if v in {"content", "packaging"}:
                return v
            return "content"
        return v


class AuditorOutput(BaseModel):
    verdict: Literal["pass", "pass_with_notes", "fail"]
    summary: str = ""
    findings: list[AuditFinding] = []


def _load_content(db: DBSession, input_data: dict) -> tuple[str, dict]:
    content = input_data.get("content")
    if content:
        return content, {}

    source_task_id = input_data.get("source_task_id")
    if source_task_id:
        task = db.query(AgentTask).filter(AgentTask.id == UUID(str(source_task_id))).first()
        if not task:
            raise ValueError(f"Source task {source_task_id} not found")
        output = (task.output_data or {}).get("output") or {}
        content = output.get("content_markdown")
        if not content:
            raise ValueError(f"Source task {source_task_id} has no content_markdown")
        meta = {
            k: output.get(k)
            for k in ("title", "meta_title", "meta_description", "archetype", "content_type", "brand")
            if output.get(k)
        }
        return content, meta

    raise ValueError("Provide either 'content' or 'source_task_id' in input_data")


def run_auditor(db: DBSession, input_data: dict) -> dict:
    content, draft_meta = _load_content(db, input_data)

    brand_input = input_data.get("brand") or ""
    brand = detect_brand(brand_input) if brand_input else detect_brand(content)

    # Governing doctrine: Doc 328 rubric + brand module for tone-anchor checks.
    governing_nums = ["328"]
    config = BRAND_CONFIG.get(brand)
    if config:
        governing_nums.append(config["brand_module"])
    governing_context, provenance = load_governing_docs(db, governing_nums)

    supplement_context, sources = build_retrieval_context(
        db,
        f"audit checks {input_data.get('content_type') or ''} {brand}".strip(),
        top_k=6,
    )
    loaded_numbers = {p["doc_number"] for p in provenance}
    extra_sources = [s for s in sources if s["doc_number"] not in loaded_numbers]

    user_message = f"""## Audit Rubric (Doc 328, live version)
{governing_context}

## Supplementary Doctrine Excerpts
{supplement_context if extra_sources else "(none beyond the rubric)"}

## Brand
{brand}

## Draft Metadata (provided by the writer — audit against this, not an assumed YAML block)
{draft_meta if draft_meta else "(no metadata provided)"}

## Content Draft Under Audit
{content}

Run the audit and return your JSON verdict."""

    response = call_llm(
        system_prompt=AUDITOR_SYSTEM_PROMPT,
        user_message=user_message,
        max_tokens=16384,
    )

    parsed = extract_json(response)
    if parsed is None:
        response = call_llm(
            system_prompt=AUDITOR_SYSTEM_PROMPT,
            user_message=user_message + "\n\nYour previous reply did not contain a parseable JSON object. "
            "Reply with ONLY the JSON verdict object and nothing else.",
            max_tokens=16384,
        )
        parsed = extract_json(response)

    if parsed is None:
        raise ValueError("Auditor response was not parseable JSON")

    try:
        result = AuditorOutput(**parsed)
    except ValidationError as e:
        raise ValueError(f"Auditor output failed validation: {e}") from e

    scoped_demoted = False
    if get_settings().scope_packaging_checks:
        for f in result.findings:
            if f.scope == "packaging":
                demoted = False
                if f.severity == "critical":
                    f.severity = "major"
                    demoted = True
                if f.status == "fail":
                    f.status = "warn"
                    demoted = True
                if demoted:
                    scoped_demoted = True
                    f.notes = (f.notes + " [Scoped: Doc 192 packaging until Phase 4]").strip()

    output = result.model_dump()

    # Enforce Doc 328's critical-fail rule mechanically, not just via prompt.
    has_critical_fail = any(f.severity == "critical" and f.status == "fail" for f in result.findings)
    if has_critical_fail and output["verdict"] != "fail":
        output["verdict"] = "fail"
        output["summary"] = (
            output["summary"] + "\n\nVerdict forced to FAIL: one or more critical checks failed."
        ).strip()
    elif scoped_demoted and output["verdict"] == "fail" and not has_critical_fail:
        # Only Doc 192 packaging checks were blocking — not content failures.
        output["verdict"] = "pass_with_notes"
        output["summary"] = (
            output["summary"] + "\n\nScoped Doc 192 packaging "
            "checks demoted (Phase 4); no content-critical fails remain."
        ).strip()

    return {
        "agent": "auditor",
        "brand": brand,
        "provenance": provenance,
        "supplementary_sources": extra_sources,
        "output": output,
    }
