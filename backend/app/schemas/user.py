from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str
    role: str = "writer"


class UpdateUser(BaseModel):
    role: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    role: str
    is_active: bool
    created_at: str
    last_login: str | None = None

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
