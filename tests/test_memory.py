"""Basic unit tests for session memory behavior."""

from app.services.memory import ChatMemoryService


def test_memory_isolated_per_session() -> None:
    service = ChatMemoryService()
    service.add_user_message("session-a", "Hello from A")
    service.add_user_message("session-b", "Hello from B")

    history_a = service.get_history("session-a")
    history_b = service.get_history("session-b")

    assert len(history_a) == 1
    assert len(history_b) == 1
    assert history_a[0].content == "Hello from A"
    assert history_b[0].content == "Hello from B"


def test_clear_history() -> None:
    service = ChatMemoryService()
    service.add_user_message("session-a", "hello")
    assert service.clear_history("session-a") is True
    assert service.get_history("session-a") == []
    assert service.clear_history("missing") is False
