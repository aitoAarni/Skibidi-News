export const API_BASES = {
  router: import.meta.env.VITE_ROUTER_API_BASE || "http://127.0.0.1:8000",
};

export const endpoints = {
  aggregateNews: `${API_BASES.router}/news`,
  comedicize: `${API_BASES.router}/humorize_news`,
  transcript: `${API_BASES.router}/transcript`,
  studioGenerate: `${API_BASES.router}/studio/generate`,
  studioVideo: (videoId: string) => `${API_BASES.router}/videos/${videoId}`,
  bestPrompt: `${API_BASES.router}/prompt/best`,
  youtubePublish: `${API_BASES.router}/youtube/publish`,
};
