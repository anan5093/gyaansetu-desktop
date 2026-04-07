import sys
import os

# Ensure Python knows where the GyaanSetu home folder is
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from config import settings
from vector_store.faiss_loader import FAISSLoader

def main():
    print(f"🔍 Testing FAISS Retrieval")
    print(f"📘 Target: Class {settings.CLASS_ID} | Subject: {settings.SUBJECT.capitalize()}")

    try:
        # This will automatically load the index based on settings.py
        vector_store = FAISSLoader()
    except Exception as e:
        print(f"\n❌ Failed to load FAISS index: {e}")
        sys.exit(1)

    # A classic Class 9 Physics question
    test_queries = [
        "What is the difference between distance and displacement?",
        "Calculate the number of electrons constituting one coulomb of charge."
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"❓ Query: {query}")
        print(f"{'='*60}")
        
        # Search the database (Pulling Top 3)
        results = vector_store.search(query, k=3)

        if not results:
            print("⚠️ No results found above the score threshold.")
        else:
            print(f"✅ Found {len(results)} relevant chunks:\n")
            for i, res in enumerate(results):
                score = res.get('score', 0)
                topic = res.get('topic', 'Unknown')
                text = res.get('text', '')
                
                print(f"--- Result {i+1} | Score: {score:.4f} ---")
                print(f"📑 Topic: {topic}")
                print(f"📝 Text: {text[:250]}...\n")

if __name__ == "__main__":
    main()
