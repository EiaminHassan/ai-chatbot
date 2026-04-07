"""Chat and memory API routes."""

from fastapi import APIRouter

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    DeleteHistoryResponse,
    HistoryResponse,
)
from app.services.ai import ai_service
from app.services.memory import memory_service

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Receive a user message and return an AI response."""
    memory_service.add_user_message(session_id=request.session_id, content=request.message)
    history = memory_service.get_history(session_id=request.session_id)
    reply = await ai_service.generate_reply(history=history)
    memory_service.add_assistant_message(session_id=request.session_id, content=reply)
    return ChatResponse(session_id=request.session_id, reply=reply)


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str) -> HistoryResponse:
    """Get full ordered conversation history for a session."""
    history = memory_service.get_history(session_id=session_id)
    return HistoryResponse(session_id=session_id, messages=history)


@router.delete("/history/{session_id}", response_model=DeleteHistoryResponse)
async def clear_history(session_id: str) -> DeleteHistoryResponse:
    """Delete all stored messages for a session."""
    deleted = memory_service.clear_history(session_id=session_id)
    return DeleteHistoryResponse(
        session_id=session_id,
        deleted=deleted,
        message="History cleared." if deleted else "Session not found; nothing to clear.",
    )
