import { useState } from "react";
import { Laugh, Wand2 } from "lucide-react";
import PanelShell from "./ui/PanelShell";
import { humorizeText } from "../api/humor";

export default function HumorPanel({
  summary,
  humor,
  setHumor,
}: {
  summary: string;
  humor: string;
  setHumor: (h: string) => void;
}) {
  const [loading, setLoading] = useState(false);
  console.log(summary);
  const handleHumorize = async () => {
    if (!summary) return;
    setLoading(true);
    try {
      const h = await humorizeText(summary);

      setHumor(h);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PanelShell accent="pink">
      <div className="flex flex-col gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-pink-500/15 text-pink-500">
              <Laugh className="size-5" />
            </span>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-pink-500/80">
                Humor Reactor
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Comedic Remix
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Spin a playful take on the summary with the MCP Humorizer
                engine.
              </p>
            </div>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-pink-400/30 bg-pink-400/10 px-3 py-1 text-xs font-medium text-pink-500 dark:text-pink-200">
            Powered by improv heuristics
          </span>
        </header>

        <button
          type="button"
          onClick={handleHumorize}
          disabled={!summary || loading}
          className="inline-flex w-fit items-center gap-2 rounded-xl bg-gradient-to-r from-pink-500 via-fuchsia-500 to-pink-500 px-5 py-2.5 text-sm font-semibold text-white shadow-[0_14px_32px_-22px_rgba(236,72,153,0.9)] transition hover:shadow-[0_22px_40px_-20px_rgba(236,72,153,0.85)] disabled:cursor-not-allowed disabled:opacity-55"
        >
          {loading ? (
            <>
              <Wand2 className="size-4 animate-spin" />
              Punching it up…
            </>
          ) : (
            <>
              <Wand2 className="size-4" />
              Make it funny
            </>
          )}
        </button>

        {humor ? (
          <blockquote className="relative overflow-hidden rounded-2xl border border-pink-400/30 bg-white/80 p-6 text-sm italic leading-relaxed text-slate-800 shadow-sm dark:border-pink-500/20 dark:bg-slate-900/50 dark:text-slate-100">
            <span className="absolute -left-3 top-6 text-5xl font-serif text-pink-500/30">
              “
            </span>
            <p className="relative whitespace-pre-wrap pl-4">{humor}</p>
          </blockquote>
        ) : (
          <div className="rounded-2xl border border-dashed border-pink-400/40 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-pink-500/30 dark:bg-slate-900/30 dark:text-slate-400">
            Awaiting a summary. Generate news first, then unleash the comedic
            remix.
          </div>
        )}
      </div>
    </PanelShell>
  );
}
