"""LLM integration service for generating assistant responses."""

from fastapi import HTTPException
import httpx

from app.config import settings
from app.models.schemas import Message


class AIService:
    """Handles communication with the Groq API."""

    async def generate_reply(self, history: list[Message]) -> str:
        """Generate an assistant response using full conversation history."""
        if not settings.groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY is not configured. Add it to your .env file.",
            )

        endpoint = "https://api.groq.com/openai/v1/chat/completions"

        payload = {
            "model": settings.groq_model,
            "messages": (
                [{"role": "system", "content": settings.system_prompt}]
                + [
                    {"role": message.role, "content": message.content}
                    for message in history
                ]
            ),
        }
        headers = {
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=504,
                detail="The LLM provider timed out while generating a response.",
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"LLM provider returned an error: {exc.response.text}",
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to call LLM provider: {str(exc)}",
            ) from exc

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise HTTPException(
                status_code=502,
                detail="LLM provider returned no choices.",
            )

        reply = choices[0].get("message", {}).get("content", "").strip()

        if not reply:
            raise HTTPException(
                status_code=502,
                detail="LLM provider returned an empty response.",
            )
        return reply


ai_service = AIService()
