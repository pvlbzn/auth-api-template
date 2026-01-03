import logging

import jwt
from fastapi import HTTPException
from fastapi.params import Header, Depends
from starlette import status
from starlette.requests import Request

from app.api.dependencies import get_user_service, get_auth_service
from app.schema.user import UserDTO
from app.services.auth import AuthService
from app.services.user import UserService

log = logging.getLogger(__name__)


async def get_auth(
    request: Request,
    authorization: str = Header(None),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
        )

    token = authorization.replace("Bearer ", "")

    try:
        decrypted_token = auth_service.verify_token(token)
        user = await user_service.get_by_email(email=decrypted_token.email)

        return user

    except jwt.ExpiredSignatureError:
        # Expected
        log.debug("token expired")
        raise HTTPException(status_code=401, detail="token expired")

    except jwt.InvalidTokenError as e:
        # Could be suspicious
        log.warning(f"invalid token attempt IP {request.client.host}: {e}")
        raise HTTPException(status_code=401, detail="invalid token")

    except Exception as e:
        # This is an error
        log.error(f"authentication error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="authentication failed")
