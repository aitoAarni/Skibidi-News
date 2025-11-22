# Use a Python image and install uv
FROM astral/uv:python3.14-rc-alpine

# Add packages to alpine
RUN apk add --update sudo ffmpeg

# Install the project into `/app`
WORKDIR /app
COPY . .
ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV NO_PROXY=localhost,127.0.0.1
ENV http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV no_proxy=localhost,127.0.0.1

# Install the project's dependencies
RUN uv sync --locked

CMD ["uv", "run", "main.py"]