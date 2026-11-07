from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    # Matches User.username (String(50)). The password ceiling is bcrypt's
    # significant-byte limit; bcrypt 4.x silently truncates beyond it, so an
    # unbounded value would store a credential shorter than the admin typed.
    # The route also enforces the byte length, since 72 characters of non-ASCII
    # text can exceed 72 bytes.
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)
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
    deleted_at: str | None = None

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
