import os
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")
YLE_API_KEY = os.getenv("YLE_API_KEY")
YLE_API_ID = os.getenv("YLE_API_ID")

