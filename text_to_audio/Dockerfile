# Use a Python image and install uv
FROM python:alpine3.22 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into `/app`
WORKDIR /app

# Optimizations
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-dev

FROM python:alpine3.22 AS runner

# Set working directory
WORKDIR /app

# Copy the environment and the source code
COPY --from=builder --chown=app:app /app /app

# Setup a non-root user in alpine
RUN apk add --update sudo
RUN adduser -D mcp \
  && echo "mcp ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mcp \
  && chmod 0440 /etc/sudoers.d/mcp

# Use the non-root user to run our application
USER mcp

# Run the main.py file directly using the virtual environment's Python
CMD ["/app/.venv/bin/python", "main.py"]