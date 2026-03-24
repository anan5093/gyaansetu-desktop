import json
import os
import re


class DatasetChunker:

    def __init__(
        self,
        input_path="data/cleaned_dataset/cleaned_rows.json",
        output_path="data/processed_chunks/chunks.json",
        chunk_size=220,
        overlap=40
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.chunk_size = chunk_size
        self.overlap = overlap

def chunk_text(self, text):



    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sent in sentences:

        sent = sent.strip()
        if not sent:
            continue

        # ⭐ Case 1 — sentence itself too large
        if len(sent) > self.chunk_size:

            # flush current
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # hard slice long sentence
            start = 0
            while start < len(sent):
                part = sent[start:start + self.chunk_size]
                chunks.append(part.strip())
                start += self.chunk_size - self.overlap

            continue

        # ⭐ Case 2 — normal packing
        if len(current_chunk) + len(sent) + 1 <= self.chunk_size:

            if current_chunk:
                current_chunk += " " + sent
            else:
                current_chunk = sent

        else:

            chunks.append(current_chunk.strip())

            overlap_text = (
                current_chunk[-self.overlap:]
                if len(current_chunk) > self.overlap
                else current_chunk
            )

            current_chunk = overlap_text + " " + sent

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
    def build_chunks(self):

        print("📖 Loading cleaned dataset...")

        with open(self.input_path, "r", encoding="utf-8") as f:
            rows = json.load(f)

        all_chunks = []
        chunk_id = 0

        for row in rows:

            text_chunks = self.chunk_text(row["text"])

            for c in text_chunks:

                all_chunks.append({
                    "chunk_id": chunk_id,
                    "text": c,
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
