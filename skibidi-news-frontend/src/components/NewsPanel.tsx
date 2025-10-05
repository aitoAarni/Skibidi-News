import { useState } from "react";
import { RefreshCw, Sparkles, Trash2 } from "lucide-react";
import PanelShell from "./ui/PanelShell";
import { fetchNewsSummary } from "../api/news";

export default function NewsPanel({
  summary,
  setSummary,
  onClear,
}: {
  summary: string;
  setSummary: (s: string) => void;
  onClear?: () => void;
}) {
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    setLoading(true);
    try {
      const s = await fetchNewsSummary();
      setSummary(s);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PanelShell accent="indigo">
      <div className="flex flex-col gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-indigo-500/80">
              Aggregation Suite
            </p>
            <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
              Latest Summarized News
            </h3>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Pull a concise digest from every monitored outlet in a single tap.
            </p>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-500 dark:text-indigo-200">
            <span className="relative flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400/60" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-indigo-500" />
            </span>
            6 sources synced
          </span>
        </header>

        <div className="flex flex-wrap items-center gap-2 sm:gap-3">
          <button
            type="button"
            onClick={handleFetch}
            className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-[0_12px_30px_-15px_rgba(79,70,229,0.9)] transition hover:shadow-[0_18px_38px_-14px_rgba(79,70,229,0.8)]"
          >
            {loading ? (
              <>
                <RefreshCw className="size-4 animate-spin" />
                Fetching…
              </>
            ) : (
              <>
                <Sparkles className="size-4" />
                Fetch latest
              </>
            )}
          </button>
          <button
            type="button"
            onClick={() => {
              setSummary("");
              onClear?.();
            }}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200/70 bg-white/60 px-4 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-slate-300 hover:bg-slate-50/80 hover:text-slate-700 dark:border-slate-700/70 dark:bg-slate-900/40 dark:text-slate-200 dark:hover:border-slate-600 dark:hover:bg-slate-900/60"
          >
            <Trash2 className="size-4" />
            Clear
          </button>
          <span className="inline-flex items-center gap-2 rounded-xl border border-slate-200/70 bg-white/70 px-4 py-2 text-xs font-medium text-slate-500 dark:border-slate-800/60 dark:bg-slate-950/40 dark:text-slate-300">
            <RefreshCw className="size-3.5" />
            Refreshed live from MCP
          </span>
        </div>

        {summary ? (
          <div className="rounded-2xl border border-slate-200/70 bg-white/80 p-5 text-sm leading-relaxed text-slate-700 shadow-sm dark:border-slate-800/70 dark:bg-slate-900/60 dark:text-slate-200">
            <p className="whitespace-pre-wrap">{summary}</p>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300/80 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-slate-700/80 dark:bg-slate-900/30 dark:text-slate-400">
            No news summary yet. Tap{" "}
            <strong className="font-semibold text-indigo-500 dark:text-indigo-300">
              Fetch latest
            </strong>{" "}
            to aggregate fresh headlines across your configured feeds.
          </div>
        )}
      </div>
    </PanelShell>
  );
}
