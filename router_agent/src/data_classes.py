
from pydantic import BaseModel

class News(BaseModel):
    news: str

class HumorText(BaseModel):
    humor_text: str