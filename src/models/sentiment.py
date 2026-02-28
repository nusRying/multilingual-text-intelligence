from transformers import pipeline
import torch
from typing import List, Dict, Any, Union

class SentimentAnalyzer:
    """
    Multilingual sentiment analysis using XLM-RoBERTa.
    """
    def __init__(self, model_name: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self._analyzer = None
        # Map labels from model to human-readable sentiment
        self.label_map = {
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }

    @property
    def analyzer(self):
        if self._analyzer is None:
            print(f"Loading sentiment model: {self.model_name}...")
            self._analyzer = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=self.device
            )
            print("Model loaded successfully.")
        return self._analyzer

    def analyze(self, texts: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Analyzes the sentiment of given text(s).
        """
        if isinstance(texts, str):
            texts = [texts]
        
        with torch.no_grad():
            results = self.analyzer(texts)
        
        formatted_results = []
        for res in results:
            label = res['label']
            formatted_results.append({
                "sentiment": self.label_map.get(label, label),
                "confidence": float(res['score'])
            })
            
        return formatted_results
