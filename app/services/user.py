from app.repositories.user import UserRepository
from app.schema.user import UserDTO


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def get_or_create(
        self, email: str, name: str, provider: str, provider_id: str, avatar_url: str
    ) -> UserDTO:
        user = await self.user_repository.find_by_provider_id(provider_id)
        if user:
            return user

        return await self.create(
            email=email,
            name=name,
            provider=provider,
            provider_id=provider_id,
            avatar_url=avatar_url,
        )

    async def create(
        self,
        email: str,
        name: str,
        provider: str,
        provider_id: str,
        avatar_url: str = None,
    ) -> UserDTO:
        return await self.user_repository.create(
            email=email,
            name=name,
            provider=provider,
            provider_id=provider_id,
            avatar_url=avatar_url,
        )

    async def get_by_email(self, email: str) -> UserDTO:
        return await self.user_repository.find_by_email(email)

    async def get_by_id(self, id: str) -> UserDTO:
        return await self.user_repository.find_by_id(id)
