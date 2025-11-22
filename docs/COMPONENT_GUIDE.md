# Skibidi News Code Components

> Use this guide together with `docs/ARCHITECTURE.md`. The architecture doc shows the big picture; this file stays close to the actual code so you know where logic lives, which files to read, and how data moves between services.

---

## Router Agent (`router_agent/src`)
The router is a FastAPI app that exposes a single HTTP surface for the frontend. It fan-outs to MCP servers over HTTP streaming via the helper decorator in `router_agent/src/services/utils.py`.

### Key Files
| File | Purpose |
| --- | --- |
| `router_agent/src/main.py` | FastAPI routes for news, humor, transcript, synth, prompt optimization, studio workflows, and YouTube publishing. |
| `router_agent/src/services/mcp_server_services.py` | Thin async clients that call MCP tools (`aggregate_news`, `comedicize`, `generate_transcript`, `synthesize`, `publish`, `best_prompt`). |
| `router_agent/src/services/utils.py` | `mcp_http_session` decorator that opens a `streamablehttp_client` connection and injects a `ClientSession` into each service function. |
| `router_agent/src/data_classes.py` | Pydantic payload models shared by the HTTP handlers. |

### REST Surface
| Method & Path | Handler | What it does |
| --- | --- | --- |
| `GET /news?category=` | `news_route` | Normalizes category (see `NEWS_CATEGORY_LOOKUP`) and calls `call_news_aggr` to fetch + summarize articles. |
| `POST /humorize_news` | `humorizer_route` | Body: `News`. Calls `call_humorizer` (`mcp_humorizer` -> tool `comedicize`) and returns `{ huomrized_news }`. |
| `POST /transcript` | `transcript_route` | Body: `HumorText`. Calls `generate_trancript` (`mcp_text_to_video.generate_transcript`). |
| `POST /synthesize` | `synthesize_route` | Body: `Transcript`. Calls `generate_video` to trigger video synthesis. |
| `POST /prompt/best` | `best_prompt_route` | Body: `PromptOptimizeRequest`. Calls `get_best_prompt` (`mcp_prompt_opt.best_prompt`). |
| `POST /studio/generate` | `studio_generate_route` | All-in-one path: takes humor text + optional `background_video`, requests transcript, synthesizes, then polls `/videos/{id}` for availability before returning both transcript and a signed URL. |
| `GET /videos/{video_id}` | `serve_video` | Streams the finished MP4 from `FINISHED_VIDEOS_DIR` (mounted to `/app/finished_videos` inside the container). |
| `POST /youtube/publish` | `youtube_publish_route` | Sends OAuth token & metadata to the MCP text-to-video server (`publish` tool) to upload Shorts. |

### MCP Client Notes
- Every call `await session.initialize()` before invoking a tool.
- `_normalize_text_payload` in `mcp_server_services.py` strips quotes/whitespace because some MCP servers respond with JSON-as-text blocks.
- Error handling: FastAPI routes translate MCP failures into HTTP 502 responses so the frontend can surface errors cleanly.

---

## MCP Services
Each MCP folder is its own deployable FastMCP/stdio server with tool definitions. Everything speaks JSON over the MCP protocol.

### News Aggregator (`mcp_news_aggr`)
- Entrypoint: `mcp_news_aggr/mcp_server.py` (tools `aggregate_news`, `get_summary`, `health`).
- Fetch layer: `fetch_news/fetch_all_news.py` picks a canonical category, uses Google News scraping first, then RSS fallback (`feedparser_fetch_category_news`). Results are cached for 120 seconds in `_category_cache` and deduped per day via `fetch_news/history_manager.py`.
- Summaries: `summarize_news.py` sends the concatenated articles to OpenAI `gpt-4o-mini` with a 100-word professional digest prompt. Output is persisted to `summarized_news.json` so `get_summary` can respond without refetching.
- Running locally: `python -m mcp_news_aggr.main` (clears JSON, fetches 3 articles, writes summary).
- Required env: `OPENAI_API_KEY`; optionally `.env` with provider settings.

### Humorizer (`mcp_humorizer`)
- Entrypoint: `mcp_humorizer/mcp_server.py` exposes `comedicize` and `health`.
- Text engines: `engine.py` chooses between OpenAI, Anthropic, or the deterministic fallback in `humor.py` (used when `MODEL_PROVIDER=none`).
- Config: `config.py` loads env + builds the base system prompt (style, provider, safety toggles). CLI driver lives in `cli.py` for local testing.
- Tests: `tests/test_engine.py` and `tests/test_humor.py` cover both deterministic and LLM-backed flows.
- Important env variables: `MODEL_PROVIDER`, `API_KEY`/`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`, `HUMOR_STYLE`, `TEMPERATURE`, `MAX_OUTPUT_TOKENS`.

### Prompt Optimizer (`mcp_prompt_opt`)
- Entrypoint: `mcp_prompt_opt/mcp_server.py` exposing `best_prompt`, `optimize`, `health`.
- Generation: `_prompt_factory.py` creates prompt packs (system prompt, structure, decoding prefs).
- Evaluation: `_optimizer.py` runs Elo-based tournaments, orchestrates judge calls, stores leaderboards in `opt_logs/` and seed variants in `variants.json`.
- Fast path: `best_prompt` first reads the leaderboard (`opt_logs/leaderboard_final.json`). If confidence is low and `allow_quick_opt=true`, it spawns a tiny optimization round before responding.
- Long runs: `run_optimization.py` & `overnight_opt.py` automate full tournaments.
- Required env: `OPENAI_API_KEY`, `MODEL_NAME`, optional `PROMPT_LIBRARY`, `PROMPT_LEADERBOARD`, plus `FAST_*` knobs for on-demand optimization.

### Text-to-Video (`mcp_text_to_video`)
- Entrypoint: `mcp_text_to_video/main.py` registering tools `generate_transcript`, `get_background_videos`, `synthesize`, `publish`.
- Transcript generation: `llm/openai.py` calls OpenAI Responses API (`gpt-4o-mini`) using instructions from `llm/system-prompt.txt`. This is what `router_agent` hits before synthesis to improve narration quality.
- Audio synthesis: `tts/polly.py` wraps AWS Polly (see `.env.example` for keys) and returns an `Engine` with batched MP3 segments.
- Video composition: `video/tools.py` stitches Polly audio + caption overlays onto looping background clips defined in the `videos` dict (default `subway-surfers`). Output MP4s land in `results/{uuid}.mp4` and are under 60 seconds for Shorts.
- Publishing: `socials/youtube/upload.py` (imported as `upload`) handles OAuth-based uploads using the YouTube Data API; the router passes tokens through.
- Dependencies: `moviepy`, `boto3`, OpenAI SDK. Environment needs `AWS_*` vars and `OPENAI_API_KEY`.
- Runtime contract: `synthesize` returns a UUID string; downstream expects to find the video file either in the MCP server's `results/` directory or bind-mounted into `finished_videos/` for serving.

---

## Data Contracts & Tooling
| Producer | Tool / Route | Request payload | Response payload |
| --- | --- | --- | --- |
| Router -> News MCP | MCP tool `aggregate_news` | `{ "category": "world" }` (optional) | `{ "category": "world", "summary": "...", "articles": [...] }` written to `summarized_news.json`. |
| Router -> Humorizer MCP | `comedicize` | `{ "id": "router-request", "summarized_text": "..." }` | `{ "id": "router-request", "comedic_text": "..." }`. Router unwraps `comedic_text`. |
| Router -> Prompt Optimizer | `best_prompt` | `{ "prompt": "...", "summary": "...", "allow_quick_opt": true }` | JSON string/object with `prompt_pack` metadata and `note`. `_normalize_text_payload` handles both stringified JSON and binary frames. |
| Router -> Text-to-Video | `generate_transcript` | `{ "summarized_news": "humorous body" }` | Raw transcript text. |
| Router -> Text-to-Video | `synthesize` | `{ "text": "transcript", "background_video": "subway-surfers" }` | Video identifier string (UUID). |
| Router -> Text-to-Video | `publish` | OAuth token + metadata JSON | Boolean success flag (string or JSON). |
| Frontend → Router | `POST /studio/generate` | `{ "humor_text": "...", "background_video": "subway-surfers" }` | `{ "transcript": "...", "video_id": "...", "video_url": "..." }`. |

All MCP responses are expected to land in `response.content[0]`; code defensively inspects both `.text` and `.data` to support providers that send binary frames.

---

## Operational Notes
- **Docker**: Every MCP module has its own `Dockerfile`. Compose the stack using `compose.yaml` at repo root so services can reach each other via container DNS names (`mcp_news_aggr`, `mcp_humorizer`, etc.).
- **Environment segregation**: keep service-specific `.env` files alongside each module (`mcp_humorizer/.env`, `mcp_text_to_video/.env`, ...). The router only needs addresses and optional tokens because it proxies calls.
- **Artifacts**:
  - News summaries live in `mcp_news_aggr/summarized_news.json` and can be inspected for debugging.
  - Prompt optimizer stores experiment logs in `mcp_prompt_opt/opt_logs/` so you can replay tournaments.
  - Text-to-video outputs store locally in `mcp_text_to_video/results/`. When running via Docker Compose, mount that directory into `finished_videos/` so `router_agent` can serve `/videos/{id}`.
- **Testing hooks**: `mcp_humorizer/tests`, `mcp_prompt_opt/tests`, and the router's `_normalize_text_payload` helper are covered by Pytest. Add more integration tests by mocking MCP responses in `router_agent/src/services/mcp_server_services.py`.

Use this guide as a map: when you need to change behavior, follow the table to jump straight to the relevant MCP tool code or router endpoint without re-deriving the system from scratch.
