import requests
from datetime import datetime
from config import NYTIMES_API_KEY

def fetch_nytimes_news(section="home", page_size=10):
    """
    Fetch latest NY Times articles using Top Stories API.
    """
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json"
    params = {"api-key": NYTIMES_API_KEY}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    today = datetime.now().date().isoformat()
    articles = []
    for item in data.get("results", []):
        published_date = item.get("published_date", "")[:10]
        if published_date == today:
            articles.append({
                "title": item.get("title"),
                "summary": item.get("abstract"),
                "date": item.get("published_date"),
                "url": item.get("url"),
                "source": "NY Times"
            })
        if len(articles) >= page_size:
            break
    
    return articles
