import base64
from router_agent.utils import mcp_http_session
from datetime import datetime


@mcp_http_session("http://mcp_humorizer:8000/mcp")
async def call_humorizer(session, text):
    print("test humorizer")

    print("Starting summary")
    await session.initialize()
    result = await session.call_tool(
        "comedicize", {"id": "test-123", "summarized_text": text}
    )

    text_result = result.content[0].text
    print(text_result)
    parsed = json.loads(text_result)
    return parsed["comedic_text"]


@mcp_http_session("http://mcp_text_to_audio:8000/mcp")
async def call_tts(session, text):
    print("test tts")
    await session.initialize()
    transcript_response = await session.call_tool(
        "generate_transcript", {"summarized_news": text}
    )
    transcript_text = transcript_response.content[0].text
    print(transcript_text)
    audio_response = await session.call_tool("synthesize", {"text": transcript_text})

    audio_data = audio_response.content[0].data
    return audio_data


@mcp_http_session("http://mcp_news_aggr:8000/mcp")
async def call_news_aggr(session):
    print("test test_news_aggr")
    await session.initialize()
    aggregated_news = await session.call_tool("aggregate_news")
    text_result = aggregated_news.content[0].text
    print(text_result)
    parsed = json.loads(text_result)
    return parsed["summary"]


def save_audio(audio_data):
    audio_bytes = base64.b64decode(audio_data)
    date_and_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
    print(date_and_time, date_and_time)
    try:
        with open(f"./synthesized_speech/audio_from_{date_and_time}.wav", "wb") as file:
            file.write(audio_bytes)
    except:
        with open(f"./synthesized_speech/new_audio3.wav", "wb") as file:
            file.write(audio_bytes)


def mock_news(fails: bool = False):
    text = ""
    with open("./synthesized_speech/news.txt") as file:
        for line in file.readlines():
            if line == "\n" or "":
                print("skippedi line: ", line, ord(line), "\n")
            else:
                text += line
    return line