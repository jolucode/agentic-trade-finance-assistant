import asyncio

from mcp import Client

from app.core.circuit_breaker import CircuitBreaker
from app.mcp.banking_server import mcp


TOOL_TIMEOUT_SECONDS = 3
MAX_RETRIES = 2


banking_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=10
)


async def get_lc_status_via_mcp(
    lc_id: str
) -> dict:

    # 1. CIRCUIT BREAKER CHECK
    if not banking_circuit_breaker.can_execute():
        return {
            "found": False,
            "error": "circuit_open",
            "message": "Banking service is temporarily unavailable."
        }

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

                    # 2. SUCCESS
                    banking_circuit_breaker.record_success()

                    return result.structured_content

                raise RuntimeError(
                    "MCP returned no structured result."
                )

            except (
                asyncio.TimeoutError,
                RuntimeError
            ) as exc:

                # solo registramos fallo cuando ya agotamos retries
                if attempt == MAX_RETRIES:

                    # 3. FAILURE
                    banking_circuit_breaker.record_failure()

                    return {
                        "found": False,
                        "error": "tool_unavailable",
                        "message": (
                            f"Tool failed after "
                            f"{MAX_RETRIES} attempts: {exc}"
                        )
                    }

                await asyncio.sleep(0.2)