import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

function getInitialTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  const stored = localStorage.getItem("theme");
  if (stored === "light" || stored === "dark") return stored;
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  return prefersDark ? "dark" : "light";
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark">(getInitialTheme());

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <button
      type="button"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="inline-flex items-center gap-2 rounded-lg border border-slate-200/60 dark:border-slate-700/60 bg-white/70 dark:bg-slate-900/60 px-3 py-2 text-slate-700 dark:text-slate-200 hover:bg-slate-50 hover:dark:bg-slate-900 transition"
      aria-label="Toggle theme"
      title="Toggle theme"
    >
      {theme === "dark" ? (
        <>
          <Sun className="size-4" />
          <span className="text-xs">Light</span>
        </>
      ) : (
        <>
          <Moon className="size-4" />
          <span className="text-xs">Dark</span>
        </>
      )}
    </button>
  );
}
