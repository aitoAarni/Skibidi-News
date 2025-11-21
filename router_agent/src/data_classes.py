from pydantic import BaseModel


class News(BaseModel):
    news: str


class HumorText(BaseModel):
    humor_text: str


class StudioGenerateRequest(BaseModel):
    humor_text: str
    background_video: str = "subway-surfers"


class Transcript(BaseModel):
    transcript: str


class VideoId(BaseModel):
    video_id: str


class PromptOptimizeRequest(BaseModel):
    prompt: str
    summary: str
    allow_quick_opt: bool | None = True


class YouTubeUploadRequest(BaseModel):
    oauth_token: str
    video_id: str
    video_title: str
    video_description: str
    keywords: str
    privacy_status: str
