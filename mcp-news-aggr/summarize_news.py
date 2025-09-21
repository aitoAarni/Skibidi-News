# summarize_news.py
import os
import openai
from config import OPENAI_API_KEY

# Set API key
openai.api_key = OPENAI_API_KEY

def summarize_article(article_text):
    """
    Summarize a single article text into 2-3 sentences.
    """
    if not article_text:
        return "No summary available."

    prompt = (
        "Act as a professional journalist. Summarize the following news article in 2-3 concise sentences:\n\n For each story include the main event, key players, and its significance. Present the information in a concise, neutral tone."
        f"{article_text}\n\nSummary:"
    )

    try:
        response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
)
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        print("Error summarizing article:", e)
        return "Error generating summary."
