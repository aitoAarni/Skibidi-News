from fetch_news.fetch_guardian import fetch_guardian_news
from fetch_news.fetch_nytimes import fetch_nytimes_news
from summarize_news import summarize_article
import json

def main():
    # Step 1: Fetch articles
    guardian_articles = fetch_guardian_news(page_size=5)
    nytimes_articles = fetch_nytimes_news(page_size=5)
    all_articles = guardian_articles + nytimes_articles

    # Step 2: Prepare combined prompt for AI
    combined_text = ""
    for idx, article in enumerate(all_articles, start=1):
        combined_text += f"Article {idx}:\n"
        combined_text += f"Title: {article['title']}\n"
        combined_text += f"Text: {article['summary']}\n"
        combined_text += f"Source: {article['source']}\n\n"

    # Step 3: Ask AI to summarize all articles in one prompt
    ai_prompt = (
        "Summarize each of the following news articles separately in 2-3 sentences each. "
        "Return the summaries as a numbered list corresponding to the article numbers.\n\n"
        f"{combined_text}"
    )

    ai_response = summarize_article(ai_prompt)

    # Step 4: Split AI response by lines to map summaries to articles
    # Assumes AI returns numbered list like "1. Summary ...", "2. Summary ..."
    lines = [line.strip() for line in ai_response.split("\n") if line.strip()]
    summaries = {}
    for line in lines:
        if line[0].isdigit() and "." in line:
            num, summary = line.split(".", 1)
            summaries[int(num.strip())] = summary.strip()

    # Step 5: Attach summaries back to articles
    summarized_news = []
    for idx, article in enumerate(all_articles, start=1):
        summary_text = summaries.get(idx, "No summary generated.")
        summarized_news.append({
            "title": article['title'],
            "summary": summary_text,
            "date": article['date'],
            "url": article['url'],
            "source": article['source']
        })

    # Step 6: Save JSON
    with open("mcp-news-aggr/summarized_news.json", "w", encoding="utf-8") as f:
        json.dump(summarized_news, f, ensure_ascii=False, indent=2)

    # Step 7: Print results
    for article in summarized_news:
        print(f"{article['source']}: {article['title']}")
        print(article['summary'])
        print("-" * 80)


if __name__ == "__main__":
    main()
