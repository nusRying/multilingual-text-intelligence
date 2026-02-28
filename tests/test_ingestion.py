import pytest
import os
import pandas as pd
from src.ingestion.csv_connector import CSVConnector
from src.ingestion.mock_api_connector import MockSocialMediaConnector

def test_csv_connector(tmp_path):
    # Create a dummy CSV
    csv_file = tmp_path / "test.csv"
    data = {
        "id": ["1", "2"],
        "text": ["Hello", "مرحبا"]
    }
    pd.DataFrame(data).to_csv(csv_file, index=False)
    
    connector = CSVConnector()
    results = connector.fetch_data(str(csv_file))
    
    assert len(results) == 2
    assert results[0]["text"] == "Hello"
    assert results[1]["text"] == "مرحبا"

def test_mock_api_connector():
    connector = MockSocialMediaConnector()
    results = connector.fetch_data(keyword="test", limit=5)
    
    assert len(results) == 5
    for item in results:
        assert "text" in item
        assert "id" in item
        assert "test" in item["text"].lower() or "test" in item["text"]
