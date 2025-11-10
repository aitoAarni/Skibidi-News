import json

from src.data_classes import News
from src.services.utils import mcp_http_session


def _normalize_text_payload(raw: str) -> str:
    """Strip whitespace and surrounding quotes from MCP text payloads."""
    normalized = raw.strip()
    if not normalized:
        return normalized

    if (normalized.startswith("\"") and normalized.endswith("\"")) or (
        normalized.startswith("\'") and normalized.endswith("\'")
    ):
        try:
            return json.loads(normalized)
        except json.JSONDecodeError:
            return normalized[1:-1]

    return normalized

@mcp_http_session("http://mcp_humorizer:8000/mcp")
async def call_humorizer(session, text):
    print(f"test humorizer with text: {text}")
    await session.initialize()
    result = await session.call_tool(
        "comedicize", {"id": "test-123", "summarized_text": text}
    )
    print(f"result: {result}")
    text_result = result.content[0].text
    print(f"text_result: { text_result }")
    parsed = json.loads(text_result)

    return parsed["comedic_text"]


@mcp_http_session("http://mcp_prompt_opt:8000/mcp")
async def get_best_prompt(session, prompt: str, summary: str, allow_quick_opt: bool = True):
    """Fetch the highest scoring prompt pack from the prompt optimizer MCP."""
    await session.initialize()
    response = await session.call_tool(
        "best_prompt",
        {
            "prompt": prompt,
            "summary": summary,
            "allow_quick_opt": allow_quick_opt,
        },
    )

    content = response.content[0]
    payload = getattr(content, "text", None)

    if payload is None:
        payload = getattr(content, "data", None)

    if payload is None:
        raise ValueError("Prompt optimizer did not return any content")

    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    if isinstance(payload, str):
        payload = _normalize_text_payload(payload)
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:  # pragma: no cover - surfaced to client
            raise ValueError(f"Failed to parse prompt optimizer response: {payload}") from exc

    return payload


@mcp_http_session("http://mcp_news_aggr:8000/mcp")
async def call_news_aggr(session, category: str | None = None):
    print("test test_news_aggr")
    await session.initialize()
    payload = {"category": category} if category else None
    aggregated_news = await session.call_tool(
        "aggregate_news",
        payload,
    )
    text_result = aggregated_news.content[0].text
    print(text_result)
    parsed = json.loads(text_result)
    return parsed


@mcp_http_session("http://mcp_text_to_video:8000/mcp")
async def generate_trancript(session, humorized_text):
    """Request a narrated transcript from the Text-to-Video MCP service."""
    print(f"humor_text in generate_transcript func {humorized_text}")
    await session.initialize()
    response = await session.call_tool(
        "generate_transcript", {"summarized_news": humorized_text}
    )
    print("\n" * 4)
    print(f"response: {response}")
    content = response.content[0]
    transcript = getattr(content, "text", None)

    if transcript is None:
        data = getattr(content, "data", None)
        if data is None:
            raise ValueError("Transcript tool did not return any content")
        if isinstance(data, bytes):
            transcript = data.decode("utf-8")
        else:
            transcript = str(data)

    transcript = _normalize_text_payload(transcript)
    print("\n" * 4)
    print(f"transcript: {transcript}")
    print(f"type(transcript): {type(transcript)}")
    return transcript

@mcp_http_session("http://mcp_text_to_video:8000/mcp")
async def generate_video(session, transcript: str):
    """Trigger synthesis in Text-to-Video MCP service and return the asset id."""
    print(f"transcript: {transcript}")
    await session.initialize()
    response = await session.call_tool("synthesize", {"text": transcript})
    print(f"response: {response}")

    content = response.content[0]
    raw_video_id = getattr(content, "text", None)
    if raw_video_id is None:
        raw_video_id = getattr(content, "data", None)

    if raw_video_id is None:
        raise ValueError("Video synthesis tool did not return an identifier")

    if isinstance(raw_video_id, bytes):
        raw_video_id = raw_video_id.decode("utf-8")

    video_id = _normalize_text_payload(str(raw_video_id))
    print(f"video_id: {video_id}")
    return video_id

def mock_news(fails: bool = False):
    text = ""
    with open("../synthesized_speech/news.txt") as file:
        for line in file.readlines():
            if line == "\n" or "":
                print("skippedi line: ", line, ord(line), "\n")
            else:
                text += line
    return text


def mock_humorizer(news: News, fails: bool = False):
    if fails:
        raise ConnectionError("Connection failed")
    text = ""
    with open("../synthesized_speech/comedic.txt") as file:
        for line in file.readlines():
            if line == "\n" or "":
                print("skippedi line: ", line, ord(line), "\n")
            else:
                text += line
    return text
