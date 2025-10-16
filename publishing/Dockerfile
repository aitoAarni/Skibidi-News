# Use a Python image and install uv
FROM astral/uv:python3.14-rc-alpine

# Add packages to alpine
RUN apk add --update sudo ffmpeg

# Install the project into `/app`
WORKDIR /app
COPY . .

# Install the project's dependencies
RUN uv sync --locked

CMD ["uv", "run", "main.py"]