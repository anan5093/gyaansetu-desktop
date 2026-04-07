import os
import json
import faiss
import numpy as np
from config import settings  # 🔥 Injecting centralized settings

# 🔥 SWITCH: ONNX or PyTorch
USE_ONNX = True

if USE_ONNX:
    from transformers import AutoTokenizer
    import onnxruntime as ort
else:
    from sentence_transformers import SentenceTransformer


class TutorVectorIndexBuilder:

    def __init__(
        self,
        class_id: int = None,
        subject: str = None,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.class_id = class_id or settings.CLASS_ID
        self.subject = (subject or settings.SUBJECT).lower()

        # Dynamically point to GyaanSetu/data/vector_store/classX/
        self.index_dir = os.path.join(
            settings.DATA_DIR,
            "vector_store",
            f"class{self.class_id}"
        )

        # 🔥 FIX: Read from the output of ChunkMerger (merged_chunks.json)
        self.chunk_path = os.path.join(
            settings.DATA_DIR,
            "chunks",
            f"class{self.class_id}",
            "merged_chunks.json"
        )

        self.index_file = os.path.join(self.index_dir, f"{self.subject}_faiss.index")
        self.meta_file = os.path.join(self.index_dir, f"{self.subject}_meta.json")

        print("🧠 Loading embedding model...")

        # 🔥 ONNX MODEL (FAST) - Using absolute paths to prevent crashes
        if USE_ONNX:
            onnx_dir = os.path.join(settings.BASE_DIR, "onnx_model")
            self.tokenizer = AutoTokenizer.from_pretrained(onnx_dir)
            self.session = ort.InferenceSession(
                os.path.join(onnx_dir, "model.onnx"),
                providers=["CPUExecutionProvider"]
            )
        else:
            self.model = SentenceTransformer(model_name, device="cpu")

    # ==============================
    # 📦 LOAD CHUNKS
    # ==============================
    def load_chunks(self):
        print(f"📖 Loading tutor chunks → {self.chunk_path}")
        
        if not os.path.exists(self.chunk_path):
            raise FileNotFoundError(f"❌ Chunk file not found at {self.chunk_path}. Run ingestion first.")

        with open(self.chunk_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"✅ Total chunks loaded: {len(chunks)}")
        return chunks

    # ==============================
    # 🔥 EMBEDDING (ONNX / TORCH)
    # ==============================
    # ==============================
    # 🔥 EMBEDDING (ONNX / TORCH)
    # ==============================
    def embed_chunks(self, chunks):

        texts = [c["text"] for c in chunks]
        print("🧠 Generating embeddings...")

        if USE_ONNX:
            batch_size = 32
            all_embeddings = []
            
            # 🔥 FIX: Feed the ONNX model in bites of 32 instead of all at once
            total_batches = (len(texts) + batch_size - 1) // batch_size
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                
                # Print progress so you know it hasn't frozen
                print(f"  → Processing batch {i//batch_size + 1}/{total_batches}...")
                
                batch_vectors = self._embed_onnx(batch_texts)
                all_embeddings.append(batch_vectors)
                
            # Combine all the small bites back into one big array
            vectors = np.vstack(all_embeddings)
        else:
            vectors = self.model.encode(
                texts,
                batch_size=32,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

        print("✅ Embeddings shape:", vectors.shape)
        return vectors

    # ==============================
    # 🔥 ONNX EMBEDDING
    # ==============================
    def _embed_onnx(self, texts):

        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="np"
        )

        outputs = self.session.run(
            None,
            dict(inputs)
        )

        embeddings = outputs[0]

        # 🔥 MEAN POOLING
        attention_mask = inputs["attention_mask"]
        mask_expanded = np.expand_dims(attention_mask, axis=-1)

        summed = np.sum(embeddings * mask_expanded, axis=1)
        counts = np.clip(mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)

        embeddings = summed / counts

        # 🔥 NORMALIZE (CRITICAL FOR FAISS)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms

        return embeddings

    # ==============================
    # 🔥 BUILD HNSW INDEX
    # ==============================
    # ==============================
    # 🔥 BUILD HNSW INDEX
    # ==============================
    def build_index(self, vectors):

        dim = vectors.shape[1]

        print("⚡ Building FAISS HNSW index...")

        # 🔥 FIX: Force vectors to be 32-bit floats and C-contiguous for FAISS C++ backend
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)

        # 🔥 Ensure normalized vectors
        faiss.normalize_L2(vectors)

        # 🔥 HNSW (FAST SEARCH)
        index = faiss.IndexHNSWFlat(dim, 16)  # M = 16

        index.hnsw.efConstruction = 200
        index.hnsw.efSearch = 64

        index.add(vectors)

        print("✅ Total vectors indexed:", index.ntotal)

        return index

    # ==============================
    # 🔥 SAVE INDEX
    # ==============================
    def save_index(self, index, chunks):

        os.makedirs(self.index_dir, exist_ok=True)

        print("💾 Saving FAISS index...")
        faiss.write_index(index, self.index_file)

        print("💾 Saving metadata mapping...")
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        print(f"✅ Index + metadata saved to {self.index_dir}")

    # ==============================
    # 🔥 RUN PIPELINE
    # ==============================
    def run(self):
        chunks = self.load_chunks()

        # 🔥 REMOVE DUPLICATES BEFORE EMBEDDING
        print("🧹 Deduplicating chunks...")

        seen = set()
        unique_chunks = []

        for c in chunks:
            key = c["text"].strip().lower()

            if key not in seen:
                seen.add(key)
                unique_chunks.append(c)

        print(f"✅ Reduced to {len(unique_chunks)} unique chunks")

        vectors = self.embed_chunks(unique_chunks)
        index = self.build_index(vectors)
        self.save_index(index, unique_chunks)


if __name__ == "__main__":
    # If run directly, it will build the index for whatever is default in settings.py
    builder = TutorVectorIndexBuilder()
    builder.run()
