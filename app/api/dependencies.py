import logging

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.conn import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.user import UserService

log = logging.getLogger(__name__)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


def get_auth_service() -> AuthService:
    return AuthService(client=OAuth())
