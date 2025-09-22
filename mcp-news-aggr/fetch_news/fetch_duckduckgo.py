from duckduckgo_search import DDGS
from datetime import datetime

def fetch_duckduckgo(page_size):
    """
    Fetch latest news from DuckDuckGo.
    Returns a list of articles with title, summary, date, url, and source.
    """
    articles = []
    today = datetime.today().strftime("%Y-%m-%d")

    with DDGS() as ddgs:
        results = ddgs.news("breaking news today", region="wt-wt", safesearch="Off", max_results=page_size)

        for item in results:
            title = item.get("title", "No title")
            summary = item.get("body", "No summary")
            date = item.get("date", today)  # DuckDuckGo already gives ISO-like dates
            url_link = item.get("url", "")
            source = item.get("source", "DuckDuckGo")

            articles.append({
                "title": title,
                "summary": summary,
                "date": date[:10],  # Ensure YYYY-MM-DD format
                "url": url_link,
                "source": source
            })

    return articles
