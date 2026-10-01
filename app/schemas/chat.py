"""Chat request/response schemas placeholder.

Pydantic models will be added in the next step.
"""
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str