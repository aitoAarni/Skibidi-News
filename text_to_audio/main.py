# from engines import polly, gcp
from fastmcp import FastMCP
from fastmcp.utilities.types import Audio
from engines import polly
from llm.openai import transcript

mcp = FastMCP("Text to Audio MCP Service")


@mcp.tool
def synthesize(text: str) -> Audio:
    """Synthesize text to speech as an MP3 audio file."""
    # Hard limit of 10k chars for Polly
    # Make separate synthesis tasks for every 2 newlines in a row
    # e.g.
    # <speak>
    #   <s>What up?</s>
    # </speak>
    #
    # <speak> ...
    parts = text[:10000].split("\n\n")

    audio_bytes = polly.PollyClient().synthesize(text_bits=parts).get_bytes()
    return Audio(data=audio_bytes, media_type="audio/mpeg")


@mcp.tool
def generate_transcript(summarized_news: str) -> str:
    """Generate a transcript from summarized news for better Audio synthesis."""
    return transcript(summarized_news)


if __name__ == "__main__":
    mcp.run()
