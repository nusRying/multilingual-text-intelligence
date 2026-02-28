import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from .base import DataConnector

class WebScraper(DataConnector):
    """
    Ingests data from news articles and blogs by scraping their content.
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_data(self, url: str) -> List[Dict[str, Any]]:
        """
        Scrapes a single URL and returns the content.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic title and text extraction
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "No Title"
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text from paragraphs
            paragraphs = soup.find_all('p')
            text = " ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            
            # Limit text length for initial analysis
            text = text[:3000]
            
            if not text:
                return []

            return [{
                "id": url,
                "text": text,
                "title": title,
                "source": "Web Scraper",
                "url": url
            }]
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
