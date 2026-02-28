from typing import List, Dict, Any
from .embeddings import EmbeddingGenerator
from ..utils.vector_store import LocalVectorStore

class SemanticSearchService:
    """
    Service to perform semantic search using embeddings and FAISS.
    """
    def __init__(self, generator: EmbeddingGenerator, store: LocalVectorStore):
        self.generator = generator
        self.store = store

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Processes query and returns top-k similar documents.
        """
        # 1. Generate query embedding
        query_emb = self.generator.generate(query)
        
        # 2. Search in vector store
        results = self.store.search(query_emb, top_k=top_k)
        
        return results
