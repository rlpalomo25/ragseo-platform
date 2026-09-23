FROM python:3.12.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Content baked at build time (staged by scripts/sync_doctrine.sh — Prompt 7).
COPY doctrine/ /app/doctrine
COPY external/ /app/external

RUN chmod +x docker-entrypoint.sh scripts/migrate.py

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
