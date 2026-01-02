import logging
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    DB_HOST: str = os.getenv("PROJECT_DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("PROJECT_DB_PORT", "5432"))
    DB_USER: str = os.getenv("PROJECT_DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("PROJECT_DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("PROJECT_DB_NAME", "postgres")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    APP_ENV: str = os.getenv("PROJECT_APP_ENV", "development")
    APP_PORT: int = os.getenv("PROJECT_APP_PORT", "8080")


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
