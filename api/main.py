from dotenv import load_dotenv
load_dotenv()

import os
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router, set_rag_instance

from vector_store.faiss_loader import FAISSLoader
from rag.rag_service import RAGService
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder


app = FastAPI(
    title="GyaanSetu NCERT Tutor API",
    version="1.2"
)

# ✅ CORS (IMPORTANT for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    try:
        print("\n🚀 Starting NCERT Tutor Backend...\n")

        # ==============================
        # 🔎 CHECK ENV VARIABLES
        # ==============================
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("⚠️ WARNING: OPENROUTER_API_KEY not found!")

        # ==============================
        # 📂 CHECK FAISS FILES
        # ==============================
        base_path = "data/vector_store/class10"

        index_path = os.path.join(base_path, "science_faiss.index")
        meta_path = os.path.join(base_path, "science_meta.json")

        print("📂 Checking vector store...")

        print("Index path:", index_path)
        print("Meta path :", meta_path)

        if not os.path.exists(index_path):
            raise FileNotFoundError(f"❌ Missing FAISS index: {index_path}")

        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"❌ Missing metadata file: {meta_path}")

        print("✅ FAISS files found")

        # ==============================
        # 🧠 LOAD VECTOR STORE
        # ==============================
        print("\n🧠 Loading FAISS vector store...")
        store = FAISSLoader(
            class_id=10,
            subject="science"
        )
        print("✅ Vector store loaded")

        # ==============================
        # 🤖 LOAD LLM
        # ==============================
        print("\n🤖 Initializing LLM...")
        llm = LLMFactory.create()
        print("✅ LLM ready")

        # ==============================
        # 🧩 PROMPT BUILDER
        # ==============================
        prompt_builder = PromptBuilder()

        # ==============================
        # 🔗 BUILD RAG PIPELINE
        # ==============================
        print("\n🔗 Building RAG pipeline...")
        rag = RAGService(
            store,
            llm,
            prompt_builder
        )

        # Inject into routes
        set_rag_instance(rag)

        print("\n🎉 Backend Ready with RAG + Metrics + Sources!\n")

    except Exception as e:
        print("\n❌ STARTUP FAILED ❌")
        print("Error:", str(e))
        traceback.print_exc()
