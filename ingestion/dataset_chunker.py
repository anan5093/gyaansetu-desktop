import json
import os


class DatasetChunker:

    def __init__(
        self,
        input_path="data/cleaned_dataset/cleaned_rows.json",
        output_path="data/processed_chunks/chunks.json",
        chunk_size=350,
        overlap=60
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text):

        chunks = []

        start = 0
        length = len(text)

        while start < length:

            end = start + self.chunk_size

            # ⭐ try extend till sentence boundary
            if end < length:
                boundary = text.find(".", end)

                if boundary != -1 and boundary - end < 80:
                    end = boundary + 1

            chunk = text[start:end].strip()

            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks

    def build_chunks(self):

        print("📖 Loading cleaned dataset...")

        with open(self.input_path, "r", encoding="utf-8") as f:
            rows = json.load(f)

        all_chunks = []
        chunk_id = 0

        for row in rows:

            full_text = row["text"]

            # ⭐ split concept and QA
            if "Question:" in full_text:

                explanation_part = full_text.split("Question:")[0].strip()
                qa_part = "Question:" + full_text.split("Question:")[1].strip()

            else:
                explanation_part = full_text
                qa_part = None

            # ⭐ concept chunks
            concept_chunks = self.chunk_text(explanation_part)

            for c in concept_chunks:

                all_chunks.append({
                    "chunk_id": chunk_id,
                    "text": c,
                    "type": "concept",
                    "topic": row["topic"],
                    "difficulty": row["difficulty"],
                    "question_type": row["question_type"],
                    "complexity": row["complexity"]
                })

                chunk_id += 1

            # ⭐ QA chunk (single intact chunk)
            if qa_part:

                all_chunks.append({
                    "chunk_id": chunk_id,
                    "text": qa_part,
                    "type": "qa",
                    "topic": row["topic"],
                    "difficulty": row["difficulty"],
                    "question_type": row["question_type"],
                    "complexity": row["complexity"]
                })

                chunk_id += 1

        print(f"✅ Total chunks created: {len(all_chunks)}")

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)

        print(f"💾 Saved chunks at {self.output_path}")

        return all_chunks
