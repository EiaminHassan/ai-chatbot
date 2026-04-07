"""In-memory chat history management with session isolation."""

from threading import Lock

from app.models.schemas import Message


class ChatMemoryService:
    """Stores and retrieves per-session chat history."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[Message]] = {}
        self._lock = Lock()

    def add_user_message(self, session_id: str, content: str) -> None:
        """Append a user message to the target session."""
        self._append_message(session_id=session_id, role="user", content=content)

    def add_assistant_message(self, session_id: str, content: str) -> None:
        """Append an assistant message to the target session."""
        self._append_message(session_id=session_id, role="assistant", content=content)

    def get_history(self, session_id: str) -> list[Message]:
        """Return a copy of ordered messages for a session."""
        with self._lock:
            history = self._sessions.get(session_id, [])
            return [Message(role=item.role, content=item.content) for item in history]

    def clear_history(self, session_id: str) -> bool:
        """Clear all messages for a session if it exists."""
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def _append_message(self, session_id: str, role: str, content: str) -> None:
        """Thread-safe message append helper."""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            self._sessions[session_id].append(Message(role=role, content=content))


memory_service = ChatMemoryService()
