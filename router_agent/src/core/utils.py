from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

url = "http://mcp_humorizer:8000/mcp"


def mcp_http_session(url: str):
    """Decorater to connect to a MCP server via http"""

    def real_decorator(fn):

        async def wrapper(*args):

            async with streamablehttp_client(url) as (
                read_stream,
                write_stream,
                _,
            ):
                async with ClientSession(read_stream, write_stream) as session:
                    return await fn(session, *args)

        return wrapper
    
    return real_decorator
