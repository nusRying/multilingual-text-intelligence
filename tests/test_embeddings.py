import pytest
import numpy as np
from src.models.embeddings import EmbeddingGenerator
from src.utils.vector_store import LocalVectorStore

@pytest.fixture(scope="module")
def generator():
    return EmbeddingGenerator()

def test_embedding_generation(generator):
    texts = ["Hello world", "مرحبا بالعالم"]
    embeddings = generator.generate(texts)
    
    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == generator.get_embedding_dimension()
    assert isinstance(embeddings, np.ndarray)

def test_vector_store(generator):
    dim = generator.get_embedding_dimension()
    store = LocalVectorStore(dim)
    
    texts = ["This is a test", "اختبار للنظام"]
    embeddings = generator.generate(texts)
    metadata = [{"text": t} for t in texts]
    
    store.add(embeddings, metadata)
    
    # Search for something similar to the first text
    query_emb = generator.generate("A test case")
    results = store.search(query_emb, top_k=1)
    
    assert len(results) == 1
    assert "text" in results[0]
    assert results[0]["distance"] >= 0

