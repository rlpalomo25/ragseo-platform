import json
from sqlalchemy.orm import Session as DBSession
from app.services.llm_client import call_llm
from app.services.agent_runner import build_retrieval_context
from app.services.doctrine import detect_brand
from app.services.external_data import build_market_context

ROUTER_SYSTEM_PROMPT = """You are the RAGSEO Router Agent. Your job is to classify an incoming content request and route it to the correct doctrine documents and downstream agents.

## Your Task
Given a content request or brief, determine:
1. **Intent classification** — what type of content is being requested
2. **Brand assignment** — which brand (MasterShield, Klean Gutter, MMGG, or generic)
3. **Content type** — what format/page type
4. **Doctrine routing** — which doctrine documents apply
5. **Next agent** — which agent should handle this next

## Intent Categories
- `broad_problem` — homeowner has a problem, not yet brand-aware
- `evaluation_aware` — homeowner is researching solutions
- `brand_evaluation` — homeowner comparing specific brands
- `replacement_intent` — homeowner ready to buy/replace
- `diagnostic_current_owner` — existing customer needs help
- `b2b` — business-to-business content request
- `internal` — internal doctrine/system content

## Brand Detection
- MasterShield — premium gutter guard, micro-mesh, AEGIS 5X
- Klean Gutter — DIY-friendly, cleaning-focused
- MMGG — Multi-brand, contractor/distributor focused
- Generic — no specific brand mentioned

## Output Format
Return a JSON object with this exact structure:
```json
{
  "intent": "intent_category",
  "brand": "brand_name",
  "content_type": "page_type",
  "applicable_docs": ["doc_number_1", "doc_number_2"],
  "next_agent": "agent_name_or_null",
  "confidence": 0.0_to_1.0,
  "reasoning": "brief explanation"
}
```

## Rules
- If intent is ambiguous, pick the most likely and note low confidence
- Always include Doc 100 (Master Content Doctrine) in applicable_docs for content requests
- Include brand-specific module (Doc 130/131/132) when brand is identified
- For B2B requests, include Doc 174 (B2B Playbook)
- Route to "gap_analyzer" if no existing doctrine covers the request
- Route to "writer" if doctrine exists and is sufficient
- Route to "validator" if content already exists and needs checking"""


def run_router(db: DBSession, input_data: dict) -> dict:
    request_text = input_data.get("request", "")
    if not request_text:
        raise ValueError("Missing 'request' field in input_data")

    context, sources = build_retrieval_context(db, request_text)

    source_lines = "\n".join(
        f"- Doc {s['doc_number']}: {s['doc_title']} | {s['heading_path'] or '(body)'}"
        for s in sources
    ) or "(no doctrine chunks retrieved)"

    pre_brand = detect_brand(request_text)
    market_context, _ = build_market_context(db, pre_brand) if pre_brand else ("", [])

    user_message = f"""## Retrieved Doctrine Excerpts
{context}

## Retrieval Index
{source_lines}

## Content Request
{request_text}

{f"## Brand Performance Context" + chr(10) + market_context if market_context else ""}

Classify this request and return your JSON routing decision. Base applicable_docs on the retrieved excerpts plus your own doctrine knowledge."""

    response = call_llm(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_message=user_message,
        max_tokens=2048,
    )

    json_str = response
    if "```json" in json_str:
        json_str = json_str.split("```json")[1].split("```")[0]
    elif "```" in json_str:
        json_str = json_str.split("```")[1].split("```")[0]

    try:
        result = json.loads(json_str.strip())
    except json.JSONDecodeError:
        result = {
            "intent": "unknown",
            "brand": "unknown",
            "content_type": "unknown",
            "applicable_docs": [],
            "next_agent": None,
            "confidence": 0.0,
            "reasoning": response[:500],
            "raw_response": response,
        }

    result["retrieved_sources"] = sources
    return result
