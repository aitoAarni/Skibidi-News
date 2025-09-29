import os
import openai
from config import OPENAI_API_KEY

# Set API key
openai.api_key = OPENAI_API_KEY

def summarize_all_articles(articles):
    """
    Create a long, full-text summary of all articles combined.
    """
    if not articles or len(articles) == 0:
        return "No articles available to summarize."

    # Combine all articles into one text block
    combined_text = "\n\n---\n\n".join(articles)

    prompt = (
        "Act as a professional journalist. Write a detailed news digest summary. The summary should:\n"
        "- Cover all main events across the articles.\n"
        "- Highlight key players, locations, and timelines.\n"
        "- Explain the broader context and significance.\n"
        "- Be written in a clear, neutral, professional tone.\n\n"
        f"Articles:\n{combined_text}\n\n"
        "Now write the full summary:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            # You may want to allow more tokens here for longer summaries
            max_tokens=1200  
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        print("Error summarizing articles:", e)
        return "Error generating summary."
