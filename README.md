# Skibidi News

Turning daily news into short, funny, and watchable bites.

## 1) What is this?

Skibidi News is a modular, agentic pipeline that:

1. Aggregates real news.
2. Summarizes it.
3. Punches it up with humor.
4. Converts it to speech.
5. (Optionally) turns speech + captions into short video.

Each step is an **MCP (Model Context Protocol) server** that can be swapped or scaled independently. A central **Router Agent** orchestrates the flow based on a user/system prompt.

## 2) Team & Responsibilities

1. **Gabi** — *News Aggregation → Summarized Text*
2. **Vien** — *Summarized Text → Comedic Text*
3. **Roni** — *Comedic Text → Transcript → Audio*
4. **Aarni** — *Router Agent (MCP client), orchestration & policies*
5. **Esa** — *Prompt Optimization* and *Comedic Text + Audio → Transcript → Video*

> These map 1:1 to MCP services/components so ownership is clear and deploys can be independent.

## 3) High-level Architecture

* **Router Agent (MCP client)**: Receives the user prompt + systemt (tone/constraints). Chooses which MCP service(s) to call, merges results, and pushes outputs downstream.
* **MCP Servers** (swappable micro-services):

  * `mcp-news-aggr` (Owner: **Gabi**): crawl/ingest → clustered topics → summarized text.
  * `mcp-humorizer` (Owner: **Vien**): summary → comedic rewrite (safe-mode, persona knobs).
  * `mcp-tts` (Owner: **Roni**): comedic text → transcript (final) → audio (TTS) with SSML.
  * `mcp-video` (Owner: **Esa**): comedic text + audio → transcript alignment → short video (subtitles, b‑roll, memes).
  * `mcp-prompt-opt` (Owner: **Esa**): prompt library + A/B testing + tracing feedback.

All services speak MCP over stdio/HTTP and return typed JSON payloads.


## 4) Planning and notes

[whiteboard](https://excalidraw.com/#room=d46c315fa785495794e0,P0k_98fYWU7qJUFfmorItA)
