from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from src.preprocessing.cleaner import TextCleaner
from src.models.sentiment import SentimentAnalyzer
from src.utils.vector_store import LocalVectorStore
from src.models.search import SemanticSearchService
from src.models.embeddings import EmbeddingGenerator
from src.models.ner import NERAnalyzer
from src.models.emotion import EmotionAnalyzer
from src.models.classification import ZeroShotClassifier
from src.models.summarizer import TextSummarizer
from src.models.comparator import TextComparator
from src.utils.monitor import monitor
import time

app = FastAPI(title="Multilingual Text Intelligence System")

# Initialize components
cleaner = TextCleaner()
sentiment_analyzer = SentimentAnalyzer()
ner_analyzer = NERAnalyzer()
emotion_analyzer = EmotionAnalyzer()
classification_engine = ZeroShotClassifier()
summarizer = TextSummarizer()
comparator = TextComparator(embedding_gen)
embedding_gen = EmbeddingGenerator()
# For demonstration, we use a fixed dimension (384 for MiniLM-L12-v2)
vector_store = LocalVectorStore(dimension=384)
search_service = SemanticSearchService(embedding_gen, vector_store)

class TextRequest(BaseModel):
    text: str
    categories: Optional[List[str]] = ["Policy", "Technology", "Economics", "Social"]

class TextResponse(BaseModel):
    original: str
    cleaned: str
    language: str
    sentiment: str
    sentiment_confidence: float
    emotion: str
    emotion_confidence: float
    category: str
    category_confidence: float
    entities: List[Dict[str, Any]]

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
    start_time = time.time()
    try:
        # 1. Clean and detect language
        cleaning_result = cleaner.clean(request.text)
        lang = cleaning_result['language']
        
        # 2. Analyze sentiment (optimized for language)
        sentiment_result = sentiment_analyzer.analyze(cleaning_result['cleaned'], language=lang)[0]
        
        # 3. Analyze Emotion
        emotion_result = emotion_analyzer.analyze(cleaning_result['cleaned'])[0]
        
        # 4. Extract Entities
        entities_result = ner_analyzer.extract_entities(cleaning_result['cleaned'])[0]
        
        # 5. Zero-Shot Classification
        class_res = classification_engine.classify(cleaning_result['cleaned'], request.categories)
        
        # 6. Ingest into vector store for search availability
        emb = embedding_gen.generate(cleaning_result['cleaned'])
        vector_store.add(emb, [{"id": "dynamic", "text": request.text}])
        
        # Log latency
        duration = (time.time() - start_time) * 1000
        monitor.log_inference("API: analyze_text", duration, len(request.text), lang)
        
        return {
            "original": request.text,
            "cleaned": cleaning_result['cleaned'],
            "language": lang,
            "sentiment": sentiment_result['sentiment'],
            "sentiment_confidence": sentiment_result['confidence'],
            "emotion": emotion_result['emotion'],
            "emotion_confidence": emotion_result['confidence'],
            "category": class_res['label'],
            "category_confidence": class_res['score'],
            "entities": entities_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/async")
async def analyze_text_async(request: TextRequest, background_tasks: BackgroundTasks):
    """
    Submits a text analysis task to be processed in the background.
    """
    background_tasks.add_task(process_analysis, request.text)
    return {"message": "Task submitted successfully", "status": "processing"}

async def process_analysis(text: str):
    # This logic can be more complex, e.g., saving to a database
    print(f"Processing background task for: {text[:50]}...")
    try:
        cleaning_result = cleaner.clean(text)
        lang = cleaning_result['language']
        sentiment_result = sentiment_analyzer.analyze(cleaning_result['cleaned'], language=lang)[0]
        # logic to store result...
        print(f"Background processing complete for: {text[:50]}")
    except Exception as e:
        print(f"Background task failed: {e}")

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


# --- Additional Endpoints ---

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150

class CompareRequest(BaseModel):
    text_a: str
    text_b: str

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    try:
        result = summarizer.summarize(request.text, max_length=request.max_length)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare")
async def compare_texts(request: CompareRequest):
    try:
        result = comparator.compare(request.text_a, request.text_b)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
