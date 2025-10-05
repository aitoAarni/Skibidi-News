import { motion, type MotionProps } from "framer-motion";
import clsx from "clsx";
import type { PropsWithChildren } from "react";

type Accent = "indigo" | "pink" | "emerald" | "violet" | "sky";

type PanelShellProps = PropsWithChildren<{
  accent?: Accent;
  className?: string;
}> &
  MotionProps;

const accentStyles: Record<Accent, string> = {
  indigo:
    "before:from-indigo-400/70 before:via-indigo-400/20 before:to-transparent after:bg-indigo-500/15",
  pink: "before:from-pink-400/70 before:via-pink-400/20 before:to-transparent after:bg-pink-500/15",
  emerald:
    "before:from-emerald-400/70 before:via-emerald-400/20 before:to-transparent after:bg-emerald-500/15",
  violet:
    "before:from-violet-400/70 before:via-violet-400/20 before:to-transparent after:bg-violet-500/15",
  sky: "before:from-sky-400/70 before:via-sky-400/20 before:to-transparent after:bg-sky-500/15",
};

export default function PanelShell({
  accent = "indigo",
  className,
  children,
  ...motionProps
}: PanelShellProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      className={clsx(
        "relative overflow-hidden rounded-3xl border border-slate-200/70 dark:border-slate-800/70 bg-white/80 dark:bg-slate-950/75 shadow-[0_18px_40px_-24px_rgba(15,23,42,0.55)] backdrop-blur",
        "before:pointer-events-none before:absolute before:inset-x-8 before:-top-px before:h-px before:bg-gradient-to-r before:opacity-80",
        "after:pointer-events-none after:absolute after:-top-24 after:-right-16 after:h-56 after:w-56 after:rounded-full after:blur-3xl after:opacity-65",
        accentStyles[accent],
        className
      )}
      {...motionProps}
    >
      <div className="relative z-10 px-6 py-7 sm:px-8 sm:py-8">{children}</div>
      <div className="pointer-events-none absolute inset-0 mix-blend-soft-light dark:mix-blend-lighten">
        <div className="absolute inset-x-10 bottom-0 h-24 bg-gradient-to-t from-slate-100/50 dark:from-slate-900/40 to-transparent" />
      </div>
    </motion.div>
  );
}
