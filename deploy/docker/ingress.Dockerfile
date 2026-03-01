# Ingress service - Syslog receiver
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY libs/ libs/
COPY services/ingress/ services/ingress/
COPY services/__init__.py services/__init__.py

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Syslog typically requires privileged ports (514)
# Docker mapping to 1514 on host handles this
EXPOSE 514/udp
EXPOSE 514/tcp

CMD ["python", "-m", "services.ingress"]
