# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Corporate proxy settings (only used for external traffic). Ensure internal
# Docker network hostnames bypass the proxy to avoid 502 errors on service calls.

WORKDIR /app
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app



ENTRYPOINT ["fastapi", "run", "src/main.py"]
