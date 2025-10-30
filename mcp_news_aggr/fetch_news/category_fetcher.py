from GoogleNews import GoogleNews
from mcp_news_aggr.fetch_news.fetch_utilities import parse_date

def fetch_category_news(category, lang="en"):
    """
    Fetches news from Google News based on a topic or a search query.
    
    :param search_params: A dict, e.g., {"topic": "WORLD"} or {"query": "US news"}
    :param page_size: How many results to fetch from Google (we fetch more to filter)
    :param lang: Language
    :return: A list of article dictionaries
    """
    googlenews = GoogleNews(lang=lang, period='1d') # Look at news from the last day

    """if "topic" in search_params:
        googlenews.set_topic(search_params["topic"])
    elif "query" in search_params:
        googlenews.search(search_params["query"])
    else:
        # Default to world news if no params are given
        googlenews.set_topic("WORLD")"""
    
    if category == 'world':
        googlenews.set_topic("WORLD")
        googlenews.search("world news")

    if category == 'europe':
        googlenews.set_topic("Europe")
        googlenews.search("Europe news")

    if category == 'US':
        googlenews.set_topic("US")
        googlenews.search("US news")

    if category == 'finland':
        googlenews.search("site:yle.fi/news")

    if category == 'financial':
        googlenews.set_topic("BUSINESS")
        googlenews.search("Financial news")

    if category == 'tech':
        googlenews.set_topic("TECHNOLOGY")
        googlenews.search("Tech news")

    if category == 'sport':
        googlenews.set_topic("SPORTS")
        googlenews.search("Sport news")
    
    if category == 'asia':
        googlenews.set_topic("Asia")
        googlenews.search("Asia news")

    """
    googlenews.set_topic("World News")
    googlenews.search("world news")
    """

    # Fetch a few pages to get a good pool of articles for filtering
    for i in range(1, 10):
        googlenews.get_page(i)
    
    results = googlenews.results()
    
    articles = []
    # We don't slice by page_size here; we return all results
    # so fetch_all_news can filter from a larger pool.
    for item in results:
        title = item.get("title", "No title")
        summary = item.get("desc", "No summary")
        date_raw = item.get("date", "")
        date = parse_date(date_raw)
        url_link = item.get("link", "")
        source = item.get("media", "Google News")

        # Basic filter to avoid articles without a proper link
        if url_link:
            articles.append({
                "title": title,
                "summary": summary,
                "date": date,
                "url": url_link,
                "source": source
            })

    return articles
