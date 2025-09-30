# MCP Server – Prompt Optimizer (Python)

This repository contains a Python MCP server that **selects or quickly optimizes the best prompt pack** for a given task. It supports a fast path that chooses the top prompt from your saved leaderboard, and an optional quick tournament that generates a few challengers, A/B judges them, and returns the winner.

- Pluggable LLM backends (OpenAI today; extensible)
- On-demand **quick optimization** (A/B + Elo pruning)
- **Library-first**: reuses your best existing prompts for speed/cost
- Exposes MCP tools over stdio using the Python `mcp` package (FastMCP)

## ✨ Features

- **Prompt Optimizer MCP server** for `prompt + summary → best prompt pack`
- Exposes MCP tools:
  - `best_prompt(prompt, summary, allow_quick_opt=true)` → returns the best available prompt pack (library first; optional quick optimize)
  - `optimize(prompt, summary, n_new=12, iterations=2, ...)` → force a short tournament and return the winner + mini leaderboard
  - `health()` → server status & library counts
- **Elo-based A/B** judging pipeline (pairwise judge, confidence-weighted Elo updates)
- **Checkpointed** evolution (variants + leaderboards on disk)
- Configurable knobs: population size, iterations, pairings, survivors, temperature, etc.
- Ready for integration with MCP-compatible clients (Claude VSCode / Cline)

## Folder Layout

- `_prompt_factory.py` – generates **prompt packs** (meta-system prompt → variants)
- `_optimizer.py` – Elo tournament, judge calls, mutation, shortlist, logging
- `mcp_prompt_opt/mcp_server.py` – MCP server entrypoint (FastMCP) exposing tools
- `variants.json` – seed library
- `opt_logs/` – iteration logs & `leaderboard_iter_*.json` / `leaderboard_final.json`
- `requirements.txt` – Python dependencies
- `README.md` – this file

> Adjust names/paths if your modules differ — these are aligned with the code you shared.

## Requirements
- Python 3.10+
- `uv`
- API key for your chosen model provider (e.g., OpenAI)

## Quickstart (Local)
1) Create & activate a virtual env:
```bash
uv init
source .venv/bin/activate
# or: uv venv && source .venv/bin/activate
```

2) Install deps:
```bash
uv add -r requirements.txt
```

3) Set environment:
```bash
export OPENAI_API_KEY=sk-...
export MODEL_NAME=gpt-4o-mini
# Optional:
export PROMPT_LIBRARY=variants.json
export PROMPT_LEADERBOARD=opt_logs/leaderboard_final.json
```

4) Run the MCP server:
```bash
uv run python -m mcp_server
```

This starts the server over stdio for MCP clients.

## 🧰 MCP Tools

### `best_prompt`
Fast path: pick a winning prompt pack from your leaderboard/library. If `allow_quick_opt=true` and no confident champ exists, it will run a **tiny optimization pass** (generate a few challengers, 1–2 iterations) and return the winner.

**Signature**
```
best_prompt(prompt: string, summary: string, allow_quick_opt: bool = true)
→ { "prompt_pack": { ... }, "note": "selected_from_library|quick_optimized|selected_from_library_low_confidence" }
```

**Example input**
```json
{
  "prompt": "Make a witty short about elevator small talk.",
  "summary": "People feel awkward; ~30s; silence vs forced chat; doors ding; everyone stares ahead."
}
```

**Example output (truncated)**
```json
{
  "prompt_pack": {
    "prompt_id": "pp-8d3a9c",
    "style": "satirical",
    "structure": "Setup→Turn→Tag",
    "devices": ["Irony", "Analogy"],
    "writer_system": "...meta-system here...",
    "writer_user_template": "PROMPT: {{prompt}}\nSUMMARY: {{summary}}\nTASK: ...",
    "decode_prefs": {"temperature": 0.6, "top_p": 0.9},
    "elo": 1127.4,
    "wins": 28,
    "losses": 13
  },
  "note": "selected_from_library"
}
```

### `optimize`
Force a short optimization (generate `n_new` challengers and run a compact tournament). Returns the **best** prompt pack plus a **top-10 leaderboard**.

**Signature**
```
optimize(prompt: string, summary: string, n_new = 12, iterations = 2, samples_per_input = 2, pairings = 1)
→ { "best": { ...prompt_pack... }, "leaderboard_top10": [ { prompt_id, elo, wins, losses }, ... ] }
```

### `health`
Basic service & library stats.

```
health() → { "name": "mcp-prompt-opt", "library_prompts": 24, "status": "ok" }
```

## Environment Variables

Core:
- `OPENAI_API_KEY` – OpenAI key
- `MODEL_NAME` – e.g., `gpt-4o-mini`

Library & logs:
- `PROMPT_LIBRARY` – path to variants file (default: `variants.json`)
- `PROMPT_LEADERBOARD` – path to leaderboard file (default: `opt_logs/leaderboard_final.json`)

Quick optimize knobs (server defaults used if unset):
- `FAST_ITERATIONS` (default: `1`)
- `FAST_SAMPLES_PER_INPUT` (default: `2`)
- `FAST_PAIRINGS` (default: `1`)
- `FAST_SURVIVORS` (default: `8`)
- `FAST_MUTANTS_PER_SURVIVOR` (default: `1`)


```json
{
  "mcpServers": {
    "mcp-prompt-opt": {
      "command": "python",
      "args": ["-m", "mcp_prompt_opt.server"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "MODEL_NAME": "gpt-4o-mini",
        "PROMPT_LIBRARY": "variants.json",
        "PROMPT_LEADERBOARD": "opt_logs/leaderboard_final.json",
        "FAST_ITERATIONS": "1",
        "FAST_SAMPLES_PER_INPUT": "2",
        "FAST_PAIRINGS": "1"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

After saving, your MCP client should launch the server and list the tools.

## Usage Flow

1) **Seed your library**  
    Generate variants once:
    ```bash
    python -m prompt_factory > variants.json
    ```
    Or run your overnight optimizer to produce `opt_logs/leaderboard_final.json`.

2) **Serve prompts via MCP**  
   - Call `best_prompt(prompt, summary)` to get a ready **prompt pack** instantly.
   - If the note returns **low confidence**, allow `quick_opt` or call `optimize(...)`.

3) **Periodically refresh**  
   Rerun your optimizer (longer iterations) to improve the leaderboard. The MCP server will automatically use the latest leaderboard/library on disk.

## Docker

A simple Dockerfile can run the MCP server over stdio:

```bash
docker build -t mcp-prompt-opt .
docker run --rm   -e OPENAI_API_KEY=sk-...   -e MODEL_NAME=gpt-4o-mini   -e PROMPT_LIBRARY=/app/variants.json   -e PROMPT_LEADERBOARD=/app/opt_logs/leaderboard_final.json   mcp-prompt-opt
```

Integrate with an MCP client that can spawn containers or forward stdio.

## Local Programmatic Use

If you want to drive the optimizer without MCP:

```python
from _prompt_factory import ask_prompt_generator, Request
from _optimizer import PromptPack, InputItem, tournament

# generate candidates
packs_raw = await ask_prompt_generator(Request(
    prompt="Make a witty short about elevator small talk.",
    summary="People feel awkward; ~30s; silence vs forced chat; doors ding; everyone stares ahead."
), n=12)

packs = [PromptPack(**p) for p in packs_raw]
inputs = [InputItem(prompt="...", summary="..."), ...]

final = await tournament(
    packs=packs,
    inputs=inputs,
    iterations=2,
    samples_per_input=2,
    pairings=1,
    survivors=8,
    mutants_per_survivor=1,
    logdir="opt_logs",
)

best = final[0]
print(best.prompt_id, best.elo)
```

## Safety & Evaluation Notes

- Judge rubric emphasizes **humor insight & originality**, **execution & craft**, **safety**, and **fidelity**.
- Elo updates are **confidence-weighted**; multiple inputs reduce noise.
- Library-first selection avoids unnecessary spend; quick optimize only when needed.

## Troubleshooting

- **No prompts found**: ensure `variants.json` or `opt_logs/leaderboard_final.json` exists and is readable.
- **429/limits**: lower concurrency/pairings and/or add exponential backoff in API call layer.
- **Model errors**: verify `OPENAI_API_KEY` and `MODEL_NAME`.
- **MCP not connecting**: confirm `command`, `args`, and env vars in your MCP settings; ensure venv Python matches installed packages.