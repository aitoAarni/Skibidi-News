import os
from dotenv import load_dotenv

load_dotenv()

from openai import AsyncOpenAI
from agents import set_tracing_disabled

BASE_URL = os.getenv("BASE_URL") or "https://api.openai.com/v1"
API_KEY  = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY") or ""
if not API_KEY:
    raise ValueError("API_KEY / OPENAI_API_KEY not set.")


client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)
