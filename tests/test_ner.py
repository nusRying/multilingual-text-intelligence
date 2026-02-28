import pytest
from src.models.ner import NERAnalyzer

@pytest.fixture
def ner_analyzer():
    return NERAnalyzer()

def test_ner_english(ner_analyzer):
    text = "Google was founded by Larry Page and Sergey Brin in California."
    results = ner_analyzer.extract_entities(text)[0]
    
    # Check if we found some entities
    assert len(results) > 0
    # Search for specific types
    groups = [r['entity_group'] for r in results]
    assert 'ORG' in groups or 'PER' in groups or 'LOC' in groups

def test_ner_arabic(ner_analyzer):
    text = "تأسست شركة آبل في الولايات المتحدة."
    results = ner_analyzer.extract_entities(text)[0]
    
    assert len(results) > 0
    # At least check if it returns entities for Arabic
    assert any(r['entity_group'] in ['ORG', 'LOC', 'PER'] for r in results)
