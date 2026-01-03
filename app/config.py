import logging
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


def get_or_throw(key: str, default: str | None = None, prefix: str = "PROJECT_") -> str:
    value = os.getenv(prefix + key, default)
    if value is None:
        raise RuntimeError(f"environment key `{key}` not found")
    return value


class Settings(BaseModel):
    # Application settings
    APP_ENV: str = get_or_throw("APP_ENV", "development")
    APP_PORT: int = int(get_or_throw("APP_PORT", "8080"))

    # Database settings
    DB_HOST: str = get_or_throw("DB_HOST", "localhost")
    DB_PORT: int = int(get_or_throw("DB_PORT", "5432"))
    DB_USER: str = get_or_throw("DB_USER")
    DB_PASSWORD: str = get_or_throw("DB_PASSWORD")
    DB_NAME: str = get_or_throw("DB_NAME")
    DB_URL: str = get_or_throw("DB_URL")

    # JWT
    JWT_SECRET: str = get_or_throw("JWT_SECRET")
    JWT_ALGORITHM: str = get_or_throw("JWT_ALGORITHM", "HS256")
    JWT_TOKEN_EXPIRE_MIN: int = int(get_or_throw("JWT_TOKEN_EXPIRE_MIN", "30"))

    # Redirect to client post auth
    FRONTEND_URL: str = get_or_throw("FRONTEND_URL")

    # Google OAuth
    GOOGLE_CLIENT_ID: str = get_or_throw("GOOGLE_CLIENT_ID")
    GOOGLE_SECRET: str = get_or_throw("GOOGLE_SECRET")
    GOOGLE_METADATA_URL: str = get_or_throw("GOOGLE_METADATA_URL")

    # Session
    SESSION_SECRET_KEY: str = get_or_throw("SESSION_SECRET_KEY")


def configure_logger(conf: Settings):
    match conf.APP_ENV:
        case "development":
            logging.basicConfig(level=logging.DEBUG)
            logging.getLogger("httpx").setLevel(logging.WARNING)
            logging.getLogger("httpcore").setLevel(logging.WARNING)
            logging.getLogger("hpack").setLevel(logging.WARNING)
        case "production":
            logging.basicConfig(level=logging.WARNING)
        case _:
            logging.basicConfig(level=logging.INFO)


settings = Settings()
configure_logger(conf=settings)
