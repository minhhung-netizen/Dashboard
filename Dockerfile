# syntax=docker/dockerfile:1
# Layered build so the heavy dependency install (vnstock -> pandas/numpy)
# is cached and only re-runs when requirements.txt changes. Frontend-only
# commits (app/static/*) reuse the cached deps layer and deploy in seconds.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=0

WORKDIR /app

# 1) Dependencies layer — cached unless requirements.txt changes.
#    BuildKit cache mount keeps the pip download cache warm across builds.
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# 2) Application code — changes here do NOT bust the deps layer above.
COPY . .

# Railway injects $PORT. railway.json deploy.startCommand takes precedence,
# but this keeps the image runnable on its own too.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
