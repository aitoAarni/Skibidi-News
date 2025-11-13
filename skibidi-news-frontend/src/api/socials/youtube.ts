declare global {
  interface Window {
    google?: {
      accounts?: any;
    };
  }
}

// Loads Google Identity Services library to dom
function loadGoogleIdentityServices() {
  // Early return if already loaded
  if (window.google && window.google.accounts) return Promise.resolve();

  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// Generates the access token using Google Identity Services
type InitTokenClientResponse = {
  access_token?: string;
};
function loadTokenClient(clientId: string, scope: string) {
  return new Promise((resolve, reject) => {
    if (window.google === undefined || window.google.accounts === undefined) {
      throw new Error("Google Identity Services not loaded.");
    }
    const client = window.google.accounts.oauth2.initTokenClient({
      client_id: clientId,
      scope: scope,
      callback: (response: InitTokenClientResponse) => {
        if (response.access_token) {
          resolve(response.access_token);
        }
        reject("Failed to obtain access token.");
      },
    });
    client.requestAccessToken();
  });
}

const YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload";

export async function authenticateYouTube() {
  const clientId = import.meta.env.VITE_YOUTUBE_CLIENT_ID;
  if (!clientId) {
    throw new Error("CLIENT_ID is not defined in environment variables.");
  }
  if (window.google === undefined) {
    await loadGoogleIdentityServices();
  }
  const accessToken = await loadTokenClient(clientId, YOUTUBE_UPLOAD_SCOPE);
  const encoded = btoa(accessToken as string);
  return encoded;
}

import axios from "axios";
import { endpoints } from "../config";

export type YouTubeUploadParams = {
  oauth_token: string;
  video_id: string;
  video_title: string;
  video_description: string;
  keywords: string;
  privacy_status: string;
};

export const uploadToYouTube = async (
  params: YouTubeUploadParams
): Promise<void> => {
  await axios.post(endpoints.youtubePublish, params);
};
