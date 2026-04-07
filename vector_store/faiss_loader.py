import faiss
import json
import os
import numpy as np
from config import settings # 🔥 Injecting centralized settings

# 🔥 SWITCH: ONNX vs PyTorch
USE_ONNX = True

if USE_ONNX:
    from transformers import AutoTokenizer
    import onnxruntime as ort
else:
    from sentence_transformers import SentenceTransformer


# ===============================
# 🔥 GLOBAL EMBEDDER (CACHED)
# ===============================
_EMBEDDER = None


def get_embedder():
    global _EMBEDDER

    if _EMBEDDER is None:
        print("🧠 Loading embedding model (once)...")

        if USE_ONNX:
            # Absolute paths for ONNX to prevent crash when running from web API folder
            onnx_dir = os.path.join(settings.BASE_DIR, "onnx_model")
            tokenizer = AutoTokenizer.from_pretrained(onnx_dir)
            session = ort.InferenceSession(
                os.path.join(onnx_dir, "model.onnx"),
                providers=["CPUExecutionProvider"]
            )
            _EMBEDDER = (tokenizer, session)

        else:
            _EMBEDDER = SentenceTransformer(
                "all-MiniLM-L6-v2",
                device="cpu"
            )

    return _EMBEDDER


# ===============================
# 📦 FAISS Loader (OPTIMIZED)
# ===============================
class FAISSLoader:

    def __init__(self, class_id=None, subject=None):

        self.class_id = class_id or settings.CLASS_ID
        self.subject = (subject or settings.SUBJECT).lower()

        # Dynamically map to GyaanSetu/data/vector_store/classX/
        self.index_path = os.path.join(
            settings.DATA_DIR,
            "vector_store",
            f"class{self.class_id}",
            f"{self.subject}_faiss.index"
        )

        self.meta_path = os.path.join(
            settings.DATA_DIR,
            "vector_store",
            f"class{self.class_id}",
            f"{self.subject}_meta.json"
        )

        print(f"📦 Loading FAISS index from {self.index_path}...")
        self.index = faiss.read_index(self.index_path)

        # 🔥 HNSW RUNTIME TUNING (CRITICAL)
        if isinstance(self.index, faiss.IndexHNSWFlat):
            self.index.hnsw.efSearch = 64

        print("📦 Loading metadata...")
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.meta = json.load(f)

        # 🔥 Cached embedder
        self.embedder = get_embedder()

    # ===============================
    # 🔥 ONNX QUERY EMBEDDING
    # ===============================
    def _embed_query_onnx(self, query):

        tokenizer, session = self.embedder

        inputs = tokenizer(
            [query],
            padding=True,
            truncation=True,
            return_tensors="np"
        )

        outputs = session.run(None, dict(inputs))
        embeddings = outputs[0]

        # 🔥 Mean pooling
        attention_mask = inputs["attention_mask"]
        mask_expanded = np.expand_dims(attention_mask, axis=-1)

        summed = np.sum(embeddings * mask_expanded, axis=1)
        counts = np.clip(mask_expanded.sum(axis=1), 1e-9, None)

        embeddings = summed / counts

        # 🔥 Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms

        return embeddings.astype("float32")

    # ===============================
    # 🔍 SEARCH (OPTIMIZED)
    # ===============================
    def search(self, query, k=None, score_threshold=None):
        
        # Dynamically pull from settings if not explicitly provided
        k = k or settings.TOP_K
        score_threshold = score_threshold if score_threshold is not None else settings.SCORE_THRESHOLD

        # 🔥 Fast embedding
        if USE_ONNX:
            qvec = self._embed_query_onnx(query)
        else:
            qvec = self.embedder.encode(
                [query],
                normalize_embeddings=True
            ).astype("float32")

        # 🔥 FAISS search
        scores, ids = self.index.search(qvec, k)

        results = []
        seen = set()

        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue

            # 🔥 FIX: Convert FAISS L2 Distance to Cosine Similarity (0.0 to 1.0)
            # Math: CosineSim = 1 - (L2_Distance / 2)
            cosine_sim = 1.0 - (float(score) / 2.0)

            # Now "Higher is Better" works perfectly with your settings.py!
            if cosine_sim < score_threshold:
                continue

            chunk = self.meta[idx]
            text = chunk.get("text", "")

            # 🔥 Deduplicate
            if text in seen:
                continue

            seen.add(text)

            result = chunk.copy()
            result["score"] = cosine_sim  # Save the readable percentage instead

            results.append(result)

        return results

        
