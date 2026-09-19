"""Hybrid retrieval over the doctrine chunk store.

Combines pgvector cosine similarity with keyword matching using reciprocal
rank fusion (RRF). Degrades to keyword-only search when embeddings are not
configured or not yet computed.
"""

import logging
from dataclasses import dataclass

from sqlalchemy import bindparam
from sqlalchemy import text as sql_text
from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.services.embeddings import embed_query

logger = logging.getLogger(__name__)
settings = get_settings()

RRF_K = 60

# Common words that match everywhere and drown out distinctive terms in
# keyword scoring. Vector search makes this moot once embeddings are enabled.
STOPWORDS = frozenset(
    [
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "but",
        "by",
        "can",
        "do",
        "does",
        "for",
        "from",
        "has",
        "have",
        "how",
        "i",
        "in",
        "into",
        "is",
        "it",
        "its",
        "of",
        "on",
        "or",
        "should",
        "so",
        "than",
        "that",
        "the",
        "their",
        "them",
        "then",
        "there",
        "these",
        "they",
        "this",
        "to",
        "was",
        "were",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "will",
        "with",
        "would",
        "you",
        "your",
    ]
)


def _extract_terms(query: str, limit: int = 8) -> list[str]:
    terms = [t for t in query.replace('"', " ").split() if len(t) >= 3 and t.lower() not in STOPWORDS]
    return terms[:limit]


@dataclass
class RetrievedChunk:
    doc_number: str
    doc_title: str
    series: str | None
    version: str | None
    heading_path: str
    content: str
    score: float

    def as_dict(self) -> dict:
        return {
            "doc_number": self.doc_number,
            "doc_title": self.doc_title,
            "series": self.series,
            "version": self.version,
            "heading_path": self.heading_path,
            "content": self.content,
            "score": round(self.score, 4),
        }


def _vector_search(
    db: DBSession, query_embedding: list[float], top_k: int, doc_numbers: list[str] | None
) -> list[RetrievedChunk]:
    filter_clause = ""
    # pgvector requires the bound parameter to be typed `vector`; raw text()
    # SQL gets no type info from SQLAlchemy, so pass the literal string + cast.
    vector_literal = "[" + ",".join(repr(float(x)) for x in query_embedding) + "]"
    params: dict = {"embedding": vector_literal, "top_k": top_k}
    if doc_numbers:
        filter_clause = "AND d.doc_number IN :doc_numbers"
        params["doc_numbers"] = list(doc_numbers)

    sql = sql_text(f"""
        SELECT d.doc_number, d.title, d.series, d.version,
               c.heading_path, c.content,
               1 - (c.embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM doc_chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE d.status = 'active' AND c.embedding IS NOT NULL
        {filter_clause}
        ORDER BY c.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """)
    if doc_numbers:
        sql = sql.bindparams(bindparam("doc_numbers", expanding=True))
    rows = db.execute(sql, params).fetchall()
    return [
        RetrievedChunk(
            doc_number=r.doc_number,
            doc_title=r.title,
            series=r.series,
            version=r.version,
            heading_path=r.heading_path or "",
            content=r.content,
            score=float(r.similarity),
        )
        for r in rows
    ]


def _keyword_search(
    db: DBSession, query: str, top_k: int, doc_numbers: list[str] | None
) -> list[RetrievedChunk]:
    terms = _extract_terms(query)
    if not terms:
        return []

    # Rank by how many query terms each chunk/doc matches (title hits weigh 2x).
    # Case-insensitive match via lower()/LIKE — dialect-agnostic (no ILIKE needed).
    score_expr = " + ".join(
        f"((CASE WHEN lower(c.content) LIKE lower(:term{i}) THEN 1 ELSE 0 END)"
        f" + (CASE WHEN lower(d.title) LIKE lower(:term{i}) THEN 2 ELSE 0 END))"
        for i in range(len(terms))
    )
    where_clauses = " OR ".join(
        f"(lower(c.content) LIKE lower(:term{i}) OR lower(d.title) LIKE lower(:term{i})"
        f" OR lower(d.doc_number) LIKE lower(:term{i}))"
        for i in range(len(terms))
    )
    filter_clause = ""
    params: dict = {f"term{i}": f"%{t}%" for i, t in enumerate(terms)}
    params["top_k"] = top_k * 2
    if doc_numbers:
        filter_clause = "AND d.doc_number IN :doc_numbers"
        params["doc_numbers"] = list(doc_numbers)

    sql = sql_text(f"""
        SELECT d.doc_number, d.title, d.series, d.version,
               c.heading_path, c.content,
               ({score_expr}) AS match_score
        FROM doc_chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE d.status = 'active' AND ({where_clauses})
        {filter_clause}
        ORDER BY match_score DESC
        LIMIT :top_k
    """)
    if doc_numbers:
        sql = sql.bindparams(bindparam("doc_numbers", expanding=True))
    rows = db.execute(sql, params).fetchall()
    max_score = max((float(r.match_score) for r in rows), default=1.0)
    return [
        RetrievedChunk(
            doc_number=r.doc_number,
            doc_title=r.title,
            series=r.series,
            version=r.version,
            heading_path=r.heading_path or "",
            content=r.content,
            score=float(r.match_score) / max_score,
        )
        for r in rows
    ]


def _reciprocal_rank_fusion(result_sets: list[list[RetrievedChunk]], top_k: int) -> list[RetrievedChunk]:
    """Fuse ranked lists via RRF keyed on chunk identity."""
    scores: dict[tuple, float] = {}
    chunks: dict[tuple, RetrievedChunk] = {}

    for results in result_sets:
        for rank, chunk in enumerate(results):
            key = (chunk.doc_number, chunk.heading_path, hash(chunk.content))
            chunks.setdefault(key, chunk)
            scores[key] = scores.get(key, 0.0) + 1.0 / (RRF_K + rank + 1)

    ordered_keys = sorted(scores, key=lambda k: scores[k], reverse=True)[:top_k]
    fused = []
    for key in ordered_keys:
        chunk = chunks[key]
        chunk.score = scores[key]
        fused.append(chunk)
    return fused


def retrieve(
    db: DBSession, query: str, top_k: int | None = None, doc_numbers: list[str] | None = None
) -> list[RetrievedChunk]:
    """Retrieve the most relevant doctrine chunks for a query."""
    top_k = top_k or settings.retrieval_top_k

    result_sets: list[list[RetrievedChunk]] = []
    query_embedding = embed_query(query)
    if query_embedding is not None:
        try:
            vector_results = _vector_search(db, query_embedding, top_k, doc_numbers)
            result_sets.append(vector_results)
        except Exception as e:
            # Table/column may not exist yet (pre-migration DB); fall back.
            logger.warning("Vector search unavailable, falling back to keyword: %s", e)

    try:
        result_sets.append(_keyword_search(db, query, top_k, doc_numbers))
    except Exception as e:
        # e.g. non-Postgres dialect in tests; document-level keyword match still works.
        logger.warning("Chunk keyword search unavailable: %s", e)

    if not result_sets or all(not rs for rs in result_sets):
        return []
    if len(result_sets) == 1:
        return result_sets[0][:top_k]

    return _reciprocal_rank_fusion(result_sets, top_k)
