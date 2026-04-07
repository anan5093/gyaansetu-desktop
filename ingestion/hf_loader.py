from datasets import load_dataset
import json
import os


class HFLoader:

    def __init__(self, class_id: int = 10, subject: str = "science"):
        """
        Dynamically sets the dataset repo and save path based on the class_id provided.
        """
        self.class_id = class_id
        
        if self.class_id == 9:
            self.dataset_name = "KadamParth/NCERT_Science_9th"
            self.save_path = f"data/raw_dataset/class9/ncert_{subject}9.json"
        else:
            self.dataset_name = "KadamParth/NCERT_Science_10th"
            self.save_path = f"data/raw_dataset/class10/ncert_{subject}10.json"

    def load(self):
        """
        Download dataset from HuggingFace and return list of rows
        """
        print(f"⬇️ Downloading dataset: {self.dataset_name} ...")

        ds = load_dataset(self.dataset_name)
        rows = list(ds["train"])

        print(f"✅ Dataset loaded. Total rows: {len(rows)}")
        return rows

    def save_local(self, rows):
        """
        Save dataset locally as JSON
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        print(f"💾 Saving dataset locally...")

        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved at {self.save_path}")

    def load_and_save(self):
        rows = self.load()
        self.save_local(rows)
        return rows

# Quick runner if executed directly
if __name__ == "__main__":
    # Example: To pull 9th grade
    loader = HFLoader(class_id=9)
    loader.load_and_save()
