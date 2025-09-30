# In router_agent/main.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_humorizer_docker(text: str) -> str:
    """Call the dockerized MCP humorizer server"""
    docker_cmd = [
        "docker",
        "run",
        "-i",
        "--rm",
        "-e",
        "MODEL_PROVIDER=none",
        "-e",
        "HUMOR_STYLE=light",
        "mcp-humorizer",
    ]

    server_params = StdioServerParameters(
        command=docker_cmd[0], args=docker_cmd[1:], env={}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "comedicize", {"id": "router-request", "summarized_text": text}
            )

            # Extract the comedic text from the result
            return result.content[0].text if result.content else text


async def main():
    text = "The economy shrank by 2% last quarter."
    comedic_text = await call_humorizer_docker(text)
    print(f"Original: {text}")
    print(f"Comedic: {comedic_text}")


if __name__ == "__main__":
    asyncio.run(main())
