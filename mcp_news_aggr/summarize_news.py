import openai
#from config import OPENAI_API_KEY
from mcp_news_aggr.config import OPENAI_API_KEY

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

def summarize_all_articles(articles):
    """
    Create a long, full-text summary of all articles combined.
    """
    if not articles:
        return "No articles available to summarize."

    combined_text = "\n\n---\n\n".join(articles)

    prompt = (
        "Act as a professional journalist. Write a detailed news digest summary. "
        "The summary should:\n"
        "- Cover all main events across the articles.\n"
        "- Highlight key players, locations, and timelines.\n"
        "- Explain the broader context and significance.\n"
        "- Do not skip any articles or information.\n"
        "- Be written in a clear, neutral, professional tone.\n\n"
        f"Articles:\n{combined_text}\n\n"
        "Now write the full summary:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2000
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except openai.error.RateLimitError:
        return "Rate limit reached. Please try again later."

    except Exception as e:
        print("Error summarizing articles:", e)
        return "Error generating summary."
