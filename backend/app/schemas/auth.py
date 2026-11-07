from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    # Bounded so an unauthenticated caller cannot force hashing/comparison of
    # arbitrarily large strings. 72 is bcrypt's significant-byte ceiling; the
    # username limit matches User.username (String(50)).
    username: str = Field(max_length=50)
    password: str = Field(max_length=72)


class TokenResponse(BaseModel):
    token: str
    user: "MeResponse"


class MeResponse(BaseModel):
    id: str
    username: str
    role: str

    model_config = {"from_attributes": True}
