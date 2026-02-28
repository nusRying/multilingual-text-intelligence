from bertopic import BERTopic
from typing import List, Dict, Any, Optional
import pandas as pd

class TopicEngine:
    """
    Topic discovery using BERTopic for multilingual text.
    """
    def __init__(self, language: str = "multilingual"):
        self.language = language
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading topic model (language={self.language})...")
            self._model = BERTopic(language=self.language, calculate_probabilities=True)
            print("Model loaded successfully.")
        return self._model

    def fit_transform(self, texts: List[str]) -> Dict[str, Any]:
        """
        Fits the model on texts and returns topics and their probabilities.
        """
        topics, probs = self.model.fit_transform(texts)
        
        # Get topic info summary
        topic_info = self.model.get_topic_info()
        
        return {
            "topics": topics,
            "probabilities": probs.tolist() if probs is not None else [],
            "info": topic_info.to_dict(orient="records")
        }

    def get_topic_details(self, topic_id: int) -> List[Dict[str, Any]]:
        """
        Returns the keywords and weights for a specific topic.
        """
        topic_words = self.model.get_topic(topic_id)
        if not topic_words:
            return []
        
        return [{"word": word, "weight": float(weight)} for word, weight in topic_words]

    def save(self, path: str):
        self.model.save(path)

    @classmethod
    def load(cls, path: str):
        instance = cls()
        instance.model = BERTopic.load(path)
        return instance
