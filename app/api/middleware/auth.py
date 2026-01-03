import logging

import jwt
from fastapi import HTTPException
from fastapi.params import Header, Depends
from starlette import status

from app.api.dependencies import get_user_service
from app.config import settings
from app.schema.user import UserDTO, JWTUserDTO
from app.services.user import UserService

log = logging.getLogger(__name__)


async def get_auth(
    authorization: str = Header(None),
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
        )

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        jwt_data = JWTUserDTO.model_validate(payload)
        user = await user_service.get_by_email(email=jwt_data.email)

        return user

    except jwt.ExpiredSignatureError:
        # Expected
        log.debug("token expired")
        raise HTTPException(status_code=401, detail="token expired")

    except jwt.InvalidTokenError as e:
        # Could be suspicious
        log.warning(f"invalid token attempt: {e}")
        raise HTTPException(status_code=401, detail="invalid token")

    except Exception as e:
        # This is an error
        log.error(f"authentication error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="authentication failed")
