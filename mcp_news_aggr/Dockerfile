# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (optional: git/curl if needed later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the server package
COPY . /app/mcp_news_aggr

# Default environment (can be overridden at runtime)
ENV MODEL_PROVIDER=none \
    MAX_OUTPUT_TOKENS=400 \
    TEMPERATURE=0.7

# Run MCP server over stdio
ENTRYPOINT ["python", "-m", "mcp_news_aggr.mcp_server"]
