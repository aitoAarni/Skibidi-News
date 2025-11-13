import { useMemo, useState } from "react";
import { Clapperboard, Server, Sparkles } from "lucide-react";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import NewsPanel from "../components/NewsPanel";
import HumorPanel from "../components/HumorPanel";
import AudioPanel from "../components/AudioPanel";
import PromptLab from "../components/PromptLab";
import YoutubePanel from "../components/YoutubePanel";

export default function Dashboard() {
  const [summary, setSummary] = useState("");
  const [humor, setHumor] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [youtubeAuthToken, setYoutubeAuthToken] = useState("");

  const overviewCards = useMemo(
    () => [
      {
        id: "sources",
        label: "Live news sources",
        value: "6 feeds",
        detail: "BBC · CNN · Bloomberg · Forbes · Google · YLE",
        icon: Server,
        accent: "from-sky-500/80 via-indigo-500/70 to-sky-400/60",
      },
      {
        id: "humor",
        label: "Humor engine",
        value: summary ? "Ready to riff" : "Awaiting summary",
        detail: summary
          ? "Summary loaded — punch it up next"
          : "Generate a news digest to unlock jokes",
        icon: Sparkles,
        accent: "from-pink-500/85 via-fuchsia-500/70 to-rose-400/60",
      },
      {
        id: "audio",
        label: "Studio pipeline",
        value: audioUrl
          ? "Video ready"
          : humor
          ? "Narration in queue"
          : "Needs comedic script",
        detail: audioUrl
          ? "Preview the generated clip below"
          : humor
          ? "Generate transcript & video from the joke"
          : "Create a comedic remix to synthesize media",
        icon: Clapperboard,
        accent: "from-emerald-500/80 via-teal-500/70 to-emerald-400/60",
      },
    ],
    [summary, humor, audioUrl]
  );

  return (
    <div className="flex min-h-screen bg-slate-100/60 dark:bg-slate-950">
      <Sidebar
        summaryReady={Boolean(summary)}
        humorReady={Boolean(humor)}
        mediaReady={Boolean(audioUrl)}
      />
      <main className="relative flex min-h-screen flex-1 flex-col overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,rgba(129,140,248,0.18),transparent_55%)] dark:bg-[radial-gradient(circle_at_top,rgba(14,116,144,0.35),transparent_60%)]" />
        <Header />
        <section className="relative flex-1 overflow-y-auto pb-10">
          <div className="px-4 py-8 sm:px-6 lg:px-8">
            <div className="mx-auto flex w-full max-w-7xl flex-col gap-8">
              <section
                id="overview"
                className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3"
              >
                {overviewCards.map((card) => {
                  const Icon = card.icon;
                  return (
                    <article
                      key={card.id}
                      className="relative overflow-hidden rounded-3xl border border-slate-200/70 bg-white/80 p-6 shadow-[0_18px_45px_-28px_rgba(15,23,42,0.55)] backdrop-blur dark:border-slate-800/70 dark:bg-slate-950/70"
                    >
                      <div
                        className={`pointer-events-none absolute inset-0 bg-gradient-to-br ${card.accent} opacity-25`}
                      />
                      <div className="relative flex items-start justify-between gap-4">
                        <div className="flex flex-col gap-2">
                          <span className="text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">
                            {card.label}
                          </span>
                          <span className="text-2xl font-semibold text-slate-900 dark:text-white">
                            {card.value}
                          </span>
                          <span className="text-sm text-slate-500 dark:text-slate-400">
                            {card.detail}
                          </span>
                        </div>
                        <span className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-white/80 text-indigo-500 shadow-sm dark:bg-slate-900/80">
                          <Icon className="size-5" />
                        </span>
                      </div>
                    </article>
                  );
                })}
              </section>

              <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.1fr_0.9fr]">
                <div id="news" className="h-full">
                  <NewsPanel
                    summary={summary}
                    setSummary={setSummary}
                    onClear={() => {
                      setSummary("");
                      setHumor("");
                      setAudioUrl("");
                    }}
                  />
                </div>
                <div id="humor" className="h-full">
                  <HumorPanel
                    summary={summary}
                    humor={humor}
                    setHumor={setHumor}
                  />
                </div>
              </section>

              <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
                <div id="audio" className="h-full xl:order-1">
                  <AudioPanel
                    text={humor}
                    audioUrl={audioUrl}
                    setAudioUrl={setAudioUrl}
                  />
                </div>
                <div id="prompt" className="h-full xl:order-2">
                  <PromptLab summary={summary} humor={humor} />
                </div>
                <div id="youtube" className="h-full">
                  <YoutubePanel
                    token={youtubeAuthToken}
                    setToken={setYoutubeAuthToken}
                  />
                </div>
              </section>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
