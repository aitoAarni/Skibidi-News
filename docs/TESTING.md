# Testing Guide

This document lists the automated tests that exist today, plus the recommended smoke checks for services that do not yet have full suites. Update it whenever you add coverage so contributors know which commands to run.

---

## Overview

| Area                                            | Automated coverage                                                 | Location                    |
| ----------------------------------------------- | ------------------------------------------------------------------ | --------------------------- |
| Humorizer MCP                                   | ✅ Deterministic unit tests for fallback engine + humor templates. | `mcp_humorizer/tests/`      |
| Other MCP servers (news, prompt, text-to-video) | ⚠️ Manual smoke tests only today.                                  | See below for curl recipes. |
| Router Agent                                    | ⚠️ Manual smoke tests (`GET /ping`, etc.).                         | `docs/RUNBOOK.md`           |
| Frontend                                        | ⚠️ Manual testing via Vite dev server; no Jest/Vitest yet.         | `skibidi-news-frontend/`    |

---

## Running Pytest Suites

From the repo root:

```bash
# Humorizer suite (fast, no network calls)
cd mcp_humorizer
python -m venv .venv && source .venv/bin/activate  # if not already
pip install -r requirements.txt
pytest tests -v
```

What the tests cover:

- `test_engine.py`: ensures `Settings` falls back to deterministic humor when OpenAI/Anthropic keys are missing. Confirms style-specific phrases and numeric quips remain intact.
- `test_humor.py`: validates `humorous_rewrite()` output length (2–4 sentences), fact preservation, and style-specific punchlines.

Add new humorizer tests in the same folder—Pytest auto-discovers files named `test_*.py`.

---

## Manual Smoke Tests (Recommended Until Automated)

| Service          | Command                                                                                                                    | Expected result                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| News Aggregator  | `curl 'http://127.0.0.1:8000/news?category=world'`                                                                         | JSON with `summary`, `category`, `available_categories`. |
| Humorizer        | `curl -X POST http://127.0.0.1:8000/humorize_news -H 'Content-Type: application/json' -d '{"news":"..."}'`                 | `{ "huomrized_news": "..." }`.                           |
| Prompt Optimizer | `curl -X POST http://127.0.0.1:8000/prompt/best -H 'Content-Type: application/json' -d '{"prompt":"...","summary":"..."}'` | JSON prompt pack with `note`.                            |
| Text-to-Video    | `curl -X POST http://127.0.0.1:8000/studio/generate -H 'Content-Type: application/json' -d '{"humor_text": "..."}'`        | `{ transcript, video_id, video_url }`.                   |
| Router health    | `curl http://127.0.0.1:8000/ping`                                                                                          | `"pong"`.                                                |

More detailed sequences (including `/transcript`, `/synthesize`, `/videos/{id}`) live in `docs/RUNBOOK.md`.

---

## Frontend Checks

1. `cd skibidi-news-frontend`
2. `npm install`
3. `npm run dev`
4. Visit `http://127.0.0.1:5173`

Verify the News → Humor → Studio pipeline works end-to-end. Use browser devtools to watch network calls; failures usually point to a specific MCP server.

Linting (currently the only automated check) runs via:

```bash
npm run lint
```

Consider adding component tests with Vitest/Testing Library if the UI grows.

---

## Writing New Tests

1. **Match runtime dependencies**: each MCP module has its own `requirements.txt`. Install them inside a local venv before running Pytest.
2. **Isolate network dependencies**: test deterministic helpers (`humor.py`, `_prompt_factory.py`, etc.) with fake data; avoid hitting OpenAI/AWS.
3. **Use sample artifacts**: store fixtures under `tests/fixtures/` (create the folder if needed) instead of referencing production JSON.
4. **Update docs**: after adding a new suite, extend the table at the top of this file so everyone knows how to run it.

---

Until full coverage exists, pair these manual checks with the automated humorizer suite to catch regressions quickly.
