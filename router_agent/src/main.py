from fastapi import FastAPI
from src.services.mcp_server_services import (
    call_humorizer,
    call_news_aggr,
    generate_trancript,
    generate_video
)

from src.data_classes import News, HumorText, Transcript

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/news")
async def news_route():
    news = await call_news_aggr()
    print(news)

    return {"news": news}


@app.post("/humorize_news")
async def humorizer_route(news: News):
    print(f"news.news: {news.news}")
    huomrized_text = await call_humorizer(news.news)

    return {"huomrized_news": huomrized_text}


@app.post("/transcript")
async def transcript_route(huomr_text: HumorText):
    print(f"humor_text: {huomr_text}")
    transcript = await generate_trancript(huomr_text.humor_text)

    return {"transcript": transcript}

@app.post("/synthesize")
async def synthesize_route(transcript: Transcript):
    video_id = await generate_video(transcript.transcript)
    return {"video_id": video_id}