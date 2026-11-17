# Layered build so the dependency install
# is cached and only re-runs when requirements.txt changes. Frontend-only
# commits (app/static/*) reuse the cached deps layer and deploy fast.

FROM python:3.11-slim

# MALLOC_ARENA_MAX=2: fewer glibc malloc arenas. The asyncio.to_thread pool
# otherwise grows one arena per thread and resident memory creeps up over weeks.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MALLOC_ARENA_MAX=2

WORKDIR /app

# 1) Dependencies layer — cached unless requirements.txt changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) Application code — changes here do NOT bust the deps layer above.
COPY . .

# Railway injects $PORT. railway.json deploy.startCommand takes precedence,
# but this keeps the image runnable on its own too.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
