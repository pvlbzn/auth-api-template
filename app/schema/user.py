from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    name: str
    provider: str
    provider_id: str
    avatar_url: str


class AuthUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    name: str
    provider_id: UUID


class JWTUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    name: str
