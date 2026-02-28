import os
import torch
from optimum.exporters.onnx import main_export
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import argparse

def optimize_model(model_name: str, output_path: str):
    """
    Exports a HuggingFace model to ONNX format for faster inference.
    """
    print(f"Exporting {model_name} to ONNX...")
    try:
        main_export(
            model_name_or_path=model_name,
            output=output_path,
            task="sequence-classification",
            opset=13
        )
        print(f"Successfully exported to {output_path}")
    except Exception as e:
        print(f"Failed to export {model_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize HF models to ONNX")
    parser.add_argument("--model", type=str, required=True, help="HF model name")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    
    args = parser.parse_args()
    optimize_model(args.model, args.output)
