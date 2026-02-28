import logging
from typing import List, Dict, Any
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NotificationHub")

class NotificationHub:
    """
    Mock notification service for Slack, Email, and System Logs.
    """
    def __init__(self):
        self.enabled_channels = ["console"]

    def notify(self, alert: Dict[str, Any]):
        """
        Dispatches alerts to all enabled channels.
        """
        msg = f"[{alert['severity']}] {alert['message']} | Topic: {alert['topic']}"
        
        if "console" in self.enabled_channels:
            logger.warning(f"SYSTEM ALERT: {msg}")

        if "slack" in self.enabled_channels:
            # Mock Slack Webhook
            logger.info(f"MOCK SLACK: Sending notification -> {msg}")

        if "email" in self.enabled_channels:
            # Mock Email
            logger.info(f"MOCK EMAIL: Sending alert to admin@example.com -> {msg}")

    def enable_channel(self, channel: str):
        if channel not in self.enabled_channels:
            self.enabled_channels.append(channel)

    def disable_channel(self, channel: str):
        if channel in self.enabled_channels:
            self.enabled_channels.remove(channel)
