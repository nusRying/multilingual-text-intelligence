import pytest
from src.models.sentiment import SentimentAnalyzer

@pytest.fixture(scope="module")
def analyzer():
    return SentimentAnalyzer()

def test_sentiment_english(analyzer):
    texts = ["I love this system!", "This is terrible."]
    results = analyzer.analyze(texts)
    
    assert len(results) == 2
    assert results[0]["sentiment"] == "positive"
    assert results[1]["sentiment"] == "negative"
    assert results[0]["confidence"] > 0.5

def test_sentiment_arabic(analyzer):
    # "هذا النظام رائع جداً" -> Positive
    # "أنا أكره هذا الخطأ" -> Negative (I hate this error)
    texts = ["هذا النظام رائع جداً", "أنا أكره هذا الخطأ"]
    results = analyzer.analyze(texts)
    
    assert len(results) == 2
    assert results[0]["sentiment"] == "positive"
    assert results[1]["sentiment"] == "negative"
