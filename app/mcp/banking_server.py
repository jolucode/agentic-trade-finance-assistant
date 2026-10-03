from pydantic import BaseModel

from mcp.server import MCPServer

from app.tools.banking_tools import get_letter_of_credit_status


class LetterOfCreditResult(BaseModel):
    found: bool
    lc_id: str | None = None
    status: str | None = None
    amount: float | None = None
    currency: str | None = None
    beneficiary: str | None = None
    message: str | None = None


mcp = MCPServer(
    "Trade Finance Banking MCP Server"
)


@mcp.tool()
def get_lc_status(
    lc_id: str
) -> LetterOfCreditResult:

    

    result = get_letter_of_credit_status(
        lc_id
    )

    return LetterOfCreditResult(
        **result
    )