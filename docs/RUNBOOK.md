# Runbook

This runbook collects the day-to-day operational procedures for Skibidi News. Use it when running E2E demos, verifying deployments, or triaging failures in the MCP pipeline.

---

## 1. End-to-End Flow (Router + Frontend)

1. Ensure the stack is up (`docker compose up --build`).
2. Visit `http://127.0.0.1:5173` and trigger a story generation from the UI, or follow the manual API flow below.

### Manual API Flow (curl)

```bash
# 1. Fetch summarized news
curl 'http://127.0.0.1:8000/news?category=world'

# 2. Humorize the summary
curl -X POST http://127.0.0.1:8000/humorize_news \
  -H 'Content-Type: application/json' \
  -d '{"news": "<summary text>"}'

# 3. Generate transcript
curl -X POST http://127.0.0.1:8000/transcript \
  -H 'Content-Type: application/json' \
  -d '{"humor_text": "<humorous text>"}'

# 4. Synthesize video
curl -X POST http://127.0.0.1:8000/synthesize \
  -H 'Content-Type: application/json' \
  -d '{"transcript": "<transcript text>"}'

# Response: {"video_id": "..."}
# 5. Download video
curl -o out.mp4 "http://127.0.0.1:8000/videos/<video_id>"
```

For an all-in-one call, use `POST /studio/generate` with `{"humor_text": "...", "background_video": "subway-surfers"}`.

---

## 2. MCP Service Smoke Tests

Use these when a single subsystem misbehaves.

| Service          | Quick command                                                                   | Expected result                                      |
| ---------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Router           | `curl http://127.0.0.1:8000/ping`                                               | `"pong"`                                             |
| News Aggregator  | `docker compose exec mcp_news_aggr curl -s localhost:8000/mcp/tools`            | Tool list includes `aggregate_news`.                 |
| Humorizer        | `docker compose exec mcp_humorizer curl -s localhost:8000/mcp/tools/comedicize` | Returns JSON schema description.                     |
| Prompt Optimizer | `docker compose exec mcp_prompt_opt ls opt_logs`                                | Leaderboard files present.                           |
| Text-to-Video    | `docker compose exec mcp_text_to_video ls results`                              | Videos accumulate; empty folder is OK on fresh boot. |

To run the news fetcher without MCP, execute `python -m mcp_news_aggr.main` inside the container or host venv. Logs will show article titles and summary output.

---

## 3. Troubleshooting Cheatsheet

| Symptom                                                     | Likely cause                                                         | Fix                                                                                                                                                         |
| ----------------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Router returns HTTP 502 with message `Failed to fetch news` | `mcp_news_aggr` container down or OpenAI key missing.                | Check `docker compose ps`, review `docker compose logs mcp_news_aggr`, ensure `OPENAI_API_KEY` is exported.                                                 |
| Humorized text is identical to summary                      | Humorizer fell back to deterministic mode or no MCP response parsed. | Confirm `MODEL_PROVIDER` and keys, inspect `router_agent/src/services/mcp_server_services.py` logs for `_normalize_text_payload` warnings.                  |
| `/synthesize` returns 500 or `Video not found`              | Text-to-video failed to stitch output or file not yet synced.        | Tail `docker compose logs mcp_text_to_video`, verify `./finished_videos` mount, rerun `POST /synthesize` and wait ~5 seconds before hitting `/videos/{id}`. |
| Prompt optimizer requests hang                              | `mcp_prompt_opt` still building leaderboard on boot.                 | Wait for container logs to show `FastMCP server running`, or hit `curl localhost:8000/mcp` inside container to verify readiness.                            |
| YouTube publish fails with `Unknown error`                  | Missing OAuth token or invalid privacy status.                       | Ensure frontend supplies `oauth_token` from manual OAuth flow; allowed `privacy_status` values: `public`, `private`, `unlisted`.                            |
| AWS Polly errors (`UnrecognizedClientException`)            | Bad AWS credentials or region mismatch.                              | Recheck `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`; restart `mcp_text_to_video`.                                                        |

---

## 4. Routine Maintenance

- **Purge artifacts**: Clean `finished_videos/` when disk usage grows (`rm finished_videos/*.mp4`). Keep at least the most recent demo clips.
- **Rotate keys**: Update OpenAI/AWS keys in the `.env` file; restart affected containers so they pick up new values.
- **Update prompt library**: Drop new `variants.json` or `leaderboard_final.json` into `mcp_prompt_opt/opt_logs/` and restart the container to load them.
- **Refresh npm deps**: Inside `skibidi-news-frontend/` run `npm install` when package.json changes, then rebuild the frontend container.

---

## 5. Debugging Tips

- Set `LOG_LEVEL=DEBUG` (supported by FastAPI and several MCP servers) to increase verbosity during local runs.
- Use `uvicorn --reload src.main:app` inside `router_agent/` when debugging without Docker.
- When testing MCP responses, call the helper directly in a Python REPL:
  ```python
  import asyncio
  from router_agent.src.services.mcp_server_services import call_humorizer
  asyncio.run(call_humorizer("Sample summary"))
  ```
- The router’s `_normalize_text_payload` already trims quotes; if parsing still fails, log `response.content` to inspect what the MCP server returned.

---

## 6. Incident Response

1. **Assess scope**: Which endpoint or UI action is failing?
2. **Check router logs**: `docker compose logs mcp_router_agent` shows precise MCP errors.
3. **Isolate service**: Use the smoke tests above to identify the unhealthy MCP server.
4. **Restart the culprit**: `docker compose restart <service>`.
5. **Document**: Capture error messages and any config changes in `docs/diary.md` or your ticketing system.

This runbook should cover the common operational loops. For deeper dives, consult module-specific READMEs or the new deployment guide.
