from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    user: "MeResponse"


class MeResponse(BaseModel):
    id: str
    username: str
    role: str

    model_config = {"from_attributes": True}
