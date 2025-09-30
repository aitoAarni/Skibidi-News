from mcp_news_aggr.fetch_news.fetch_google_news import fetch_google_news
from mcp_news_aggr.fetch_news.fetch_yle_news import fetch_yle_news

def fetch_all_news(page_size=10, lang="en"):
    """
    Fetch news from both Google News and Yle, combine them into one list.
    """
    google_articles = fetch_google_news(page_size=page_size)
    yle_articles = fetch_yle_news(page_size=page_size)

    all_articles = google_articles + yle_articles

    # Sort by date (newest first if possible)
    try:
        all_articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    except Exception:
        pass

    return all_articles