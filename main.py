from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.preprocessing.cleaner import TextCleaner
from src.models.sentiment import SentimentAnalyzer
from src.utils.vector_store import LocalVectorStore
from src.models.search import SemanticSearchService
from src.models.embeddings import EmbeddingGenerator

app = FastAPI(title="Multilingual Text Intelligence System")

# Initialize components
cleaner = TextCleaner()
sentiment_analyzer = SentimentAnalyzer()
embedding_gen = EmbeddingGenerator()
# For demonstration, we use a fixed dimension (384 for MiniLM-L12-v2)
vector_store = LocalVectorStore(dimension=384)
search_service = SemanticSearchService(embedding_gen, vector_store)

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    original: str
    cleaned: str
    language: str
    sentiment: str
    confidence: float

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    distance: float

@app.get("/")
async def root():
    return {"message": "Welcome to the Multilingual Text Intelligence System API"}

@app.post("/analyze", response_model=TextResponse)
async def analyze_text(request: TextRequest):
    try:
        # 1. Clean and detect language
        cleaning_result = cleaner.clean(request.text)
        
        # 2. Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze(cleaning_result['cleaned'])[0]
        
        # 3. (Optional) Ingest into vector store for search availability
        emb = embedding_gen.generate(cleaning_result['cleaned'])
        vector_store.add(emb, [{"id": "dynamic", "text": request.text}])
        
        return {
            "original": request.text,
            "cleaned": cleaning_result['cleaned'],
            "language": cleaning_result['language'],
            "sentiment": sentiment_result['sentiment'],
            "confidence": sentiment_result['confidence']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=List[SearchResult])
async def search_documents(request: SearchRequest):
    try:
        results = search_service.search(request.query, top_k=request.top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
