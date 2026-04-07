import json
import os
import re
from config import settings


class DatasetCleaner:
    """
    Stage 1 — Raw JSON → Cleaned + chunked rows.
    Reads from:  data/raw_dataset/class{id}/{subject}{id}.json
    Writes to:   data/cleaned_dataset/class{id}/cleaned_rows.json
    """

    def __init__(
        self,
        class_id: int = None,
        subject: str = None,
        base_data_dir: str = "data",
        chunk_size: int = 200,
        overlap: int = 40,
    ):
        self.class_id      = class_id or settings.CLASS_ID
        self.subject       = (subject or settings.SUBJECT).lower()
        self.base_data_dir = base_data_dir
        self.chunk_size    = chunk_size
        self.overlap       = overlap

        self.input_path = os.path.join(
            base_data_dir,
            "raw_dataset",
            f"class{self.class_id}",
            f"ncert_{self.subject}{self.class_id}.json",
        )
        self.output_path = os.path.join(
            base_data_dir,
            "cleaned_dataset",
            f"class{self.class_id}",
            "cleaned_rows.json",
        )

    # ==============================
    # ✂️ SENTENCE-AWARE CHUNKING
    # ==============================
    def chunk_text(self, text: str) -> list[str]:
        if len(text) < 50:
            return []

        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks        = []
        current_chunk = ""

        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue

            if len(current_chunk) + len(sent) + 1 <= self.chunk_size:
                current_chunk = (current_chunk + " " + sent).strip() if current_chunk else sent
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                overlap_text  = current_chunk[-self.overlap:] if current_chunk else ""
                current_chunk = (overlap_text + " " + sent).strip()

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    # ==============================
    # 🏗️ BUILD CLEANED DATASET
    # ==============================
    def build_clean_dataset(self) -> list[dict]:
        print(f"\n🧹 Cleaning dataset → Class {self.class_id} | Subject: {self.subject}")
        print(f"   Input : {self.input_path}")

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Raw dataset not found: {self.input_path}")

        with open(self.input_path, "r", encoding="utf-8") as f:
            rows = json.load(f)

        print(f"   Rows loaded: {len(rows)}")

        cleaned_rows = []
        seen_texts   = set()

        for row in rows:
            explanation = row.get("Explanation", "").strip()
            question    = row.get("Question", "").strip()
            answer      = row.get("Answer", "").strip()
            topic       = row.get("Topic", "").strip()

            merged_text = f"{topic}. {explanation} {question} {answer}".strip()
            chunks      = self.chunk_text(merged_text)

            for chunk in chunks:
                key = chunk.lower().strip()
                if key in seen_texts:
                    continue
                seen_texts.add(key)
                cleaned_rows.append({
                    "text":          chunk,
                    "topic":         topic,
                    "difficulty":    row.get("Difficulty"),
                    "question_type": row.get("QuestionType"),
                    "complexity":    row.get("QuestionComplexity"),
                    # ✅ NEW: track source for multi-dataset support
                    "source":        f"ncert_class{self.class_id}_{self.subject}",
                    "class_id":      self.class_id,
                    "subject":       self.subject,
                })

        print(f"✅ Cleaned rows created : {len(cleaned_rows)}")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_rows, f, ensure_ascii=False, indent=2)

        print(f"💾 Saved → {self.output_path}\n")
        return cleaned_rows


# ==============================
# 🏃 CLI RUNNER
# ==============================
if __name__ == "__main__":
    cleaner = DatasetCleaner()
    cleaner.build_clean_dataset()
