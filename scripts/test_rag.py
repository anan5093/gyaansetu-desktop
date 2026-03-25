import os
import sys
import time
from dotenv import load_dotenv


# ===============================
# 🔧 Setup Project Root Path
# ===============================
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

# ===============================
# 🔐 Load Environment Variables
# ===============================
load_dotenv()


# ===============================
# 📦 Imports (After Path Fix)
# ===============================
from rag.rag_service import RAGService
from vector_store.faiss_loader import FAISSLoader
from ingestion.embedder import Embedder

from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder

from config.settings import (
    CLASS_ID,
    SUBJECT,
    TOP_K,
    DEBUG_MODE,
    USE_MOCK_LLM
)


# ===============================
# 🚀 Bootstrap Tutor
# ===============================
def build_tutor():

    print("\n🚀 Initialising NCERT RAG Tutor")
    print(f"📘 Class: {CLASS_ID} | Subject: {SUBJECT}")
    print(f"⚙️ LLM Mode: {'MOCK' if USE_MOCK_LLM else 'REAL'}")
    print("")

    embedder = Embedder()

    vector_store = FAISSLoader(
        class_id=CLASS_ID,
        subject=SUBJECT
    )

    llm_client = LLMFactory.create()

    prompt_builder = PromptBuilder()

    rag = RAGService(
        vector_store=vector_store,
        embedder=embedder,
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        top_k=TOP_K
    )

    print("✅ Tutor Ready!\n")

    return rag


# ===============================
# 💬 Interactive CLI Loop
# ===============================
def chat_loop(rag):

    print("💡 Ask NCERT Questions (type 'exit' to quit)\n")

    while True:

        try:
            question = input("🧠 You: ").strip()

            if not question:
                continue

            if question.lower() in ["exit", "quit", "q"]:
                print("\n👋 Exiting Tutor...\n")
                break

            start = time.time()

            answer, chunks = rag.ask_with_debug(question)

            latency = time.time() - start

            if DEBUG_MODE:
                print("\n📚 Retrieved Chunks:")
                for c in chunks:
                    topic = c.get("topic")
                    ctype = c.get("type")
                    print(f"— {topic} | {ctype}")

            print("\n🤖 Tutor Answer:\n")
            print(answer)

            print(f"\n⏱ Latency: {latency:.2f} sec")

            print("\n" + "=" * 70 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!\n")
            break

        except Exception as e:
            print("\n❌ Runtime Error:", str(e))
            print("Continuing...\n")


# ===============================
# 🎯 Entry Point
# ===============================
def main():

    rag = build_tutor()
    chat_loop(rag)


if __name__ == "__main__":
    main()