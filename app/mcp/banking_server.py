from mcp.server import MCPServer

from app.tools.banking_tools import get_letter_of_credit_status


mcp = MCPServer(
    "Trade Finance Banking MCP Server"
)


@mcp.tool()
def get_lc_status(lc_id: str) -> dict:
    """
    Get the current status and details of a letter of credit.

    Args:
        lc_id: Letter of credit identifier, for example LC-10025.
    """

    return get_letter_of_credit_status(
        lc_id
    )