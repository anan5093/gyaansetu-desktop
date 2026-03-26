from fastapi import APIRouter
from api.schemas import ChatRequest
from rag.rag_service import RAGService

router = APIRouter()

# ⭐ create global variable
rag_instance = None


def set_rag_instance(rag):
    global rag_instance
    rag_instance = rag


@router.post("/chat")
def chat_endpoint(req: ChatRequest):

    answer = rag_instance.ask(req.question)

    return {
        "answer": answer
    }
