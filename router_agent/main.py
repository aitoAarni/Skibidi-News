# In router_agent/main.py
import asyncio
import json
import base64
from mcp.client.streamable_http import streamablehttp_client
from router_agent.utils import mcp_http_session
from datetime import datetime


@mcp_http_session("http://mcp_humorizer:8000/mcp")
async def test_humorizer(session, text):

    print("Starting summary")
    await session.initialize()
    result = await session.call_tool(
        "comedicize", {"id": "test-123", "summarized_text": text}
    )

    text_result = result.content[0].text
    parsed = json.loads(text_result)
    return parsed["comedic_text"]


@mcp_http_session("http://mcp_text_to_audio:8000/mcp")
async def test_tts(session, text):
    print("starting tts")
    await session.initialize()
    transcript_response = await session.call_tool(
        "generate_transcript", {"summarized_news": text}
    )
    transcript_text = transcript_response.content[0].text
    with open("./synthesized_speech/transcript_mock.txt", "w") as file:
        file.write(transcript_text)

    audio_response = await session.call_tool("synthesize", {"text": transcript_text})
    try:
        print("dir(audio_response.content[0]): ", dir(audio_response.content[0]))
        print("len(audio_response.content)", len(audio_response.content))
        print("audio_response.content", audio_response.content)
    except:
        print("dir command failed")
        print("audio_response.conent[0]", audio_response.content[0])
        print("len(audio_response.content)", len(audio_response.content))
        print("audio_response.content", audio_response.content)
    try:

        audio_data = audio_response.content[0].data
        print("audio_response.content[0].type", audio_response.content[0].type)
        print(
            "audio_response.content[0].schema_json",
            audio_response.content[0].schema_json,
        )
        print("audio_data = audio_response.content[0].data")
        print("worked")
        return audio_data
    except:

        audio_data = audio_response.content[0].text
        print(audio_response.content[0].type)
        print(audio_response.content[0].schema_json)
        print("seconds way worked")
        print("audio written as text to file")
        return audio_data


@mcp_http_session("http://mcp_news_aggr:8000/mcp")
async def test_news_aggr(session):
    print("starting news aggregation")
    # return "This news digest encapsulates significant global events, highlighting key players, locations, and the broader context surrounding these developments.\n\nIn the Himalayas, a severe blizzard struck the eastern face of Mount Everest, leaving hundreds of trekkers stranded. Rescuers successfully guided these individuals to safety, as reported by Chinese state media. The extreme weather conditions, including heavy snow and rainfall, contributed to the perilous situation, emphasizing the dangers faced by mountaineers in this region.\n\nIn Southeast Asia, Indonesia has been grappling with ongoing street protests against youth unemployment, which have resulted in the deaths of ten individuals since late August. Although the protests have calmed, the discontent among the youth remains palpable, highlighting a critical socio-economic issue in the country.\n\nThe severe weather has also affected neighboring Nepal and parts of India, where heavy rains have triggered flooding and landslides, claiming over 60 lives. The devastation has impacted wide areas, including urban centers like Kathmandu, underscoring the vulnerability of these regions to climate-related disasters.\n\nIn the Pacific, Australia and Papua New Guinea have reached a landmark defense agreement, pledging mutual support in the event of an attack. This historic deal reflects growing security concerns in the region, particularly in light of geopolitical tensions and the need for stronger defense partnerships.\n\nOn the sports front, the excitement surrounding the 2026 FIFA World Cup continues to build. An organizing board member and a professional freestyler discussed the upcoming event and its preparations, including a closer look at the match ball, signaling the importance of this global sporting event.\n\nIn Europe, Germany resumed its World Cup qualifying campaign, with Borussia Dortmund's Karim Adeyemi aiming to translate his domestic success to the international stage as the national team prepares to face Luxembourg.\n\nMeanwhile, the UK has been in the spotlight due to a reported stalking incident involving Prince Harry during his recent visit. A known stalker reportedly came close to him on two occasions, raising concerns about security for prominent figures.\n\nIn the Middle East, Russia faced condemnation for a large-scale missile and drone attack on civilian infrastructure in Ukraine, resulting in five fatalities. This incident has intensified international scrutiny of Russia's military actions amid ongoing conflict in the region.\n\nIn Asia, Japan's Nikkei 225 index surged to a record high following the election of Takaichi Sanae as the head of the ruling Liberal Democratic Party, reflecting investor optimism regarding economic policies under her leadership.\n\nIn a significant political development, French Prime Minister Sébastien Lecornu resigned just hours after unveiling his new cabinet, a move that has plunged the country into further uncertainty. This resignation adds to the ongoing political turbulence in France.\n\nIn Ecuador, a state of emergency was declared in ten provinces amid protests for and against President Daniel Noboa. The situation reflects deep divisions within the country and the challenges faced by the government in maintaining order.\n\nAs the world grapples with various crises, from natural disasters to political upheavals, these events underscore the interconnectedness of global issues and the need for collaborative solutions. Each incident not only impacts the immediate region but also resonates on a broader scale, affecting international relations and humanitarian efforts."

    await session.initialize()
    aggregated_news = await session.call_tool("aggregate_news")
    text_result = aggregated_news.content[0].text
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
        with open(f"./synthesized_speech/new_audio2.wav", "wb") as file:
            file.write(audio_bytes)


async def main():
    await asyncio.sleep(10)
    # summary = await test_news_aggr()
    # humorized_text = await test_humorizer(summary)
    # print(humorized_text)
    humorized_text = "In a week marked by significant global events, a diverse array of stories emerged, shedding light on advancements in science, ongoing geopolitical tensions, and local incidents of violence and discrimination. The scientific community celebrated as John Clarke, Michel Devoret, and John Martinis were awarded the 2025 Nobel Prize for Physics for their groundbreaking research on quantum tunneling in superconducting circuits. Their work is expected to have profound implications for the future of quantum computing, highlighting the importance of innovation in this rapidly evolving field. In the realm of international politics, former U.S. President Donald Trump provided updates on ongoing peace negotiations aimed at resolving the conflict in Gaza, two years after the Hamas attacks on October 7, 2023. His remarks come amid criticism directed at Israeli Prime Minister Benjamin Netanyahu over perceived missteps regarding hostages, illustrating the complexities and sensitivities surrounding the peace talks. The situation in Ukraine remains tense, with Trump indicating that he has made a tentative decision regarding the supply of Tomahawk missiles to Kyiv. This statement follows a warning from Russian President Vladimir Putin, who cautioned that such military support could severely damage U.S.-Russia relations, highlighting the precarious balance of international diplomacy in the region. In England, a mosque was set ablaze in what authorities suspect to be a hate crime. Video footage captured masked individuals attempting to force entry before igniting the structure, raising concerns about rising instances of religiously motivated violence and discrimination in the UK. Amid these troubling events, a survey indicated that salaries in India are projected to rise by 9% in 2026, slightly up from the 8.9% growth observed in 2025. This increase comes in the context of global economic uncertainties, reflecting a potential resilience in the Indian job market. On a lighter note, Canadian Prime Minister Mark Carney was seen joking with Trump during a recent meeting at the White House, where discussions included bilateral relations and ongoing challenges such as the war in Ukraine. This interaction underscores the ongoing diplomatic dialogues between the U.S. and Canada. In sports, Indonesia is set to face Saudi Arabia in the final AFC qualifiers for the 2026 FIFA World Cup, co-hosted by Qatar. This match is part of a broader effort to strengthen regional football ties and enhance the profile of the sport in Asia. In a significant policy development, the Vatican has committed to prioritizing climate education, a move welcomed by environmental organizations and youth movements worldwide. This commitment reflects a growing recognition of the church's role in addressing climate change and promoting sustainability. Meanwhile, in the U.S., the Children's Hospital of Orange County (CHOC) received national recognition from U.S. News & World Report, reinforcing its reputation as a leading pediatric healthcare provider. Lastly, the formation of Tropical Storm Jerry over the central Atlantic Ocean has raised concerns as it is expected to strengthen into a hurricane, prompting monitoring and preparedness efforts in affected regions. Overall, this week’s news highlights the interplay of science, politics, and social issues, emphasizing the need for continued dialogue and action across various sectors to address both immediate challenges and long-term goals. On the bright side, my diet is shrinking faster. Perfect for a 15‑second attention span recap. Like, follow, and pretend you learned economics."
    audio_data = await test_tts(humorized_text)
    save_audio(audio_data)


if __name__ == "__main__":
    asyncio.run(main())
