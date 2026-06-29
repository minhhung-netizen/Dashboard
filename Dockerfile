# Layered build so the heavy dependency install (vnstock -> pandas/numpy)
# is cached and only re-runs when requirements.txt changes. Frontend-only
# commits (app/static/*) reuse the cached deps layer and deploy fast.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Dependencies layer — cached unless requirements.txt changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) Application code — changes here do NOT bust the deps layer above.
COPY . .

# Railway injects $PORT. railway.json deploy.startCommand takes precedence,
# but this keeps the image runnable on its own too.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
