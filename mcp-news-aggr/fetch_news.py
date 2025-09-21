import requests
from config import GUARDIAN_API_KEY
from datetime import datetime

def fetch_guardian_news(section="world", page_size=10):
    today = datetime.now().strftime("%Y-%m-%d")
    url = "https://content.guardianapis.com/search"
    params = {
        "api-key": GUARDIAN_API_KEY,
        "section": section,
        "page-size": page_size,
        "orderBy": "relevance", #newest, oldest, relevance only
        "show-fields": "headline,trailText,webPublicationDate,shortUrl",
        "from-date": today,
        "to-date": today
    }
    response = requests.get(url, params=params)
    data = response.json()
    articles = []
    for item in data.get("response", {}).get("results", []):
        articles.append({
            "title": item["fields"]["headline"],
            "summary": item["fields"]["trailText"],
            "date": item["webPublicationDate"],
            "url": item["fields"]["shortUrl"],
            "source": "The Guardian"
        })
    return articles

"""
guardian documentation: https://open-platform.theguardian.com/documentation/search
"""