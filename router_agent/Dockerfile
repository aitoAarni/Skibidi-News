# syntax=docker/dockerfile:1
FROM python:3.11-slim


WORKDIR /app
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    NO_PROXY=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,mcp_text_to_video,skibidinews_appnet,*.local,172.23.0.0/16 \
    http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    no_proxy=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,mcp_text_to_video,skibidinews_appnet,*.local,172.23.0.0/16

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app



ENTRYPOINT ["fastapi", "run", "src/main.py"]
