from mcp_news_aggr.fetch_news.category_fetcher import google_fetch_category_news, feedparser_fetch_category_news
from mcp_news_aggr.fetch_news.history_manager import (
    get_fetched_today,
    log_fetched_articles,
)
import urllib.error
import time


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

_category_cache: dict[str, tuple[float, list[dict]]] = {}
CACHE_TTL = 120
BACKOFF_ON_429 = 5
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
    # ---------- CACHING / RATE-LIMIT PROTECTION ----------
    now = time.time()
    if chosen_category in _category_cache:
        ts, cached = _category_cache[chosen_category]
        if now - ts < CACHE_TTL:
            print("Using cached results (TTL not expired).")
            all_possible_articles = cached
        else:
            all_possible_articles = None
    else:
        all_possible_articles = None
    # ------------------------------------------------------

    if all_possible_articles is None:
        # ---- PRIMARY PROVIDER: GoogleNews scraper ----
        try:
            print("Trying Google News provider...")
            all_possible_articles = google_fetch_category_news(chosen_category)

            # If Google returns nonsense or 0 results → treat as failure
            if not all_possible_articles:
                raise ValueError("Google provider returned empty list.")

            # Cache result
            _category_cache[chosen_category] = (time.time(), all_possible_articles)

        except Exception as e:
            print(f"Google provider failed: {e}")

            try:
                print("Trying RSS fallback provider...")
                all_possible_articles = feedparser_fetch_category_news(chosen_category)

                if not all_possible_articles:
                    raise ValueError("RSS provider returned empty list.")

                _category_cache[chosen_category] = (time.time(), all_possible_articles)

            except Exception as e2:
                print(f"RSS fallback failed: {e2}")

                if chosen_category in _category_cache:
                    print("Using cached result as last resort.")
                    all_possible_articles = _category_cache[chosen_category][1]
                else:
                    print("No cache available — returning empty list.")
                    time.sleep(BACKOFF_ON_429)
                    return []

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
