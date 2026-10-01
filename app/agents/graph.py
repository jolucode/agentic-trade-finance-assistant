from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.router import route_message
from app.rag.retriever import Retriever
from app.tools.banking_tools import get_letter_of_credit_status
from app.llm.llm_client import LLMClient

import re


class AgentState(TypedDict, total=False):
    message: str
    route: str
    context: str
    tool_result: dict
    answer: str


retriever = Retriever()
llm_client = LLMClient()


def router_node(state: AgentState):

    route = route_message(
        state["message"]
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

    if not match:
        return {
            "tool_result": {
                "found": False,
                "message": "No LC ID was found."
            }
        }

    lc_id = match.group()

    result = get_letter_of_credit_status(
        lc_id
    )

    return {
        "tool_result": result
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


agent_graph = builder.compile()