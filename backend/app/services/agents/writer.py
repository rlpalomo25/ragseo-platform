"""RAGSEO Writer Agent.

Generates content drafts grounded in the governing doctrine for the detected
brand: the brand's writer playbook (Doc 316/320/324), its brand module
(Doc 130/131/132), and — for MasterShield — the page-structure companion
matching the content type (Doc 316-* series). Supplementary doctrine is
pulled via hybrid retrieval. Output carries a provenance stamp of every doc
version used (Doc 329/C17).
"""
import json
from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlalchemy.orm import Session as DBSession

from app.services.llm_client import call_llm
from app.services.doctrine import (
    BRAND_CONFIG,
    detect_brand,
    load_governing_docs,
    structure_doc_for,
)
from app.services.agent_runner import build_retrieval_context
from app.services.external_data import build_market_context
from app.services.agents.llm_output import (
    CONTENT_DELIMITER,
    META_DELIMITER,
    parse_meta_content_response,
)

WRITER_SYSTEM_PROMPT = """You are the RAGSEO Writer Agent. You produce content drafts that comply exactly with the RAGSEO doctrine excerpts provided to you.

## Hard Rules (Doc 230 mandatory enforcement)
- Follow the Execution Plan / request structure exactly; do not invent H1/H2/H3 headings that contradict it.
- AEGIS 5X: minimum 2 Guardians explained per article where doctrine requires it; each Guardian follows problem -> mechanism -> outcome.
- Trust: every claim Level 2+ minimum; at least one Level 3 or 4 claim per article. Trust flow: early authority, mid transparency, late social proof.
- CTA type must match what the request specifies; never soften or harden it.
- Zero-click defense: include deeper explanation that can't be easily summarized.
- Match the brand voice defined in the brand module excerpt exactly.

## Output Format (mandatory)
Respond with EXACTLY this structure and nothing else:

===RAGSEO_META===
{"title": "...", "meta_title": "...", "meta_description": "...", "archetype": "...", "content_type": "...", "brand": "..."}
===RAGSEO_CONTENT===
<the full content draft in markdown>

The meta block must be a single valid JSON object on one line. The content section is the draft itself in markdown."""


class WriterMeta(BaseModel):
    title: str = Field(min_length=1)
    meta_title: str = Field(min_length=1)
    meta_description: str = Field(min_length=1)
    archetype: str | None = None
    content_type: str | None = None
    brand: str | None = None

    @field_validator(
        "title", "meta_title", "meta_description",
        "archetype", "content_type", "brand", mode="before",
    )
    @classmethod
    def coerce_string(cls, v):
        if isinstance(v, str) or v is None:
            return v
        if isinstance(v, (int, float, bool)):
            return str(v)
        if isinstance(v, dict):
            for key in ("primary", "value", "name", "label"):
                if key in v and isinstance(v[key], str):
                    return v[key]
            prims = [val for val in v.values() if isinstance(val, (str, int, float, bool))]
            return str(prims[0]) if prims else json.dumps(v)
        return json.dumps(v)


def run_writer(db: DBSession, input_data: dict) -> dict:
    request_text = input_data.get("request", "")
    if not request_text:
        raise ValueError("Missing 'request' field in input_data")

    brand_input = input_data.get("brand") or ""
    brand = detect_brand(brand_input) if brand_input else detect_brand(request_text)
    content_type = input_data.get("content_type")

    # 1. Governing doctrine: writer playbook + brand module (+ structure doc).
    config = BRAND_CONFIG.get(brand)
    governing_nums: list[str] = ["100"]  # Master Content Doctrine always applies
    if config:
        governing_nums += [config["writer_doc"], config["brand_module"]]
    structure_num = structure_doc_for(content_type)
    if structure_num and structure_num not in governing_nums:
        governing_nums.append(structure_num)

    governing_context, provenance = load_governing_docs(db, governing_nums)

    # 2. Supplementary retrieval for anything the governing docs don't cover.
    supplement_query = f"{request_text} {content_type or ''} {brand}".strip()
    supplement_context, sources = build_retrieval_context(
        db, supplement_query, top_k=6,
        doc_numbers=input_data.get("applicable_docs") or None,
    )
    loaded_numbers = {p["doc_number"] for p in provenance}
    extra_sources = [s for s in sources if s["doc_number"] not in loaded_numbers]

    # 3. Market data (GSC/GA4/calls/leads/competitors) if available.
    market_context, market_sources = build_market_context(db, brand) if brand else ("", [])

    user_message = f"""## Governing Doctrine (source of truth — comply exactly)
{governing_context}

## Supplementary Doctrine Excerpts
{supplement_context if extra_sources else "(none beyond governing docs)"}

{f"## Supporting Market Data" + chr(10) + market_context if market_context else ""}

## Writing Request
{request_text}

Brand: {brand}
Content type: {content_type or "determine from request"}
"""

    revision_feedback = input_data.get("revision_feedback")
    if revision_feedback:
        user_message += f"""
## Revision Feedback — the previous draft FAILED audit. Fix every finding.
{revision_feedback}
"""

    user_message += "\nWrite the draft now, following the output format exactly."

    response = call_llm(
        system_prompt=WRITER_SYSTEM_PROMPT,
        user_message=user_message,
        max_tokens=16000,
    )

    meta_raw, content_markdown = parse_meta_content_response(response)
    try:
        meta = WriterMeta(**meta_raw).model_dump()
    except ValidationError as e:
        raise ValueError(f"Writer meta block failed validation: {e}") from e

    return {
        "agent": "writer",
        "brand": brand,
        "provenance": provenance,
        "supplementary_sources": extra_sources,
        "market_sources": market_sources,
        "output": {**meta, "content_markdown": content_markdown},
    }
