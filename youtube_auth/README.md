# youtube_auth

Used to get an OAuth2 session token from Google, so that YouTube uploads work.

This is separate from the workflow, because the auth token flow will open a
browser window.

Fill in `CLIENT_SECRETS_BASE64` in `.env` and then run:

```
uv run --env-file .env main.py
```
