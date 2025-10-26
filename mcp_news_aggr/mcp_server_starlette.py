from __future__ import annotations

import contextlib

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP


# Create an API server and a Chat server
api_mcp = FastMCP("API Server", stateless_http=True)  # stateless is fine for demo
chat_mcp = FastMCP("Chat Server", stateless_http=True)

# Mount at the root of each path (i.e., /api and /chat instead of /api/mcp and /chat/mcp)
api_mcp.settings.streamable_http_path = "/"
chat_mcp.settings.streamable_http_path = "/"


@api_mcp.tool()
def api_status() -> str:
    """Get API status."""
    return "API is running"


@chat_mcp.tool()
def send_message(message: str) -> str:
    """Send a chat message."""
    return f"Message sent: {message}"


# Optional: manage both session managers if running stateful servers
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        # For stateless demos we don't need to run session managers.
        # For stateful servers use:
        await stack.enter_async_context(api_mcp.session_manager.run())
        await stack.enter_async_context(chat_mcp.session_manager.run())
        yield


# Create the Starlette app and mount the MCP servers
app = Starlette(
    routes=[
        Mount("/api", app=api_mcp.streamable_http_app()),
        Mount("/chat", app=chat_mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# Configure CORS; expose "Mcp-Session-Id" for browser-based clients
app = CORSMiddleware(
    app,
    allow_origins=["*"],  # Configure appropriately for production
    allow_methods=["GET", "POST", "DELETE"],  # Supported methods for MCP streamable HTTP
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)

# Run with:
#   uvicorn examples.starlette-mount.app:app --reload
#
# Endpoints:
#   http://localhost:8000/api        (Streamable HTTP MCP root at /api)
#   http://localhost:8000/chat       (Streamable HTTP MCP root at /chat)
