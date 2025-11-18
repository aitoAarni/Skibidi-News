import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request

# Import the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.services.mcp_server_services import (
    call_humorizer,
    call_news_aggr,
    generate_trancript,
    generate_video,
    get_best_prompt,
    publish_to_youtube,
)

from src.data_classes import (
    News,
    HumorText,
    StudioGenerateRequest,
    Transcript,
    VideoId,
    PromptOptimizeRequest,
    YouTubeUploadRequest,
)

FINISHED_VIDEOS_DIR = Path("/app/finished_videos")
FINISHED_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

NEWS_CATEGORY_LOOKUP = {
    "world": "world",
    "europe": "europe",
    "us": "US",
    "finland": "finland",
    "financial": "financial",
    "tech": "tech",
    "sport": "sport",
    "sports": "sport",
    "asia": "asia",
}

AVAILABLE_NEWS_CATEGORIES = (
    "world",
    "europe",
    "US",
    "finland",
    "financial",
    "tech",
    "sport",
    "asia",
)

app = FastAPI()

# --- CORS CONFIGURATION START ---

# Define the list of origins that are allowed to make requests.
# Your frontend is running on http://localhost:5173
origins = [
    "http://localhost:5173",
    "http://localhost:5173/",  # Also good to include the trailing slash
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5173/",
]

# Add the CORSMiddleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies (if you use them)
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- CORS CONFIGURATION END ---


@app.get("/ping")
def ping():
    return "pong"


@app.get("/news")
async def news_route(category: str = Query("world")):
    canonical_category = NEWS_CATEGORY_LOOKUP.get(category.lower(), "world")

    try:
        news_payload = await call_news_aggr(canonical_category)
    except Exception as exc:  # pragma: no cover - surfaced to client
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch news: {exc}"
        ) from exc

    summary = news_payload.get("summary", "")
    resolved_category = news_payload.get("category", canonical_category)

    return {
        "summary": summary,
        "category": resolved_category,
        "available_categories": list(AVAILABLE_NEWS_CATEGORIES),
    }


@app.post("/humorize_news")
async def humorizer_route(news: News):
    print(f"news.news: {news.news}")
    huomrized_text = await call_humorizer(news.news)

    return {"huomrized_news": huomrized_text}


@app.post("/transcript")
async def transcript_route(huomr_text: HumorText):
    print(f"humor_text: {huomr_text}")
    transcript = await generate_trancript(huomr_text.humor_text)

    return {"transcript": transcript}


@app.post("/synthesize")
async def synthesize_route(transcript: Transcript):
    video_id = await generate_video(transcript.transcript)
    return {"video_id": video_id}


@app.post("/prompt/best")
async def best_prompt_route(request: PromptOptimizeRequest):
    allow_quick_opt = (
        True if request.allow_quick_opt is None else request.allow_quick_opt
    )

    try:
        result = await get_best_prompt(request.prompt, request.summary, allow_quick_opt)
    except Exception as exc:  # pragma: no cover - surfaced to client
        raise HTTPException(
            status_code=502, detail=f"Failed to optimize prompt: {exc}"
        ) from exc

    return result


@app.post("/studio/generate")
async def studio_generate_route(
    studio_request: StudioGenerateRequest, request: Request
):
    """Generate both transcript and synthesized video for the provided humor text."""
    transcript = await generate_trancript(studio_request.humor_text)
    video_id = await generate_video(transcript, studio_request.background_video)

    video_id_str = str(video_id)
    video_path = FINISHED_VIDEOS_DIR / f"{video_id_str}.mp4"

    if not video_path.exists():
        for _ in range(10):
            await asyncio.sleep(0.5)
            if video_path.exists():
                break

    if not video_path.exists():
        print(f"Warning: expected video file missing at {video_path}")

    video_url = str(request.url_for("serve_video", video_id=video_id_str))
    return {
        "transcript": transcript,
        "video_id": video_id_str,
        "video_url": video_url,
    }


@app.get("/videos/{video_id}", name="serve_video")
async def serve_video(video_id: str):
    """Stream a synthesized video file to the caller."""
    video_path = FINISHED_VIDEOS_DIR / f"{video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4",
    )


@app.post("/youtube/publish")
async def youtube_publish_route(upload_request: YouTubeUploadRequest):
    """Publish a video to YouTube using the provided OAuth token and video details."""
    try:
        await publish_to_youtube(
            upload_request.oauth_token,
            upload_request.video_id,
            upload_request.video_title,
            upload_request.video_description,
            upload_request.keywords,
            upload_request.privacy_status,
        )
        return {"success": True, "message": "Video published successfully to YouTube"}
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Failed to publish video: {exc}"
        ) from exc


@app.post("/upload-video")
async def upload_video_route(video_id: VideoId):
    pass
