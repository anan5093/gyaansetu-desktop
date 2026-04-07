from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

model_id = "sentence-transformers/all-MiniLM-L6-v2"

print("⚡ Converting to ONNX...")

model = ORTModelForFeatureExtraction.from_pretrained(
    model_id,
    export=True
)

model.save_pretrained("onnx_model")

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained("onnx_model")

print("✅ ONNX model saved to ./onnx_model")
