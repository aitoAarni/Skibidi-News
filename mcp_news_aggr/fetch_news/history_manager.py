import json
import os
from datetime import datetime

# This JSON file will store the URLs of fetched articles by date
DB_FILE = "mcp_news_aggr/fetch_news/fetched_articles_history.json"

def _get_today_str():
    """Returns today's date as 'YYYY-MM-DD'."""
    return datetime.today().strftime("%Y-%m-%d")

def _read_db():
    """Reads the JSON database file."""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle case where file is empty or corrupt
        return {}

def _write_db(data):
    """Writes data to the JSON database file."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_fetched_today():
    """
    Gets a set of (title, source) tuples for all articles fetched today.
    """
    db = _read_db()
    today = _get_today_str()
    # Data is stored as a list of dicts: [{"title": "t1", "source": "s1"}, ...]
    articles_list = db.get(today, [])
    
    # Return a set of tuples for efficient lookup
    return set((article.get('title'), article.get('summary'), article.get('source')) for article in articles_list)

def log_fetched_articles(articles):
    """
    Logs a list of new articles (title and source) to the database for today.
    """
    if not articles:
        return

    db = _read_db()
    today = _get_today_str()
    
    # Get existing articles for today
    today_articles_list = db.get(today, [])
    # Convert to set of tuples for efficient checking
    today_articles_set = set((a.get('title'), a.get('summary'), a.get('source')) for a in today_articles_list)
    
    new_articles_logged = False
    for article in articles:
        article_tuple = (article['title'], article['summary'], article['source'])
        
        # Only add if this (title, source) combo hasn't been logged today
        if article_tuple not in today_articles_set:
            today_articles_list.append({
                "title": article['title'],
                "summary": article['summary'],
                "source": article['source']
            })
            today_articles_set.add(article_tuple) # Keep set in sync
            new_articles_logged = True

    # Write back to the DB only if we added something new
    if new_articles_logged:
        db[today] = today_articles_list
        _write_db(db)

