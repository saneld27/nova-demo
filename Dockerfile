# ── Stage 1: dependency builder ───────────────────────────────────────────────
FROM python:3.11-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY pyproject.toml .
# uv needs a README for hatchling metadata
COPY README.md .

# Install dependencies into a virtual environment
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python --no-cache -e ".[dev]"

# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Non-root user for security
RUN addgroup --system nova && adduser --system --ingroup nova nova

WORKDIR /app

# Bring in the pre-built venv from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY app/ ./app/

# Make sure the venv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER nova

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
