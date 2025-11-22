# Skibidi News

Turning daily news into short, funny, watchable bites powered by a fleet of MCP services.

![router](sample/frontend-2.png)

![frontend](sample/frontend-1.png)

## Highlights

- Fully modular MCP pipeline: news aggregation, humorization, prompt optimization, and text-to-video.
- Router Agent (FastAPI) exposes a single HTTP API for the frontend and proxies every MCP call.
- Docker Compose stack for one-command bringup plus standalone module workflows for rapid iteration.
- Prompt optimizer keeps humor quality consistent via Elo tournaments and reusable prompt packs.

For the deep dive, see `docs/ARCHITECTURE.md` (big picture) and `docs/COMPONENT_GUIDE.md` (code map).

```mermaid
flowchart LR
	Frontend((Vite UI)) -- REST --> Router[Router Agent \n FastAPI]
	Router -- aggregate_news --> NewsAggr[mcp_news_aggr]
	Router -- comedicize --> Humorizer[mcp_humorizer]
	Router -- best_prompt --> PromptOpt[mcp_prompt_opt]
	Router -- transcript/synthesize/publish --> TTV[mcp_text_to_video]
	TTV -- results bind mount --> Videos[(finished_videos/)]
	Router -- MP4 stream --> Videos
	Router -- HTTP API --> Frontend
```

## Architecture at a Glance

| Component        | Responsibility                                                                                     | Key Path                 |
| ---------------- | -------------------------------------------------------------------------------------------------- | ------------------------ |
| Router Agent     | FastAPI server that orchestrates MCP calls and serves assets to the frontend.                      | `router_agent/src`       |
| News Aggregator  | Fetches fresh headlines per category and builds a 100-word professional digest.                    | `mcp_news_aggr/`         |
| Humorizer        | Rewrites summaries into comedic scripts using OpenAI/Anthropic or deterministic fallback.          | `mcp_humorizer/`         |
| Prompt Optimizer | Stores prompt packs, runs quick Elo tournaments, and surfaces the best prompt to the router.       | `mcp_prompt_opt/`        |
| Text-to-Video    | Generates transcripts, calls AWS Polly, overlays captions on background clips, and uploads Shorts. | `mcp_text_to_video/`     |
| Frontend         | Vite + React UI for selecting categories, generating stories, and previewing clips.                | `skibidi-news-frontend/` |

More implementation context lives in `docs/COMPONENT_GUIDE.md`.

## Repository Map

| Path                     | Description                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------- |
| `compose.yaml`           | Docker Compose definition for the router, frontend, and every MCP service.                           |
| `router_agent/`          | FastAPI router + MCP client helpers.                                                                 |
| `mcp_news_aggr/`         | News fetching, summarization logic, and MCP server entrypoint.                                       |
| `mcp_humorizer/`         | Humor engine, deterministic fallback, and MCP tooling.                                               |
| `mcp_prompt_opt/`        | Prompt library, optimizer, and FastMCP server.                                                       |
| `mcp_text_to_video/`     | Transcript LLM calls, AWS Polly synthesis, video compositor, and YouTube uploader.                   |
| `skibidi-news-frontend/` | Web client.                                                                                          |
| `docs/`                  | Architecture, component guide, frontend guide, deployment guide, runbook, testing, and repomix dump. |

## Router API Surface

| Method | Path                 | Purpose                                                         | Downstream tool                         |
| ------ | -------------------- | --------------------------------------------------------------- | --------------------------------------- |
| GET    | `/ping`              | Health probe for the router container.                          | —                                       |
| GET    | `/news?category=`    | Normalizes category and calls `mcp_news_aggr.aggregate_news`.   | `aggregate_news`                        |
| POST   | `/humorize_news`     | Accepts `{ "news": str }` and returns comedic rewrite.          | `mcp_humorizer.comedicize`              |
| POST   | `/transcript`        | Turns humor text into a narrated transcript.                    | `mcp_text_to_video.generate_transcript` |
| POST   | `/synthesize`        | Requests a background video + captions, returns `video_id`.     | `mcp_text_to_video.synthesize`          |
| POST   | `/prompt/best`       | Fetches the highest-scoring prompt pack for a prompt+summary.   | `mcp_prompt_opt.best_prompt`            |
| POST   | `/studio/generate`   | One-shot transcript + video pipeline, returns signed video URL. | combo of tools above                    |
| GET    | `/videos/{video_id}` | Streams finished MP4s from `finished_videos/`.                  | —                                       |
| POST   | `/youtube/publish`   | Sends OAuth token and metadata to upload Shorts.                | `mcp_text_to_video.publish`             |

## MCP Tooling

| Service          | Tool(s)                                                                 | File                           |
| ---------------- | ----------------------------------------------------------------------- | ------------------------------ |
| News Aggregator  | `aggregate_news`, `get_summary`, `health`                               | `mcp_news_aggr/mcp_server.py`  |
| Humorizer        | `comedicize`, `health`                                                  | `mcp_humorizer/mcp_server.py`  |
| Prompt Optimizer | `best_prompt`, `optimize`, `health`                                     | `mcp_prompt_opt/mcp_server.py` |
| Text-to-Video    | `generate_transcript`, `get_background_videos`, `synthesize`, `publish` | `mcp_text_to_video/main.py`    |

## Getting Started

### Requirements

- Docker 24+ with Compose plugin (preferred path) or Python 3.10+ / Node 20+ for manual runs.
- OpenAI API key plus AWS Polly credentials (see `docs/DEPLOYMENT.md`).

### Environment Setup

1. Copy `.env.example` files in each MCP folder to `.env` and fill in required keys.
2. Export shared variables (OpenAI, AWS) in a repo-root `.env` so Compose can read them.

```
OPENAI_API_KEY=sk-...
MODEL_PROVIDER=openai
HUMOR_STYLE=light
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-1
```

### One-Command Stack

```bash
docker compose up --build
```

- Router API: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`
- Generated videos land in `finished_videos/`; the router serves them via `GET /videos/{id}`.

### Iterating on a Single Service

1. Stop the corresponding container.
2. Run the module locally (e.g., `python -m mcp_humorizer.mcp_server`).
3. Point the router to the local MCP endpoint (see service README for exact command).

Refer to `docs/DEPLOYMENT.md` for more Docker tricks and hybrid workflows, plus `docs/FRONTEND.md` if you plan to run the UI outside of Compose.

## Development & Testing

- **Python services**: activate a virtual env inside each MCP folder (`python -m venv .venv && source .venv/bin/activate`), install requirements, then run `python -m <module>.mcp_server` for local iteration.
- **Router**: `uvicorn src.main:app --reload` inside `router_agent/` for hot reloads.
- **Frontend**: `npm install && npm run dev` inside `skibidi-news-frontend/` when not using Docker (see `docs/FRONTEND.md`).
- **Tests**: run targeted suites such as `pytest mcp_humorizer/tests`. See `docs/TESTING.md` for the current coverage matrix and smoke tests.

## Data & Artifacts

- `mcp_news_aggr/summarized_news.json` — latest summary blob consumed by downstream steps.
- `mcp_prompt_opt/opt_logs/*.json` — Elo tournament history and leaderboards.
- `finished_videos/` — MP4 outputs copied from the text-to-video container; served via `/videos/{id}`.
- `synthesized_speech/` — convenience folder for local speech assets and mock data.

## Release Notes

- Latest milestone write-up lives in `RELEASE_NOTE.md` (current tag: **2025.11**) covering router/API unification, Docker stack updates, service highlights, testing, and deployment tips.
  - Use it when you need a quick changelog for GitHub Releases, stakeholder emails, or internal status updates.

## Operations & Runbook

- Manual API flow, smoke tests, troubleshooting cheatsheet, and incident response live in `docs/RUNBOOK.md`.
- For day-to-day diary entries or experiments, use `diary.md`.

## Team & Ownership

- **Gabi** — News Aggregation → Summarized text.
- **Vien** — Summarized text → Comedic text.
- **Roni** — Comedic text → Transcript → Audio.
- **Aarni** — Router agent, orchestration, and policies.
- **Esa** — Prompt optimization and video pipeline.

Responsibilities line up with MCP services so releases can stay independent.

## Reference Docs & Planning

- `docs/ARCHITECTURE.md` — system overview and diagrams.
- `docs/COMPONENT_GUIDE.md` — code-focused component map and data contracts.
- `docs/DEPLOYMENT.md` — docker-compose bringup and environment matrix.
- `docs/RUNBOOK.md` — operational procedures and troubleshooting.
- `docs/FRONTEND.md` — UI architecture, API usage, and dev workflow.
- `docs/TESTING.md` — automated coverage and recommended smoke tests.
- [Planning Whiteboard](https://excalidraw.com/#room=d46c315fa785495794e0,P0k_98fYWU7qJUFfmorItA)

Happy Skibidi-ing!
