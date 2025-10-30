# from engines import polly, gcp
from fastmcp import FastMCP
from tts import polly
from llm.openai import transcript
from socials.youtube import upload
import os
import logging
from video import tools

logger = logging.getLogger(__name__)

app = FastMCP("Text to Audio MCP Service")


@app.tool
def generate_transcript(summarized_news: str) -> str:
    """Generate a transcript from summarized news for better Video synthesis."""
    return transcript(summarized_news)


@app.tool
def synthesize(text: str) -> str:
    """Synthesize text to video and save it on the MCP server.
    Return an ID which can be used to publish that video later."""
    # Hard limit of 10k chars for Polly
    # Make separate synthesis tasks for every 2 newlines in a row
    # e.g.
    # bla bla bla bla
    #
    # more bla bla bla

    client = polly.PollyClient().synthesize(text=text)
    return tools.combine_audio_and_video(client)


@app.tool
def publish(
    video_id: str,
    video_title: str,
    video_description: str,
    keywords: str,
    privacy_status: str,
) -> bool:
    """Publish a locally stored video with given ID to YouTube as YouTube Shorts.

    Args:
        video_id: Video ID which to publish.
        video_title: Title of the video.
        video_description: Description of the video.
        keywords: comma-separated string of keywords, e.g. "keyword1,keyword2,keyword3"
    """
    upload(
        f"results/{video_id}.mp4",  # Make sure this is ≤60s and vertical/square format
        video_title,
        video_description,
        keywords,
        privacy_status="unlisted",
    )


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8000))
    logger.info(f"Starting Text to Video MCP Service on {host}:{port}")
    app.settings.host = host
    app.settings.port = port
    app.run(transport="streamable-http")
