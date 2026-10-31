# syntax=docker/dockerfile:1
FROM python:3.12-slim

LABEL org.opencontainers.image.title="daily-tutor-mcp" \
      org.opencontainers.image.description="Duolingo-style daily practice MCP server" \
      org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/fritnes/daily-tutor-mcp"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install .

# Run as an unprivileged user; all state lives in the /data volume.
RUN useradd --create-home --uid 10001 tutor && mkdir /data && chown tutor:tutor /data
USER tutor

# Container defaults to the authenticated HTTP transport.
# Set TUTOR_API_TOKENS (required), or TUTOR_TRANSPORT=stdio for `docker run -i`.
ENV TUTOR_DATA_PATH=/data \
    TUTOR_TRANSPORT=streamable-http \
    TUTOR_HOST=0.0.0.0 \
    TUTOR_PORT=8000
VOLUME ["/data"]
EXPOSE 8000

ENTRYPOINT ["python", "-m", "daily_tutor"]
