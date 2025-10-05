# Use a Python image and install uv
FROM python:alpine3.22
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Add packages to alpine
RUN apk add --update sudo ffmpeg

# Install the project into `/app`
WORKDIR /app
COPY . .

# Install the project's dependencies
RUN uv sync --locked

# Setup a non-root user in alpine
RUN adduser -D mcp \
  && echo "mcp ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mcp \
  && chmod 0440 /etc/sudoers.d/mcp

# Use the non-root user to run our application
USER mcp

CMD ["uv", "run", "main.py"]