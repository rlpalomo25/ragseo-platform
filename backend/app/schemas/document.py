from pydantic import BaseModel
from typing import Optional


class DocumentResponse(BaseModel):
    id: str
    doc_number: str
    title: str
    filename: str
    version: Optional[str] = None
    series: Optional[str] = None
    doc_type: Optional[str] = None
    status: str
    word_count: Optional[int] = None
    last_updated: Optional[str] = None
    snippet: Optional[str] = None
    score: Optional[float] = None
    chunk_count: Optional[int] = None
    embedded_chunks: Optional[int] = None

    model_config = {"from_attributes": True}


class DocumentDetail(DocumentResponse):
    content: str
    file_hash: Optional[str] = None


class DocumentList(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int
