import requests
import json
import time

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Test Analysis (English)
    print("Testing English Analysis...")
    resp = requests.post(f"{base_url}/analyze", json={"text": "I love this intelligent system! It is very helpful."})
    print(json.dumps(resp.json(), indent=2, ensure_ascii=True))
    
    # 2. Test Analysis (Arabic)
    print("\nTesting Arabic Analysis...")
    resp = requests.post(f"{base_url}/analyze", json={"text": "هذا النظام رائع جداً ومفيد للمستخدمين."})
    print(json.dumps(resp.json(), indent=2, ensure_ascii=True))
    
    # 3. Test Analysis (Urdu)
    print("\nTesting Urdu Analysis...")
    resp = requests.post(f"{base_url}/analyze", json={"text": "یہ سسٹم بہت اچھا ہے اور بہت مددگار ہے۔"})
    print(json.dumps(resp.json(), indent=2, ensure_ascii=True))
    
    # 4. Test Search
    print("\nTesting Semantic Search (Query: 'system problems')...")
    resp = requests.post(f"{base_url}/search", json={"query": "system problems", "top_k": 2})
    print(json.dumps(resp.json(), indent=2, ensure_ascii=True))

if __name__ == "__main__":
    # Wait a moment for server to start
    # time.sleep(60)
    try:
        test_api()
    except Exception as e:
        print(f"Error testing API: {e}")
