from dotenv import load_dotenv
load_dotenv()

import os
import traceback
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router, set_rag_instance

from vector_store.faiss_loader import FAISSLoader
from rag.rag_service import RAGService
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder


# ==============================
# 🔽 DOWNLOAD HELPER
# ==============================
def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        print(f"⬇️ Downloading: {path}")

        r = requests.get(url)

        if r.status_code != 200:
            raise Exception(f"❌ Failed to download file: {url}")

        with open(path, "wb") as f:
            f.write(r.content)

        print("✅ Download complete")


app = FastAPI(
    title="GyaanSetu NCERT Tutor API",
    version="1.4"
)

# ==============================
# ✅ CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"message": "GyaanSetu API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ==============================
# 🚀 STARTUP
# ==============================
@app.on_event("startup")
def startup_event():
    try:
        print("\n🚀 Starting NCERT Tutor Backend...\n")

        # ==============================
        # 🔐 ENV CHECK
        # ==============================
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("⚠️ WARNING: OPENROUTER_API_KEY not found!")

        # ==============================
        # 🌐 GET FILE URLS FROM ENV
        # ==============================
        FAISS_URL = os.getenv("FAISS_URL")
        META_URL = os.getenv("META_URL")

        if not FAISS_URL or not META_URL:
            print("⚠️ WARNING: FAISS_URL or META_URL not set. Skipping download.")
        
        # ==============================
        # 📂 PATHS
        # ==============================
        base_path = "data/vector_store/class10"

        index_path = os.path.join(base_path, "science_faiss.index")
        meta_path = os.path.join(base_path, "science_meta.json")

        # ==============================
        # ⬇️ DOWNLOAD FILES (SAFE)
        # ==============================
        if FAISS_URL:
            download_file(FAISS_URL, index_path)

        if META_URL:
            download_file(META_URL, meta_path)

        print("✅ FAISS setup complete")

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
        # 🤖 LLM
        # ==============================
        print("\n🤖 Initializing LLM...")
        llm = LLMFactory.create()
        print("✅ LLM ready")

        # ==============================
        # 🧩 PROMPT BUILDER
        # ==============================
        prompt_builder = PromptBuilder()

        # ==============================
        # 🔗 RAG
        # ==============================
        print("\n🔗 Building RAG pipeline...")
        rag = RAGService(
            store,
            llm,
            prompt_builder
        )

        set_rag_instance(rag)

        print("\n🎉 Backend Ready with RAG!\n")

    except Exception as e:
        print("\n❌ STARTUP FAILED ❌")
        print("Error:", str(e))
        traceback.print_exc()
