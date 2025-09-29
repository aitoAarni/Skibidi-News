from fetch_google_news import fetch_google_news
from summarize_news import summarize_all_articles
import json

def main():
    # Fetch articles
    google_articles = fetch_google_news(page_size=20)

    # Combine all article texts into a single string for summarization
    combined_text = ""
    for idx, article in enumerate(google_articles, start=1):
        combined_text += f"Article {idx}:\n"
        combined_text += f"Title: {article['title']}\n"
        combined_text += f"Summary: {article['summary']}\n"
        combined_text += f"Source: {article['source']}\n\n"

    # Generate one long, full-text summary for all articles
    full_summary = summarize_all_articles([combined_text])

    # Prepare JSON with the combined summary
    summarized_news = {
        "summary": full_summary
    }

    # Save JSON
    with open("mcp-news-aggr/summarized_news.json", "w", encoding="utf-8") as f:
        json.dump(summarized_news, f, ensure_ascii=False, indent=2)

    # Print the full summary
    print("=== Full Combined Summary ===")
    print(full_summary)


if __name__ == "__main__":
    main()
