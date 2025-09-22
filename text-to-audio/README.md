# Text to Audio

This component will produce an audio file from the given text input.

## Findings

| Product              | Quality | SSLM | Free Quota         | Cost                  |
| -------------------- | ------- | ---- | ------------------ | --------------------- |
| ElevenLabs           | Amazing | No   | 10k chars/mo       | 11$/mo for 100k chars |
| Deepgram             | Good    | No   | 6.6M chars         | $0.03/1k chars        |
| Polly Neural         | Good    | Yes  | 1M chars/mo for 1y | $0.02/1k chars        |
| Google Cloud Chirp 3 | Good    | No   | 1M chars/mo        | $0.03/1k chars        |

## Getting started

Install `uv`: https://docs.astral.sh/uv/#highlights  
Install `gcloud`: https://cloud.google.com/sdk/docs/install

Login to Google Cloud, make a project, and enable the Text to Speech API for the
project.

Authenticate with `gcloud`:

```
gcloud init
```

```
gcloud auth application-default login
```

Then run

```
uv run main.py
```
