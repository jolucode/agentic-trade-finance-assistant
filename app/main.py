from fastapi import FastAPI
from app.api.rag import router as rag_router
from app.api.chat import router as chat_router
from app.api.tools import router as tools_router

app = FastAPI(
    title="Agentic Trade Finance Assistant",
    description="Base API for an Agentic AI Trade Finance project.",
    version="0.1.0",
)

app.include_router(chat_router)
app.include_router(rag_router)
app.include_router(tools_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP"
    }
