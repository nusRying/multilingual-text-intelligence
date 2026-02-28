import time
import json
import os
from datetime import datetime
from typing import Dict, Any, List

class PerformanceMonitor:
    """
    Simple MLOps utility to track model inference latency and system metrics.
    """
    def __init__(self, log_dir: str = "logs/metrics"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.metrics_history = []

    def log_inference(self, model_name: str, duration_ms: float, text_length: int, language: str):
        """
        Logs a single inference event.
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "latency_ms": round(duration_ms, 2),
            "chars": text_length,
            "language": language
        }
        self.metrics_history.append(metric)
        
        # In a real app, you'd write to a database or Prometheus
        self._save_to_file(metric)

    def _save_to_file(self, metric: Dict[str, Any]):
        filename = f"{self.log_dir}/inference_log_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(filename, "a") as f:
            f.write(json.dumps(metric) + "\n")

    def get_summary(self) -> Dict[str, Any]:
        """
        Returns average latency and throughput stats.
        """
        if not self.metrics_history:
            return {"avg_latency": 0, "total_calls": 0}
        
        avg_lat = sum(m['latency_ms'] for m in self.metrics_history) / len(self.metrics_history)
        return {
            "avg_latency_ms": round(avg_lat, 2),
            "total_calls": len(self.metrics_history),
            "languages": list(set(m['language'] for m in self.metrics_history))
        }

# Global monitor instance
monitor = PerformanceMonitor()
