from transformers import pipeline
import torch
from typing import List, Dict, Any, Union

class NERAnalyzer:
    """
    Multilingual Named Entity Recognition (NER) using XLM-RoBERTa.
    Detects People (PER), Organizations (ORG), and Locations (LOC).
    """
    def __init__(self, model_name: str = "Davlan/xlm-roberta-base-ner-hrl"):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self._ner_pipeline = None

    @property
    def ner_pipeline(self):
        if self._ner_pipeline is None:
            print(f"Loading NER model: {self.model_name}...")
            # aggregation_strategy="simple" groups subtokens into full words
            self._ner_pipeline = pipeline(
                "ner",
                model=self.model_name,
                device=self.device,
                aggregation_strategy="simple"
            )
            print("NER Model loaded successfully.")
        return self._ner_pipeline

    def extract_entities(self, texts: Union[str, List[str]]) -> List[List[Dict[str, Any]]]:
        """
        Extracts entities from given text(s).
        """
        if isinstance(texts, str):
            texts = [texts]
        
        results = self.ner_pipeline(texts)
        
        # Handle single vs multiple text output format from pipeline
        if isinstance(texts, str) or len(texts) == 1:
            if not isinstance(results[0], list):
                results = [results]

        formatted_results = []
        for text_entities in results:
            entities = []
            for ent in text_entities:
                entities.append({
                    "entity_group": ent['entity_group'],
                    "word": ent['word'],
                    "score": float(ent['score']),
                    "start": ent['start'],
                    "end": ent['end']
                })
            formatted_results.append(entities)
            
        return formatted_results
