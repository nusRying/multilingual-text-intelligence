import praw
import os
from datetime import datetime
from typing import List, Dict, Any
from .base import DataConnector

class RedditConnector(DataConnector):
    """
    Real-world data ingestion from Reddit.
    Requires REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT.
    """
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "Multilingual-NLP-Intelligence/1.0")
        
        if not (self.client_id and self.client_secret):
            print("WARNING: Reddit credentials not found. RedditConnector will not be functional.")
            self.reddit = None
        else:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )

    def fetch_data(self, query: str = "technology", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetches submissions from Reddit based on a search query.
        """
        if not self.reddit:
            return []

        results = []
        # Search all subreddits
        for submission in self.reddit.subreddit("all").search(query, limit=limit):
            results.append({
                "id": submission.id,
                "text": submission.title + " " + (submission.selftext or ""),
                "source": "Reddit",
                "author": str(submission.author),
                "timestamp": datetime.fromtimestamp(submission.created_utc).isoformat(),
                "url": f"https://reddit.com{submission.permalink}"
            })
        
        return results
