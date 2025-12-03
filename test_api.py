import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_health():
    print("Testing /api/health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
        else:
            print("❌ Health check failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ Health check error:", e)

def test_options():
    print("\nTesting /api/options...")
    try:
        response = requests.get(f"{BASE_URL}/options")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Options retrieved: {len(data['locations'])} locations, {len(data['occupations'])} occupations")
        else:
            print("❌ Options check failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ Options check error:", e)

def test_recommend():
    print("\nTesting /api/recommend...")
    payload = {
        "criteria": {
            "location": "台北",
            "hobby": "攝影"
        },
        "top_k": 3
    }
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommendation successful: Found {data['count']} matches")
            for user in data['recommendations']:
                print(f"   - {user['name']} ({user['age']}): {user['occupation']}")
        else:
            print("❌ Recommendation failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ Recommendation error:", e)

if __name__ == "__main__":
    print("🚀 Starting API Tests...")
    print("Make sure the server is running on http://localhost:5000")
    print("-" * 50)
    
    # Wait a bit to ensure server is ready if just started
    time.sleep(1)
    
    test_health()
    test_options()
    test_recommend()
    print("-" * 50)
    print("Tests completed.")
