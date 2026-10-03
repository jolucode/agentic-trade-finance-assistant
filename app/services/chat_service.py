from app.agents.graph import agent_graph


class ChatService:

    async def process_message(
        self,
        message: str,
        thread_id: str
    ) -> str:

        result = await agent_graph.ainvoke(
            {
                "message": message
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                },
            "recursion_limit": 10
            }
        )

        return result["answer"]