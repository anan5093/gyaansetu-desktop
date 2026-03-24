from datasets import load_dataset
import json
import os


class HFLoader:

    def __init__(
        self,
        dataset_name: str = "KadamParth/NCERT_Science_10th",
        save_path: str = "data/raw_dataset/ncert_science10.json"
    ):
        self.dataset_name = dataset_name
        self.save_path = save_path

    def load(self):
        """
        Download dataset from HuggingFace and return list of rows
        """
        print("⬇️ Downloading dataset from HuggingFace...")

        ds = load_dataset(self.dataset_name)

        rows = list(ds["train"])

        print(f"✅ Dataset loaded. Total rows: {len(rows)}")

        return rows

    def save_local(self, rows):
        """
        Save dataset locally as JSON
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        print("💾 Saving dataset locally...")

        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved at {self.save_path}")

    def load_and_save(self):
        rows = self.load()
        self.save_local(rows)
        return rows
