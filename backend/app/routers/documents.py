from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import or_, func
from app.database import get_db
from app.schemas.document import DocumentResponse, DocumentDetail, DocumentList
from app.models.document import Document, DocReference
from app.models.chunk import DocChunk
from app.models.user import User
from app.dependencies import get_current_user, require_admin
from app.services.doc_ingestion import ingest_all_docs
from app.services.retrieval import retrieve, RetrievedChunk

router = APIRouter()


def _chunk_stats(db: DBSession, doc_ids: list[UUID] | list[str]) -> dict[str, tuple[int, int]]:
    """Chunk total + embedded count per document, as {id: (chunks, embedded)}."""
    if not doc_ids:
        return {}
    rows = (
        db.query(DocChunk.document_id, func.count(DocChunk.id), func.count(DocChunk.embedding))
        .filter(DocChunk.document_id.in_(doc_ids))
        .group_by(DocChunk.document_id)
        .all()
    )
    return {str(doc_id): (total, embedded) for doc_id, total, embedded in rows}


def _to_response(doc: Document, stats: tuple[int, int] | None, snippet: str | None = None,
                 score: float | None = None) -> DocumentResponse:
    return DocumentResponse(
        id=str(doc.id),
        doc_number=doc.doc_number,
        title=doc.title,
        filename=doc.filename,
        version=doc.version,
        series=doc.series,
        doc_type=doc.doc_type,
        status=doc.status,
        word_count=doc.word_count,
        last_updated=doc.last_updated.isoformat() if doc.last_updated else None,
        snippet=snippet,
        score=score,
        chunk_count=stats[0] if stats else None,
        embedded_chunks=stats[1] if stats else None,
    )


@router.get("", response_model=DocumentList)
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    series: str | None = None,
    doc_type: str | None = None,
    status: str = "active",
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    query = db.query(Document)
    if status != "all":
        query = query.filter(Document.status == status)
    if series:
        query = query.filter(Document.series == series)
    if doc_type:
        query = query.filter(Document.doc_type == doc_type)
    total = query.count()
    docs = query.order_by(Document.doc_number).offset((page - 1) * page_size).limit(page_size).all()
    stats = _chunk_stats(db, [d.id for d in docs])
    return DocumentList(
        documents=[_to_response(d, stats.get(str(d.id))) for d in docs],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/search", response_model=DocumentList)
def search_documents(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    # Hybrid path: semantic + keyword chunk retrieval, grouped per document.
    chunks = retrieve(db, q, top_k=page_size * 2)
    if chunks:
        by_doc: dict[str, RetrievedChunk] = {}
        for chunk in chunks:
            if chunk.doc_number not in by_doc or chunk.score > by_doc[chunk.doc_number].score:
                by_doc[chunk.doc_number] = chunk

        ranked = sorted(by_doc.values(), key=lambda c: c.score, reverse=True)
        total = len(ranked)
        window = ranked[(page - 1) * page_size: (page - 1) * page_size + page_size]

        docs_by_number = {
            d.doc_number: d
            for d in db.query(Document).filter(Document.doc_number.in_([c.doc_number for c in window])).all()
        }
        stats = _chunk_stats(db, [d.id for d in docs_by_number.values()])

        documents = []
        for chunk in window:
            doc = docs_by_number.get(chunk.doc_number)
            if not doc:
                continue
            documents.append(_to_response(
                doc,
                stats.get(str(doc.id)),
                snippet=_make_snippet(chunk.content, q),
                score=round(chunk.score, 4),
            ))
        return DocumentList(documents=documents, total=total, page=page, page_size=page_size)

    # Fallback: plain keyword match over document fields.
    search_term = f"%{q}%"
    query = db.query(Document).filter(
        or_(
            Document.title.ilike(search_term),
            Document.content.ilike(search_term),
            Document.doc_number.ilike(search_term),
            Document.filename.ilike(search_term),
        )
    )
    total = query.count()
    docs = query.order_by(Document.doc_number).offset((page - 1) * page_size).limit(page_size).all()
    stats = _chunk_stats(db, [d.id for d in docs])
    return DocumentList(
        documents=[_to_response(d, stats.get(str(d.id))) for d in docs],
        total=total,
        page=page,
        page_size=page_size,
    )


def _make_snippet(content: str, query: str, length: int = 240) -> str:
    body = content.split("\n\n", 1)[-1]
    lower_body = body.lower()
    for term in query.split():
        idx = lower_body.find(term.lower())
        if idx != -1:
            start = max(0, idx - 60)
            prefix = "…" if start > 0 else ""
            return f"{prefix}{body[start:start + length]}…"
    return body[:length] + ("…" if len(body) > length else "")


@router.get("/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: UUID, user: User = Depends(get_current_user), db: DBSession = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    detail = _to_response(doc, _chunk_stats(db, [doc.id]).get(str(doc.id))).model_dump()
    return DocumentDetail(
        **detail,
        content=doc.content,
        file_hash=doc.file_hash,
    )


@router.get("/{doc_id}/references")
def get_references(doc_id: UUID, user: User = Depends(get_current_user), db: DBSession = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    refs = db.query(DocReference).filter(DocReference.source_doc_id == doc.id).all()
    referenced_by = db.query(DocReference).filter(DocReference.target_doc_number == doc.doc_number).all()
    outgoing = [{"target": r.target_doc_number, "type": r.reference_type} for r in refs]
    incoming_docs = db.query(Document).filter(
        Document.id.in_([r.source_doc_id for r in referenced_by])
    ).all()
    incoming = [{"doc_number": d.doc_number, "title": d.title} for d in incoming_docs]
    return {"outgoing": outgoing, "incoming": incoming}


@router.post("/reingest")
def reingest_documents(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    stats = ingest_all_docs(db)
    return {"message": "Reingestion complete", "stats": stats}
