
from pydantic import BaseModel

class News(BaseModel):
    news: str

class HumorText(BaseModel):
    humor_text: str

class Transcript(BaseModel):
    transcript: str

class VideoId(BaseModel):
    video_id: str