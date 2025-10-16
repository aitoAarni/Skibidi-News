#!/usr/bin/env python3
import os, shutil, math, uuid, shlex, re
import subprocess
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

DEFAULT_CKPT = os.getenv("MODEL_DIR", "/models/Wan2.2-S2V-14B")
OUT_DIR = os.getenv("OUT_DIR", "/workspace/output")
CACHE_DIR = os.getenv("CACHE_DIR", "/workspace/cache")
CHUNK_SEC = max(1, int(os.getenv("WAN_CHUNK_SEC", "10")))

WAN_S2V_CMD = os.getenv("WAN_S2V_CMD", "").strip()

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

app = FastAPI(title="Wan S2V Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run(cmd: List[str]) -> subprocess.CompletedProcess:
    print("[CMD]", " ".join(shlex.quote(c) for c in cmd))
    return subprocess.run(cmd, check=True, text=True, capture_output=True)

def duration_seconds(path: str) -> float:
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path],
        ).decode().strip()
        return float(out)
    except Exception:
        return 0.0

def looks_like_resolution(s: str) -> bool:
    return bool(re.fullmatch(r"\d{2,5}x\d{2,5}", s))

def build_s2v_cmd_structured(
    audio_path: str, prompt: str, out_mp4: str, fps: int, resolution: str
) -> List[str]:
    """
    Default runner using the installed package: python -m wan.speech2video
    """
    return [
        "python", "-m", "wan.speech2video",
        "--ckpt_dir", DEFAULT_CKPT,
        "--offload_model", "True",
        "--convert_model_dtype",
        "--audio", audio_path,
        "--prompt", prompt,
        "--out", out_mp4,
        "--fps", str(fps),
        "--resolution", resolution,
    ]

def build_s2v_cmd_from_env(
    audio_path: str, prompt: str, out_mp4: str, fps: int, resolution: str
) -> List[str]:
    """
    Use user-provided WAN_S2V_CMD as a shell snippet; append args.
    We pass through bash -lc so ${MODEL_DIR} etc. expand.
    """
    base = WAN_S2V_CMD
    cmdline = (
        f'{base} --audio {shlex.quote(audio_path)} '
        f'--prompt {shlex.quote(prompt)} '
        f'--out {shlex.quote(out_mp4)} '
        f'--fps {fps} --resolution {shlex.quote(resolution)}'
    )
    return ["/bin/bash", "-lc", cmdline]

@app.get("/")
def index():
    return {
        "name": "Wan S2V Server",
        "health": "/health",
        "infer": "POST /s2v (multipart form: audio file field 'audio', plus form fields 'prompt', optional 'job','fps','resolution','crf')",
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_ready": os.path.exists(DEFAULT_CKPT)}

@app.get("/download")
def download(path: str):
    if os.path.isfile(path):
        return FileResponse(path, filename=os.path.basename(path))
    return JSONResponse({"error": "File not found"}, status_code=404)

@app.post("/s2v")
async def s2v(
    audio: UploadFile = File(...),
    prompt: str = Form(""),
    job: Optional[str] = Form(None),
    fps: int = Form(24),
    resolution: str = Form("768x432"),
    crf: int = Form(18),
):
    job = job or uuid.uuid4().hex[:8]
    work = os.path.join(CACHE_DIR, job)
    os.makedirs(work, exist_ok=True)

    in_name = audio.filename or "input.audio"
    input_path = os.path.join(work, in_name)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    total = duration_seconds(input_path)
    if total <= 0:
        return JSONResponse({"error": "Invalid or unreadable audio file"}, status_code=400)

    chunks: List[str] = []
    n_chunks = max(1, math.ceil(total / CHUNK_SEC))
    for i in range(n_chunks):
        start = i * CHUNK_SEC
        chunk_path = os.path.join(work, f"chunk_{i:03d}.wav")
        try:
            run([
                "ffmpeg", "-hide_banner", "-nostdin", "-y",
                "-i", input_path,
                "-ss", str(start),
                "-t", str(CHUNK_SEC),
                "-ac", "1",
                "-ar", "24000",
                chunk_path,
            ])
        except subprocess.CalledProcessError as e:
            return JSONResponse(
                {"error": f"ffmpeg split failed at chunk {i}", "stderr": e.stderr[-4000:] if e.stderr else ""},
                status_code=500,
            )
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)

    if not chunks:
        return JSONResponse({"error": "Audio splitting produced no chunks"}, status_code=500)

    segments: List[str] = []
    for i, wav in enumerate(chunks):
        seg_mp4 = os.path.join(work, f"seg_{i:03d}.mp4")

        cmd = (
            build_s2v_cmd_from_env(wav, prompt, seg_mp4, fps, resolution)
            if WAN_S2V_CMD
            else build_s2v_cmd_structured(wav, prompt, seg_mp4, fps, resolution)
        )

        try:
            cp = run(cmd)
            if cp.stdout:
                print(cp.stdout[-2000:])
            if cp.stderr:
                print(cp.stderr[-2000:])
        except subprocess.CalledProcessError as e:
            return JSONResponse(
                {"error": f"S2V command failed on chunk {i}", "stderr": e.stderr[-4000:] if e.stderr else ""},
                status_code=500,
            )

        if not os.path.exists(seg_mp4) or os.path.getsize(seg_mp4) == 0:
            return JSONResponse({"error": f"Segment missing for chunk {i}"}, status_code=500)

        segments.append(seg_mp4)

    concat_inputs = []
    for seg in segments:
        concat_inputs.extend(["-i", seg])

    video_no_audio = os.path.join(work, "video_no_audio.mp4")
    try:
        run(
            ["ffmpeg", "-hide_banner", "-nostdin", "-y", *concat_inputs,
            "-filter_complex", f"concat=n={len(segments)}:v=1:a=0[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            video_no_audio]
        )
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {"error": "ffmpeg concat failed", "stderr": e.stderr[-4000:] if e.stderr else ""},
            status_code=500,
        )

    final_path = os.path.join(OUT_DIR, f"wan_s2v_{job}.mp4")
    try:
        run(
            ["ffmpeg", "-hide_banner", "-nostdin", "-y",
            "-i", video_no_audio, "-i", input_path,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", final_path]
        )
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {"error": "ffmpeg mux failed", "stderr": e.stderr[-4000:] if e.stderr else ""},
            status_code=500,
        )

    return {
        "job": job,
        "segments": len(segments),
        "fps": fps,
        "resolution": resolution,
        "result_path": final_path,
        "download": f"/download?path={shlex.quote(final_path)}",
    }
