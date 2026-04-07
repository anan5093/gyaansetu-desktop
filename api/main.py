from dotenv import load_dotenv
load_dotenv()

import os
import traceback

# ==============================
# 🔥 CPU OPTIMIZATION (CRITICAL)
# ==============================
NUM_CORES = "8"
os.environ["OMP_NUM_THREADS"] = NUM_CORES
os.environ["OPENBLAS_NUM_THREADS"] = NUM_CORES
os.environ["MKL_NUM_THREADS"] = NUM_CORES
os.environ["NUMEXPR_NUM_THREADS"] = NUM_CORES
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import router, set_rag_instance
from vector_store.faiss_loader import FAISSLoader
from rag.rag_service import RAGService
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder


# ==============================
# 🚀 LIFESPAN (replaces deprecated @on_event)
# ==============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown lifecycle cleanly."""
    try:
        print("\n🚀 Initializing GyaanSetu NCERT Tutor\n")

        # 📦 FAISS
        print("📦 Loading FAISS index...")
        store = FAISSLoader(class_id=10, subject="science")
        print("✅ FAISS loaded")

        # 🤖 LLM
        print("🤖 Loading LLM (Ollama/Gemma)...")
        llm = LLMFactory.create()
        print("✅ LLM ready")

        # 🧩 Prompt Builder
        prompt_builder = PromptBuilder()

        # 🔗 RAG Service (single shared instance)
        rag = RAGService(store, llm, prompt_builder)
        set_rag_instance(rag)

        print("\n🎉 Tutor Ready!\n")

    except Exception as e:
        print("\n❌ STARTUP FAILED ❌")
        print("Error:", str(e))
        traceback.print_exc()
        raise  # Let FastAPI know startup failed

    yield  # App runs here

    # 🧹 Shutdown cleanup (if needed)
    print("\n🛑 Shutting down gracefully...\n")


# ==============================
# 🚀 FASTAPI APP
# ==============================
app = FastAPI(
    title="GyaanSetu NCERT Tutor",
    version="3.0-chat",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# ==============================
# ✅ BASIC ROUTES
# ==============================
@app.get("/")
def root():
    return {"message": "GyaanSetu NCERT Tutor Running 🚀", "version": "3.0-chat"}


@app.get("/health")
def health():
    return {"status": "ok"}
