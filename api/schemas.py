from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    class_id: int
    subject: str


class ChatResponse(BaseModel):
    answer: str
    latency: float
