import { useEffect, useState } from "react";
import { Loader, User2Icon, Video, Upload, CheckCircle } from "lucide-react";
import PanelShell from "./ui/PanelShell";
import { authenticateYouTube, uploadToYouTube } from "../api/socials/youtube";

type YoutubePanelProps = {
  token: string;
  setToken: (token: string) => void;
  videoId: string;
};
export default function YoutubePanel({
  token,
  setToken,
  videoId,
}: YoutubePanelProps) {
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [uploadForm, setUploadForm] = useState({
    title: "Skibidi News Daily",
    description: "Today's news in a fun and engaging format! #Shorts #News",
    keywords: "news,shorts,daily,entertainment",
    privacyStatus: "unlisted",
  });

  const handleAuth = async () => {
    setLoading(true);
    try {
      const result = await authenticateYouTube();
      setToken(result);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!token || !videoId) return;

    setUploading(true);
    try {
      await uploadToYouTube({
        oauth_token: token,
        video_id: videoId,
        video_title: uploadForm.title,
        video_description: uploadForm.description,
        keywords: uploadForm.keywords,
        privacy_status: uploadForm.privacyStatus,
      });
      setUploaded(true);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  useEffect(() => {
    // Reset upload status when videoId changes
    setUploaded(false);
  }, [videoId]);

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
                YouTube Publishing
              </p>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                Upload to YouTube
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Authenticate and upload your generated videos to YouTube Shorts.
              </p>
            </div>
          </div>
        </header>

        {!token ? (
          <div className="space-y-4">
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
            <div className="rounded-2xl border border-dashed border-red-400/40 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-red-500/30 dark:bg-slate-900/30 dark:text-slate-400">
              Please authenticate with YouTube first to enable video uploads.
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-2xl border border-red-400/30 bg-white/80 p-4 text-sm shadow-sm dark:border-red-500/20 dark:bg-slate-900/50">
              <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                <CheckCircle className="size-4" />
                <span className="font-medium">Authenticated successfully!</span>
              </div>
            </div>

            {videoId ? (
              <div className="space-y-4">
                <div className="grid gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Video Title
                    </label>
                    <input
                      type="text"
                      value={uploadForm.title}
                      onChange={(e) =>
                        setUploadForm({ ...uploadForm, title: e.target.value })
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                      placeholder="Enter video title"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Description
                    </label>
                    <textarea
                      value={uploadForm.description}
                      onChange={(e) =>
                        setUploadForm({
                          ...uploadForm,
                          description: e.target.value,
                        })
                      }
                      rows={3}
                      className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                      placeholder="Enter video description"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Keywords (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={uploadForm.keywords}
                      onChange={(e) =>
                        setUploadForm({
                          ...uploadForm,
                          keywords: e.target.value,
                        })
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                      placeholder="news,shorts,entertainment"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Privacy Status
                    </label>
                    <select
                      value={uploadForm.privacyStatus}
                      onChange={(e) =>
                        setUploadForm({
                          ...uploadForm,
                          privacyStatus: e.target.value,
                        })
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                    >
                      <option value="unlisted">Unlisted</option>
                      <option value="public">Public</option>
                      <option value="private">Private</option>
                    </select>
                  </div>
                </div>

                {uploaded ? (
                  <div className="rounded-2xl border border-green-400/30 bg-green-50/80 p-6 text-sm shadow-sm dark:border-green-500/20 dark:bg-green-900/20">
                    <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                      <CheckCircle className="size-5" />
                      <span className="font-semibold">
                        Video uploaded successfully!
                      </span>
                    </div>
                    <p className="mt-2 text-green-700 dark:text-green-300">
                      Your video has been uploaded to YouTube. Check your
                      YouTube channel to see the video.
                    </p>
                  </div>
                ) : (
                  <button
                    type="button"
                    onClick={handleUpload}
                    disabled={uploading || !uploadForm.title.trim()}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-red-500 via-pink-500 to-red-500 px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_32px_-22px_rgba(239,68,68,0.9)] transition hover:shadow-[0_22px_40px_-20px_rgba(239,68,68,0.85)] disabled:cursor-not-allowed disabled:opacity-55"
                  >
                    {uploading ? (
                      <>
                        <Loader className="size-4 animate-spin" />
                        Uploading to YouTube...
                      </>
                    ) : (
                      <>
                        <Upload className="size-4" />
                        Upload to YouTube
                      </>
                    )}
                  </button>
                )}
              </div>
            ) : (
              <div className="rounded-2xl border border-dashed border-red-400/40 bg-white/20 p-6 text-sm text-slate-500 backdrop-blur-sm dark:border-red-500/30 dark:bg-slate-900/30 dark:text-slate-400">
                Generate a video in the Studio Pipeline first to enable YouTube
                upload.
              </div>
            )}
          </div>
        )}
      </div>
    </PanelShell>
  );
}
