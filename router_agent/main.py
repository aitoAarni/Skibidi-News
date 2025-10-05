# In router_agent/main.py
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from router_agent.utils import mcp_http_session


async def test_humorizer_http(text: str) -> str:
    """Call the dockerized MCP humorizer server"""
    async with streamablehttp_client("http://mcp_humorizer:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Tools: {tools}")

            result = await session.call_tool(
                "comedicize", {"id": "router-request", "summarized_text": text}
            )

            return result.content[0].text if result.content else text


@mcp_http_session("http://0.0.0.0:8000/mcp")
async def test_refactor(session):
    await session.initialize()
    tools = await session.list_tools()
    print(f"tools: {tools}")


async def main():
    # await asyncio.sleep(5)
    await test_refactor()
    # text = "The economy shrank by 2% last quarter."
    # comedic_text = await test_humorizer_http(text)
    # print("works")
    # print(f"Original: {text}")
    # print(f"Comedic: {comedic_text}")


if __name__ == "__main__":
    asyncio.run(main())
