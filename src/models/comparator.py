import numpy as np
from typing import List, Dict, Any
from src.models.embeddings import EmbeddingGenerator

class TextComparator:
    """
    Compares texts using cosine similarity on their dense embeddings.
    Supports cross-lingual comparison (e.g., English vs Arabic).
    """
    def __init__(self, embedding_gen: EmbeddingGenerator = None):
        self.embedding_gen = embedding_gen or EmbeddingGenerator()

    def cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Computes cosine similarity between two vectors.
        """
        dot = np.dot(vec_a.flatten(), vec_b.flatten())
        norm_a = np.linalg.norm(vec_a.flatten())
        norm_b = np.linalg.norm(vec_b.flatten())
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

    def compare(self, text_a: str, text_b: str) -> Dict[str, Any]:
        """
        Compares two texts and returns their semantic similarity score.
        """
        emb_a = self.embedding_gen.generate(text_a)
        emb_b = self.embedding_gen.generate(text_b)
        
        similarity = self.cosine_similarity(emb_a, emb_b)
        
        return {
            "text_a": text_a[:100],
            "text_b": text_b[:100],
            "similarity": round(similarity, 4),
            "is_similar": similarity > 0.7
        }

    def find_duplicates(self, texts: List[str], threshold: float = 0.85) -> List[Dict[str, Any]]:
        """
        Finds near-duplicate texts in a batch.
        """
        embeddings = [self.embedding_gen.generate(t) for t in texts]
        duplicates = []
        
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = self.cosine_similarity(embeddings[i], embeddings[j])
                if sim >= threshold:
                    duplicates.append({
                        "index_a": i,
                        "index_b": j,
                        "text_a": texts[i][:80],
                        "text_b": texts[j][:80],
                        "similarity": round(sim, 4)
                    })
        
        return duplicates
