from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    doc_number: str
    title: str
    filename: str
    version: str | None = None
    series: str | None = None
    doc_type: str | None = None
    status: str
    word_count: int | None = None
    last_updated: str | None = None
    snippet: str | None = None
    score: float | None = None
    chunk_count: int | None = None
    embedded_chunks: int | None = None

    model_config = {"from_attributes": True}


class DocumentDetail(DocumentResponse):
    content: str
    file_hash: str | None = None


class DocumentList(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int
