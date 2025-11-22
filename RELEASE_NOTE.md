# Skibidi News – Release 2025.11

AI-powered satirical newsroom-in-a-box: fetch headlines, comedicize them, optimize prompts, turn the jokes into Shorts, and serve everything through one FastAPI router plus a Vite UI.

## 🚀 Highlights

- **Unified Router API**: `router_agent/src/main.py` now fronts every MCP tool (`aggregate_news`, `comedicize`, `generate_transcript`, `synthesize`, `publish`, `best_prompt`) so the frontend only talks to one HTTP host (`/studio/generate`, `/videos/{id}`, `/youtube/publish`, etc.).
- **Composable Docker Stack**: `compose.yaml` spins up router, frontend, and all MCP servers with shared volumes (`finished_videos/`, `synthesized_speech/`) and environment passthrough for OpenAI + AWS Polly credentials.
- **Specialized MCP Services**: dedicated modules handle news ingestion (`mcp_news_aggr/`), humor rewriting (`mcp_humorizer/`), prompt tuning (`mcp_prompt_opt/`), and transcript-to-video rendering plus Shorts upload (`mcp_text_to_video/`).
- **Frontend Experience**: `skibidi-news-frontend/` (Vite + React) lets operators pick categories, generate stories, and preview MP4s backed by router endpoints.
- **Comprehensive Docs**: refreshed `README.md` and deep dives in `docs/ARCHITECTURE.md`, `docs/COMPONENT_GUIDE.md`, `docs/FRONTEND.md`, `docs/DEPLOYMENT.md`, `docs/RUNBOOK.md`, and `docs/TESTING.md` cover architecture, ops, and workflows.

## 🧩 Service Notes

| Service / Path             | Key Capabilities |
| -------------------------- | ---------------- |
| `mcp_news_aggr/`           | GoogleNews+RSS fetch, 120 s cache, OpenAI 100-word digest persisted to `summarized_news.json`. |
| `mcp_humorizer/`           | Pluggable LLM providers, deterministic fallback (`humor.py`), env-driven humor styles, pytest coverage in `tests/`. |
| `mcp_prompt_opt/`          | Prompt pack factory, Elo tournaments (`_optimizer.py`), quick-opt responses, experiment logs in `opt_logs/`. |
| `mcp_text_to_video/`       | Transcript LLM, AWS Polly synthesis, captioned clip composer, Shorts uploader (`socials/youtube/upload.py`). |
| `skibidi-news-frontend/`   | Vite UI wired to router for News → Humor → Studio flow with MP4 previews. |

## 🧪 Testing & Verification

- Automated: `pytest mcp_humorizer/tests -v` (covers deterministic engine + humor templates).
- Manual smoke: documented curl flows in `docs/TESTING.md` (`/news`, `/humorize_news`, `/studio/generate`, `/videos/{id}`) and router checks in `docs/RUNBOOK.md`.
- Frontend lint: `npm run lint` inside `skibidi-news-frontend/`.

## 🔧 Deployment

1. Copy `.env.example` per module, export shared secrets at repo root (OpenAI, AWS, humor style).
2. Run `docker compose up --build` for the full stack.
3. Generated MP4s land in `finished_videos/` and are served by the router via `GET /videos/{video_id}`.

## ⚠️ Known Gaps / Next Steps

1. Expand automated coverage beyond the humorizer (router + other MCPs still rely on manual smoke tests).
2. Add frontend component tests (Vitest/Testing Library) to complement linting.
3. Improve resiliency of YouTube publishing (`mcp_text_to_video/socials/`) with retry/backoff logging.

Let us know if you need this note reiterated for GitHub Releases, changelog formatting, or customer-facing copy.
