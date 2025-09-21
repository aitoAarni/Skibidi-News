# fetch_news/fetch_google_news.py
from GoogleNews import GoogleNews
from datetime import datetime, timedelta

def parse_date(date_str):
    """
    Convert GoogleNews date strings to YYYY-MM-DD format.
    Handles 'Today', 'Yesterday', and 'X hours ago'.
    """
    today = datetime.today()
    date_str = date_str.lower()
    
    if "today" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "yesterday" in date_str:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "hours ago" in date_str or "minutes ago" in date_str:
        return today.strftime("%Y-%m-%d")
    else:
        # Try parsing exact date formats
        try:
            # Some results may be like "Sep 21, 2025"
            parsed_date = datetime.strptime(date_str, "%b %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except:
            return today.strftime("%Y-%m-%d")

def fetch_google_news(page_size):
    """
    Fetch latest news from Google News using GoogleNews Python package.
    Returns a list of articles with title, summary, date, url, and source.
    """
    googlenews = GoogleNews(lang='en', region='US')
    googlenews.search("breaking news today") 

    results = googlenews.result()  # list of articles
    articles = []

    for item in results[:page_size]:
        title = item.get("title", "No title")
        summary = item.get("desc", "No summary")
        date_raw = item.get("date", "")
        date = parse_date(date_raw)
        url_link = item.get("link", "")
        source = "Google News", item.get("media", "Google News")

        articles.append({
            "title": title,
            "summary": summary,
            "date": date,
            "url": url_link,
            "source": source
        })

    return articles
