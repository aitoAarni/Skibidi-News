# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    NO_PROXY=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,skibidinews_appnet,*.local,172.23.0.0/16 \
    http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    no_proxy=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,skibidinews_appnet,*.local,172.23.0.0/16

# System deps (optional: git/curl if needed later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first for better layer caching
COPY pyproject.toml pyproject.toml
COPY opt_logs/* ./opt_logs/
COPY variants.json .
COPY meta_system.txt .
COPY judge_prompt.txt .

RUN pip install uv
RUN uv sync

# Copy the server package
COPY . /app/mcp_prompt_opt

# Default environment (can be overridden at runtime)
ENV MODEL_PROVIDER=none \
    MAX_OUTPUT_TOKENS=400 \
    TEMPERATURE=0.7

# Run MCP server over stdio
ENTRYPOINT ["uv", "run", "python", "-m", "mcp_prompt_opt.mcp_server"]
