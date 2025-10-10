from openai import OpenAI
from mcp_news_aggr.config import OPENAI_API_KEY

# Set OpenAI key
client = OpenAI(api_key=OPENAI_API_KEY)

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
        "- Cover all main events across all the articles.\n"
        "- Highlight key players, locations, and timelines.\n"
        "- Explain the broader context and significance.\n"
        "- Do not skip any articles or information.\n"
        "- Be written in a clear, neutral, professional tone.\n\n"
        "- Write an coherent text instead of bullet points.\n"
        f"Articles:\n{combined_text}\n\n"
        "Now write the full summary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=2000
    )

    summary = response.choices[0].message.content.strip()
    return summary