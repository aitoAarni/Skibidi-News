from fastapi import FastAPI
from src.services.mcp_server_services import (
    call_humorizer,
    call_news_aggr,
)

from src.data_classes import News

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

    huomrized_text = await call_humorizer(news.news)

    return {"huomrized_news": huomrized_text}
