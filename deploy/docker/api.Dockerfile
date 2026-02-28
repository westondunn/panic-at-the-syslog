# API service - REST endpoints for UI and external integrations
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY libs/ libs/
COPY services/api/ services/api/
COPY services/__init__.py services/__init__.py
COPY contracts/ contracts/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# FastAPI with Uvicorn
CMD ["uvicorn", "services.api.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
