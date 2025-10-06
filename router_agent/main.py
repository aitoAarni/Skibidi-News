# In router_agent/main.py
import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from router_agent.utils import mcp_http_session


async def test_humorizer_http(text: str) -> str:
    """Call the dockerized MCP humorizer server"""
    async with streamablehttp_client("http://mcp_humorizer:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Tools: {tools}")

            result = await session.call_tool(
                "comedicize", {"id": "router-request", "summarized_text": text}
            )

            return result.content[0].text if result.content else text


@mcp_http_session("http://mcp_humorizer:8000/mcp")
async def test_humorizer(session, text):
    await session.initialize()
    tools = await session.list_tools()
    result = await session.call_tool(
        "comedicize", {"id": "test-123", "summarized_text": text}
    )
    text_result = result.content[0].text
    print("HUMORIZED TEXT")
    print(text_result)
    parsed = json.loads(text_result)
    print("PARSED TEXT")
    print(parsed)

    return parsed["comedic_text"]


@mcp_http_session("http://mcp_text_to_audio:8000/mcp")
async def test_tts(session, text):
    await session.initialize()
    response = await session.call_tool("generate_transcript", {"summarized_news": text})
    text_result = response.content[0].text
    print(text_result)


@mcp_http_session("http://mcp_news_aggr:8000/mcp")
async def test_news_aggr(session):
    await session.initialize()
    aggregated_news = await session.call_tool("aggregate_news")
    text_result = aggregated_news.content[0].text

    print(text_result)  # this should be a JSON string

    parsed = json.loads(text_result)
    print(parsed)
    return "This news digest encapsulates significant global events, highlighting key players, locations, and the broader context surrounding these developments.\n\nIn the Himalayas, a severe blizzard struck the eastern face of Mount Everest, leaving hundreds of trekkers stranded. Rescuers successfully guided these individuals to safety, as reported by Chinese state media. The extreme weather conditions, including heavy snow and rainfall, contributed to the perilous situation, emphasizing the dangers faced by mountaineers in this region.\n\nIn Southeast Asia, Indonesia has been grappling with ongoing street protests against youth unemployment, which have resulted in the deaths of ten individuals since late August. Although the protests have calmed, the discontent among the youth remains palpable, highlighting a critical socio-economic issue in the country.\n\nThe severe weather has also affected neighboring Nepal and parts of India, where heavy rains have triggered flooding and landslides, claiming over 60 lives. The devastation has impacted wide areas, including urban centers like Kathmandu, underscoring the vulnerability of these regions to climate-related disasters.\n\nIn the Pacific, Australia and Papua New Guinea have reached a landmark defense agreement, pledging mutual support in the event of an attack. This historic deal reflects growing security concerns in the region, particularly in light of geopolitical tensions and the need for stronger defense partnerships.\n\nOn the sports front, the excitement surrounding the 2026 FIFA World Cup continues to build. An organizing board member and a professional freestyler discussed the upcoming event and its preparations, including a closer look at the match ball, signaling the importance of this global sporting event.\n\nIn Europe, Germany resumed its World Cup qualifying campaign, with Borussia Dortmund's Karim Adeyemi aiming to translate his domestic success to the international stage as the national team prepares to face Luxembourg.\n\nMeanwhile, the UK has been in the spotlight due to a reported stalking incident involving Prince Harry during his recent visit. A known stalker reportedly came close to him on two occasions, raising concerns about security for prominent figures.\n\nIn the Middle East, Russia faced condemnation for a large-scale missile and drone attack on civilian infrastructure in Ukraine, resulting in five fatalities. This incident has intensified international scrutiny of Russia's military actions amid ongoing conflict in the region.\n\nIn Asia, Japan's Nikkei 225 index surged to a record high following the election of Takaichi Sanae as the head of the ruling Liberal Democratic Party, reflecting investor optimism regarding economic policies under her leadership.\n\nIn a significant political development, French Prime Minister Sébastien Lecornu resigned just hours after unveiling his new cabinet, a move that has plunged the country into further uncertainty. This resignation adds to the ongoing political turbulence in France.\n\nIn Ecuador, a state of emergency was declared in ten provinces amid protests for and against President Daniel Noboa. The situation reflects deep divisions within the country and the challenges faced by the government in maintaining order.\n\nAs the world grapples with various crises, from natural disasters to political upheavals, these events underscore the interconnectedness of global issues and the need for collaborative solutions. Each incident not only impacts the immediate region but also resonates on a broader scale, affecting international relations and humanitarian efforts."
    # return parsed["summary"]


async def main():
    await asyncio.sleep(5)

    summary = await test_news_aggr()
    humorized_text = await test_humorizer(summary)
    tts = await test_tts(humorized_text)
    
    # await test_humorizer()
    # await test_news_aggr()
    # print("tts")
    # await test_tts()  #not working currently
    # text = "The economy shrank by 2% last quarter."
    # comedic_text = await test_humorizer_http(text)
    # print("works")
    # print(f"Original: {text}")
    # print(f"Comedic: {comedic_text}")


if __name__ == "__main__":
    asyncio.run(main())
