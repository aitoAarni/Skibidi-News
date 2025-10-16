# from engines import polly, gcp
from fastmcp import FastMCP
from fastmcp.utilities.types import Audio
from engines import polly
from llm.openai import transcript
import os
import logging

logger = logging.getLogger(__name__)

app = FastMCP("Text to Audio MCP Service")


@app.tool
def synthesize(text: str) -> Audio:
    """Synthesize text to speech as an MP3 audio file."""
    # Hard limit of 10k chars for Polly
    # Make separate synthesis tasks for every 2 newlines in a row
    # e.g.
    # bla bla bla bla
    #
    # more bla bla bla
    parts = text[:10000].split("\n\n")

    audio_bytes = polly.PollyClient().synthesize(text_bits=parts).get_bytes()
    return Audio(data=audio_bytes)


@app.tool
def generate_transcript(summarized_news: str) -> str:
    """Generate a transcript from summarized news for better Audio synthesis."""
    return transcript(summarized_news)


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8000))
    logger.info(f"Starting Text to Audio MCP Service on {host}:{port}")
    app.settings.host = host
    app.settings.port = port
    app.run(transport="streamable-http")
