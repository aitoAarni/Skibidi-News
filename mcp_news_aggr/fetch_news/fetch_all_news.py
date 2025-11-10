from mcp_news_aggr.fetch_news.category_fetcher import fetch_category_news
from mcp_news_aggr.fetch_news.history_manager import (
    get_fetched_today,
    log_fetched_articles,
)

AVAILABLE_CATEGORIES = (
    "world",
    "europe",
    "US",
    "finland",
    "financial",
    "tech",
    "sport",
    "asia",
)

CANONICAL_BY_KEY = {key.lower(): key for key in AVAILABLE_CATEGORIES}


def fetch_all_news(category: str | None):
    """
    Fetches 3 new news articles from a single randomly chosen category.
    
    This function ensures that no article is fetched more than once per day.
    """
    requested = (category or "world").lower()
    chosen_category = CANONICAL_BY_KEY.get(requested, "world")
    print(f"Fetching news for category: {chosen_category}")

    # 2. Get articles already fetched today
    fetched_urls_today = get_fetched_today()

    # 3. Fetch a pool of possible articles (more than 3, to filter)
    # We fetch 20 to have a good chance of finding 3 new ones.
    all_possible_articles = fetch_category_news(chosen_category)

    # 4. Filter out any articles we've already fetched today
    new_articles = []
    for article in all_possible_articles:
        key = (article.get("title", ""), article.get("summary", ""), article.get("source", ""))
        if key not in fetched_urls_today:
            new_articles.append(article)
            if len(new_articles) >= 3:
                break
        
        # 5. Stop once we have 3 new articles
        if len(new_articles) >= 3:
            break
            
    # 6. Log the newly fetched articles to our history
    if new_articles:
        log_fetched_articles(new_articles)
        print(f"Found and logged {len(new_articles)} new articles.")
    else:
        print("No new articles found for this category today.")

    # 7. Return only the 3 (or fewer) new articles
    return new_articles
