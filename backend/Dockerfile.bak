# ===== Stage 1: Python dependencies =====
FROM python:3.11-slim AS base

# System dependencies for TensorFlow, OpenCV, and scientific libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===== Stage 2: Application =====
FROM base AS app

WORKDIR /app

# Copy application code
COPY app/ ./app/

# Copy ML model files
COPY *.h5 ./
COPY models/ ./models/

# Copy database (will be overridden by volume mount in production)
COPY cancercare_secure.db ./cancercare_secure.db

# Environment defaults
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DEBUG=false
ENV CORS_ORIGINS=http://localhost,http://localhost:80

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
