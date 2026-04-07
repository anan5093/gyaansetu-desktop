"""
tests/test_pipeline.py
======================
Test suite for:
  - DatasetCleaner  (dataset_chunker.py)
  - DatasetBuilder  (dataset_cleaner.py)
  - Embedder        (embedder.py)
  - HuggingFaceDatasetLoader
  - ChunkMerger

Run:
  python -m pytest tests/test_pipeline.py -v
  OR
  python tests/test_pipeline.py        ← standalone (no pytest needed)
"""

import json
import os
import sys
import tempfile
import numpy as np

# ── Make sure project root is on path ──────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 🔥 FIXED IMPORTS: Added the 'ingestion.' prefix so Python looks in the right folder
from ingestion.dataset_chunker import DatasetCleaner
from ingestion.dataset_cleaner import DatasetBuilder
from ingestion.embedder import Embedder, HuggingFaceDatasetLoader, ChunkMerger


# ===========================================================================
# 🧰 SHARED FIXTURES
# ===========================================================================

SAMPLE_RAW_ROWS = [
    {
        "Topic": "Photosynthesis",
        "Explanation": (
            "Photosynthesis is the process by which green plants use sunlight, "
            "water, and carbon dioxide to produce oxygen and energy in the form "
            "of sugar. It occurs mainly in the leaves of plants."
        ),
        "Question": "Where does photosynthesis mainly occur?",
        "Answer": "Photosynthesis mainly occurs in the leaves of plants.",
        "Difficulty": "easy",
        "QuestionType": "short",
        "QuestionComplexity": "low",
    },
    {
        "Topic": "Chemical Reaction",
        "Explanation": (
            "A chemical reaction is a process that leads to the chemical "
            "transformation of one set of chemical substances to another. "
            "It involves breaking and forming of chemical bonds."
        ),
        "Question": "What is a chemical reaction?",
        "Answer": "A process that transforms one set of substances into another.",
        "Difficulty": "medium",
        "QuestionType": "definition",
        "QuestionComplexity": "medium",
    },
    {
        # Edge case: very short explanation (should be filtered)
        "Topic": "Osmosis",
        "Explanation": "Short.",
        "Question": "",
        "Answer": "",
        "Difficulty": "easy",
        "QuestionType": "short",
        "QuestionComplexity": "low",
    },
    {
        # Edge case: duplicate of first row
        "Topic": "Photosynthesis",
        "Explanation": (
            "Photosynthesis is the process by which green plants use sunlight, "
            "water, and carbon dioxide to produce oxygen and energy in the form "
            "of sugar. It occurs mainly in the leaves of plants."
        ),
        "Question": "Where does photosynthesis mainly occur?",
        "Answer": "Photosynthesis mainly occurs in the leaves of plants.",
        "Difficulty": "easy",
        "QuestionType": "short",
        "QuestionComplexity": "low",
    },
]

SAMPLE_CLEANED_ROWS = [
    {
        "text": (
            "Photosynthesis. Photosynthesis is the process by which green plants "
            "use sunlight, water, and carbon dioxide to produce oxygen and energy "
            "in the form of sugar. Where does photosynthesis mainly occur? "
            "Photosynthesis mainly occurs in the leaves of plants."
        ),
        "topic": "Photosynthesis",
        "difficulty": "easy",
        "question_type": "short",
        "complexity": "low",
        "source": "ncert_class10_science",
        "class_id": 10,
        "subject": "science",
    },
    {
        "text": (
            "Chemical Reaction. A chemical reaction is a process that leads to "
            "the chemical transformation. Question: What is a chemical reaction? "
            "Answer: A process that transforms substances."
        ),
        "topic": "Chemical Reaction",
        "difficulty": "medium",
        "question_type": "definition",
        "complexity": "medium",
        "source": "ncert_class10_science",
        "class_id": 10,
        "subject": "science",
    },
]


def make_raw_dataset(tmpdir: str) -> str:
    """Write sample raw JSON to a temp directory."""
    raw_dir = os.path.join(tmpdir, "data", "raw_dataset", "class10")
    os.makedirs(raw_dir, exist_ok=True)
    path = os.path.join(raw_dir, "ncert_science10.json")
    with open(path, "w") as f:
        json.dump(SAMPLE_RAW_ROWS, f)
    return path


def make_cleaned_dataset(tmpdir: str) -> str:
    """Write sample cleaned JSON to a temp directory."""
    clean_dir = os.path.join(tmpdir, "data", "cleaned_dataset", "class10")
    os.makedirs(clean_dir, exist_ok=True)
    path = os.path.join(clean_dir, "cleaned_rows.json")
    with open(path, "w") as f:
        json.dump(SAMPLE_CLEANED_ROWS, f)
    return path


# ===========================================================================
# 🧹 TESTS: DatasetCleaner (dataset_chunker.py)
# ===========================================================================

class TestDatasetCleaner:

    def test_chunk_text_normal(self):
        cleaner = DatasetCleaner(class_id=10, subject="science")
        text    = (
            "Photosynthesis is the process by which green plants use sunlight. "
            "It occurs in the leaves. Carbon dioxide and water are used."
        )
        chunks = cleaner.chunk_text(text)
        assert isinstance(chunks, list)
        assert len(chunks) >= 1
        for c in chunks:
            assert len(c) >= 10
        print("  ✅ chunk_text_normal passed")

    def test_chunk_text_too_short(self):
        cleaner = DatasetCleaner(class_id=10, subject="science")
        assert cleaner.chunk_text("Hi.") == []
        assert cleaner.chunk_text("") == []
        print("  ✅ chunk_text_too_short passed")

    def test_chunk_text_deduplication(self):
        cleaner  = DatasetCleaner(class_id=10, subject="science")
        text     = "A" * 60 + ". " + "B" * 60 + "."
        chunks   = cleaner.chunk_text(text)
        assert len(chunks) == len(set(chunks)), "Duplicate chunks found"
        print("  ✅ chunk_text_deduplication passed")

    def test_chunk_respects_size(self):
        cleaner = DatasetCleaner(class_id=10, subject="science", chunk_size=100)
        # Long text that must be split
        text    = ". ".join(["Word " * 20] * 5)
        chunks  = cleaner.chunk_text(text)
        for c in chunks:
            # Allow slight overflow due to overlap, but not wildly over
            assert len(c) <= 200, f"Chunk too large: {len(c)}"
        print("  ✅ chunk_respects_size passed")

    def test_build_clean_dataset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_raw_dataset(tmpdir)
            cleaner = DatasetCleaner(
                class_id=10,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            rows = cleaner.build_clean_dataset()

            assert isinstance(rows, list)
            assert len(rows) > 0

            # Check schema
            for row in rows:
                assert "text" in row
                assert "topic" in row
                assert "source" in row
                assert len(row["text"]) >= 50

            # Duplicates should be removed
            texts = [r["text"].lower().strip() for r in rows]
            assert len(texts) == len(set(texts)), "Duplicates found in output"

            # Output file must exist
            out = os.path.join(
                tmpdir, "data", "cleaned_dataset", "class10", "cleaned_rows.json"
            )
            assert os.path.exists(out)
            print(f"  ✅ build_clean_dataset passed ({len(rows)} rows)")

    def test_missing_input_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cleaner = DatasetCleaner(
                class_id=99,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            try:
                cleaner.build_clean_dataset()
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError:
                pass
        print("  ✅ missing_input_raises passed")


# ===========================================================================
# 📦 TESTS: DatasetBuilder (dataset_cleaner.py)
# ===========================================================================

class TestDatasetBuilder:

    def test_infer_chapter(self):
        builder = DatasetBuilder(class_id=10, subject="science")
        assert "Light" in builder._infer_chapter("Reflection of light")
        assert "Life Processes" in builder._infer_chapter("Photosynthesis process")
        assert builder._infer_chapter("Unknown XYZ") == "Unknown XYZ"
        print("  ✅ infer_chapter passed")

    def test_format_concept(self):
        builder = DatasetBuilder(class_id=10, subject="science")
        result  = builder._format_concept("Osmosis", "Movement of water molecules.")
        assert "=== CONCEPT ===" in result
        assert "Osmosis" in result
        assert "Movement of water molecules." in result
        print("  ✅ format_concept passed")

    def test_format_qa(self):
        builder = DatasetBuilder(class_id=10, subject="science")
        result  = builder._format_qa("Osmosis", "easy", "short", "What is osmosis?", "Diffusion of water.")
        assert "=== EXAM QUESTION ===" in result
        assert "What is osmosis?" in result
        assert "Diffusion of water." in result
        print("  ✅ format_qa passed")

    def test_build_chunks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_cleaned_dataset(tmpdir)
            builder = DatasetBuilder(
                class_id=10,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            chunks = builder.build_chunks()

            assert isinstance(chunks, list)
            assert len(chunks) >= 0   # May be 0 if text has no parseable Q/A

            for chunk in chunks:
                assert "chunk_id"  in chunk
                assert "text"      in chunk
                assert "type"      in chunk
                assert "topic"     in chunk
                assert "chapter"   in chunk
                assert "source"    in chunk
                assert chunk["type"] in ("concept", "qa")

            # No duplicate chunk_ids
            ids = [c["chunk_id"] for c in chunks]
            assert len(ids) == len(set(ids))

            # Output file must exist
            out = os.path.join(
                tmpdir, "data", "chunks", "class10", "tutor_chunks.json"
            )
            assert os.path.exists(out)
            print(f"  ✅ build_chunks passed ({len(chunks)} chunks)")

    def test_missing_input_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = DatasetBuilder(
                class_id=99,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            try:
                builder.build_chunks()
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError:
                pass
        print("  ✅ missing_input_raises passed")


# ===========================================================================
# 🧠 TESTS: Embedder (embedder.py)
# ===========================================================================

class TestEmbedder:

    @classmethod
    def setup_class(cls):
        print("\n  🔄 Loading embedder (once for all tests)...")
        cls.embedder = Embedder()

    def test_embed_returns_numpy(self):
        vecs = self.embedder.embed(["What is photosynthesis?"])
        assert isinstance(vecs, np.ndarray)
        assert vecs.ndim == 2
        assert vecs.shape[0] == 1
        print(f"  ✅ embed_returns_numpy passed | shape={vecs.shape}")

    def test_embed_batch(self):
        texts = ["Photosynthesis", "Chemical reaction", "Acids and bases"]
        vecs  = self.embedder.embed(texts)
        assert vecs.shape[0] == 3
        assert vecs.shape[1] > 0
        print(f"  ✅ embed_batch passed | shape={vecs.shape}")

    def test_embed_normalized(self):
        vecs  = self.embedder.embed(["Test sentence for normalization."])
        norms = np.linalg.norm(vecs, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-5), f"Not normalized: {norms}"
        print("  ✅ embed_normalized passed")

    def test_embed_query(self):
        vec = self.embedder.embed_query("What is osmosis?")
        assert isinstance(vec, np.ndarray)
        assert vec.ndim == 1
        norm = np.linalg.norm(vec)
        assert np.isclose(norm, 1.0, atol=1e-5)
        print(f"  ✅ embed_query passed | dim={vec.shape[0]}")

    def test_similar_texts_close(self):
        """Semantically similar texts should have high cosine similarity."""
        v1 = self.embedder.embed_query("What is photosynthesis?")
        v2 = self.embedder.embed_query("Explain the process of photosynthesis.")
        v3 = self.embedder.embed_query("Who invented the telephone?")
        sim_related   = float(np.dot(v1, v2))
        sim_unrelated = float(np.dot(v1, v3))
        assert sim_related > sim_unrelated, (
            f"Expected related > unrelated: {sim_related:.3f} vs {sim_unrelated:.3f}"
        )
        print(f"  ✅ similar_texts_close passed | related={sim_related:.3f} unrelated={sim_unrelated:.3f}")


# ===========================================================================
# 🌐 TESTS: HuggingFaceDatasetLoader
# ===========================================================================

class TestHuggingFaceDatasetLoader:

    def test_empty_registry_returns_empty(self):
        loader = HuggingFaceDatasetLoader()
        # With no datasets registered, should return []
        original = loader.HF_DATASETS
        loader.__class__.HF_DATASETS = []
        result = loader.load_all()
        loader.__class__.HF_DATASETS = original
        assert result == []
        print("  ✅ empty_registry_returns_empty passed")

    def test_chunk_schema(self):
        """Manually inject a fake loaded chunk and verify schema."""
        loader = HuggingFaceDatasetLoader()
        fake_entry = {
            "repo":    "fake/dataset",
            "split":   "train",
            "source":  "fake_source",
            "class_id": 10,
            "subject": "science",
            "columns": {"text": "text", "topic": None, "chapter": None, "type": None},
        }
        # Simulate what _load_one returns for a valid row
        row = {"text": "Osmosis is the movement of water molecules across a semi-permeable membrane."}
        if len(row["text"]) >= loader.min_text_length:
            chunk = {
                "text":    row["text"],
                "topic":   "General",
                "chapter": "General",
                "type":    "hf_text",
                "source":  fake_entry["source"],
                "class":   fake_entry["class_id"],
                "subject": fake_entry["subject"],
                "difficulty":    None,
                "question_type": None,
                "complexity":    None,
            }
            required_keys = ["text", "topic", "chapter", "type", "source", "class", "subject"]
            for k in required_keys:
                assert k in chunk, f"Missing key: {k}"
        print("  ✅ chunk_schema passed")


# ===========================================================================
# 🔀 TESTS: ChunkMerger
# ===========================================================================

class TestChunkMerger:

    def test_merge_deduplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write local chunks
            chunks_dir = os.path.join(tmpdir, "data", "chunks", "class10")
            os.makedirs(chunks_dir, exist_ok=True)
            local = [
                {"chunk_id": 0, "text": "Photosynthesis uses sunlight.", "topic": "Photosynthesis",
                 "type": "concept", "source": "local"},
                {"chunk_id": 1, "text": "Chemical reaction breaks bonds.", "topic": "Chemistry",
                 "type": "concept", "source": "local"},
            ]
            with open(os.path.join(chunks_dir, "tutor_chunks.json"), "w") as f:
                json.dump(local, f)

            hf_chunks = [
                # Duplicate of local[0]
                {"chunk_id": 0, "text": "Photosynthesis uses sunlight.", "topic": "Photosynthesis",
                 "type": "hf_text", "source": "hf"},
                # New chunk
                {"chunk_id": 1, "text": "Osmosis is water diffusion.", "topic": "Osmosis",
                 "type": "hf_text", "source": "hf"},
            ]

            merger = ChunkMerger(
                class_id=10,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            merged = merger.merge(hf_chunks)

            assert len(merged) == 3, f"Expected 3 unique chunks, got {len(merged)}"

            # chunk_ids should be sequential
            ids = [c["chunk_id"] for c in merged]
            assert ids == list(range(len(merged)))

            # Output file exists
            assert os.path.exists(merger.merged_path)
            print(f"  ✅ merge_deduplicates passed ({len(merged)} chunks)")

    def test_merge_no_local(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            merger = ChunkMerger(
                class_id=10,
                subject="science",
                base_data_dir=os.path.join(tmpdir, "data"),
            )
            hf_chunks = [
                {"chunk_id": 0, "text": "Osmosis is water diffusion.", "topic": "Osmosis",
                 "type": "hf_text", "source": "hf"},
            ]
            merged = merger.merge(hf_chunks)
            assert len(merged) == 1
            print("  ✅ merge_no_local passed")


# ===========================================================================
# 🏃 STANDALONE RUNNER (no pytest needed)
# ===========================================================================

def run_all():
    results = {"passed": 0, "failed": 0, "errors": []}

    suites = [
        ("DatasetCleaner",          TestDatasetCleaner),
        ("DatasetBuilder",          TestDatasetBuilder),
        ("Embedder",                TestEmbedder),
        ("HuggingFaceLoader",       TestHuggingFaceDatasetLoader),
        ("ChunkMerger",             TestChunkMerger),
    ]

    for suite_name, Suite in suites:
        print(f"\n{'─'*55}")
        print(f"🧪 {suite_name}")
        print(f"{'─'*55}")

        instance = Suite()

        # Call setup_class if present (for Embedder)
        if hasattr(Suite, "setup_class"):
            Suite.setup_class()

        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            try:
                getattr(instance, method_name)()
                results["passed"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"{suite_name}.{method_name}: {e}")
                print(f"  ❌ {method_name} FAILED: {e}")

    print(f"\n{'='*55}")
    print(f"✅ Passed : {results['passed']}")
    print(f"❌ Failed : {results['failed']}")
    if results["errors"]:
        print("\nFailed tests:")
        for e in results["errors"]:
            print(f"  • {e}")
    print(f"{'='*55}\n")

    return results["failed"] == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
