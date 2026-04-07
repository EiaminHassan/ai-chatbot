"""Pydantic schemas for request/response payloads."""

from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Single chat message in a conversation."""

    role: Literal["user", "assistant"] = Field(..., description="Message role")
    content: str = Field(..., min_length=1, description="Message content")


class ChatRequest(BaseModel):
    """Input schema for sending a chat message."""

    session_id: str = Field(..., min_length=1, description="Unique conversation session")
    message: str = Field(..., min_length=1, description="User message")


class ChatResponse(BaseModel):
    """Response schema containing AI reply."""

    session_id: str
    reply: str


class HistoryResponse(BaseModel):
    """Response schema for conversation history."""

    session_id: str
    messages: list[Message]


class DeleteHistoryResponse(BaseModel):
    """Response schema for history reset endpoint."""

    session_id: str
    deleted: bool
    message: str


class HealthResponse(BaseModel):
    """Simple health check response."""

    status: str
    app: str
    version: str
