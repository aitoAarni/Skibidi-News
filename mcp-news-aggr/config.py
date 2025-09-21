import os
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")