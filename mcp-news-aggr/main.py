from fetch_news import fetch_guardian_news
from summarize_news import summarize_article
import json 

def main():
    # Empty the JSON file at the start
    with open("mcp-news-aggr/summarized_news.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    #Fetch articles
    articles = fetch_guardian_news(section="world", page_size=20)
    
    #Summarize each article
    summarized_news = []
    for article in articles:
        summarized_news.append(summarize_article(article))
    
    #Save summarized news to JSON file
    with open("mcp-news-aggr/summarized_news.json", "w", encoding="utf-8") as f:
        json.dump(summarized_news, f, ensure_ascii=False, indent=2)
    
    #Print results
    for news in summarized_news:
        print(news)

if __name__ == "__main__":
    main()
