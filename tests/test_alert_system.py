import pandas as pd
from src.utils.alert_engine import AlertEngine
from src.utils.notifications import NotificationHub

def test_alert_flow():
    print("Testing Alert Flow...")
    engine = AlertEngine(threshold=0.3)
    hub = NotificationHub()
    hub.enable_channel("slack")
    
    # Negative spike data
    data = pd.DataFrame({
        'sentiment': ['negative', 'negative', 'positive', 'negative', 'neutral'],
        'text': ['bad', 'awful', 'good', 'horrible', 'ok']
    })
    
    print(f"Checking for spikes in data (Neg Ratio: 3/5 = 60%)...")
    alert = engine.check_for_spikes(data, topic="Test Toxicity")
    
    if alert:
        print(f"SUCCESS: Alert triggered! -> {alert['message']}")
        hub.notify(alert)
    else:
        print("FAILED: No alert triggered.")

if __name__ == "__main__":
    test_alert_flow()
