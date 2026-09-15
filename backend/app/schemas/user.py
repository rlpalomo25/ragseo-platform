from pydantic import BaseModel
from typing import Optional


class CreateUser(BaseModel):
    username: str
    password: str
    role: str = "writer"


class UpdateUser(BaseModel):
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    username: str
    role: str
    is_active: bool
    created_at: str
    last_login: Optional[str] = None

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
