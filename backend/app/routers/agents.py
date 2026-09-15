from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.agent_task import AgentTask
from app.dependencies import get_current_user, require_writer
from app.services.agent_runner import create_task
from app.tasks import run_agent_task, AGENT_FUNCTIONS

router = APIRouter()


class AgentRunRequest(BaseModel):
    agent_type: str
    input_data: dict


class AgentTaskResponse(BaseModel):
    id: str
    agent_type: str
    status: str
    input_data: dict
    output_data: dict | None
    error_message: str | None
    created_at: str
    started_at: str | None
    completed_at: str | None

    model_config = {"from_attributes": True}


@router.get("/agents")
def list_agents(user: User = Depends(require_writer)):
    agents = []
    for name in AGENT_FUNCTIONS:
        agents.append({
            "name": name,
            "display_name": name.replace("_", " ").title(),
            "status": "ready",
        })
    return {"agents": agents}


@router.post("/agents/run", response_model=AgentTaskResponse)
def trigger_agent(
    body: AgentRunRequest,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    if body.agent_type not in AGENT_FUNCTIONS:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {body.agent_type}")

    task = create_task(
        db=db,
        agent_type=body.agent_type,
        input_data=body.input_data,
        created_by=user.id,
    )

    run_agent_task.delay(str(task.id), body.agent_type, body.input_data)

    return AgentTaskResponse(
        id=str(task.id),
        agent_type=task.agent_type,
        status=task.status,
        input_data=task.input_data,
        output_data=task.output_data,
        error_message=task.error_message,
        created_at=task.created_at.isoformat() if task.created_at else "",
        started_at=task.started_at.isoformat() if task.started_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
    )


@router.get("/agents/tasks")
def list_tasks(
    agent_type: str | None = None,
    limit: int = 20,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    query = db.query(AgentTask).order_by(AgentTask.created_at.desc())
    if agent_type:
        query = query.filter(AgentTask.agent_type == agent_type)
    tasks = query.limit(limit).all()

    return {
        "tasks": [
            {
                "id": str(t.id),
                "agent_type": t.agent_type,
                "status": t.status,
                "input_data": t.input_data,
                "output_data": t.output_data,
                "error_message": t.error_message,
                "created_at": t.created_at.isoformat() if t.created_at else "",
                "started_at": t.started_at.isoformat() if t.started_at else None,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
            for t in tasks
        ]
    }


@router.get("/agents/tasks/{task_id}", response_model=AgentTaskResponse)
def get_task(
    task_id: UUID,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return AgentTaskResponse(
        id=str(task.id),
        agent_type=task.agent_type,
        status=task.status,
        input_data=task.input_data,
        output_data=task.output_data,
        error_message=task.error_message,
        created_at=task.created_at.isoformat() if task.created_at else "",
        started_at=task.started_at.isoformat() if task.started_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
    )
