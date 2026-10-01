"""Chat service placeholder.

We will implement the application/service layer in the next step.
"""
from app.llm.llm_client import LLMClient


class ChatService:

    def __init__(self):
        self.llm_client = LLMClient()

    def process_message(self, message: str) -> str:

        return self.llm_client.generate_response(
            message
        )