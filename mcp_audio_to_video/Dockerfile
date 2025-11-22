# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY opt_logs/* ./opt_logs/
COPY variants.json .
COPY meta_system.txt .
COPY judge_prompt.txt .

RUN pip install uv
RUN uv sync

COPY . /app/mcp_prompt_opt

ENV MODEL_PROVIDER=none \
    MAX_OUTPUT_TOKENS=400 \
    TEMPERATURE=0.7

ENTRYPOINT ["uv", "run", "python", "-m", "mcp_prompt_opt.mcp_server"]
