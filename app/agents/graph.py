from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.router import route_message
from app.rag.retriever import Retriever
from app.tools.banking_tools import get_letter_of_credit_status
from app.llm.llm_client import LLMClient
from langgraph.checkpoint.memory import InMemorySaver

import re




class AgentState(TypedDict, total=False):
    message: str
    route: str
    context: str
    tool_result: dict
    answer: str



memory = InMemorySaver()
retriever = Retriever()
llm_client = LLMClient()


def router_node(state: AgentState):

    route = route_message(
        message=state["message"],
        last_lc_id=state.get("last_lc_id")
    )

    return {
        "route": route
    }


def rag_node(state: AgentState):

    results = retriever.search(
        query=state["message"],
        top_k=3
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    return {
        "context": context
    }


def tool_node(state: AgentState):

    match = re.search(
        r"\bLC-\d+\b",
        state["message"].upper()
    )

    if match:
        lc_id = match.group()

    else:
        lc_id = state.get("last_lc_id")

    if not lc_id:
        return {
            "tool_result": {
                "found": False,
                "message": "No LC ID was found."
            }
        }

    result = get_letter_of_credit_status(
        lc_id
    )

    return {
        "tool_result": result,
        "last_lc_id": lc_id
    }


def rag_answer_node(state: AgentState):

    answer = llm_client.generate_response(
        message=state["message"],
        context=state["context"]
    )

    return {
        "answer": answer
    }


def tool_answer_node(state: AgentState):

    answer = llm_client.generate_tool_response(
        message=state["message"],
        tool_result=state["tool_result"]
    )

    return {
        "answer": answer
    }


def route_decision(state: AgentState):

    return state["route"]


builder = StateGraph(AgentState)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "rag",
    rag_node
)

builder.add_node(
    "tool",
    tool_node
)

builder.add_node(
    "rag_answer",
    rag_answer_node
)

builder.add_node(
    "tool_answer",
    tool_answer_node
)


builder.add_edge(
    START,
    "router"
)


builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "rag": "rag",
        "tool": "tool"
    }
)


builder.add_edge(
    "rag",
    "rag_answer"
)

builder.add_edge(
    "tool",
    "tool_answer"
)


builder.add_edge(
    "rag_answer",
    END
)

builder.add_edge(
    "tool_answer",
    END
)


agent_graph = builder.compile(
    checkpointer=memory
)