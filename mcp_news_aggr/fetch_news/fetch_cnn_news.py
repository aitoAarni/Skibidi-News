from GoogleNews import GoogleNews
from datetime import datetime, timedelta

def parse_date(date_str):
    today = datetime.today()
    date_str = date_str.lower()
    
    if "today" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "yesterday" in date_str:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "hours ago" in date_str or "minutes ago" in date_str:
        return today.strftime("%Y-%m-%d")
    else:
        try:
            parsed_date = datetime.strptime(date_str, "%b %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except:
            return today.strftime("%Y-%m-%d")

def fetch_cnn_news(page_size=10):
    googlenews = GoogleNews(lang='en', period='1d')
    #googlenews.set_topic("World News")
    googlenews.search("site:cnn.com")
    #googlenews.search("world news")
    #googlenews.search("breaking")

    """for i in range(1,2):
        googlenews.get_page(i)"""
    
    googlenews.get_page(1)

    results = googlenews.result()

    articles = []
    for item in results[:page_size]:
        title = item.get("title", "No title")
        summary = item.get("desc", "No summary")
        date_raw = item.get("date", "")
        date = parse_date(date_raw)
        url_link = item.get("link", "")
        source = item.get("media", "Google News")

        articles.append({
            "title": title,
            "summary": summary,
            "date": date,
            "url": url_link,
            "source": source
        })

    return articles
