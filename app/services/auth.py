import logging
from datetime import timedelta, datetime, UTC
from typing import Optional

import jwt
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel

from app.config import settings


class DecryptedToken(BaseModel):
    sub: str
    email: str
    provider: str
    exp: int

    class Config:
        from_attributes = True


class AuthService:
    def __init__(self, client: OAuth):
        self.log = logging.getLogger(__name__)
        self.oauth = client
        self.initialize_google()

    def initialize_google(self) -> None:
        self.oauth.register(
            name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_SECRET,
            server_metadata_url=settings.GOOGLE_METADATA_URL,
            client_kwargs={"scope": ["openid email profile"]},
        )
        self.log.debug("Google OAuth initialized")

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> bytes:
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MIN)
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> DecryptedToken:
        data = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return DecryptedToken.model_validate(data)
