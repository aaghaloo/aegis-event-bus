# Dockerfile
# Purpose: Build reproducible image using pinned deps in requirements.lock

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# psycopg2 needs headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy deps first for better caching
COPY requirements.txt requirements.lock ./

# Install pinned deps
RUN pip install --no-cache-dir -r requirements.lock

# Copy the rest
COPY . .

EXPOSE 8000

CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
