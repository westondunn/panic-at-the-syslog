# Base Python image for Panic! At The Syslog services
# Provides common dependencies and structure for all Python-based services

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY libs/ libs/
COPY services/ services/
COPY contracts/ contracts/

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default user (override in service-specific Dockerfiles if needed)
RUN useradd -m -u 1000 panic && chown -R panic:panic /app
USER panic
