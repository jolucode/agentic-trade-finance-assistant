# IA Core Bank - Agentic Trade Finance Assistant

Initial FastAPI project structure for an Agentic AI banking assistant.

## Current endpoints

- `GET /health`
- `GET /api/chat/hello`
- Swagger UI: `/docs`

## Run locally

Activate your virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Then open:

- http://localhost:8000/health
- http://localhost:8000/api/chat/hello
- http://localhost:8000/docs
