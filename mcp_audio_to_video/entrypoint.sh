#!/usr/bin/env bash
set -e
. /workspace/.venv/bin/activate
export HF_HUB_ENABLE_HF_TRANSFER=1
mkdir -p /models /workspace/output

if [ ! -d "$MODEL_DIR" ] || [ ! -f "$MODEL_DIR/config.json" ]; then
    echo "[init] downloading model to $MODEL_DIR"
    huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir "$MODEL_DIR"
fi

uvicorn wan_s2v_server:app --host 0.0.0.0 --port 7861
