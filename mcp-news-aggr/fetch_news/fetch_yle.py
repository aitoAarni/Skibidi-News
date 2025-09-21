# fetch_news/fetch_yle.py
import requests
from datetime import datetime

# Example keys (replace with your actual keys)
YLE_APP_ID = "fdsafdsfsfafaadafds1542af86"
YLE_APP_KEY = "gfysagdyusgsa"

def fetch_yle_news(page_size=10):
    return []
    """
    Fetch latest news from Yle API using app_id and app_key.
    Returns a list of articles with title, summary, date, url, and source.
    """
    url = "https://external.api.yle.fi"
    params = {
        "app_id": YLE_APP_ID,
        "app_key": YLE_APP_KEY,
        "limit": page_size,
        "start": 0,
        "published": "true",
        "order": "desc",
        "orderBy": "publicationTime"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Yle API request failed:", response.status_code, response.text)
        return []

    try:
        data = response.json()
    except ValueError:
        print("Yle API returned invalid JSON:", response.text)
        return []

    articles = []

    for item in data.get("data", []):
        title = item.get("title", "No title")
        summary = item.get("lead", "No summary available")
        date = item.get("publicationTime", datetime.now().strftime("%Y-%m-%d"))
        url_link = item.get("link", "")

        articles.append({
            "title": title,
            "summary": summary,
            "date": date,
            "url": url_link,
            "source": "Yle"
        })

    return articles