import { useEffect, useRef, useState } from "react";
import { Loader, User2Icon, Video } from "lucide-react";
import PanelShell from "./ui/PanelShell";
import { authenticateYouTube } from "../api/socials/youtube";

type YoutubePanelProps = {
  token: string;
  setToken: (token: string) => void;
};
export default function YoutubePanel({ token, setToken }: YoutubePanelProps) {
  const [loading, setLoading] = useState(false);
  const passInput = useRef<HTMLInputElement | null>(null);
  const [copied, setCopied] = useState(false);

  const handleAuth = async () => {
    setLoading(true);
    try {
      const result = await authenticateYouTube();
      setToken(result);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (passInput && passInput.current) {
      passInput.current.value = token;
    }
  }, [token]);

  return (
    <PanelShell accent="red">
      <div className="flex flex-col gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-red-500/15 text-red-500">
              <Video className="size-5" />
            </span>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-red-500/80">
                YouTube Authentication
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Authenticate your YouTube account
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Authenticate your Google account to enable video uploads to
                YouTube.
              </p>
            </div>
          </div>
        </header>

        <button
          type="button"
          onClick={handleAuth}
          disabled={loading}
          className="inline-flex w-fit items-center gap-2 rounded-xl bg-gradient-to-r from-pink-500 via-fuchsia-500 to-pink-500 px-5 py-2.5 text-sm font-semibold text-white shadow-[0_14px_32px_-22px_rgba(236,72,153,0.9)] transition hover:shadow-[0_22px_40px_-20px_rgba(236,72,153,0.85)] disabled:cursor-not-allowed disabled:opacity-55"
        >
          {loading ? (
            <>
              <Loader className="size-4 animate-spin" />
              Authenticating...
            </>
          ) : (
            <>
              <User2Icon className="size-4" />
              Get authenticated
            </>
          )}
        </button>
        <label>Auth Token:</label>
        <input ref={passInput} id="auth-token" type="password" />
        <button
          type="button"
          onClick={async () => {
            await navigator.clipboard.writeText(token);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          }}
        >
          {copied ? "Copied!" : "Copy to clipboard "}
        </button>
      </div>
    </PanelShell>
  );
}
