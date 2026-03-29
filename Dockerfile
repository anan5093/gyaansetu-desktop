
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

# ✅ Copy only required folders
COPY api ./api
COPY config ./config
COPY rag ./rag
COPY vector_store ./vector_store
COPY llm ./llm

# ❌ DO NOT COPY data folder

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
