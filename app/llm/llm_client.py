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

    def generate_tool_response(
        self,
        message: str,
        tool_result: dict
    ) -> str:

        response = self.client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a Trade Finance banking assistant.

                    You receive structured data returned by a banking tool.

                    Rules:
                    - Use only the provided tool result.
                    - Do not invent information.
                    - Explain the result clearly and professionally.
                    - If the tool says the operation was not found, say so clearly.
                    - Return plain text only.
                    - Do not use Markdown, bold text, bullet points, or special formatting.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    User question:
                    {message}

                    Tool result:
                    {tool_result}
                    """
                }
            ]
        )

        return response.choices[0].message.content