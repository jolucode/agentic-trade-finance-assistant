from app.agents.graph import agent_graph


class ChatService:

    def process_message(
        self,
        message: str,
        thread_id: str
    ) -> str:

        result = agent_graph.invoke(
            {
                "message": message
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        return result["answer"]