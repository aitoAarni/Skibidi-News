#!/usr/bin/env python3
import os, shutil, math, uuid, shlex, re
import subprocess
from typing import Optional, List

from fastapi import FastAPI, Form
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


def looks_like_resolution(s: str) -> bool:
    return bool(re.fullmatch(r"\d{2,5}x\d{2,5}", s))


def build_s2v_cmd_structured(
    prompt: str, out_mp4: str, fps: int, resolution: str
) -> List[str]:
    """
    Default runner using the installed package: python -m wan.speech2video
    """
    return [
        "python",
        "-m",
        "wan.speech2video",
        "--ckpt_dir",
        DEFAULT_CKPT,
        "--offload_model",
        "True",
        "--convert_model_dtype",
        "--prompt",
        prompt,
        "--out",
        out_mp4,
        "--fps",
        str(fps),
        "--resolution",
        resolution,
    ]


def build_s2v_cmd_from_env(
    prompt: str, out_mp4: str, fps: int, resolution: str
) -> List[str]:
    """
    Use user-provided WAN_S2V_CMD as a shell snippet; append args.
    We pass through bash -lc so ${MODEL_DIR} etc. expand.
    """
    base = WAN_S2V_CMD
    cmdline = (
        f"{base} "
        f"--prompt {shlex.quote(prompt)} "
        f"--out {shlex.quote(out_mp4)} "
        f"--fps {fps} --resolution {shlex.quote(resolution)}"
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
    prompt: str = Form(""),
    job: Optional[str] = Form(None),
    fps: int = Form(24),
    resolution: str = Form("432x768"),
):
    job = job or uuid.uuid4().hex[:8]
    output = os.path.join(OUT_DIR, f"wan_s2v_{job}.mp4")
    cmd = (
        build_s2v_cmd_from_env(prompt, output, fps, resolution)
        if WAN_S2V_CMD
        else build_s2v_cmd_structured(prompt, output, fps, resolution)
    )

    try:
        cp = run(cmd)
        if cp.stdout:
            print(cp.stdout[-2000:])
        if cp.stderr:
            print(cp.stderr[-2000:])
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {
                "error": f"S2V command failed with code {e.returncode}",
                "stderr": e.stderr[-4000:] if e.stderr else "",
            },
            status_code=500,
        )

    if not os.path.exists(output) or os.path.getsize(output) == 0:
        return JSONResponse({"error": "Error generating video"}, status_code=500)

    return {
        "job": job,
        "fps": fps,
        "resolution": resolution,
        "result_path": output,
        "download": f"/download?path={shlex.quote(output)}",
    }
