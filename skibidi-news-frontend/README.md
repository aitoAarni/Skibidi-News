# Skibidi News Frontend

Polished control center for the MCP microservices: fetch news, make it funny, and synthesize audio. Built with React + Vite + Tailwind + Framer Motion.

## Quick start

1. Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

2. Configure API bases (optional; defaults assume services on localhost)

### Env variables

Create `.env` in this folder (or export via shell) to override defaults:

```
VITE_NEWS_API_BASE=http://localhost:8000/mcp-news-aggr
VITE_HUMOR_API_BASE=http://localhost:8001/mcp-humorizer
VITE_AUDIO_API_BASE=http://localhost:8002/text-to-audio
VITE_PROMPT_API_BASE=http://localhost:8003/mcp-prompt-opt
VITE_ROUTER_API_BASE=http://localhost:8010
```

### Scripts

- dev: start vite dev server
- build: production build
- preview: preview production build

### Styling

- Tailwind layers are imported in `src/index.css`; global tweaks can live below the imports.
- Extend the design system via `tailwind.config.js` (`container` defaults are already centralized).

### UX flow

- Panels share state from the dashboard: News → Humor → Audio.
- Prompt Lab lets you query the prompt optimizer’s best pack for a given (prompt, summary).
