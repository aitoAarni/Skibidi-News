# from engines import polly, gcp
from fastmcp import FastMCP
from fastmcp.utilities.types import Audio
from engines import polly

mcp = FastMCP("Text to Audio MCP Service")


@mcp.tool
def synthesize(text: str) -> Audio:
    """Synthesize text to speech as an MP3 audio file."""
    audio_bytes = polly.PollyClient().synthesize(text).get_bytes()
    return Audio(data=audio_bytes, media_type="audio/mpeg")


if __name__ == "__main__":
    mcp.run()
