from transformers import pipeline
import torch
from typing import List, Dict, Any, Union

class ZeroShotClassifier:
    """
    Multilingual Zero-Shot Classification using mDeBERTa-v3.
    Allows for dynamic categorization of text into user-defined labels.
    """
    def __init__(self, model_name: str = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self._classifier = None

    @property
    def classifier(self):
        if self._classifier is None:
            print(f"Loading Zero-Shot model: {self.model_name}...")
            self._classifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=self.device
            )
            print("Zero-Shot Model loaded successfully.")
        return self._classifier

    def classify(self, text: str, candidate_labels: List[str]) -> Dict[str, Any]:
        """
        Classifies the text into candidate labels.
        """
        if not candidate_labels:
            return {"label": "unknown", "score": 0.0}
            
        result = self.classifier(text, candidate_labels, multi_label=False)
        
        return {
            "label": result['labels'][0],
            "score": float(result['scores'][0])
        }
