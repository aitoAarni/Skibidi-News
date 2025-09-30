from __future__ import annotations
import sys
import logging

try:
    from mcp.server.fastmcp import FastMCP
except Exception as e:
    print("ERROR: Missing or incompatible 'mcp' Python package. Install with:")
    print("  pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)

from mcp_news_aggr.fetch_news.fetch_all_news import fetch_all_news
from mcp_news_aggr.summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastMCP("mcp-news-aggr")

@app.tool()
def aggregate_news(page_size: int = 20, lang: str = "en") -> dict:
    try:
        articles = fetch_all_news(page_size=page_size, lang=lang)
        if not articles:
            return {"summary": "No articles found."}

        combined_texts = []
        for idx, article in enumerate(articles, start=1):
            combined_texts.append(
                f"Article {idx}:\nTitle: {article['title']}\n"
                f"Summary: {article['summary']}\nSource: {article['source']}"
            )

        summary = summarize_all_articles(combined_texts)
        return {
            "summary": summary,
            "articles": [{"title": a["title"], "source": a["source"], "url": a["url"]} for a in articles]
        }

    except Exception as e:
        logger.exception("Error in aggregate_news tool")
        return {"summary": f"Error fetching or summarizing news: {e}"}

@app.tool()
def health() -> dict:
    return {
        "name": "mcp-news-aggr",
        "status": "ok",
        "articles_provider": ["Google News", "Yle News"],
    }

def main() -> None:
    app.run()

if __name__ == "__main__":
    main()

# Run with:
# python3 -m mcp_news_aggr.mcp_server
