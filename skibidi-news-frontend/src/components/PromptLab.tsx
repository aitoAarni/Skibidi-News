import { useCallback, useEffect, useMemo, useState } from "react";
import { BrainCircuit, PenLine, Sparkles, SquarePen, Zap } from "lucide-react";
import { fetchBestPrompt, type BestPromptResponse } from "../api/prompt";
import PanelShell from "./ui/PanelShell";

type PromptLabProps = {
  summary: string;
  humor: string;
};

export default function PromptLab({ summary, humor }: PromptLabProps) {
  const [prompt, setPrompt] = useState("Caption about today's top headline");
  const [summaryDraft, setSummaryDraft] = useState(summary);
  const [summaryDirty, setSummaryDirty] = useState(false);
  const [resp, setResp] = useState<BestPromptResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [autoOptimize, setAutoOptimize] = useState(false);

  useEffect(() => {
    if (!summaryDirty) {
      setSummaryDraft(summary);
    }
  }, [summary, summaryDirty]);

  const runOptimization = useCallback(async () => {
    setLoading(true);
    try {
      const r = await fetchBestPrompt(prompt, summaryDraft, true);
      setResp(r);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to contact prompt optimizer";
      setResp({ error: message });
    } finally {
      setLoading(false);
    }
  }, [prompt, summaryDraft]);

  useEffect(() => {
    if (autoOptimize && summaryDraft.trim().length > 0) {
      void runOptimization();
    }
  }, [summaryDraft, autoOptimize, runOptimization]);

  const canOptimize = useMemo(
    () => summaryDraft.trim().length > 0 && !loading,
    [summaryDraft, loading]
  );

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
              value={summaryDraft}
              onChange={(e) => {
                setSummaryDirty(true);
                setSummaryDraft(e.target.value);
              }}
              className="h-28 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 py-3 text-sm text-slate-900 shadow-sm transition focus:border-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:border-slate-700/70 dark:bg-slate-900/60 dark:text-slate-100"
              placeholder="Paste or craft the news summary you want optimized"
            />
          </label>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={runOptimization}
            disabled={!canOptimize}
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
          <button
            type="button"
            onClick={() => {
              setSummaryDirty(false);
              setSummaryDraft(summary);
            }}
            disabled={!summary.length}
            className="inline-flex items-center gap-2 rounded-xl border border-violet-300/60 bg-white/60 px-4 py-2.5 text-sm font-semibold text-violet-600 shadow-sm transition hover:border-violet-400 hover:bg-violet-50/80 dark:border-violet-500/40 dark:bg-violet-500/15 dark:text-violet-200 disabled:cursor-not-allowed disabled:opacity-55"
          >
            <PenLine className="size-4" />
            Use summary
          </button>
          <button
            type="button"
            onClick={() => {
              setSummaryDirty(true);
              setSummaryDraft(humor);
            }}
            disabled={!humor.length}
            className="inline-flex items-center gap-2 rounded-xl border border-violet-300/60 bg-white/60 px-4 py-2.5 text-sm font-semibold text-violet-600 shadow-sm transition hover:border-violet-400 hover:bg-violet-50/80 dark:border-violet-500/40 dark:bg-violet-500/15 dark:text-violet-200 disabled:cursor-not-allowed disabled:opacity-55"
          >
            <Sparkles className="size-4" />
            Use comedic script
          </button>
          <span className="inline-flex items-center gap-2 rounded-xl border border-slate-200/70 bg-white/70 px-4 py-2 text-xs font-medium text-slate-500 dark:border-slate-800/60 dark:bg-slate-950/40 dark:text-slate-300">
            MCP Prompt Optimizer v2
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => setAutoOptimize((prev) => !prev)}
            className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-xs font-semibold transition ${
              autoOptimize
                ? "border-emerald-400/70 bg-emerald-500/15 text-emerald-600 dark:border-emerald-500/50 dark:bg-emerald-500/20 dark:text-emerald-200"
                : "border-slate-200/70 bg-white/70 text-slate-500 hover:border-emerald-200/60 hover:bg-emerald-50/80 dark:border-slate-700/60 dark:bg-slate-900/40 dark:text-slate-300 dark:hover:border-emerald-400/40 dark:hover:bg-emerald-500/10"
            }`}
          >
            <Zap className="size-3.5" />
            Auto-optimize on summary updates
          </button>
          {autoOptimize && (
            <span className="text-xs text-emerald-600 dark:text-emerald-300">
              Runs whenever the pipeline produces a new summary.
            </span>
          )}
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
