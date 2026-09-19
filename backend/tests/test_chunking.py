import pytest
from app.services.chunking import chunk_content_hash, chunk_document

SAMPLE = """# Doc 999: Test Document

**Version:** 1.0

Intro paragraph before any heading. This preamble should become its own chunk
so that front matter is retrievable separately.

## Section One

This is the body of section one. It explains the core mechanism in enough
depth to stand alone when retrieved by an LLM without surrounding context.

### Subsection One-A

Detail under the subsection. Context independence requires this chunk to name
its subject explicitly rather than relying on "as mentioned above".

## Section Two

Second major section with distinct strategy content for retrieval testing.
"""


def test_preamble_becomes_own_chunk():
    chunks = chunk_document(SAMPLE, "999", "Test Document")
    assert chunks[0]["heading_path"] == ""
    assert "Intro paragraph" in chunks[0]["content"]


def test_chunks_are_heading_aligned():
    chunks = chunk_document(SAMPLE, "999", "Test Document")
    paths = [c["heading_path"] for c in chunks]
    assert "Section One" in paths
    assert "Section One > Subsection One-A" in paths
    assert "Section Two" in paths


def test_every_chunk_carries_provenance_header():
    chunks = chunk_document(SAMPLE, "999", "Test Document")
    for chunk in chunks:
        assert chunk["content"].startswith("[Doc 999: Test Document")
        if chunk["heading_path"]:
            assert chunk["heading_path"] in chunk["content"].split("]")[0]


def test_chunk_indexes_are_sequential():
    chunks = chunk_document(SAMPLE, "999", "Test Document")
    assert [c["chunk_index"] for c in chunks] == list(range(len(chunks)))


def test_oversized_section_splits_at_paragraph_boundaries():
    big_section = "## Big\n\n" + "\n\n".join(f"Paragraph {i} " + "x" * 300 for i in range(30))
    chunks = chunk_document(big_section, "998", "Big Doc")
    assert len(chunks) > 1
    for chunk in chunks:
        # Heading line is repeated on every piece of a split section.
        assert chunk["content"].startswith("[Doc 998: Big Doc")
        assert "## Big" in chunk["content"]
    # No paragraph is cut in half.
    all_text = "\n".join(c["content"] for c in chunks)
    for i in range(30):
        assert f"Paragraph {i} " + "x" * 300 in all_text


def test_tiny_fragments_are_dropped():
    content = "# T\n\n## Empty Heading\n\n## Real Section\n\nActual meaningful retrieval content goes here."
    chunks = chunk_document(content, "997", "T")
    headings = [c["heading_path"] for c in chunks]
    assert "Empty Heading" not in headings


def test_content_hash_is_stable():
    assert chunk_content_hash("abc") == chunk_content_hash("abc")
    assert chunk_content_hash("abc") != chunk_content_hash("abd")


def test_no_headings_single_chunk():
    content = "Just plain text with no markdown headings at all, long enough to survive."
    chunks = chunk_document(content, "996", "Plain")
    assert len(chunks) == 1
    assert chunks[0]["heading_path"] == ""


@pytest.mark.parametrize("doc_number,title", [("123", "X"), ("316-MS", "Y")])
def test_doc_numbers_with_suffixes(doc_number, title):
    chunks = chunk_document("# H\n\nBody content for the heading.", doc_number, title)
    assert f"[Doc {doc_number}: {title}" in chunks[-1]["content"]
