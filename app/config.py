"""Application configuration loaded from environment variables."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized settings for the API and LLM integration."""

    app_name: str = Field(default="AI Chatbot API")
    app_version: str = Field(default="1.0.0")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    debug: bool = Field(default=False)

    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="llama-3.1-8b-instant")
    llm_timeout_seconds: int = Field(default=30)
    system_prompt: str = Field(
        default="You are a helpful AI assistant. Keep responses concise and accurate."
    )

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
