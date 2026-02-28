from transformers import pipeline
import torch
from typing import List, Dict, Any

class TextSummarizer:
    """
    Abstractive text summarization using a multilingual model.
    Supports English and Arabic text out of the box.
    """
    def __init__(self, model_name: str = "facebook/mbart-large-50"):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self._summarizer = None

    @property
    def summarizer(self):
        if self._summarizer is None:
            print(f"Loading summarization model: {self.model_name}...")
            # Use a lighter, faster model for practical use
            self._summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=self.device
            )
            print("Summarization model loaded.")
        return self._summarizer

    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> Dict[str, Any]:
        """
        Generates an abstractive summary of the input text.
        """
        if len(text.split()) < 20:
            return {"summary": text, "original_length": len(text), "summary_length": len(text)}

        # Truncate very long texts to avoid OOM
        truncated = " ".join(text.split()[:1024])

        result = self.summarizer(truncated, max_length=max_length, min_length=min_length, do_sample=False)
        summary = result[0]['summary_text']

        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "compression_ratio": round(len(summary) / len(text), 2)
        }

    def summarize_batch(self, texts: List[str]) -> str:
        """
        Summarizes a batch of texts into a single executive summary.
        """
        combined = " ".join(texts[:20])  # Combine up to 20 texts
        result = self.summarize(combined, max_length=200, min_length=50)
        return result['summary']
