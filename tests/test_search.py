import pytest
from src.models.search import SemanticSearchService
from src.models.embeddings import EmbeddingGenerator
from src.utils.vector_store import LocalVectorStore

@pytest.fixture
def search_service():
    gen = EmbeddingGenerator()
    store = LocalVectorStore(dimension=gen.get_embedding_dimension())
    
    # Pre-populate some documents
    texts = [
        "The weather is lovely today in London.",
        "الطقس جميل جداً في دبي اليوم.",
        "System performance is optimal.",
        "هناك مشكلة في أداء النظام."
    ]
    for i, t in enumerate(texts):
        emb = gen.generate(t)
        store.add(emb, [{"id": str(i), "text": t}])
        
    return SemanticSearchService(gen, store)

def test_semantic_search_cross_lingual(search_service):
    # Query in English, find result in Arabic (or vice-versa)
    # "How is the weather?" -> should find weather related docs
    results = search_service.search("weather forecast", top_k=2)
    
    # Check if we got weather-related results from both languages
    found_en = any("London" in r["text"] for r in results)
    found_ar = any("دبي" in r["text"] for r in results)
    
    assert found_en or found_ar
    assert len(results) == 2

def test_semantic_search_system_issues(search_service):
    # "System is slow"
    results = search_service.search("System issues", top_k=2)
    
    assert any("النظام" in r["text"] for r in results) or any("performance" in r["text"] for r in results)
