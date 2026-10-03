import asyncio

from mcp import Client

from app.mcp.banking_server import mcp


TOOL_TIMEOUT_SECONDS = 3


async def get_lc_status_via_mcp(
    lc_id: str
) -> dict:

    async with Client(mcp) as client:

        try:
            result = await asyncio.wait_for(
                client.call_tool(
                    "get_lc_status",
                    {
                        "lc_id": lc_id
                    }
                ),
                timeout=TOOL_TIMEOUT_SECONDS
            )

        except asyncio.TimeoutError:
            return {
                "found": False,
                "error": "timeout",
                "message": "The banking tool took too long to respond."
            }

        if result.is_error:
            return {
                "found": False,
                "error": "tool_error",
                "message": "MCP tool execution failed."
            }

        if result.structured_content:
            return result.structured_content

        return {
            "found": False,
            "error": "empty_result",
            "message": "MCP returned no structured result."
        }