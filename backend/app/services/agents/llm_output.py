"""Shared helpers for extracting structured LLM output.

Writer-style agents return long markdown content, where JSON-escaping is
error-prone — they use a delimiter protocol instead. Structured-verdict
agents (auditor) return pure JSON.
"""
import json

META_DELIMITER = "===RAGSEO_META==="
CONTENT_DELIMITER = "===RAGSEO_CONTENT==="


def _first_json_object(text: str) -> str | None:
    """Return the first balanced JSON object substring in text (brace-aware)."""
    in_string = False
    escape = False
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                return text[start:i + 1]
    return None


def extract_json(text: str) -> dict | None:
    """Extract the first JSON object from an LLM response (fenced or bare)."""
    candidates: list[str] = []

    if "```json" in text:
        candidates.append(text.split("```json", 1)[1].split("```", 1)[0])
    if "```" in text:
        candidates.append(text.split("```", 1)[1].split("```", 1)[0])

    fragment = _first_json_object(text)
    if fragment is not None:
        candidates.append(fragment)
    candidates.append(text)

    for candidate in candidates:
        try:
            parsed = json.loads(candidate.strip())
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            continue
    return None


def parse_meta_content_response(text: str) -> tuple[dict, str]:
    """Parse the writer delimiter protocol into (meta_dict, content_markdown).

    Raises ValueError when either section is missing/unparseable so the task
    fails loudly instead of persisting garbage.
    """
    if META_DELIMITER not in text or CONTENT_DELIMITER not in text:
        raise ValueError("LLM response missing RAGSEO meta/content delimiters")

    meta_raw = text.split(META_DELIMITER)[1].split(CONTENT_DELIMITER)[0]
    content = text.split(CONTENT_DELIMITER)[1].strip()
    if not content:
        raise ValueError("LLM response has empty content section")

    meta_text = meta_raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        meta = json.loads(meta_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM meta block is not valid JSON: {e}") from e
    if not isinstance(meta, dict):
        raise ValueError("LLM meta block is not a JSON object")

    return meta, content
