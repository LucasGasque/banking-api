from pydantic import BaseModel, Field


class BaseAuthSerializer(BaseModel):
    username: str


class AuthSerializer(BaseAuthSerializer):
    password: str


class AuthTokenPayload(BaseModel):
    username: str
    exp: float


class AuthToken(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
