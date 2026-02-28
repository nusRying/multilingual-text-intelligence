from typing import List, Dict, Any
import time
import random
from .base import BaseConnector

class MockSocialMediaConnector(BaseConnector):
    """
    Mock connector simulating social media API ingestion.
    """
    def fetch_data(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        mock_data = []
        templates = [
            "Just tried the new system, it's amazing! #AI {keyword}",
            "I'm having some issues with the login. #Support {keyword}",
            "هذا النظام رائع جداً! #ذكاء_اصطناعي {keyword}",
            "أواجه مشكلة في تسجيل الدخول. #دعم {keyword}",
            "Innovation for NLP. {keyword}",
            "خدمة رائعة جداً، شكراً لكم. {keyword}",
            "یہ سسٹم بہت اچھا ہے اور بہت مددگار ہے۔ {keyword}",
            "مجھے لاگ ان کرنے میں کچھ مسئلہ ہو رہا ہے۔ {keyword}"
        ]
        
        for i in range(limit):
            mock_data.append({
                "id": f"tweet_{int(time.time())}_{i}",
                "text": random.choice(templates).format(keyword=keyword),
                "source": "twitter_mock"
            })
            
        return mock_data
