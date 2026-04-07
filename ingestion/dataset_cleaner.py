import json
import os
import re
from config import settings


class DatasetBuilder:
    """
    Stage 2 — Cleaned rows → Tutor chunks (concept + QA pairs).
    Reads from:  data/cleaned_dataset/class{id}/cleaned_rows.json
    Writes to:   data/chunks/class{id}/tutor_chunks.json

    Each chunk carries full metadata so FAISS results can be used
    directly in routes.py without post-processing.
    """

    # Maps known topic keywords → chapter names
    CHAPTER_MAP = {
        "chemical reaction":    "Chemical Reactions and Equations",
        "acid":                 "Acids, Bases and Salts",
        "base":                 "Acids, Bases and Salts",
        "salt":                 "Acids, Bases and Salts",
        "metal":                "Metals and Non-metals",
        "non-metal":            "Metals and Non-metals",
        "carbon":               "Carbon and its Compounds",
        "life process":         "Life Processes",
        "respiration":          "Life Processes",
        "photosynthesis":       "Life Processes",
        "control":              "Control and Coordination",
        "nervous":              "Control and Coordination",
        "hormone":              "Control and Coordination",
        "reproduction":         "How do Organisms Reproduce",
        "heredity":             "Heredity and Evolution",
        "evolution":            "Heredity and Evolution",
        "light":                "Light – Reflection and Refraction",
        "reflection":           "Light – Reflection and Refraction",
        "refraction":           "Light – Reflection and Refraction",
        "electricity":          "Electricity",
        "magnetic":             "Magnetic Effects of Electric Current",
        "energy":               "Sources of Energy",
        "environment":          "Our Environment",
        "ecosystem":            "Our Environment",
        "natural resource":     "Management of Natural Resources",
    }

    def __init__(
        self,
        class_id: int = None,
        subject: str = None,
        base_data_dir: str = "data",
    ):
        self.class_id      = class_id or settings.CLASS_ID
        self.subject       = (subject or settings.SUBJECT).lower()
        self.base_data_dir = base_data_dir

        self.input_path = os.path.join(
            base_data_dir,
            "cleaned_dataset",
            f"class{self.class_id}",
            "cleaned_rows.json",
        )
        self.output_path = os.path.join(
            base_data_dir,
            "chunks",
            f"class{self.class_id}",
            "tutor_chunks.json",
        )

    # ==============================
    # 📖 CHAPTER INFERENCE
    # ==============================
    def _infer_chapter(self, topic: str) -> str:
        if not topic:
            return "General"
        topic_lower = topic.lower()
        for keyword, chapter in self.CHAPTER_MAP.items():
            if keyword in topic_lower:
                return chapter
        return topic  # Fallback: use topic itself

    # ==============================
    # 🖊️ CONCEPT CHUNK FORMATTER
    # ==============================
    def _format_concept(self, topic: str, explanation: str) -> str:
        return (
            f"=== CONCEPT ===\n"
            f"Topic: {topic}\n"
            f"Explanation: {explanation}"
        )

    # ==============================
    # ❓ QA CHUNK FORMATTER
    # ==============================
    def _format_qa(
        self,
        topic: str,
        difficulty: str,
        qtype: str,
        question: str,
        answer: str,
    ) -> str:
        return (
            f"=== EXAM QUESTION ===\n"
            f"Topic: {topic}\n"
            f"Difficulty: {difficulty} | Type: {qtype}\n"
            f"Question: {question}\n"
            f"Answer: {answer}"
        )

    # ==============================
    # 🏗️ BUILD TUTOR CHUNKS
    # ==============================
    def build_chunks(self) -> list[dict]:
        print(f"\n📦 Building tutor chunks → Class {self.class_id} | Subject: {self.subject}")
        print(f"   Input : {self.input_path}")

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(
                f"Cleaned dataset not found: {self.input_path}\n"
                f"Run DatasetCleaner.build_clean_dataset() first."
            )

        with open(self.input_path, "r", encoding="utf-8") as f:
            rows = json.load(f)

        print(f"   Cleaned rows loaded: {len(rows)}")

        all_chunks  = []
        seen_chunks = set()
        chunk_id    = 0

        for row in rows:
            text       = row.get("text", "")
            topic      = row.get("topic", "")
            difficulty = row.get("difficulty")
            qtype      = row.get("question_type")
            complexity = row.get("complexity")
            source     = row.get("source", f"ncert_class{self.class_id}_{self.subject}")
            chapter    = self._infer_chapter(topic)

            # Parse structured fields out of merged text
            explanation_match = re.search(r"Explanation:(.*?)Question:", text, re.DOTALL)
            question_match    = re.search(r"Question:(.*?)Answer:", text, re.DOTALL)
            answer_match      = re.search(r"Answer:(.*)", text, re.DOTALL)

            explanation = explanation_match.group(1).strip() if explanation_match else ""
            question    = question_match.group(1).strip()    if question_match    else ""
            answer      = answer_match.group(1).strip()      if answer_match      else ""

            # ── Concept chunk ──────────────────────────────────────────
            if explanation and len(explanation) > 50:
                concept_text = self._format_concept(topic, explanation)
                key = concept_text.lower().strip()
                if key not in seen_chunks:
                    seen_chunks.add(key)
                    all_chunks.append({
                        "chunk_id":     chunk_id,
                        "text":         concept_text,
                        "type":         "concept",
                        "topic":        topic,
                        "class":        self.class_id,
                        "subject":      self.subject,
                        "chapter":      chapter,
                        "difficulty":   difficulty,
                        "question_type": qtype,
                        "complexity":   complexity,
                        "source":       source,
                    })
                    chunk_id += 1

            # ── QA chunk ───────────────────────────────────────────────
            if question and answer:
                qa_text = self._format_qa(topic, difficulty, qtype, question, answer)
                key = qa_text.lower().strip()
                if key not in seen_chunks:
                    seen_chunks.add(key)
                    all_chunks.append({
                        "chunk_id":     chunk_id,
                        "text":         qa_text,
                        "type":         "qa",
                        "topic":        topic,
                        "class":        self.class_id,
                        "subject":      self.subject,
                        "chapter":      chapter,
                        "difficulty":   difficulty,
                        "question_type": qtype,
                        "complexity":   complexity,
                        "source":       source,
                    })
                    chunk_id += 1

        print(f"✅ Total tutor chunks created : {len(all_chunks)}")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)

        print(f"💾 Saved → {self.output_path}\n")
        return all_chunks


# ==============================
# 🏃 CLI RUNNER
# ==============================
if __name__ == "__main__":
    builder = DatasetBuilder()
    builder.build_chunks()
