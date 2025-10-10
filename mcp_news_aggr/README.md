# MCP News Aggregator

This module is the **News Aggregation MCP Server** for Skibidi News. It fetches, parses, and summarizes news articles from multiple sources: Google News, BBC, Yle, CNN, Bloomberg, and Forbes. 

## Folder Structure

```
mcp_news_aggr/
  main.py                # Use to run news_aggr without having to run MCP server
  mcp_server.py          # MCP server with tools
  summarize_news.py      # Summarizes fetched articles using OpenAI API
  summarized_news.json   # Output file: generated summary (used by MCP tools)
  config.py              # Loads environment variables (API keys)
  requirements.txt       # Python dependencies
  Dockerfile             # Containerization for MCP deployment
  fetch_news/            # News source modules (Google, BBC, Yle, etc.)
    fetch_all_news.py    # Aggregates all sources
    fetch_google_news.py # Google News (Python Library)
    fetch_bbc_news.py    # BBC through Google News
    fetch_yle_news.py    # Yle through Google News
    fetch_cnn_news.py    # CNN through Google News
    fetch_bloomberg_news.py # Bloomberg through Google News
    fetch_forbes_news.py # Forbes through Google News
    __init__.py
  .env.example           # Example environment config
  .env                   # Actual environment config (not tracked)
```

## How to run news_aggr locally

1. **Configure environment:**
   - Copy `.env.example` to `.env` and fill in your API keys (e.g., `OPENAI_API_KEY`).

2. **Run aggregation and summarization locally:**
   ```sh
   python -m mcp_news_aggr.main
   ```
   - This will fetch news, summarize, and save output to `summarized_news.json`.


## MCP Tools

Exposed via [`mcp_server.py`](mcp_news_aggr/mcp_server.py):

- `aggregate_news()`  
  Fetches articles from all sources, summarizes them, and returns the summary.

- `get_summary()`  
  Returns the latest summary from `summarized_news.json`.

- `health()`  
  Returns basic server status and available sources.

## News Fetching

All news source logic is in [`fetch_news/`](mcp_news_aggr/fetch_news):

- Each `fetch_X.py` module implements a `fetch_X_news(page_size)` function.
- Sources: Google News, BBC, Yle, CNN, Bloomberg, Forbes.
- Today's news only.

[`fetch_all_news.py`](mcp_news_aggr/fetch_news/fetch_all_news.py) combines all sources and sorts by date.

## News Summarization

- [`summarize_news.py`](mcp_news_aggr/summarize_news.py) uses OpenAI GPT-40-mini model to summarize all articles into a digest.
- The summary is written to `summarized_news.json`.

## Docker

Build and run the MCP server in a container:

```sh
docker build . -t mcp-news-aggr
docker run --env-file .env mcp-news-aggr
```

## Environment Variables

See `.env.example` for required keys:

- `OPENAI_API_KEY` (required for summarization)
