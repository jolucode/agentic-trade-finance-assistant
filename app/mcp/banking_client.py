import asyncio

from mcp import Client

from app.mcp.banking_server import mcp


TOOL_TIMEOUT_SECONDS = 3
MAX_RETRIES = 2


async def get_lc_status_via_mcp(
    lc_id: str
) -> dict:

    async with Client(mcp) as client:

        for attempt in range(1, MAX_RETRIES + 1):

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

                if result.is_error:
                    raise RuntimeError(
                        "MCP tool returned an error."
                    )

                if result.structured_content:
                    return result.structured_content

                raise RuntimeError(
                    "MCP returned no structured result."
                )

            except (
                asyncio.TimeoutError,
                RuntimeError
            ) as exc:

                if attempt == MAX_RETRIES:
                    return {
                        "found": False,
                        "error": "tool_unavailable",
                        "message": (
                            f"Tool failed after {MAX_RETRIES} attempts: {exc}"
                        )
                    }

                await asyncio.sleep(0.2)
                