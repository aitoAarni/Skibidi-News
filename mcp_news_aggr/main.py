"""
    run main to get news + summary without running the router
"""

import os
import json
import logging

from mcp_news_aggr.fetch_news.fetch_all_news import fetch_all_news
from mcp_news_aggr.summarize_news import summarize_all_articles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSON_FILE = "mcp_news_aggr/summarized_news.json"

def clear_json_file():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def main():

    #'world', 'europe','US', 'finland','financial','tech','sport', 'asia'

    articles = fetch_all_news('asia')
    if not articles:
        logger.error("No articles fetched.")
        return

    combined_texts = [
        f"Article {i+1}:\nTitle: {a['title']}\nSummary: {a['summary']}\nSource: {a['source']}\n"
        for i, a in enumerate(articles)
    ]

    full_summary = summarize_all_articles(combined_texts)

    clear_json_file()
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({"summary": full_summary}, f, ensure_ascii=False, indent=2)

    print("=== Full Combined Summary ===")
    print(full_summary)

if __name__ == "__main__":
    main()
