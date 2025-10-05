import { useCallback } from "react";
import { ArrowRight, Cpu, Radio } from "lucide-react";
import ThemeToggle from "./ThemeToggle.tsx";

const navLinks = [
  { href: "#overview", label: "Overview" },
  { href: "#news", label: "News Engine" },
  { href: "#humor", label: "Humorizer" },
  { href: "#audio", label: "Audio Studio" },
  { href: "#prompt", label: "Prompt Lab" },
];

export default function Header() {
  const handleScrollTop = useCallback(() => {
    if (typeof window === "undefined") return;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <header className="sticky top-0 z-30 w-full border-b border-slate-200/70 bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:border-slate-800/70 dark:bg-slate-950/60 supports-[backdrop-filter]:dark:bg-slate-950/40">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-indigo-400/40 to-transparent" />
      <div className="relative mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-fuchsia-500 text-white shadow-lg">
            <Cpu className="size-5" />
          </div>
          <div className="space-y-1">
            <h1 className="text-base font-semibold tracking-tight text-slate-900 dark:text-white sm:text-lg">
              Skibidi News Control Center
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 sm:text-sm">
              Aggregate, punch up, and voice your daily headlines in one pass.
            </p>
          </div>
        </div>

        <nav className="hidden items-center gap-2 rounded-full border border-slate-200/70 bg-white/70 px-2 py-1 text-xs font-medium text-slate-500 shadow-sm backdrop-blur md:flex dark:border-slate-800/70 dark:bg-slate-950/50 dark:text-slate-300">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="rounded-full px-3 py-1.5 transition hover:bg-indigo-500/10 hover:text-indigo-500 dark:hover:bg-indigo-500/15 dark:hover:text-indigo-200"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <span className="hidden items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-[11px] font-medium text-emerald-600 md:inline-flex dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-200">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400/70" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
            </span>
            MCP cluster healthy
          </span>
          <button
            type="button"
            onClick={handleScrollTop}
            className="inline-flex items-center gap-2 rounded-full border border-slate-200/70 bg-white/80 px-3 py-2 text-xs font-semibold text-slate-700 shadow-sm transition hover:border-indigo-300 hover:bg-indigo-50/80 hover:text-indigo-500 dark:border-slate-700/70 dark:bg-slate-900/50 dark:text-slate-200 dark:hover:border-indigo-500/50 dark:hover:bg-slate-900/70"
          >
            <Radio className="size-3.5" />
            Sync all
            <ArrowRight className="size-3.5" />
          </button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
