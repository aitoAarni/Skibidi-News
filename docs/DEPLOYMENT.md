# Deployment Guide

This document explains how to boot the full Skibidi News stack locally or on a single host using Docker Compose. Pair it with `docs/ARCHITECTURE.md` for the big picture and `docs/COMPONENT_GUIDE.md` for module-level details.

---

## Prerequisites

- Docker 24+ and Docker Compose plugin
- Make sure `OPENAI_API_KEY`, AWS credentials, and (optionally) Anthropic keys are available in your shell or a `.env` file at the repository root. Compose reads `${VAR}` references from the environment.
- 16 GB RAM recommended: the router, four MCP services, and the frontend all run concurrently.

Optional helpers:

- `direnv` or `dotenvx` for loading environment variables
- `docker compose logs -f` familiarity for debugging

---

## Environment Variables

| Var                                                                                 | Used By                                                               | Purpose                                                                           |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `OPENAI_API_KEY`                                                                    | News aggregator, prompt optimizer, text-to-video transcript generator | Required for OpenAI GPT-4o-mini calls.                                            |
| `MODEL_PROVIDER`, `HUMOR_STYLE`, `HTTP_TIMEOUT`, `MAX_OUTPUT_TOKENS`, `TEMPERATURE` | Humorizer MCP                                                         | Configure backend LLM choice and generation knobs.                                |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`                          | Text-to-video MCP                                                     | Credentials for AWS Polly TTS.                                                    |
| `ANTHROPIC_API_KEY` (optional)                                                      | Humorizer MCP                                                         | Only needed if `MODEL_PROVIDER=anthropic`.                                        |
| `PROMPT_LIBRARY`, `PROMPT_LEADERBOARD` (optional)                                   | Prompt optimizer MCP                                                  | Override paths for stored prompt packs/leaderboards; defaults ship with the repo. |

Create a `.env` file in the repo root (same folder as `compose.yaml`) and export the variables above. Docker Compose will substitute the values automatically.

```
OPENAI_API_KEY=sk-...
MODEL_PROVIDER=openai
HUMOR_STYLE=light
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-1
```

---

## Docker Compose Services

The `compose.yaml` file defines six containers on the `appnet` bridge network:

| Service             | Context                  | Ports            | Notes                                                                                                                                                           |
| ------------------- | ------------------------ | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mcp_router_agent`  | `router_agent/`          | `127.0.0.1:8000` | FastAPI router that proxies MCP calls. Mounts `./synthesized_speech` and `./finished_videos` for shared artifacts. Depends on every MCP server.                 |
| `mcp_frontend`      | `skibidi-news-frontend/` | `127.0.0.1:5173` | Vite dev server; environment variables point it to the router’s endpoints. Mounts the source dir for live reload.                                               |
| `mcp_humorizer`     | `mcp_humorizer/`         | internal         | Uses FastMCP over HTTP (no host port exposed). Reads humor style/model knobs from env.                                                                          |
| `mcp_news_aggr`     | `mcp_news_aggr/`         | internal         | Summarizes news and exposes MCP tools. Marked `restart: unless-stopped`.                                                                                        |
| `mcp_prompt_opt`    | `mcp_prompt_opt/`        | internal         | Serves prompt packs and on-demand optimization.                                                                                                                 |
| `mcp_text_to_video` | `mcp_text_to_video/`     | internal         | Generates transcripts, calls AWS Polly, stitches video, and publishes to YouTube. Mounts `./finished_videos` as `/app/results` to share output with the router. |

---

## Bootstrapping the Stack

1. Ensure Docker daemon is running and `.env` variables are set.
2. From the repo root, build and start everything:
   ```bash
   docker compose up --build
   ```
3. The router becomes available at `http://127.0.0.1:8000`; the frontend at `http://127.0.0.1:5173`.
4. To detach, add `-d`. Stop with `docker compose down`.

### Selective rebuilds

- Change in `mcp_humorizer` only? Run `docker compose build mcp_humorizer`.
- Need to restart a single container: `docker compose up -d mcp_router_agent`.

---

## Local Development Outside Docker

Each module can still run natively (see module READMEs). Typical workflow:

1. Start the MCP servers you need via `uv run python -m ...` or `python -m ...`.
2. Point `router_agent` env vars (`MCP_*` URLs) to `http://localhost:<port>/mcp`.
3. Run the frontend with `npm install && npm run dev` inside `skibidi-news-frontend/`.

This hybrid mode is helpful when iterating on a single service while the rest stay in containers.

---

## Volumes & Artifacts

- `./finished_videos` is shared between router and text-to-video containers. Router serves `/videos/{id}` directly from this folder.
- `./synthesized_speech` is mounted into the router for mock data/testing.
- MCP modules keep their own state inside their containers (e.g., `mcp_prompt_opt/opt_logs`). If you need persistence, add more bind mounts in `compose.yaml`.

---

## Health & Troubleshooting

- Use `docker compose ps` to see statuses and mapped ports.
- `docker compose logs -f mcp_router_agent` surfaces MCP call errors returned via FastAPI (HTTP 502).
- Most MCP servers expose a `health` tool. You can `docker exec -it <container> bash` and hit `curl http://localhost:8000/mcp/tools/health` if necessary, or use the router’s `/ping` endpoint to confirm baseline connectivity.
- When Polly or OpenAI calls fail due to missing credentials, the containers print explicit warnings at startup. Check the service logs and your `.env` values.

---

## Production Notes

- Harden secrets delivery (e.g., Docker secrets or cloud secret managers) instead of raw `.env` files.
- Consider enabling `restart: unless-stopped` on every service (router, frontend) for extra resilience.
- Add HTTPS termination (NGINX, Caddy, or cloud load balancer) in front of the router before exposing it publicly.
- Monitor `finished_videos` disk usage; older runs should be archived or pruned.

With these steps you can spin up, monitor, and iterate on the full MCP pipeline with minimal guesswork.
