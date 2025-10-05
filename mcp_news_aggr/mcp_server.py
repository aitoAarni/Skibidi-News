# mcp_news_aggr/mcp_server.py

import os
import json
import logging
from mcp.server.fastmcp import FastMCP
#from fastmcp.utilities.types import Text

from .fetch_news.fetch_all_news import fetch_all_news
from .summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSON_FILE = os.path.join(os.path.dirname(__file__), "summarized_news.json")

app = FastMCP("MCP News Aggregator Service")

def clear_json_file():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

@app.tool()
def aggregate_news() -> dict:
    """Fetch, summarize, and store news."""
    articles = fetch_all_news(page_size=10, lang="en")
    if not articles:
        return {"error": "No articles fetched."}

    combined_texts = [
        f"Article {i+1}:\nTitle: {a['title']}\nSummary: {a['summary']}\nSource: {a['source']}\n"
        for i, a in enumerate(articles)
    ]

    summary_text = summarize_all_articles(combined_texts)

    clear_json_file()
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({"summary": summary_text}, f, ensure_ascii=False, indent=2)

    return {"summary": summary_text}

@app.tool()
def get_summary() -> dict:
    """
    Returns the latest summarized news from JSON_FILE.
    """
    if not os.path.exists(JSON_FILE):
        return {"summary": "No summarized news available."}

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"summary": data.get("summary", "")}
    except Exception as e:
        logger.exception("Failed to read summarized news JSON")
        return {"summary": f"Error reading news: {e}"}

@app.tool()
def health() -> dict:
    return {"name": "mcp-news-aggregator", "status": "ok"}

def main():
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8000))
    logger.info(f"Starting MCP News Aggregator on {host}:{port}")
    app.settings.host = host
    app.settings.port = port
    app.run(transport="streamable-http")

if __name__ == "__main__":
    main()
