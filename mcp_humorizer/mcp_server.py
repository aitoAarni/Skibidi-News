from __future__ import annotations

import os
import sys
import logging

try:
    # FastMCP is the ergonomic Python helper for building MCP servers
    from mcp.server.fastmcp import FastMCP  # type: ignore
except Exception as e:  # pragma: no cover
    print("ERROR: Missing or incompatible 'mcp' Python package. Please install with:")
    print("  pip install -r mcp_humorizer/requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)

from .config import Settings
from .engine import comedicize_text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastMCP("mcp-humorizer")


@app.tool()
def comedicize(id: str, summarized_text: str) -> dict:
    """
    Transform summarized news text into comedic text.

    API Contract:
    Input:
    {
      "id": "uuid",
      "summarized_text": "The economy shrank by 2% last quarter."
    }

    Output:
    {
      "id": "uuid",
      "comedic_text": "The economy shrank by 2%. Don’t worry, my diet is shrinking faster!"
    }
    """
    settings = Settings.from_env()
    result = comedicize_text(summarized_text, settings)
    return {"id": id, "comedic_text": result}


@app.tool()
def health() -> dict:
    """
    Simple health check tool to verify server connectivity.
    """
    settings = Settings.from_env()
    return {
        "name": "mcp-humorizer",
        "provider": settings.model_provider,
        "humor_style": settings.humor_style,
        "status": "ok",
    }


def main() -> None:
    # Runs an MCP server over http
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8000))
    logger.info(f"Starting MCP Humorizer on {host}:{port}")
    app.settings.host = host
    app.settings.port = port
    app.run(transport="streamable-http")


if __name__ == "__main__":
    main()
