"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.config import settings
from app.models.schemas import HealthResponse
from app.routes.chat import router as chat_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="ChatGPT-style chatbot API with per-session memory.",
)

app.include_router(chat_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        version=settings.app_version,
    )
