from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: UUID
    email: str
    name: str
    provider: str
    provider_id: str
    avatar_url: str

    class Config:
        from_attributes = True


class AuthUserDTO(BaseModel):
    email: str
    name: str
    provider_id: UUID

    class Config:
        from_attributes = True


class JWTUserDTO(BaseModel):
    email: str
    name: str

    class Config:
        from_attributes = True
