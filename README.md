# GyaanSetu — Desktop Edition 🎓

> **GyaanSetu** (ज्ञानसेतु) means *Bridge of Knowledge* — a privacy-first, locally-run AI tutor that answers NCERT curriculum questions using Retrieval-Augmented Generation (RAG).

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20%2F%20Gemma-blueviolet)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Table of Contents

- [What is GyaanSetu Desktop?](#what-is-gyaansetu-desktop)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
  - [Optional: FastAPI Backend](#optional-fastapi-backend)
- [Configuration](#configuration)
- [ONNX Model](#onnx-model)
- [Scripts](#scripts)
- [Getting Help](#getting-help)
- [Contributing](#contributing)
- [Maintainers](#maintainers)

---

## What is GyaanSetu Desktop?

GyaanSetu Desktop is a **fully local, offline-capable** AI study companion for CBSE students in **Class 9 and Class 10 Science**. It uses a RAG pipeline to retrieve the most relevant chunks from NCERT textbooks (loaded from HuggingFace) and streams answers through a locally-hosted large language model via [Ollama](https://ollama.com/).

The entire stack — embeddings, vector search, and LLM inference — runs on your machine. No data leaves your computer.

> **Desktop Edition vs. Web Edition:** The Desktop Edition replaces the React + FastAPI web stack with a single-command [Streamlit](https://streamlit.io/) UI that any student can run with one Python command.

---

## Key Features

- 🖥️ **One-command launch** — `python run_app.py` starts the full Streamlit interface
- 🔒 **Privacy-first** — all processing happens locally; no API keys required for the LLM
- 🧠 **RAG-powered answers** — FAISS semantic search retrieves relevant NCERT chunks before answering
- ⚡ **Streaming responses** — answers stream token-by-token via `st.write_stream`
- 📚 **Multi-class support** — switch between Class 9 and Class 10 Science from the sidebar
- 💬 **Conversation memory** — maintains per-session chat history for multi-turn questions
- 🔁 **Graceful fallback** — falls back to a safe response if Ollama is unreachable
- 🧩 **ONNX embeddings** — quantized `all-MiniLM-L6-v2` model in `onnx_model/` for fast CPU inference

---

## Architecture

```
HuggingFace Dataset (NCERT Class 9 / 10 Science)
        │
        ▼
┌─────────────────────────────────────────┐
│           Ingestion Pipeline            │
│  HFLoader → Cleaner → Chunker → Embedder│
└──────────────────┬──────────────────────┘
                   │  FAISS index + metadata JSON
                   ▼
┌──────────────────────────────────────────┐
│              RAG Service                 │
│  embed query → FAISS search →            │
│  build context → Gemma (Ollama)          │
└──────────────────┬───────────────────────┘
                   │  streaming tokens
                   ▼
┌──────────────────────────────────────────┐
│         Streamlit UI  (ui/app.py)        │
│  Sidebar (class select) │ Chat window    │
└──────────────────────────────────────────┘
```

The LLM is served by a local [Ollama](https://ollama.com/) instance (default model: `gemma4:e2b`). For resource-constrained environments, you can point `OLLAMA_HOST` to an ngrok tunnel from a Colab notebook instead.

---

## Project Structure

```
gyaansetu-desktop/
├── api/                    # Optional FastAPI backend (routes, schemas, lifespan)
├── config/
│   └── settings.py         # All environment-based settings with typed helpers
├── convert_to_onnx.py      # One-time script: export sentence-transformer → ONNX
├── data/                   # Raw + processed NCERT dataset (auto-created by ingestion)
├── ingestion/              # HFLoader, cleaner, chunker, embedder
├── llm/
│   ├── gemma_client.py     # Streaming Ollama client with chat-history injection
│   ├── llm_factory.py      # Factory with health-check and FallbackLLM
│   └── prompt_builder.py   # Prompt templates (stateless & multi-turn)
├── onnx_model/             # Pre-exported ONNX tokenizer & config for all-MiniLM-L6-v2
├── rag/
│   └── rag_service.py      # Core pipeline: retrieve → build context → stream
├── requirements.txt
├── run_app.py              # 🚀 Main entry point — launches Streamlit
├── scripts/
│   ├── test_ingestion.py   # Download & process the NCERT dataset
│   ├── test_rag.py         # End-to-end RAG smoke test
│   └── test_retrieval.py   # FAISS retrieval accuracy check
├── ui/
│   └── app.py              # Streamlit chat interface
└── vector_store/
    ├── build_faiss_index.py # Builds FAISS index from processed chunks
    └── faiss_loader.py      # Loads index + metadata and exposes .search()
```

---

## Getting Started

### Prerequisites

| Tool | Minimum Version | Notes |
|------|----------------|-------|
| Python | 3.11 | Earlier versions untested |
| Ollama | Latest | [Install guide](https://ollama.com/download) |
| Gemma model | `gemma4:e2b` | Pulled via `ollama pull gemma4:e2b` |

> **No GPU required.** The app runs on CPU. ONNX embeddings and Ollama CPU inference are both supported.

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/anan5093/gyaansetu-desktop.git
cd gyaansetu-desktop
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Pull the Gemma model into Ollama**

```bash
ollama pull gemma4:e2b
```

**5. Build the FAISS index** (downloads NCERT data from HuggingFace — one-time step)

```bash
python scripts/test_ingestion.py
python -m vector_store.build_faiss_index
```

This creates the `data/` directory with the processed dataset and the FAISS index files.

---

### Running the App

```bash
python run_app.py
```

Streamlit opens automatically at **http://localhost:8501**. Use the sidebar to switch between Class 9 and Class 10 Science, then type your question in the chat box.

---

### Optional: FastAPI Backend

The `api/` folder contains a standalone FastAPI server for programmatic access:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive docs are available at **http://localhost:8000/docs**.

**Example request:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is Newton's second law of motion?\"}"
```

**Example response:**

```json
{
  "answer": "Newton's second law states that the force acting on an object equals its mass times acceleration (F = ma).",
  "sources": [
    { "topic": "Force and Laws of Motion", "chapter": "Force and Laws of Motion", "type": "concept" }
  ],
  "session": "stateless",
  "metrics": { "latency_sec": 0.38, "chunks_used": 3, "mode": "stateless" }
}
```

---

## Configuration

All settings are read from environment variables or a `.env` file in the project root.

| Variable | Default | Description |
|----------|---------|-------------|
| `CLASS_ID` | `10` | NCERT class (`9` or `10`) |
| `SUBJECT` | `science` | Subject name |
| `TOP_K` | `7` | Number of FAISS chunks retrieved per query |
| `SCORE_THRESHOLD` | `0.20` | Minimum cosine-similarity score to include a chunk |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL (local or ngrok tunnel) |
| `OLLAMA_MODEL` | `gemma4:e2b` | Model name served by Ollama |
| `LLM_TEMPERATURE` | `0.1` | Low temperature for factual, curriculum-accurate answers |
| `LLM_NUM_CTX` | `2048` | Context window size (tokens) |
| `LLM_TIMEOUT` | `120` | Request timeout in seconds (increase for tunnel use) |
| `CHAT_MAX_HISTORY_TURNS` | `6` | Number of past conversation turns to keep in memory |
| `MAX_CONTEXT_CHARS` | `1500` | Maximum characters of NCERT context per prompt |
| `API_HOST` | `127.0.0.1` | Host for the optional FastAPI server |
| `API_PORT` | `8000` | Port for the optional FastAPI server |
| `ENABLE_LOGS` | `true` | Print verbose startup and retrieval logs |

**Example `.env` (local Ollama):**

```dotenv
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma4:e2b
CLASS_ID=10
TOP_K=5
ENABLE_LOGS=true
```

**Example `.env` (Colab ngrok tunnel):**

```dotenv
OLLAMA_HOST=https://your-ngrok-url.ngrok-free.app
OLLAMA_MODEL=gemma4:e2b
LLM_TIMEOUT=180
```

---

## ONNX Model

The `onnx_model/` directory contains a pre-exported ONNX version of `sentence-transformers/all-MiniLM-L6-v2`. This enables faster, dependency-light embedding on CPU without needing a full PyTorch installation at runtime.

To regenerate it (requires `optimum[onnxruntime]`):

```bash
pip install optimum[onnxruntime]
python convert_to_onnx.py
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/test_ingestion.py` | Download and process NCERT data from HuggingFace |
| `scripts/test_rag.py` | Run a sample question through the full RAG pipeline |
| `scripts/test_retrieval.py` | Check that FAISS retrieval returns relevant chunks |
| `convert_to_onnx.py` | One-time export of the sentence-transformer model to ONNX |

---

## Getting Help

- **Bug reports & feature requests** — open an issue on [GitHub Issues](https://github.com/anan5093/gyaansetu-desktop/issues)
- **Ollama setup** — see the [Ollama documentation](https://ollama.com/download) for installation and model management
- **NCERT datasets** — hosted on HuggingFace: [`KadamParth/NCERT_Science_9th`](https://huggingface.co/datasets/KadamParth/NCERT_Science_9th) and [`KadamParth/NCERT_Science_10th`](https://huggingface.co/datasets/KadamParth/NCERT_Science_10th)

---

## Contributing

Contributions are welcome! Please open an issue first to discuss significant changes.

1. Fork the repository and create a feature branch from `main`
2. Make your changes with clear, descriptive commit messages
3. Verify the pipeline still works end-to-end:

```bash
python scripts/test_ingestion.py
python scripts/test_rag.py
python scripts/test_retrieval.py
```

4. Open a pull request against `main`

---

## Maintainers

| Name | GitHub | Contact |
|------|--------|---------|
| Anand | [@anan5093](https://github.com/anan5093) | [anand.ar1806@gmail.com](mailto:anand.ar1806@gmail.com) |

---

*GyaanSetu Desktop is an open-source project. See [LICENSE](LICENSE) for details.*
