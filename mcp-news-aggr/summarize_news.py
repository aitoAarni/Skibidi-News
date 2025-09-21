from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_article(article):
    prompt = f"Summarize the following news into 2-3 sentences:\n\nTitle: {article['title']}\nSummary: {article['summary']}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    summary_text = response.choices[0].message.content
    
    return {
        "header": article["title"],
        "summary": summary_text,
        "date": article["date"],
        "source": article["source"],
        "url": article["url"]
    }
