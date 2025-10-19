from openai import OpenAI

import os


def get_system_prompt() -> str:
    with open("./llm/system-prompt.txt", "r") as input_file:
        text = input_file.read()
    return text


def transcript(summarized_news: str) -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=get_system_prompt(),
        input=summarized_news,
        max_output_tokens=5000,
    )

    return response.output_text
