# Detector service - Rule-based pattern detection
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY libs/ libs/
COPY services/detector/ services/detector/
COPY services/__init__.py services/__init__.py
COPY contracts/ contracts/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Entry point placeholder - TODO: implement consumer runner
CMD ["python", "-c", "import time; print('Detector consumer - TODO: implement Kafka consumer loop'); time.sleep(9999999)"]
