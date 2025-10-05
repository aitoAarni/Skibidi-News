import { useState } from "react";
import { BrainCircuit, SquarePen } from "lucide-react";
import { fetchBestPrompt, type BestPromptResponse } from "../api/prompt";
import PanelShell from "./ui/PanelShell";

export default function PromptLab() {
  const [prompt, setPrompt] = useState("Caption about today's top headline");
  const [summary, setSummary] = useState("");
  const [resp, setResp] = useState<BestPromptResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const onRun = async () => {
    setLoading(true);
    try {
      const r = await fetchBestPrompt(prompt, summary, true);
      setResp(r);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PanelShell accent="violet">
      <div className="flex flex-col gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-violet-500/15 text-violet-500">
              <BrainCircuit className="size-5" />
            </span>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-violet-500/80">
                Prompt Lab
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Optimize prompting on the fly
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Feed in the summary and we’ll surface the best-performing prompt
                template.
              </p>
            </div>
          </div>
          {resp?.note && (
            <span className="inline-flex items-center gap-2 rounded-full border border-violet-400/30 bg-violet-500/10 px-3 py-1 text-xs font-medium text-violet-500 dark:text-violet-200">
              {resp.note}
            </span>
          )}
        </header>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          <label className="flex flex-col gap-2">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
              Prompt seed
            </span>
            <div className="relative">
              <SquarePen className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-violet-400" />
              <input
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full rounded-xl border border-slate-200/70 bg-white/70 py-3 pl-10 pr-3 text-sm text-slate-900 shadow-sm transition focus:border-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:border-slate-700/70 dark:bg-slate-900/60 dark:text-slate-100"
                placeholder="e.g., Give me a witty caption about..."
              />
            </div>
          </label>
          <label className="flex flex-col gap-2">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
              Summary context
            </span>
            <textarea
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              className="h-28 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 py-3 text-sm text-slate-900 shadow-sm transition focus:border-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:border-slate-700/70 dark:bg-slate-900/60 dark:text-slate-100"
              placeholder="Paste or craft the news summary you want optimized"
            />
          </label>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={onRun}
            disabled={loading || !summary}
            className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 via-indigo-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-[0_14px_34px_-20px_rgba(139,92,246,0.9)] transition hover:shadow-[0_22px_42px_-18px_rgba(139,92,246,0.85)] disabled:cursor-not-allowed disabled:opacity-55"
          >
            {loading ? "Optimizing…" : "Get best prompt"}
          </button>
          <button
            type="button"
            onClick={() => setResp(null)}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200/70 bg-white/60 px-4 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-slate-300 hover:bg-slate-50/80 hover:text-slate-700 dark:border-slate-700/70 dark:bg-slate-900/40 dark:text-slate-200 dark:hover:border-slate-600 dark:hover:bg-slate-900/60"
          >
            Clear
          </button>
          <span className="inline-flex items-center gap-2 rounded-xl border border-slate-200/70 bg-white/70 px-4 py-2 text-xs font-medium text-slate-500 dark:border-slate-800/60 dark:bg-slate-950/40 dark:text-slate-300">
            MCP Prompt Optimizer v2
          </span>
        </div>

        {resp?.error && (
          <p className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-600 dark:border-rose-500/40 dark:bg-rose-500/15 dark:text-rose-200">
            {resp.error}
          </p>
        )}

        {resp?.prompt_pack && (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-200/70 bg-white/80 p-4 shadow-sm dark:border-slate-800/70 dark:bg-slate-900/50">
              <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                Writer System
              </h4>
              <pre className="mt-2 whitespace-pre-wrap text-sm text-slate-600 dark:text-slate-300">
                {resp.prompt_pack.writer_system}
              </pre>
            </div>
            <div className="rounded-2xl border border-slate-200/70 bg-white/80 p-4 shadow-sm dark:border-slate-800/70 dark:bg-slate-900/50">
              <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                User Template
              </h4>
              <pre className="mt-2 whitespace-pre-wrap text-sm text-slate-600 dark:text-slate-300">
                {resp.prompt_pack.writer_user_template}
              </pre>
            </div>
          </div>
        )}
      </div>
    </PanelShell>
  );
}
