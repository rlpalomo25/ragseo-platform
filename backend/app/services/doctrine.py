"""Doctrine loading helpers shared by agents.

Governing doctrine (writer playbooks, brand modules, audit rubrics) is loaded
in full from the ingested corpus — the DB is the source of truth, not prompts
hardcoded in code. Every load produces a provenance stamp (doc number + live
version) per the Doc 329/C17 rule that agents must record which doc versions
they ran against.
"""
from sqlalchemy.orm import Session as DBSession
from app.models.document import Document
from app.config import get_settings

settings = get_settings()


def get_doc(db: DBSession, doc_number: str) -> Document | None:
    return (
        db.query(Document)
        .filter(Document.doc_number == doc_number, Document.status == "active")
        .first()
    )


def stamp_provenance(db: DBSession, doc_numbers: list[str]) -> list[dict]:
    """Provenance stamps for the given doc numbers (missing docs skipped)."""
    if not doc_numbers:
        return []
    docs = db.query(Document).filter(Document.doc_number.in_(doc_numbers)).all()
    by_number = {d.doc_number: d for d in docs}
    stamps = []
    for num in doc_numbers:
        doc = by_number.get(num)
        if not doc:
            continue
        stamps.append({
            "doc_number": doc.doc_number,
            "title": doc.title,
            "version": doc.version,
            "filename": doc.filename,
        })
    return stamps


def load_governing_docs(
    db: DBSession,
    doc_numbers: list[str],
    max_chars_each: int | None = None,
) -> tuple[str, list[dict]]:
    """Load full text of governing docs, formatted for prompt injection.

    Returns (context_text, provenance_stamps). Docs missing from the corpus
    are noted in the context so the agent knows its doctrine coverage is
    partial rather than silently proceeding.
    """
    max_chars = max_chars_each or settings.governing_doc_max_chars
    parts: list[str] = []
    loaded: list[str] = []

    for num in doc_numbers:
        doc = get_doc(db, num)
        if not doc:
            parts.append(f"--- Doc {num}: NOT FOUND IN CORPUS ---")
            continue
        version_note = f" (v{doc.version})" if doc.version else ""
        content = doc.content
        truncated = False
        if len(content) > max_chars:
            content = content[:max_chars]
            truncated = True
        suffix = "\n\n[...truncated at budget...]" if truncated else ""
        parts.append(f"--- Doc {doc.doc_number}{version_note}: {doc.title} ---\n{content}{suffix}\n")
        loaded.append(num)

    return "\n".join(parts), stamp_provenance(db, loaded)


def detect_brand(text: str) -> str:
    """Detect brand from free text. Returns normalized brand key."""
    lower = text.lower()
    if "mastershield" in lower or "master shield" in lower:
        return "mastershield"
    if "klean gutter" in lower or "kleangutter" in lower or "klean-gutter" in lower:
        return "klean_gutter"
    if "mmgg" in lower or "michael & son" in lower:
        return "mmgg"
    return "generic"


BRAND_CONFIG = {
    "mastershield": {"writer_doc": "316", "brand_module": "130"},
    "klean_gutter": {"writer_doc": "320", "brand_module": "131"},
    "mmgg": {"writer_doc": "324", "brand_module": "132"},
}

# MasterShield page-structure companions (Doc 316-* series).
CONTENT_TYPE_STRUCTURE_MAP = {
    "guide": "316-G",
    "pillar": "316-G",
    "local": "316-L",
    "mechanism": "316-M",
    "pricing": "316-P",
    "value": "316-P",
    "comparison": "316-C",
    "category": "316-C",
    "faq": "316-FAQ",
    "answer": "316-FAQ",
    "symptom": "316-Sym",
    "problem": "316-Sym",
    "installation": "316-Ins",
    "b2b": "316-B2B",
    "dealer": "316-B2B",
}


def structure_doc_for(content_type: str | None) -> str | None:
    if not content_type:
        return None
    lower = content_type.lower()
    for key, doc_num in CONTENT_TYPE_STRUCTURE_MAP.items():
        if key in lower:
            return doc_num
    return None
