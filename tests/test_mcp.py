import anyio

from mcp import Client
from mcp.types import TextContent

from app.mcp.banking_server import mcp


async def main():

    async with Client(mcp) as client:

        result = await client.list_tools()

        print("AVAILABLE TOOLS:")

        for tool in result.tools:
            print(f"- {tool.name}")

        tool_result = await client.call_tool(
            "get_lc_status",
            {
                "lc_id": "LC-10025"
            }
        )

        print("\nIS ERROR:")
        print(tool_result.is_error)

        print("\nCONTENT:")

        for block in tool_result.content:
            if isinstance(block, TextContent):
                print(block.text)

        print("\nSTRUCTURED CONTENT:")
        print(tool_result.structured_content)


if __name__ == "__main__":
    anyio.run(main)