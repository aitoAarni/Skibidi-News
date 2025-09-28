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

### To use Poly

Install `aws-cli`:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

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
- Now when possible to retrieve access keys:
- Open terminal and run:

```
aws configure
```

- Paste in Access key ID and secret access key
- Select some region e.g. `eu-west-1`
- Rest doesn't matter
- Confirm you have CLI access:

```
aws sts get-caller-identity
```

### Running the program

```
uv run main.py
```
