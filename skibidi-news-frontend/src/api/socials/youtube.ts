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

// Enhanced response type to capture more OAuth information
type InitTokenClientResponse = {
  access_token?: string;
  expires_in?: number;
  scope?: string;
  token_type?: string;
  error?: string;
};

export type OAuth2Credentials = {
  access_token: string;
  client_id: string;
  expires_in: number;
  token_expiry: string;
  scope: string;
  token_type: string;
  obtained_at: string;
};

function loadTokenClient(
  clientId: string,
  scope: string
): Promise<OAuth2Credentials> {
  return new Promise((resolve, reject) => {
    if (window.google === undefined || window.google.accounts === undefined) {
      throw new Error("Google Identity Services not loaded.");
    }
    const client = window.google.accounts.oauth2.initTokenClient({
      client_id: clientId,
      scope: scope,
      callback: (response: InitTokenClientResponse) => {
        if (response.access_token) {
          const obtainedAt = new Date();
          const expiresIn = response.expires_in || 3599; // Default to 1 hour
          const tokenExpiry = new Date(obtainedAt.getTime() + expiresIn * 1000);

          const credentials: OAuth2Credentials = {
            access_token: response.access_token,
            client_id: clientId,
            expires_in: expiresIn,
            token_expiry: tokenExpiry.toISOString(),
            scope: response.scope || scope,
            token_type: response.token_type || "Bearer",
            obtained_at: obtainedAt.toISOString(),
          };

          resolve(credentials);
        } else {
          reject(new Error(response.error || "Failed to obtain access token."));
        }
      },
    });
    client.requestAccessToken();
  });
}

const YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload";

export async function authenticateYouTube(): Promise<OAuth2Credentials> {
  const clientId = (import.meta as any).env?.VITE_YOUTUBE_CLIENT_ID;
  if (!clientId) {
    throw new Error("CLIENT_ID is not defined in environment variables.");
  }
  if (window.google === undefined) {
    await loadGoogleIdentityServices();
  }
  const credentials = await loadTokenClient(clientId, YOUTUBE_UPLOAD_SCOPE);
  return credentials;
}

// Helper function to get just the encoded access token (for backward compatibility)
export async function getEncodedAccessToken(): Promise<string> {
  const credentials = await authenticateYouTube();
  return btoa(credentials.access_token);
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

// Utility functions for credential management
export function isTokenExpired(credentials: OAuth2Credentials): boolean {
  const now = new Date();
  const expiry = new Date(credentials.token_expiry);
  return now >= expiry;
}

export function getTokenExpiryTime(credentials: OAuth2Credentials): number {
  const expiry = new Date(credentials.token_expiry);
  const now = new Date();
  return Math.max(0, expiry.getTime() - now.getTime());
}

// Store credentials in localStorage
export function storeCredentials(credentials: OAuth2Credentials): void {
  localStorage.setItem(
    "youtube_oauth_credentials",
    JSON.stringify(credentials)
  );
}

// Retrieve credentials from localStorage
export function getStoredCredentials(): OAuth2Credentials | null {
  const stored = localStorage.getItem("youtube_oauth_credentials");
  if (!stored) return null;

  try {
    const credentials: OAuth2Credentials = JSON.parse(stored);
    return isTokenExpired(credentials) ? null : credentials;
  } catch {
    return null;
  }
}

// Get valid credentials (from storage or by re-authenticating)
export async function getValidCredentials(): Promise<OAuth2Credentials> {
  const stored = getStoredCredentials();
  if (stored && !isTokenExpired(stored)) {
    return stored;
  }

  const newCredentials = await authenticateYouTube();
  storeCredentials(newCredentials);
  return newCredentials;
}

// Convert frontend credentials to oauth2.json-like format
export function toOAuth2JsonFormat(
  credentials: OAuth2Credentials,
  clientSecret?: string
): any {
  return {
    access_token: credentials.access_token,
    client_id: credentials.client_id,
    client_secret: (import.meta as any).env?.VITE_YOUTUBE_CLIENT_SECRET,
    refresh_token: null, // Not available from browser OAuth flow
    token_expiry: credentials.token_expiry,
    token_uri: "https://oauth2.googleapis.com/token",
    user_agent: null,
    revoke_uri: "https://oauth2.googleapis.com/revoke",
    id_token: null,
    id_token_jwt: null,
    token_response: {
      access_token: credentials.access_token,
      expires_in: credentials.expires_in,
      scope: credentials.scope,
      token_type: credentials.token_type,
    },
    scopes: [credentials.scope],
    token_info_uri: "https://oauth2.googleapis.com/tokeninfo",
    invalid: false,
    _class: "OAuth2Credentials",
    _module: "oauth2client.client",
  };
}
