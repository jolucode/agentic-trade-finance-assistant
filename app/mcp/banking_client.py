from mcp import Client

from app.mcp.banking_server import mcp


async def get_lc_status_via_mcp(
    lc_id: str
) -> dict:

    async with Client(mcp) as client:

        result = await client.call_tool(
            "get_lc_status",
            {
                "lc_id": lc_id
            }
        )

        if result.is_error:
            return {
                "found": False,
                "message": "MCP tool execution failed."
            }

        if result.structured_content:
            return result.structured_content

        return {
            "found": False,
            "message": "MCP returned no structured result."
        }