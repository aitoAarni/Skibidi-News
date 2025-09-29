import sys
import logging
from mcp.server.fastmcp import FastMCP

from .config import Settings
from .engine import comedicize_text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = FastMCP("mcp-humorizer")


@app.tool()
def optimize(id: str, summarized_text: str) -> dict:
    """
    Transform any prompt into a prompt optimized for comedy.
    API Contract:
    Input:
    {
        "id": "uuid",
        "prompt": "The economy shrank by 2% last quarter."
    }
    Output:
    {
        "id": "uuid",
        "optimized_prompt": "The economy shrank by 2%. Don’t worry, my diet is shrinking faster!"
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
    app.run()


if __name__ == "__main__":
    main()
