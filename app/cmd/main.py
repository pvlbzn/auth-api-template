import uvicorn

from app.config import Settings


def run():
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=Settings.APP_PORT,
        reload=True,
    )
