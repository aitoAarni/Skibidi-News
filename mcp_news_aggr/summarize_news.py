from openai import OpenAI
from mcp_news_aggr.config import OPENAI_API_KEY

# Set OpenAI key
client = OpenAI(api_key=OPENAI_API_KEY)

"""def get_prompt() -> str:
    with open("mcp_news_aggr.prompt.txt", "r") as input_file:
        text = input_file.read()
    return text"""

def summarize_all_articles(articles):
    """
    Create a long, full-text summary of all articles combined.
    """
    if not articles:
        return "No articles available to summarize."

    combined_text = "\n\n---\n\n".join(articles)


    prompt = (
        "Act as a professional journalist. Write a story-telling news digest summary. Write 100 words. DO NOT GO OVER THE 100 WORDS LIMIT." 
        "Your writing style is objective, insightful, and professional. "
        "You possess a unique ability to see the big picture and connect disparate events into a single, compelling narrative.\n"

        "Mandatory Rules:\n"
        "Create a Coherent Narrative: Do not produce a bulleted list or a Here's what happened in topic A, and here's what happened in topic B summary. "
        "Be Detailed: This is a detailed digest. While you are synthesizing, you must still pull specific, key facts, figures, names from each article to substantiate your narrative."
        "Do not generate final summary at the end."
        "Professional Tone: The output must be written in clear, professional journalistic prose."

        "The summary should:\n"
        "- Cover all main events across all given articles.\n"
        "- Highlight key players, locations, and timelines.\n"
        "- Explain the broader context and significance.\n"
        "- Do not skip any articles or information.\n"
        "- Be written in a clear, neutral, professional tone.\n\n"
        "- Write an coherent text instead of bullet points.\n"
        "- Do not summarize at the end.\n"

        f"Articles:\n{combined_text}\n\n"
        "Now write the full summary following all above mentioned rules."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=2000
    )

    summary = response.choices[0].message.content.strip()
    return summary
