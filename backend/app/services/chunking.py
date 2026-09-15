"""Chunking service implementing Doc 122 (Retrieval & Chunking Doctrine).

Core principle: every chunk must be context-independent — understandable on its
own when retrieved by an LLM — while preserving the strategic integrity of the
section it came from. Chunks are heading-aligned, never split mid-paragraph,
and each carries a provenance header (doc number, title, heading path) so the
passage is self-describing outside its page.
"""
import hashlib
import re

from app.config import get_settings

settings = get_settings()

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def _split_markdown_sections(content: str) -> list[tuple[list[str], str]]:
    """Split markdown into (heading_path, section_text) at every heading.

    The document preamble (before the first heading) gets an empty path.
    """
    sections: list[tuple[list[str], str]] = []
    matches = list(HEADING_RE.finditer(content))

    if not matches:
        return [([], content)]

    preamble = content[: matches[0].start()].strip()
    if preamble:
        sections.append(([], preamble))

    path_by_level: dict[int, str] = {}
    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        # Level-1 headings are the document title itself — already carried by
        # the provenance header — so they don't repeat inside heading paths.
        if level > 1:
            path_by_level[level] = title
            for deeper in [l for l in path_by_level if l > level]:
                del path_by_level[deeper]
        heading_path = [path_by_level[l] for l in sorted(path_by_level)]
        sections.append((heading_path, content[match.start():end].strip()))

    return sections


def _split_long_section(text: str, max_chars: int) -> list[str]:
    """Split a section that exceeds max_chars at paragraph boundaries."""
    paragraphs = re.split(r"\n\s*\n", text)
    parts: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current and current_len + para_len > max_chars:
            parts.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        parts.append("\n\n".join(current))
    return parts


def _is_heading_only(text: str) -> bool:
    """True when a piece consists solely of heading lines — no retrievable body."""
    remaining = "\n".join(
        line for line in text.strip().splitlines() if not line.lstrip().startswith("#")
    ).strip()
    return not remaining


def chunk_document(
    content: str,
    doc_number: str,
    doc_title: str,
) -> list[dict]:
    """Chunk a doctrine document into context-independent retrieval units.

    Returns a list of dicts: {chunk_index, heading_path, content}.
    """
    max_chars = settings.chunk_max_chars
    chunks: list[dict] = []

    for heading_path, section_text in _split_markdown_sections(content):
        if not section_text.strip():
            continue

        pieces = [section_text]
        if len(section_text) > max_chars:
            # Keep the heading line attached to every piece of an oversized section.
            heading_line = ""
            first_line = section_text.split("\n", 1)[0]
            if first_line.startswith("#"):
                heading_line = first_line + "\n\n"
                body = section_text[len(heading_line):]
            else:
                body = section_text
            pieces = [heading_line + p for p in _split_long_section(body, max_chars)]

        for piece in pieces:
            body = piece.strip()
            if not body or _is_heading_only(body):
                # Bare headings carry no retrievable meaning on their own.
                continue

            header = f"[Doc {doc_number}: {doc_title}"
            if heading_path:
                header += " > " + " > ".join(heading_path)
            header += "]"

            chunks.append({
                "chunk_index": len(chunks),
                "heading_path": " > ".join(heading_path) if heading_path else "",
                "content": f"{header}\n\n{body}",
            })

    return chunks


def chunk_content_hash(chunk_content: str) -> str:
    return hashlib.sha256(chunk_content.encode()).hexdigest()
