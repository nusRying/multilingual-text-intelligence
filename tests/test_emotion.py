import pytest
from src.models.emotion import EmotionAnalyzer

@pytest.fixture
def emotion_analyzer():
    return EmotionAnalyzer()

def test_emotion_detection(emotion_analyzer):
    text = "I am so happy and excited about this new project!"
    results = emotion_analyzer.analyze(text)[0]
    
    assert 'emotion' in results
    assert results['emotion'] == 'joy'

def test_emotion_neutral(emotion_analyzer):
    text = "The weather is okay today."
    results = emotion_analyzer.analyze(text)[0]
    
    assert 'emotion' in results
    # Might be neutral or others depending on model, but should exist
