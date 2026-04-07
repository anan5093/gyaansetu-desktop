import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
from config import settings


# ==============================
# 🧠 EMBEDDER
# ==============================
class Embedder:
    """
    CPU-optimized text embedder using sentence-transformers.
    Used by FAISSLoader to embed both stored chunks and query strings.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print("🧠 Loading embedding model (CPU optimized)...")
        self.model = SentenceTransformer(model_name, device="cpu")
        print(f"✅ Embedder ready → {model_name}")

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a list of strings. Returns normalized float32 numpy array."""
        return self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,   # Required for cosine similarity in FAISS
            show_progress_bar=len(texts) > 100,
        )

    def embed_query(self, query: str) -> np.ndarray:
        """Single query embedding — used at retrieval time."""
        return self.embed([query])[0]


# ==============================
# 🌐 HUGGINGFACE MULTI-DATASET LOADER
# ==============================
class HuggingFaceDatasetLoader:
    """
    Loads one or more HuggingFace datasets and converts them into
    the standard chunk format used throughout GyaanSetu.
    """

    # ==============================
    # 📋 DATASET REGISTRY
    # ==============================
    HF_DATASETS = [
        {
            "repo": "KadamParth/NCERT_Science_9th",
            "split": "train",
            "columns": {
                "text": "Explanation",  # The KadamParth dataset uses 'Explanation' for core text
                "topic": "Topic",
                "chapter": "Topic",     # Fallback since chapter isn't explicitly defined
                "type": None,           # Will default to "hf_text"
            },
            "source": "hf_kadamparth_9th",
            "class_id": 9,
            "subject": "science",
        }
    ]

    def __init__(self, min_text_length: int = 40):
        self.min_text_length = min_text_length

    def load_all(self) -> list[dict]:
        """
        Loads all registered HuggingFace datasets and returns
        a merged list of standard chunks.
        """
        all_chunks = []

        if not self.HF_DATASETS:
            print("ℹ️  No HuggingFace datasets registered in HF_DATASETS.")
            return all_chunks

        for entry in self.HF_DATASETS:
            chunks = self._load_one(entry)
            print(f"   → {entry['source']}: {len(chunks)} chunks loaded")
            all_chunks.extend(chunks)

        print(f"\n✅ Total HuggingFace chunks loaded: {len(all_chunks)}")
        return all_chunks

    def _load_one(self, entry: dict) -> list[dict]:
        print(f"\n📥 Loading HuggingFace dataset: {entry['repo']} ({entry['split']})")
        try:
            ds      = load_dataset(entry["repo"], split=entry["split"])
            columns = entry.get("columns", {})
            chunks  = []

            for row in ds:
                text_col = columns.get("text")
                text     = row.get(text_col, "").strip() if text_col else ""

                if len(text) < self.min_text_length:
                    continue

                topic_col   = columns.get("topic")
                chapter_col = columns.get("chapter")
                type_col    = columns.get("type")

                chunks.append({
                    "text":    text,
                    "topic":   row.get(topic_col, "General") if topic_col else "General",
                    "chapter": row.get(chapter_col, "General") if chapter_col else "General",
                    "type":    row.get(type_col, "hf_text") if type_col else "hf_text",
                    "source":  entry.get("source", entry["repo"]),
                    "class":   entry.get("class_id", settings.CLASS_ID),
                    "subject": entry.get("subject", settings.SUBJECT),
                    "difficulty":    None,
                    "question_type": None,
                    "complexity":    None,
                })

            return chunks

        except Exception as e:
            print(f"⚠️  Failed to load {entry['repo']}: {e}")
            return []


# ==============================
# 🔀 CHUNK MERGER
# ==============================
class ChunkMerger:
    """
    Merges local tutor chunks with any HuggingFace
    chunks into a single deduplicated list ready for FAISS ingestion.
    """

    def __init__(self, class_id: int = None, subject: str = None, base_data_dir: str = "data"):
        self.class_id      = class_id or settings.CLASS_ID
        self.subject       = (subject or settings.SUBJECT).lower()
        self.local_path    = os.path.join(
            base_data_dir, "chunks", f"class{self.class_id}", "tutor_chunks.json"
        )
        self.merged_path   = os.path.join(
            base_data_dir, "chunks", f"class{self.class_id}", "merged_chunks.json"
        )

    def merge(self, hf_chunks: list[dict] = None) -> list[dict]:
        """
        Loads local chunks, merges with hf_chunks, deduplicates,
        saves merged_chunks.json, and returns the list.
        """
        local_chunks = []
        if os.path.exists(self.local_path):
            with open(self.local_path, "r", encoding="utf-8") as f:
                local_chunks = json.load(f)
            print(f"📂 Local chunks loaded : {len(local_chunks)}")
        else:
            print(f"⚠️  No local chunks at {self.local_path} — using HF only")

        hf_chunks = hf_chunks or []
        combined  = local_chunks + hf_chunks

        # Deduplicate on text content
        seen    = set()
        merged  = []
        for chunk in combined:
            key = chunk.get("text", "").lower().strip()
            if key and key not in seen:
                seen.add(key)
                merged.append(chunk)

        # Re-assign sequential chunk_ids
        for i, chunk in enumerate(merged):
            chunk["chunk_id"] = i

        print(f"✅ Merged chunks (deduped) : {len(merged)}")
        os.makedirs(os.path.dirname(self.merged_path), exist_ok=True)
        with open(self.merged_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved → {self.merged_path}\n")

        return merged


# ==============================
# 🏃 CLI
# ==============================
if __name__ == "__main__":
    import sys
    if "--ingest" in sys.argv:
        print("\n🚀 Running full ingest pipeline...\n")
        hf_loader = HuggingFaceDatasetLoader()
        hf_chunks = hf_loader.load_all()

        merger    = ChunkMerger()
        merged    = merger.merge(hf_chunks)

        embedder  = Embedder()
        texts     = [c["text"] for c in merged]
        print(f"\n🔢 Embedding {len(texts)} chunks...")
        vectors   = embedder.embed(texts)
        print(f"✅ Embeddings shape: {vectors.shape}")
    else:
        print("Usage: python embedder.py --ingest")
        print("       Runs HuggingFace load → merge → embed pipeline.")
