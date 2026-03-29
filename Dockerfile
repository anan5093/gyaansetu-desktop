FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy project files
COPY api ./api
COPY config ./config
COPY rag ./rag
COPY vector_store ./vector_store
COPY data/vector_store ./data/vector_store

# Expose port
EXPOSE 7860

# Run app
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
