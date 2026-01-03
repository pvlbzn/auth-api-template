from uuid import UUID


from app.schema.base import BaseDTO


class UserDTO(BaseDTO):
    id: UUID
    email: str
    name: str
    provider: str
    provider_id: str
    avatar_url: str


class AuthUserDTO(BaseDTO):
    email: str
    name: str
    provider_id: UUID


class JWTUserDTO(BaseDTO):
    email: str
    name: str
