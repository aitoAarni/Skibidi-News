import asyncio
from mcp_humorizer import comedicize_text, Settings


async def run_humorizer():
    settings = Settings.from_env()
    text = comedicize_text("The economy shrank by 2% last quarter.", settings)
    print(text)



if __name__ == "__main__":
    print("Hello worlds!")
    asyncio.run(run_humorizer())
