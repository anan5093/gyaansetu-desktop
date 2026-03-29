FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

COPY api ./api
COPY config ./config
COPY rag ./rag
COPY vector_store ./vector_store
COPY data/vector_store ./data/vector_store

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
