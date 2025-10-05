import { useEffect, useState } from "react";
import { synthesizeAudio } from "../api/audio";
import PanelShell from "./ui/PanelShell";
import { Volume2, Waves } from "lucide-react";

export default function AudioPanel({
  text,
  audioUrl,
  setAudioUrl,
}: {
  text: string;
  audioUrl: string;
  setAudioUrl: (u: string) => void;
}) {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // reset audio when text changes
    setAudioUrl("");
  }, [text, setAudioUrl]);

  const handleGenerate = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const url = await synthesizeAudio(text);
      setAudioUrl(url);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PanelShell accent="emerald">
      <div className="flex flex-col gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-500/15 text-emerald-600 dark:text-emerald-300">
              <Volume2 className="size-5" />
            </span>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-emerald-500/80">
                Voice Forge
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Audio Studio
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Turn your comedic script into a natural-sounding voiceover ready
                to deploy.
              </p>
            </div>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-200">
            <Waves className="size-3.5" />
            GCP + Polly available
          </span>
        </header>

        <button
          type="button"
          onClick={handleGenerate}
          disabled={!text || loading}
          className="inline-flex w-fit items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 via-emerald-600 to-emerald-500 px-5 py-2.5 text-sm font-semibold text-white shadow-[0_14px_34px_-20px_rgba(16,185,129,0.9)] transition hover:shadow-[0_22px_42px_-18px_rgba(16,185,129,0.85)] disabled:cursor-not-allowed disabled:opacity-55"
        >
          {loading ? (
            <>
              <Waves className="size-4 animate-spin" />
              Synthesizing…
            </>
          ) : (
            <>
              <Volume2 className="size-4" />
              Generate audio
            </>
          )}
        </button>

        {audioUrl ? (
          <div className="rounded-2xl border border-emerald-400/30 bg-white/80 p-6 shadow-sm dark:border-emerald-500/20 dark:bg-slate-900/50">
            <audio controls src={audioUrl} className="w-full" />
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-emerald-400/40 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-emerald-500/30 dark:bg-slate-900/30 dark:text-slate-400">
            No audio yet. Produce a comedic script first, then synthesize a
            voiceover in seconds.
          </div>
        )}
      </div>
    </PanelShell>
  );
}
