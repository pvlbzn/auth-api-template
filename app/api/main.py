from fastapi import FastAPI

from app.api.v1 import health

app = FastAPI(debug=True)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
