import os
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
import numpy as np

class PineconeVectorStore:
    """
    Production-grade vector store using Pinecone.
    Requires PINECONE_API_KEY in environment variables.
    """
    def __init__(self, index_name: str, dimension: int):
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            print("WARNING: PINECONE_API_KEY not found. Pinecone store will not be functional.")
            self.index = None
            return

        self.pc = Pinecone(api_key=self.api_key)
        self.index_name = index_name
        self.dimension = dimension

        # Create index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            print(f"Creating Pinecone index: {self.index_name}...")
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        
        self.index = self.pc.Index(self.index_name)

    def add(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Upserts vectors into Pinecone.
        """
        if self.index is None:
            return

        vectors = []
        for i, (emb, meta) in enumerate(zip(embeddings, metadata)):
            # Use 'id' from metadata if available, otherwise use index
            vec_id = meta.get('id', str(i))
            vectors.append({
                "id": vec_id,
                "values": emb.tolist(),
                "metadata": meta
            })
        
        self.index.upsert(vectors=vectors)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Queries Pinecone for nearest neighbors.
        """
        if self.index is None:
            return []

        response = self.index.query(
            vector=query_embedding.tolist()[0],
            top_k=top_k,
            include_metadata=True
        )
        
        results = []
        for match in response['matches']:
            res = match['metadata']
            res['distance'] = float(match['score'])
            results.append(res)
        
        return results
