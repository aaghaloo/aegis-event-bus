# Dockerfile - Hardened with security best practices
# Purpose: Build reproducible image using pinned deps in requirements.lock

# Multi-stage build for security
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for building
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy deps first for better caching
COPY requirements.txt requirements.lock ./

# Install pinned deps
RUN pip install --no-cache-dir --user -r requirements.lock

# Production stage
FROM python:3.11-slim

# Security: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Security: Update system packages and install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Security: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH=/home/appuser/.local/bin:$PATH

# Security: Create app directory with proper permissions
WORKDIR /app
RUN mkdir -p /app && chown -R appuser:appuser /app

# Copy Python packages from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Security: Switch to non-root user
USER appuser

# Security: Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/certs && \
    chmod 755 /app/logs /app/certs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

EXPOSE 8000

# Security: Use exec form for CMD
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
