# AI Chatbot API (FastAPI + Groq)

ChatGPT-style conversational API with per-session memory, built for the AI Developer assessment task.

## Features

- Multi-turn conversation with session-based context memory
- Session isolation (`session_id` scoped history)
- Groq LLM integration via API
- FastAPI REST endpoints with request/response schemas
- Docker and Docker Compose setup
- Basic unit tests for memory service

## Project Structure

```text
app/
  main.py
  config.py
  models/
    schemas.py
  routes/
    chat.py
  services/
    ai.py
    memory.py
Dockerfile
docker-compose.yml
.env.example
README.md
tests/
  test_memory.py
```

## API Endpoints

- `POST /chat`  
  Send user message and get AI reply.
- `GET /history/{session_id}`  
  Get full message history for one session.
- `DELETE /history/{session_id}`  
  Clear conversation memory for one session.
- `GET /health`  
  Health check.

Swagger docs available at: `http://localhost:8000/docs`

## Local Run (without Docker)

1. Create and activate virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env template and update values:
   ```bash
   cp .env.example .env
   ```
   On Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```
4. Add your `GROQ_API_KEY` in `.env`
5. Start API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Run with Docker Compose

1. Create `.env` from `.env.example` and set `GROQ_API_KEY`
2. Run:
   ```bash
   docker compose up --build
   ```
3. API available at `http://localhost:8000`

## Quick API Examples

### 1) Chat request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"demo-1\",\"message\":\"Hello\"}"
```

### 2) Retrieve history

```bash
curl "http://localhost:8000/history/demo-1"
```

### 3) Clear history

```bash
curl -X DELETE "http://localhost:8000/history/demo-1"
```

## Architecture Notes

- `routes/chat.py`: thin API handlers that orchestrate services
- `services/memory.py`: in-memory ordered message storage with lock for thread safety
- `services/ai.py`: Groq API integration and provider error handling
- `models/schemas.py`: all request/response contracts with Pydantic
- `config.py`: environment-based configuration loading

On every `POST /chat`, the app:
1. stores the user message in session memory
2. sends full session history to Groq
3. stores assistant reply back into same session

This guarantees coherent multi-turn responses with strict session isolation.

## Testing

Run:

```bash
pytest -q
```

## Mandatory Video Demo

Add your video link below before submission:

- Video link: `PASTE_YOUR_UNLISTED_VIDEO_LINK_HERE`

The video should show:
- `docker compose up --build`
- API requests to `/chat`, `/history/{session_id}`, and delete history
- Memory persistence across multiple turns in one session
