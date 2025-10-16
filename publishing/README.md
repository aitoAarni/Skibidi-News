# Publishing

This component will publish the given audio or video file to social media
platforms.

## Getting started

Install `uv`: https://docs.astral.sh/uv/#highlights

Find `client_secrets.json` and place it at the root of the project:
`publishing/client_secrets.json`

### Publishing a test file

```
uv run main.py
```

## Docker

Building the app:

```bash
DOCKER_BUILDKIT=1 docker build . -t "publishing"
```

### Running the app in Docker

```bash
docker run --rm publishing
```
