from app.agents.graph import agent_graph


class ChatService:

    def process_message(
        self,
        message: str
    ) -> str:

        result = agent_graph.invoke({
            "message": message
        })

        return result["answer"]