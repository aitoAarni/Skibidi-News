# MCP Server – Summarized Text → Comedic Text (Python)

This repository contains a Python MCP server that receives summarized news text and transforms it into comedic text, preserving meaning while injecting punchy humor suited for short-form content. It’s the Humor Engine for Skibidi News.

- Pluggable LLM backends (OpenAI, Anthropic) via environment configuration
- Safe, deterministic offline fallback humorizer (no API key required)
- Exposes MCP tools over stdio using the Python `mcp` package (FastMCP)

## Features

- Input: summarized text
- Processing: humor prompt templates + strategies (style configurable)
- Output: comedic text, short and platform-ready
- Production-ready knobs: model, temperature, max tokens, timeout, seed, humor style
- Minimal, deterministic fallback when no model provider is configured

## Folder Layout

- `__init__.py` – package metadata/exports
- `config.py` – env-driven settings and system prompt builder
- `engine.py` – provider selection and generation flow (OpenAI, Anthropic, fallback)
- `humor.py` – deterministic humorizer used for offline fallback
- `mcp_server.py` – MCP server entrypoint (FastMCP) exposing tools over stdio
- `requirements.txt` – Python dependencies
- `README.md` – this file
- `mcp-humorizer.md` – architecture/contract document (to be added)

## Requirements

- Python 3.10+
- pip
- (Optional) API key for selected model provider

## Quickstart (Local)

1) Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:
```bash
pip install -r mcp_humorizer/requirements.txt
```

3) (Optional) Copy and update environment variables:
```bash
cp mcp_humorizer/.env.example mcp_humorizer/.env
# edit .env with your preferred MODEL_PROVIDER, API_KEY, HUMOR_STYLE, etc.
```
Stdio servers run as local subprocesses and communicate via standard input/output streams. These are typically used for local tools.


4) Run the MCP server (stdio):
```bash
python -m mcp_humorizer.mcp_server
```

The process will wait on stdio for MCP clients. You can integrate it with compatible clients (e.g., Cline/Claude VSCode extension) via MCP settings (see below).

## Environment Variables

- `MODEL_PROVIDER`: one of `openai`, `anthropic`, `none` (default: `none`)
- `API_KEY`: generic API key (falls back to `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`)
- `OPENAI_API_KEY`: provider-specific key (optional)
- `ANTHROPIC_API_KEY`: provider-specific key (optional)
- `HUMOR_STYLE`: one of `sarcastic|light|absurd|deadpan|wholesome|satirical|roast|random` (default: `light`)
- `MODEL_NAME`: override the backend model (e.g., `gpt-4o-mini`, `claude-3-5-sonnet-latest`)
- `HTTP_TIMEOUT`: HTTP timeout seconds (default: `30`)
- `MAX_OUTPUT_TOKENS`: upper bound on output tokens (default: `400`)
- `TEMPERATURE`: sampling temperature (default: `0.7`)
- `SEED`: optional deterministic seed if supported (default: unset)

A ready-to-edit `.env.example` is provided in this folder.

## MCP Tools

The server exposes two tools:

- `comedicize(id: string, summarized_text: string) -> { id, comedic_text }`
- `health() -> { name, provider, humor_style, status }`

### API Contract

Input:
```json
{
  "id": "uuid",
  "summarized_text": "The economy shrank by 2% last quarter."
}
```

Output:
```json
{
  "id": "uuid",
  "comedic_text": "The economy shrank by 2%. Don’t worry, my diet is shrinking faster!"
}
```

## Configure in Cline (VSCode) MCP Settings

Add a server entry to your MCP settings file:
`/home/duha/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Example:
```json
{
  "mcpServers": {
    "mcp-humorizer": {
      "command": "python",
      "args": ["-m", "mcp_humorizer.mcp_server"],
      "env": {
        "MODEL_PROVIDER": "none",
        "HUMOR_STYLE": "light",
        "MAX_OUTPUT_TOKENS": "400",
        "TEMPERATURE": "0.7"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

- If using OpenAI:
```json
"env": {
  "MODEL_PROVIDER": "openai",
  "API_KEY": "sk-...",
  "MODEL_NAME": "gpt-4o-mini",
  "HUMOR_STYLE": "satirical"
}
```

- If using Anthropic:
```json
"env": {
  "MODEL_PROVIDER": "anthropic",
  "API_KEY": "anthropic_api_key",
  "MODEL_NAME": "claude-3-5-sonnet-latest",
  "HUMOR_STYLE": "light"
}
```

After saving, the MCP client should launch the server and list its tools. If it shows “not connected”, double-check the `args` path/module and Python environment.

## Docker

A `Dockerfile` is provided in this folder. Build and run:

```bash
docker build -f mcp_humorizer/Dockerfile -t mcp-comedy mcp_humorizer
docker run --rm -e MODEL_PROVIDER=none mcp-comedy
```

For OpenAI:
```bash
docker run --rm \
  -e MODEL_PROVIDER=openai \
  -e API_KEY=sk-... \
  -e MODEL_NAME=gpt-4o-mini \
  -e HUMOR_STYLE=satirical \
  mcp-comedy
```

Note: The container runs the MCP server over stdio; integrate with a client that supports spawning containers or redirect stdio as needed.

## Local Programmatic Use

You can import and use the engine directly:
```python
from mcp_humorizer import Settings, comedicize_text

settings = Settings.from_env()
text = comedicize_text("The economy shrank by 2% last quarter.", settings)
print(text)
```

## Safety and Content Notes

- The humorizer avoids slurs, targeted harassment, or fabrications.
- Keep output aligned with the summarized facts.
- Use `HUMOR_STYLE` to tune tone; `random` will pick a style deterministically.

## Troubleshooting

- If OpenAI/Anthropic calls fail or keys are missing, the engine falls back to the deterministic humorizer.
- Ensure your Python environment is using the correct interpreter with required packages installed.
- For MCP client configuration, verify the `command`, `args`, and environment values.

## License

Proprietary or per-repo default. Replace with your license of choice if needed.
