import { Brain, Laugh, Newspaper, Volume2 } from "lucide-react";

const routes = [
  {
    href: "#news",
    label: "News Feed",
    icon: Newspaper,
    description: "Curated daily pulse",
  },
  {
    href: "#humor",
    label: "Comedic View",
    icon: Laugh,
    description: "Punch up summaries",
  },
  {
    href: "#prompt",
    label: "Prompt Lab",
    icon: Brain,
    description: "Optimize prompts",
  },
  {
    href: "#audio",
    label: "Audio Studio",
    icon: Volume2,
    description: "Voice your script",
  },
];

export default function Sidebar() {
  return (
    <aside className="sticky top-0 hidden h-screen w-72 flex-col border-r border-slate-200/70 bg-white/85 backdrop-blur-xl dark:border-slate-800/70 dark:bg-slate-950/70 md:flex">
      <div className="relative flex flex-col gap-3 px-6 py-6">
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-500/5 via-transparent to-purple-500/5" />
        <p className="text-xs font-semibold uppercase tracking-widest text-indigo-500/90">
          Control Room
        </p>
        <h1 className="text-xl font-semibold text-slate-900 dark:text-white">
          🧠 Skibidi Dashboard
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Keep tabs on every MCP service—news, humor, prompts, and narration—in
          one clean runbook.
        </p>
      </div>

      <nav className="flex-1 space-y-1 px-4">
        {routes.map((route) => {
          const Icon = route.icon;
          const isPrimary = route.href === "#news";
          return (
            <a
              key={route.href}
              href={route.href}
              className={`group mb-1 flex flex-col gap-1 rounded-2xl border border-transparent px-4 py-3 transition hover:border-indigo-300/60 hover:bg-indigo-500/10 dark:hover:border-indigo-400/40 dark:hover:bg-indigo-500/15 ${
                isPrimary
                  ? "border-indigo-300/60 bg-indigo-500/10 text-indigo-600 dark:border-indigo-400/50 dark:bg-indigo-500/15 dark:text-indigo-200"
                  : "text-slate-600 dark:text-slate-300"
              }`}
            >
              <div className="flex items-center gap-3 text-sm font-semibold">
                <span className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-white/80 text-indigo-500 shadow-sm transition group-hover:scale-105 dark:bg-slate-900/70">
                  <Icon className="size-4" />
                </span>
                {route.label}
              </div>
              <p className="pl-12 text-xs text-slate-500 transition group-hover:text-indigo-500 dark:text-slate-400 dark:group-hover:text-indigo-200">
                {route.description}
              </p>
            </a>
          );
        })}
      </nav>

      <div className="mt-auto border-t border-slate-200/70 px-6 py-5 text-xs text-slate-500 dark:border-slate-800/70 dark:text-slate-400">
        <p className="font-medium text-slate-600 dark:text-slate-300">
          Live MCP endpoints
        </p>
        <ul className="mt-2 space-y-1">
          <li className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" /> News
            aggregator
          </li>
          <li className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />{" "}
            Humorizer engine
          </li>
          <li className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" /> Prompt
            optimizer
          </li>
          <li className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />{" "}
            Text-to-voice
          </li>
        </ul>
      </div>
    </aside>
  );
}
