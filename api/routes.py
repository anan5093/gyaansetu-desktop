from fastapi import APIRouter, HTTPException, Header
from api.schemas import ChatRequest
from typing import Optional
import time

router = APIRouter()

# ==============================
# 🔗 GLOBAL RAG INSTANCE
# Set once at startup via main.py lifespan
# ==============================
rag_instance = None

def set_rag_instance(rag):
    global rag_instance
    rag_instance = rag


# ==============================
# 💬 CHAT ENDPOINT
# Supports both multi-turn (session_id header) and stateless fallback
# ==============================
@router.post("/chat")
def chat_endpoint(
    req: ChatRequest,
    x_session_id: Optional[str] = Header(default=None),  # Optional session header
):
    if rag_instance is None:
        raise HTTPException(status_code=500, detail="RAG not initialized. Check server startup logs.")

    try:
        start_time = time.time()

        # ==============================
        # 🔍 RETRIEVE CONTEXT (FAISS)
        # ==============================
        chunks = rag_instance.store.search(req.question)

        # ==============================
        # 🧩 BUILD PROMPT
        # Multi-turn if session_id present, stateless otherwise
        # ==============================
        if x_session_id:
            prompt = rag_instance.prompt_builder.build_chat(
                context=[c["text"] for c in chunks],
                question=req.question,
                session_id=x_session_id,
            )
        else:
            prompt = rag_instance.prompt_builder.build(
                context=[c["text"] for c in chunks],
                question=req.question,
            )

        # ==============================
        # 🤖 GENERATE ANSWER (LLM)
        # ==============================
        answer = rag_instance.llm.generate(
            prompt=prompt,
            session_id=x_session_id,   # None = stateless fallback in GemmaClient
        )

        latency = round(time.time() - start_time, 2)

        # ==============================
        # 📚 BUILD SOURCES (top 3)
        # ==============================
        sources = [
            {
                "topic":   c.get("topic"),
                "chapter": c.get("chapter"),
                "type":    c.get("type"),
            }
            for c in chunks[:3]
        ]

        return {
            "answer":  answer,
            "sources": sources,
            "session": x_session_id or "stateless",
            "metrics": {
                "latency_sec":  latency,
                "chunks_used":  len(chunks),
                "mode":         "multi-turn" if x_session_id else "stateless",
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# 🗑️ CLEAR CHAT HISTORY
# Clears in-memory history for a given session
# ==============================
@router.delete("/chat/history")
def clear_history(x_session_id: Optional[str] = Header(default=None)):
    if not x_session_id:
        raise HTTPException(status_code=400, detail="X-Session-ID header required to clear history.")
    try:
        from llm.gemma_client import clear_history
        clear_history(x_session_id)
        return {"status": "cleared", "session": x_session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# 📊 EVALUATION ENDPOINT
# ==============================
@router.get("/evaluation")
def run_evaluation():
    if rag_instance is None:
        raise HTTPException(status_code=500, detail="RAG not initialized.")
    try:
        from evaluation.evaluator import Evaluator
        evaluator = Evaluator(rag_instance)
        results = evaluator.run_all()
        return {"status": "success", "evaluation": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ❤️ HEALTH CHECK
# ==============================
@router.get("/health")
def health():
    return {
        "status":     "ok",
        "rag_loaded": rag_instance is not None,
    }
