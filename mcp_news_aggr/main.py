from __future__ import annotations
import json
import os
import sys
import logging

try:
    from mcp_news_aggr.fetch_google_news import fetch_google_news
    from mcp_news_aggr.summarize_news import summarize_all_articles
except ModuleNotFoundError:
    # fallback for running main.py directly from mcp_news_aggr folder
    from fetch_google_news import fetch_google_news
    from summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSON_FILE = "summarized_news.json"

def main():
    articles = []
    try:
        articles = fetch_google_news(page_size=20)
    except Exception as e:
        if "429" in str(e) or "Too Many Requests" in str(e):
            logger.warning("HTTP 429 received from Google News. Using previously saved JSON if available.")
        else:
            logger.exception("Error fetching Google News")
    
    if not articles:
        if os.path.exists(JSON_FILE):
            logger.info(f"Loading summary from existing {JSON_FILE}")
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                summarized_news = json.load(f)
            print("=== Full Combined Summary (from cache) ===")
            print(summarized_news.get("summary", "No summary available."))
            return
        else:
            logger.error("No articles fetched.")
            return

    # Combine articles into a single string for summarization
    combined_text = ""
    for idx, article in enumerate(articles, start=1):
        combined_text += f"Article {idx}:\n"
        combined_text += f"Title: {article['title']}\n"
        combined_text += f"Summary: {article['summary']}\n"
        combined_text += f"Source: {article['source']}\n\n"

    # Summarize
    full_summary = summarize_all_articles([combined_text])

    # Save JSON
    summarized_news = {"summary": full_summary}
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(summarized_news, f, ensure_ascii=False, indent=2)

    # Print summary
    print("=== Full Combined Summary ===")
    print(full_summary)


if __name__ == "__main__":
    main()


#python3 -m mcp_news_aggr.main