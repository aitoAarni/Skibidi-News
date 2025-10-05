export const API_BASES = {
  news:
    import.meta.env.VITE_NEWS_API_BASE || "http://localhost:8000/mcp-news-aggr",
  humor:
    import.meta.env.VITE_HUMOR_API_BASE ||
    "http://localhost:8001/mcp-humorizer",
  audio:
    import.meta.env.VITE_AUDIO_API_BASE ||
    "http://localhost:8002/text-to-audio",
  prompt:
    import.meta.env.VITE_PROMPT_API_BASE ||
    "http://localhost:8003/mcp-prompt-opt",
  router: import.meta.env.VITE_ROUTER_API_BASE || "http://localhost:8010",
};

export const endpoints = {
  aggregateNews: `${API_BASES.news}/aggregate_news`,
  comedicize: `${API_BASES.humor}/comedicize`,
  synthesize: `${API_BASES.audio}/synthesize`,
  bestPrompt: `${API_BASES.prompt}/best_prompt`,
};
