from __future__ import annotations
import json
import os
import logging

try:
    from mcp_news_aggr.fetch_news.fetch_all_news import fetch_all_news
    from mcp_news_aggr.summarize_news import summarize_all_articles
except ModuleNotFoundError:
    from fetch_news.fetch_all_news import fetch_all_news
    from summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSON_FILE = "mcp_news_aggr/summarized_news.json"

def clear_json_file():
    """Reset the JSON file to an empty object before writing new data."""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def main():
    # Always clear file at start
    clear_json_file()

    articles = []
    try:
        articles = fetch_all_news(page_size=10, lang="en")
    except Exception as e:
        logger.exception("Error fetching news")

    if not articles:
        logger.error("No articles fetched.")
        return

    combined_texts = []
    for idx, article in enumerate(articles, start=1):
        combined_texts.append(
            f"Article {idx}:\n"
            f"Title: {article['title']}\n"
            f"Summary: {article['summary']}\n"
            f"Source: {article['source']}\n"
        )

    # Summarize
    full_summary = summarize_all_articles(combined_texts)

    # Save JSON
    summarized_news = {
        "summary": full_summary
        #"articles": [{"title": a["title"], "source": a["source"], "url": a["url"]} for a in articles]
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(summarized_news, f, ensure_ascii=False, indent=2)

    # Print summary
    print("=== Full Combined Summary ===")
    print(full_summary)


if __name__ == "__main__":
    main()


# Run with:
# python3 -m mcp_news_aggr.main
