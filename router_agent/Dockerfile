# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Corporate proxy settings (only used for external traffic). Ensure internal
# Docker network hostnames bypass the proxy to avoid 502 errors on service calls.
ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV NO_PROXY=localhost,127.0.0.1,mcp_news_aggr,mcp_humorizer,mcp_prompt_opt,mcp_text_to_video,mcp_router_agent,router_agent
ENV no_proxy=localhost,127.0.0.1,mcp_news_aggr,mcp_humorizer,mcp_prompt_opt,mcp_text_to_video,mcp_router_agent,router_agent

WORKDIR /app
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app



ENTRYPOINT ["fastapi", "run", "src/main.py"]
