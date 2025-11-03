import json
import os
from datetime import datetime

# JSON file that stores fetched articles by date
DB_FILE = "mcp_news_aggr/fetch_news/fetched_articles_history.json"


def _get_today_str():
    """Returns today's date as 'YYYY-MM-DD'."""
    return datetime.today().strftime("%Y-%m-%d")


def _read_db():
    """Reads the JSON database file, or returns an empty dict if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def _write_db(data):
    """Writes data safely to the JSON database file."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_fetched_today():
    """
    Returns a set of (title, summary, source) tuples for all articles fetched today.
    """
    db = _read_db()
    today = _get_today_str()
    articles_list = db.get(today, [])
    return set(
        (a.get("title", ""), a.get("summary", ""), a.get("source", ""))
        for a in articles_list
    )


def log_fetched_articles(articles):
    """
    Logs new articles (title, summary, source) to the database for today.
    Avoids logging duplicates.
    """
    if not articles:
        return

    db = _read_db()
    today = _get_today_str()

    # Ensure today's entry exists
    if today not in db:
        db[today] = []

    # Create a set for fast lookup
    existing = set(
        (a.get("title", ""), a.get("summary", ""), a.get("source", ""))
        for a in db[today]
    )

    new_articles_logged = False
    for article in articles:
        key = (article.get("title", ""), article.get("summary", ""), article.get("source", ""))
        if key not in existing:
            db[today].append({
                "title": article.get("title", ""),
                "summary": article.get("summary", ""),
                "source": article.get("source", ""),
                "url": article.get("url", ""),
                "date": article.get("date", today)
            })
            existing.add(key)
            new_articles_logged = True

    if new_articles_logged:
        _write_db(db)
