/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_NEWS_API_BASE?: string;
  readonly VITE_HUMOR_API_BASE?: string;
  readonly VITE_AUDIO_API_BASE?: string;
  readonly VITE_PROMPT_API_BASE?: string;
  readonly VITE_ROUTER_API_BASE?: string;
  // other env vars...
  readonly [key: string]: string | undefined;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
