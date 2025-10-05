from __future__ import annotations

import os
import sys
import json
import logging

try:
    # FastMCP is the ergonomic Python helper for building MCP servers
    from mcp.server.fastmcp import FastMCP  # type: ignore
except Exception as e:  # pragma: no cover
    print("ERROR: Missing or incompatible 'mcp' Python package. Please install with:")
    print("  pip install mcp")
    print(f"Details: {e}")
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the MCP application
app = FastMCP("mcp-news-aggregator")


@app.tool()
def aggregate_news() -> dict:
    """
    Aggregate and summarize global news articles.

    Reads from summarized_news.json and returns the summary text.

    Output Example:
    {
        "summary": "In recent news, significant developments across various global issues..."
    }
    """
    json_path = os.path.join(os.path.dirname(__file__), "mcp_news_aggr/summarized_news.json")

    if not os.path.exists(json_path):
        logger.error(f"File not found: {json_path}")
        return {"error": "summarized_news.json not found"}

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        summary = data.get("summary", "").strip()
        return {"summary": summary}
    except Exception as e:
        logger.exception("Failed to read summarized_news.json")
        return {"error": str(e)}


@app.tool()
def health() -> dict:
    """
    Simple health check tool to verify server connectivity.
    """
    return {
        "name": "mcp-news-aggregator",
        "status": "ok"
    }


def main() -> None:
    # Runs an MCP server over HTTP
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8000))
    logger.info(f"Starting MCP News Aggregator on {host}:{port}")
    app.settings.host = host
    app.settings.port = port
    app.run(transport="streamable-http")


if __name__ == "__main__":
    main()
