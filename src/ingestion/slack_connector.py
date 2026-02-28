import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from typing import List, Dict, Any
from .base import DataConnector

class SlackConnector(DataConnector):
    """
    Ingests messages from Slack channels for sentiment and topic analysis.
    Requires SLACK_BOT_TOKEN in environment variables.
    """
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        if not self.token:
            print("WARNING: SLACK_BOT_TOKEN not found. SlackConnector will not be functional.")
            self.client = None
        else:
            self.client = WebClient(token=self.token)

    def fetch_data(self, channel_id: str = "general", limit: int = 20) -> List[Dict[str, Any]]:
        """
        Fetches the latest messages from a Slack channel.
        """
        if not self.client:
            return []

        try:
            # Call the conversations.history method using the WebClient
            result = self.client.conversations_history(channel=channel_id, limit=limit)
            messages = result["messages"]
            
            processed_data = []
            for msg in messages:
                # Skip bot messages or non-text messages
                if "text" in msg and "bot_id" not in msg:
                    processed_data.append({
                        "id": msg.get("ts"),
                        "text": msg["text"],
                        "source": "Slack",
                        "user": msg.get("user"),
                        "timestamp": datetime.fromtimestamp(float(msg["ts"])).isoformat(),
                        "channel": channel_id
                    })
            return processed_data

        except SlackApiError as e:
            print(f"Error fetching Slack history: {e.response['error']}")
            return []
        except Exception as e:
            print(f"General error in SlackConnector: {e}")
            return []
