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

    """prompt = (
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
    )"""

    #prompt = f"{get_prompt()} + Input Artiles: {combined_text}"

    prompt = (
        "Act as a professional journalist. Write a detailed news digest summary. " 
        "Your writing style is authoritative, objective, insightful, and professional. "
        "You possess a unique ability to see the big picture and connect disparate events into a single, compelling narrative.\n"

        "Mandatory Rules:\n"
        "Include All Articles: Every single article provided in the input must be referenced or have its core information integrated into your final narrative."
        "No article can be skipped."
        "Create a Coherent Narrative: Do not produce a bulleted list or a Here's what happened in topic A, and here's what happened in topic B summary. "
        "Follow this exact order: World News (multiple articles, multiple sources), Finland news (one or multiple articles), Forbes financial news (one article), Bloomberg tech news (one article), sport news (one article)"
        "Be Detailed: This is a detailed digest. While you are synthesizing, you must still pull specific, key facts, figures, names, or quotes from each article to substantiate your narrative."
        "Do not generate final summary at the end."
        "Professional Tone: The output must be written in clear, professional journalistic prose."

        "The summary should:\n"
        "- Cover all main events across all the articles.\n"
        "- Highlight key players, locations, and timelines.\n"
        "- Explain the broader context and significance.\n"
        "- Do not skip any articles or information.\n"
        "- You MUST include world news, bbc news, cnn news, yle news (Finland), and at least one piece of news from bloomberg and at least one piece of news from forbes.\n"
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
