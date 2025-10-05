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

### To use GCP

Install `gcloud`: https://cloud.google.com/sdk/docs/install

- Login to Google Cloud
- Create a new project
- Search Text to Speech API
- Enable API for the project.
- Open terminal

Authenticate with `gcloud`:

```
gcloud init
```

```
gcloud auth application-default login
```

### To use Polly

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your AWS credentials:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=eu-west-1
```

3. To get your AWS credentials:
   - Login to AWS console via a browser
   - Go to "IAM"
   - Under "Access Management", click "Users"
   - Create user
   - Select from "Permission options": "Attach policies directly"
   - Tick from "Permission policies": AmazonPollyFullAccess
   - Create user
   - Select new user
   - Go to "Security credentials" tab
   - Scroll to "Access keys"
   - Create access key
   - Command Line Interface (CLI)
     - Confirm "I understand above recommendation..."
   - Copy the Access Key ID and Secret Access Key to your `.env` file

### Running the mcp server

```
uv run --env-file .env main.py
```

### Running a test synthesis

```
uv run --env-file .env synth.py
```

## Docker

Building the app:

```bash
DOCKER_BUILDKIT=1 docker build . -t "text-to-audio"
```

### Running the app in Docker

```bash
docker run -it --rm --env-file .env text-to-audio
```

**Note:** The `-it` flag is required because stdio needs standard input session,
otherwise the app will close immediately.
