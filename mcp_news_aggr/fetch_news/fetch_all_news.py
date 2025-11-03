import random
from mcp_news_aggr.fetch_news.category_fetcher import fetch_category_news
from mcp_news_aggr.fetch_news.history_manager import get_fetched_today, log_fetched_articles
#from mcp_news_aggr.fetch_news.history_manager import _hash_url

# Define the categories and their corresponding Google News search parameters
CATEGORIES = ['world', 'europe', 'US', 'finland', 'financial', 'tech', 'sport']

CATEGORY_MAPPINGS = {
    'world': {"topic": "WORLD"},
    'europe': {"topic": "Europe"},
    'US': {"topic": "US"},
    'finland': {"query": "site:yle.fi/news"}, # Specific to YLE's English news
    'financial': {"topic": "BUSINESS"},
    'tech': {"topic": "TECHNOLOGY"},
    'sport': {"topic": "SPORTS"},
    'asia' : {"topic": "Asia"},
}

def fetch_all_news(category):
    """
    Fetches 3 new news articles from a single randomly chosen category.
    
    This function ensures that no article is fetched more than once per day.
    """
    # 1. Choose a random category
    chosen_category = category
    search_params = CATEGORY_MAPPINGS[chosen_category]
    
    
    search_params = CATEGORY_MAPPINGS['finland']
    print(f"Fetching news for category: {chosen_category}")

    # 2. Get articles already fetched today
    fetched_urls_today = get_fetched_today()

    # 3. Fetch a pool of possible articles (more than 3, to filter)
    # We fetch 20 to have a good chance of finding 3 new ones.
    #all_possible_articles = fetch_category_news(search_params)
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
