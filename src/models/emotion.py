from transformers import pipeline
import torch
from typing import List, Dict, Any, Union

class EmotionAnalyzer:
    """
    Emotion recognition using DistilRoBERTa.
    Identifies: anger, disgust, fear, joy, sadness, surprise, neutral.
    """
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self._emotion_pipeline = None

    @property
    def emotion_pipeline(self):
        if self._emotion_pipeline is None:
            print(f"Loading emotion model: {self.model_name}...")
            self._emotion_pipeline = pipeline(
                "sentiment-analysis", # Emotion is often a sub-task of sentiment in transformers
                model=self.model_name,
                device=self.device
            )
            print("Emotion Model loaded successfully.")
        return self._emotion_pipeline

    def analyze(self, texts: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Detects emotions in given text(s).
        """
        if isinstance(texts, str):
            texts = [texts]
        
        results = self.emotion_pipeline(texts)
        
        formatted_results = []
        for res in results:
            formatted_results.append({
                "emotion": res['label'],
                "confidence": float(res['score'])
            })
            
        return formatted_results
