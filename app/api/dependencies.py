import logging

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.infra.db.conn import get_db
from app.repositories.user import UserRepository
from app.schema.user import UserDTO
from app.services.auth import AuthService
from app.services.user import UserService

security = HTTPBearer()
log = logging.getLogger(__name__)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


def get_auth_service() -> AuthService:
    return AuthService(client=OAuth())


async def get_user(
    credentials=Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    token = credentials.credentials
    payload = auth_service.verify_token(token)

    invalid_auth_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )

    if payload is None:
        raise invalid_auth_credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise invalid_auth_credentials_exception

    user = await user_service.get_by_id(user_id)
    if user is None:
        log.error(f"user {user_id} not found while token is valid")
        raise user_not_found_exception

    return user
