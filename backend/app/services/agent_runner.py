import traceback
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session as DBSession
from app.models.agent_task import AgentTask
from app.models.document import Document
from app.config import get_settings
from app.services.retrieval import retrieve

settings = get_settings()


def get_doctrine_context(db: DBSession, doc_numbers: list[str] | None = None) -> str:
    """Full-document context for explicitly named docs (agent handoffs)."""
    if doc_numbers:
        docs = db.query(Document).filter(Document.doc_number.in_(doc_numbers)).all()
    else:
        docs = db.query(Document).filter(Document.status == "active").all()

    parts = []
    for doc in docs:
        parts.append(f"--- Doc {doc.doc_number}: {doc.title} ---\n{doc.content}\n")
    return "\n".join(parts)


def build_retrieval_context(
    db: DBSession,
    query: str,
    top_k: int | None = None,
    doc_numbers: list[str] | None = None,
) -> tuple[str, list[dict]]:
    """Build a token-budgeted doctrine context from hybrid retrieval.

    Returns (context_text, sources) where sources carries per-chunk provenance
    so agents can stamp which doctrine material they used.
    """
    chunks = retrieve(db, query, top_k=top_k, doc_numbers=doc_numbers)

    parts = []
    sources = []
    budget = settings.context_budget_chars
    used = 0

    for chunk in chunks:
        source = chunk.as_dict()
        if used + len(chunk.content) > budget:
            remaining = budget - used
            if remaining < 500:
                break
            source["truncated"] = True
            content = chunk.content[:remaining]
        else:
            content = chunk.content

        version_note = f" (v{chunk.version})" if chunk.version else ""
        parts.append(f"--- Doc {chunk.doc_number}{version_note}: {chunk.doc_title}"
                     f" | Section: {chunk.heading_path or '(document body)'} ---\n{content}\n")
        sources.append(source)
        used += len(content)

        if used >= budget:
            break

    return "\n".join(parts), sources


def create_task(
    db: DBSession,
    agent_type: str,
    input_data: dict,
    created_by: UUID,
) -> AgentTask:
    task = AgentTask(
        agent_type=agent_type,
        status="pending",
        input_data=input_data,
        created_by=created_by,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def run_agent(
    db: DBSession,
    task_id: UUID,
    agent_fn,
    input_data: dict,
) -> AgentTask:
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise ValueError(f"Task {task_id} not found")

    task.status = "running"
    task.started_at = datetime.now(timezone.utc)
    db.commit()

    try:
        result = agent_fn(db, input_data)
        task.status = "completed"
        task.output_data = result
        task.completed_at = datetime.now(timezone.utc)
    except Exception as e:
        task.status = "failed"
        task.error_message = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
        task.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    return task
