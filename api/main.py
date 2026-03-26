from fastapi import FastAPI

from api.routes import router, set_rag_instance

from vector_store.faiss_loader import FAISSLoader
from ingestion.embedder import Embedder
from rag.rag_service import RAGService
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder


app = FastAPI(
    title="GyaanSetu NCERT Tutor API",
    version="1.0"
)

app.include_router(router)


@app.on_event("startup")
def startup_event():

    print("\n🚀 Starting NCERT Tutor Backend...")

    # ⭐ Vector Store
    store = FAISSLoader(
        class_id=10,
        subject="science"
    )

    # ⭐ Embedder
    embedder = Embedder()

    # ⭐ LLM
    llm = LLMFactory.create()

    # ⭐ Prompt Builder
    prompt_builder = PromptBuilder()

    # ⭐ RAG Service
    rag = RAGService(
        store,
        embedder,
        llm,
        prompt_builder
    )

    set_rag_instance(rag)

    print("✅ Tutor Backend Ready!\n")
