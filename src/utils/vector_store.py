import faiss
import numpy as np
import os
from typing import List, Dict, Any

class LocalVectorStore:
    """
    A simple local vector store using FAISS.
    """
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Adds embeddings and their corresponding metadata to the store.
        """
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch. Expected {self.dimension}, got {embeddings.shape[1]}")
        
        self.index.add(embeddings.astype('float32'))
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for the nearest neighbors of a query embedding.
        """
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):
                res = self.metadata[idx].copy()
                res['distance'] = float(dist)
                results.append(res)
        
        return results

    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        # In a real app, you'd save metadata separately (e.g., JSON or Pickle)
        import pickle
        with open(f"{path}.meta", 'wb') as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls, path: str):
        index = faiss.read_index(f"{path}.index")
        import pickle
        with open(f"{path}.meta", 'rb') as f:
            metadata = pickle.load(f)
        
        store = cls(index.d)
        store.index = index
        store.metadata = metadata
        return store
