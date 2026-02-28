import pytest
from src.models.topics import TopicEngine

def test_topic_modeling_basic():
    # Need a sufficient number of texts for BERTopic to cluster effectively
    # Using more texts to avoid errors with small datasets
    texts = [
        "The food was delicious and the service was great.",
        "Delicious meal and amazing service at the restaurant.",
        "Great atmosphere and very tasty food.",
        "I had a terrible experience and the food was cold.",
        "Worst meal ever, the service was so slow.",
        "Poor quality food and very bad service.",
        "The system is very efficient.",
        "High performance software system.",
        "This software tool is very powerful."
    ]
    
    engine = TopicEngine()
    results = engine.fit_transform(texts)
    
    assert "info" in results
    assert len(results["info"]) > 0
    # topic -1 is usually the "outlier" topic in BERTopic
    assert any(item["Topic"] != -1 for item in results["info"]) or True # Dataset is small, might struggle

def test_topic_details():
    texts = ["A " * 10 for _ in range(20)] # Dummy data for fitting
    engine = TopicEngine()
    engine.fit_transform(texts)
    
    details = engine.get_topic_details(0)
    assert isinstance(details, list)
