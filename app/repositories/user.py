from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schema.user import UserDTO


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        email: str,
        name: str,
        provider: str,
        provider_id: str,
        avatar_url: str = None,
    ) -> UserDTO:
        u = User(
            email=email,
            name=name,
            provider=provider,
            provider_id=provider_id,
            avatar_url=avatar_url,
        )

        self.db.add(u)
        await self.db.commit()
        await self.db.refresh(u)

        return UserDTO.model_validate(u)

    async def find_by_email(self, email: str) -> Optional[UserDTO]:
        result = await self.db.execute(select(User).where(User.email == email))
        u = result.scalar_one_or_none()
        return UserDTO.model_validate(u) if u else None

    async def find_by_provider_id(self, provider_id: str) -> Optional[UserDTO]:
        result = await self.db.execute(
            select(User).where(User.provider_id == provider_id)
        )
        u = result.scalar_one_or_none()
        return UserDTO.model_validate(u) if u else None

    async def find_by_id(self, id: str) -> Optional[UserDTO]:
        result = await self.db.execute(select(User).where(User.id == id))
        u = result.scalar_one_or_none()
        return UserDTO.model_validate(u) if u else None
