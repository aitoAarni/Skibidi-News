A **high-level architecture diagram and explanation** for MCP system — a modular AI pipeline that transforms **real-world news** into **summarized, humorous, and audio-ready stories**.

---

## 🧩 **High-Level Architecture**

```
                   ┌────────────────────────────────┐
                   │          Router Agent          │
                   │ (orchestrates all MCP servers) │
                   │  └─ router_agent/main.py        │
                   └──────────────┬─────────────────┘
                                  │  (HTTP / MCP protocol)
                                  ▼
        ┌────────────────────────────────────────────────────────┐
        │                        MCP Layer                       │
        │ Each component exposes tools via FastMCP (LLM protocol)│
        └───────────────────┬────────────┬────────────┬──────────┘
                            │            │            │
                            ▼            ▼            ▼
 ┌────────────────┐  ┌─────────────────────┐  ┌───────────────────────┐
 │  mcp-news-aggr │  │   mcp-humorizer    │  │   text-to-audio       │
 │  (Aggregator)  │  │ (Comedic Rewriter) │  │ (Speech Generator)    │
 ├────────────────┤  ├─────────────────────┤  ├───────────────────────┤
 │ • Fetches news │  │ • Converts factual  │  │ • Converts text → MP3 │
 │   (Google, Yle,│  │   summaries into    │  │   via Polly/GCP TTS   │
 │   CNN, BBC...) │  │   humorous versions │  │ • Returns `Audio` obj │
 │ • Summarizes   │  │ • Deterministic or  │  │   for playback/export │
 │   using OpenAI │  │   model-based logic │  │                       │
 └────────────────┘  └─────────────────────┘  └───────────────────────┘
                            │
                            ▼
                   ┌────────────────────┐
                   │  mcp-prompt-opt    │
                   │ (Prompt Optimizer) │
                   ├────────────────────┤
                   │ • Evolves LLM      │
                   │   prompt variants  │
                   │   using ELO ranking│
                   │ • Generates prompt │
                   │   packs & metadata │
                   │ • Supports         │
                   │   auto-tuning runs │
                   └────────────────────┘

                                  │
                                  ▼
                      ┌─────────────────────────┐
                      │     Output Layer        │
                      │ ─────────────────────── │
                      │ • Summarized news.json  │
                      │ • Comedic text          │
                      │ • MP3 audio             │
                      │ • Optimized prompt data │
                      └─────────────────────────┘
```

---

## 🧠 **Data Flow Overview**

| Stage                                 | Component                      | Description                                                                  | Example Input    | Example Output            |
| ------------------------------------- | ------------------------------ | ---------------------------------------------------------------------------- | ---------------- | ------------------------- |
| 1️⃣ **News Fetching**                  | `mcp_news_aggr.fetch_news`     | Scrapes/queries multiple sources using GoogleNews API.                       | _(none)_         | Raw article list          |
| 2️⃣ **Summarization**                  | `mcp_news_aggr.summarize_news` | Summarizes all articles into a concise digest using GPT model.               | News articles    | Summarized text           |
| 3️⃣ **Humorization**                   | `mcp_humorizer.humor`          | Rewrites the summary into comedic, short-form text.                          | Summarized news  | Humorous version          |
| 4️⃣ **Prompt Optimization (optional)** | `mcp_prompt_opt`               | Evolves and ranks prompt variants for humorization or summarization quality. | Prompt + summary | Optimized “prompt packs”  |
| 5️⃣ **Audio Generation**               | `text_to_audio`                | Converts comedic text to speech (Polly or GCP TTS).                          | Comedic text     | MP3 audio                 |
| 6️⃣ **Routing & Integration**          | `router_agent`                 | Coordinates the MCP servers through HTTP streaming or stdio.                 | Summarized text  | Final humorous MP3 output |

---

## 🏗️ **System Responsibilities**

| Layer                    | Description                                                                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Router Agent**         | Acts as the orchestrator. Calls individual MCP servers via HTTP streams.                                   |
| **MCP Servers**          | Each is self-contained, exposing tools (`aggregate_news`, `comedicize`, `synthesize`, etc.) via `FastMCP`. |
| **Prompt Optimizer**     | Improves LLM prompts for consistency, humor quality, and tone using tournament-style evolution.            |
| **Text-to-Audio Engine** | Converts humorized text to audio using TTS engines (AWS Polly / GCP).                                      |
| **Logging & Configs**    | Each module includes JSON logging, `.env` configuration, and reproducible testing setups.                  |

---

## ⚙️ **Execution Pipeline Example**

```
$ python3 -m router_agent.main
     ↓
[Router] → (MCP) mcp-news-aggr.aggregate_news
     ↓
Summarized JSON
     ↓
[Router] → (MCP) mcp-humorizer.comedicize
     ↓
Humorous text
     ↓
[Router] → (MCP) text-to-audio.synthesize
     ↓
Audio (MP3) output file
```

---

## 🧱 **Core Technologies**

| Domain                  | Technology                                               |
| ----------------------- | -------------------------------------------------------- |
| **Orchestration**       | MCP Framework (`fastmcp`, `ClientSession`, HTTP streams) |
| **LLM Integration**     | OpenAI GPT-4o-mini (via OpenAI API)                      |
| **Prompt Optimization** | ELO ranking, genetic mutation of prompt variants         |
| **TTS Engines**         | AWS Polly, Google Cloud Text-to-Speech                   |
| **News Scraping**       | GoogleNews API                                           |
| **Storage**             | JSON outputs, log directories for variants & leaderboard |
| **Environment Mgmt**    | Python 3.13, virtualenv, dotenv                          |

---

## 🌐 **Summary**

This repository is a **modular generative content pipeline** that:

1. **Fetches global news**,
2. **Summarizes it professionally**,
3. **Adds humor and personality**,
4. **Optimizes AI prompts continuously**, and
5. **Converts it all into spoken audio**,
   enabling an end-to-end workflow for an _AI-powered satirical news generator_ (like “Skibidi News”).

---
