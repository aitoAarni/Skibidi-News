#!/usr/bin/env python3
"""
Standalone test client for MCP streamable-http server.
Usage: python test_mcp_client.py [URL]
Example: python test_mcp_client.py http://localhost:8000/mcp
"""

import asyncio
import sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_mcp_server(url: str):
    """Test the MCP server by calling its tools"""
    print(f"🔌 Connecting to MCP server at: {url}")

    try:
        async with streamablehttp_client(url) as (read_stream, write_stream, _):
            print("✅ Connection established!")

            async with ClientSession(read_stream, write_stream) as session:
                print("🤝 Initializing session...")
                await session.initialize()
                print("✅ Session initialized!")

                # List available tools
                print("\n📋 Listing available tools...")
                tools = await session.list_tools()
                print(f"✅ Found {len(tools.tools)} tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Test the health tool
                print("\n🏥 Testing 'health' tool...")
                health_result = await session.call_tool("health", {})
                print(f"✅ Health check result:")
                print(
                    f"  {health_result.content[0].text if health_result.content else 'No content'}"
                )

                # Test the comedicize tool
                print("\n😄 Testing 'comedicize' tool...")
                test_text = "The economy shrank by 2% last quarter."
                comedic_result = await session.call_tool(
                    "comedicize", {"id": "test-123", "summarized_text": test_text}
                )
                print(f"✅ Comedicize result:")
                if comedic_result.content:
                    print(f"  Original: {test_text}")
                    print(f"  Comedic: {comedic_result.content[0].text}")
                else:
                    print("  No content returned")

                print("\n🎉 All tests passed!")

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    # Get URL from command line or use default
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/mcp"

    print("=" * 60)
    print("MCP Streamable HTTP Test Client")
    print("=" * 60)

    asyncio.run(test_mcp_server(url))


if __name__ == "__main__":
    main()
