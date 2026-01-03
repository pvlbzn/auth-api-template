import uvicorn

from app.config import settings


def run():
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    run()
