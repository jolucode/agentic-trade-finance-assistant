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
from app.llm.llm_client import LLMClient
from app.rag.retriever import Retriever


class ChatService:

    def __init__(self):
        self.llm_client = LLMClient()
        self.retriever = Retriever()

    def process_message(self, message: str) -> str:

        results = self.retriever.search(
            query=message,
            top_k=3
        )

        context = "\n\n".join(
            result["text"]
            for result in results
        )

        return self.llm_client.generate_response(
            message=message,
            context=context
        )