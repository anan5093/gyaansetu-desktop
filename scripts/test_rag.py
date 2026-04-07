import sys
import os
import time

# Ensure Python knows where the GyaanSetu home folder is
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from config import settings
from vector_store.faiss_loader import FAISSLoader
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder
from rag.rag_service import RAGService

def build_tutor():
    print("🚀 Initialising NCERT RAG Tutor")
    # 🔥 Dynamically pull from settings! Notice the capitalize()
    print(f"📘 Class: {settings.CLASS_ID} | Subject: {settings.SUBJECT.capitalize()}")

    print("📦 Loading FAISS index...")
    # 🔥 No hardcoded numbers here anymore.
    vector_store = FAISSLoader()

    print("🤖 Loading LLM...")
    llm_client = LLMFactory.create()

    print("🧩 Initializing Prompt Builder...")
    prompt_builder = PromptBuilder()

    print("🔗 Building RAG Service...")
    rag = RAGService(
        vector_store=vector_store,
        llm_client=llm_client,
        prompt_builder=prompt_builder
    )

    print("✅ Tutor Ready!\n")
    return rag

def main():
    try:
        rag = build_tutor()
    except Exception as e:
        print(f"\n❌ Failed to initialize Tutor: {e}")
        sys.exit(1)

    print("💡 Ask NCERT Questions (type 'exit' to quit)")

    while True:
        try:
            user_query = input("\n🧠 You: ").strip()

            if not user_query:
                continue

            if user_query.lower() in ['exit', 'quit']:
                print("👋 Exiting Tutor...")
                break

            # Start timer
            start_time = time.time()

            # Use the built-in debug wrapper from your rag_service.py
            rag.ask_with_debug(user_query)

            # Calculate and print latency
            latency = time.time() - start_time
            print(f"⏱ Latency: {latency:.2f} sec")

        except KeyboardInterrupt:
            print("\n👋 Exiting Tutor...")
            break
        except Exception as e:
            print(f"\n❌ An error occurred during query processing: {e}")

if __name__ == "__main__":
    main()
