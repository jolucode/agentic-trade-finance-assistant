import re

from app.llm.llm_client import LLMClient
from app.rag.retriever import Retriever
from app.agents.router import route_message
from app.tools.banking_tools import get_letter_of_credit_status


class ChatService:

    def __init__(self):
        self.llm_client = LLMClient()
        self.retriever = Retriever()

    def process_message(
        self,
        message: str
    ) -> str:

        route = route_message(
            message
        )

        if route == "tool":
            return self._process_tool(
                message
            )

        return self._process_rag(
            message
        )

    def _process_rag(
        self,
        message: str
    ) -> str:

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

    def _process_tool(
        self,
        message: str
    ) -> str:

        match = re.search(
            r"\bLC-\d+\b",
            message.upper()
        )

        if not match:
            return "I could not identify the letter of credit ID."

        lc_id = match.group()

        result = get_letter_of_credit_status(
            lc_id
        )

        return self.llm_client.generate_tool_response(
            message=message,
            tool_result=result
        )