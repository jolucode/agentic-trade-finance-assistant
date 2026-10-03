from typing import TypedDict

from langgraph.graph import StateGraph, START, END
import logging
import time
from app.agents.router import route_message
from app.rag.retriever import Retriever
from app.mcp.banking_client import get_lc_status_via_mcp
from app.llm.llm_client import LLMClient
from langgraph.checkpoint.memory import InMemorySaver

import re


logger = logging.getLogger(__name__)

class AgentState(TypedDict, total=False):
    message: str
    route: str
    context: str
    tool_result: dict
    answer: str
    last_lc_id: str



memory = InMemorySaver()
retriever = Retriever()
llm_client = LLMClient()


def router_node(state: AgentState):

    route = route_message(
        message=state["message"],
        last_lc_id=state.get("last_lc_id")
    )

    logger.info(
        "Router selected route=%s message=%s",
        route,
        state["message"]
    )

    return {
        "route": route
    }


def rag_node(state: AgentState):

    start = time.perf_counter()

    results = retriever.search(
        query=state["message"],
        top_k=3
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    elapsed = time.perf_counter() - start

    logger.info(
        "RAG completed chunks=%s latency=%.3fs",
        len(results),
        elapsed
    )

    return {
        "context": context
    }

async def tool_node(state: AgentState):

    start = time.perf_counter()

    match = re.search(
        r"\bLC-\d+\b",
        state["message"].upper()
    )

    if match:
        lc_id = match.group()
    else:
        lc_id = state.get("last_lc_id")

    if not lc_id:

        logger.warning(
            "Tool requested but no LC ID available"
        )

        return {
            "tool_result": {
                "found": False,
                "message": "No LC ID was found."
            }
        }

    result = await get_lc_status_via_mcp(
        lc_id
    )

    elapsed = time.perf_counter() - start

    logger.info(
        "Tool executed tool=get_letter_of_credit_status "
        "lc_id=%s found=%s latency=%.3fs",
        lc_id,
        result.get("found"),
        elapsed
    )

    return {
        "tool_result": result,
        "last_lc_id": lc_id
    }


def rag_answer_node(state: AgentState):

    start = time.perf_counter()

    answer = llm_client.generate_response(
        message=state["message"],
        context=state["context"]
    )

    elapsed = time.perf_counter() - start

    logger.info(
        "LLM RAG response generated latency=%.3fs",
        elapsed
    )

    return {
        "answer": answer
    }


def tool_answer_node(state: AgentState):

    start = time.perf_counter()
    
    tool_result = state["tool_result"]

    if tool_result.get("error"):
        return {
            "answer": tool_result["message"]
        }

    answer = llm_client.generate_tool_response(
        message=state["message"],
        tool_result=state["tool_result"]
    )

    elapsed = time.perf_counter() - start

    logger.info(
        "LLM tool response generated latency=%.3fs",
        elapsed
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