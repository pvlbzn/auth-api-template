import logging

import jwt
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.api.dependencies import get_auth_service, get_user_service
from app.api.middleware.auth import get_auth
from app.config import settings
from app.schema.user import UserDTO
from app.services.auth import AuthService
from app.services.user import UserService

router = APIRouter()
log = logging.getLogger(__name__)
supported_providers = [
    "google",
]


@router.get("/login/{provider}")
async def login(
    provider: str, req: Request, auth: AuthService = Depends(get_auth_service)
):
    if provider not in supported_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider {provider}, supported providers are {supported_providers}",
        )

    redirect_url = req.url_for("auth_callback", provider=provider)
    print("REDIRECT URL:", redirect_url)

    return await auth.oauth.create_client(provider).authorize_redirect(
        req, redirect_url
    )


@router.get("/callback/{provider}")
async def auth_callback(
    provider: str,
    req: Request,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
):
    try:
        if provider not in supported_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported provider {provider}, supported providers are {supported_providers}",
            )

        token = await auth_service.oauth.create_client(provider).authorize_access_token(
            req
        )

        if provider == "google":
            data = jwt.decode(
                token.get("id_token"), options={"verify_signature": False}
            )
            email = data.get("email")
            name = data.get("name", "")
            provider_id = data.get("sub")
            avatar_url = data.get("picture")

        user = await user_service.get_or_create(
            email=email,
            name=name,
            provider=provider,
            provider_id=provider_id,
            avatar_url=avatar_url,
        )

        access_token = auth_service.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "provider": provider,
            }
        )

        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={access_token}"

        return RedirectResponse(url=redirect_url)

    except Exception as e:
        log.error(f"/callback/{provider} failed with {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"couldn't authorize with {provider} provider",
        )


@router.get("/user")
def get_current_user(
    user=Depends(get_auth),
) -> UserDTO:
    return user
