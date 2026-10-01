from openai import OpenAI

from app.core.config import OPENROUTER_API_KEY


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )

    def generate_response(
        self,
        message: str,
        context: str
    ) -> str:

        response = self.client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a Trade Finance banking assistant.

                    Answer using the provided context.

                    Rules:
                    - Use the context as the main source of truth.
                    - Do not invent banking policies or customer information.
                    - If the context does not contain enough information,
                      clearly say that there is not enough information.
                    - Keep answers clear and professional.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    Context:
                    {context}

                    Question:
                    {message}
                    """
                }
            ]
        )

        return response.choices[0].message.content