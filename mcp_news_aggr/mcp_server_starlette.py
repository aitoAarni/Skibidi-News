from __future__ import annotations
import os
import json
import logging
import contextlib

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

from .fetch_news.fetch_all_news import fetch_all_news
from .summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSON_FILE = os.path.join(os.path.dirname(__file__), "summarized_news.json")

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

def clear_json_file():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

@chat_mcp.tool()
def aggregate_news() -> dict:
    """Fetch, summarize, and store news."""
    articles = fetch_all_news("world")
    if not articles:
        return {"error": "No articles fetched."}

    combined_texts = [
        f"Article {i+1}:\nTitle: {a['title']}\nSummary: {a['summary']}\nSource: {a['source']}\n"
        for i, a in enumerate(articles)
    ]

    summary_text = summarize_all_articles(combined_texts)

    clear_json_file()
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({"summary": summary_text}, f, ensure_ascii=False, indent=2)
    return {"summary": summary_text}


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
