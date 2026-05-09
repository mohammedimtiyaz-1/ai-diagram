# Dockerfile for FastAPI backend
# Deploy target: Render (or any Docker-compatible host)

FROM python:3.11-slim

WORKDIR /app

# Install build deps if any wheels need compiling
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition first for layer caching
COPY pyproject.toml ./

# Install app and dependencies
RUN pip install --no-cache-dir -e "."

# Copy application code
COPY app/ ./app/
COPY tests/ ./tests/

# Expose the port (Render sets PORT env var)
EXPOSE 8000

# Start uvicorn; PORT is provided by Render at runtime
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
