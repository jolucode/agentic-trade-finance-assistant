from openai import OpenAI

from app.core.config import OPENROUTER_API_KEY


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )

    def generate_response(self, message: str) -> str:

        response = self.client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a Trade Finance banking assistant.

                    Your specialization includes:
                    - Letters of Credit
                    - International Trade
                    - Imports and Exports
                    - SWIFT
                    - Banking operations related to Trade Finance

                    Rules:
                    - Explain concepts clearly and professionally.
                    - Do not invent banking policies or customer information.
                    - If you do not know something, say that you do not have enough information.
                    - Keep answers focused on Trade Finance and banking.
                    """
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content