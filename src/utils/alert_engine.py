import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime

class AlertEngine:
    """
    Analyzes batches of processed text to detect anomalies or spikes in negative sentiment.
    """
    def __init__(self, threshold: float = 0.35, min_samples: int = 5):
        self.threshold = threshold  # Percentage of negative sentiment to trigger alert
        self.min_samples = min_samples
        self.alert_history = []

    def check_for_spikes(self, data: pd.DataFrame, topic: str = "Global") -> Optional[Dict[str, Any]]:
        """
        Calculates negative sentiment percentage and triggers an alert if above threshold.
        """
        if len(data) < self.min_samples:
            return None

        negative_count = (data['sentiment'] == 'negative').sum()
        total_count = len(data)
        neg_ratio = negative_count / total_count

        if neg_ratio >= self.threshold:
            alert = {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "severity": "CRITICAL" if neg_ratio > 0.5 else "WARNING",
                "message": f"Negative Sentiment Spike detected: {neg_ratio:.1%} (Threshold: {self.threshold:.1%})",
                "stats": {
                    "total": total_count,
                    "negative": int(negative_count),
                    "ratio": float(neg_ratio)
                }
            }
            self.alert_history.append(alert)
            return alert
        
        return None

    def get_history(self) -> List[Dict[str, Any]]:
        return self.alert_history
