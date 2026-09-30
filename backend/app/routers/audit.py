from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.dependencies import require_admin
from app.models.audit import AuditLog
from app.models.user import User

router = APIRouter()


class AuditEntry(BaseModel):
    id: str
    username: str
    action: str
    route: str | None
    detail: str | None
    status_code: int | None
    created_at: str


class AuditList(BaseModel):
    entries: list[AuditEntry]
    total: int


@router.get("/audit")
def list_audit(
    limit: int = Query(50, ge=1, le=200),
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db),
):
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return AuditList(
        entries=[
            AuditEntry(
                id=str(a.id),
                username=a.username,
                action=a.action,
                route=a.route,
                detail=a.detail,
                status_code=a.status_code,
                created_at=a.created_at.isoformat() if a.created_at else "",
            )
            for a in rows
        ],
        total=len(rows),
    )
