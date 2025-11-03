from src.data_classes import News
from src.services.utils import mcp_http_session
import json

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

@mcp_http_session("http://mcp_news_aggr:8000/mcp")
async def call_news_aggr(session):
    print("test test_news_aggr")
    await session.initialize()
    aggregated_news = await session.call_tool("aggregate_news")
    text_result = aggregated_news.content[0].text
    print(text_result)
    parsed = json.loads(text_result)
    return parsed["summary"]


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