from sentence_transformers import SentenceTransformer
import torch
from typing import List, Union
import numpy as np

class EmbeddingGenerator:
    """
    Generates embeddings using multilingual transformer models.
    """
    def __init__(self, model_name: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name, device=self.device)
            print("Model loaded successfully.")
        return self._model

    def generate(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encodes text(s) into embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        with torch.no_grad():
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings

    def get_embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
