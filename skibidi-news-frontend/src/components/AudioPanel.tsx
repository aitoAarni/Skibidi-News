import { useEffect, useState } from "react";
import { generateStudioAsset } from "../api/audio";
import PanelShell from "./ui/PanelShell";
import { Clapperboard, Film, Waves } from "lucide-react";

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
  const [transcript, setTranscript] = useState("");
  const [videoId, setVideoId] = useState("");

  useEffect(() => {
    // reset audio when text changes
    setAudioUrl("");
    setTranscript("");
    setVideoId("");
  }, [text, setAudioUrl]);

  const handleGenerate = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const result = await generateStudioAsset(text);
      setTranscript(result.transcript);
      setAudioUrl(result.video_url);
      setVideoId(result.video_id);
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
              <Film className="size-5" />
            </span>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-emerald-500/80">
                Studio Pipeline
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Video &amp; Voice Studio
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Turn your comedic script into a narrated transcript and short
                vertical video ready to share.
              </p>
            </div>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-200">
            <Waves className="size-3.5" />
            Polly narration + MCP video
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
              <Clapperboard className="size-4" />
              Generate video
            </>
          )}
        </button>

        {transcript ? (
          <div className="rounded-2xl border border-emerald-400/30 bg-white/80 p-6 text-sm shadow-sm dark:border-emerald-500/20 dark:bg-slate-900/50">
            <h4 className="mb-3 font-semibold text-emerald-600 dark:text-emerald-300">
              Transcript
            </h4>
            <p className="whitespace-pre-wrap text-slate-700 dark:text-slate-200">
              {transcript}
            </p>
          </div>
        ) : null}

        {audioUrl ? (
          <div className="rounded-3xl border border-emerald-400/30 bg-white/90 p-6 shadow-xl shadow-emerald-500/10 dark:border-emerald-500/30 dark:bg-slate-900/60">
            <div className="mx-auto w-full max-w-2xl">
              <div
                className="relative w-full overflow-hidden rounded-2xl border border-emerald-400/40 bg-slate-950/5 dark:bg-emerald-500/10"
                style={{ aspectRatio: "9 / 16" }}
              >
                <video
                  controls
                  src={audioUrl}
                  className="h-full w-full object-cover"
                />
              </div>
              <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-emerald-600/80 dark:text-emerald-200/80">
                {videoId ? (
                  <span className="font-semibold uppercase tracking-wider">
                    Video ID: {videoId}
                  </span>
                ) : (
                  <span />
                )}
                <a
                  href={audioUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-xl border border-emerald-400/40 px-3 py-1.5 font-semibold text-emerald-600 transition hover:border-emerald-500/60 hover:bg-emerald-500/10 dark:text-emerald-200"
                >
                  Open in new tab
                </a>
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-emerald-400/40 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-emerald-500/30 dark:bg-slate-900/30 dark:text-slate-400">
            No media yet. Produce a comedic script first, then synthesize the
            transcript and video in seconds.
          </div>
        )}
      </div>
    </PanelShell>
  );
}
