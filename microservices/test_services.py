"""🧪 Test All Microservices"""
import requests
import time

SERVICES = {
    "Document Service": "http://localhost:8001",
    "Vector Service": "http://localhost:8002",
    "LLM Service": "http://localhost:8003",
    "Frontend Service": "http://localhost:8501"
}

def test_service(name, url):
    """Test if service is running"""
    try:
        response = requests.get(f"{url}/health" if "LLM" in name else url, timeout=2)
        if response.status_code == 200:
            print(f"✅ {name} - Running")
            return True
        else:
            print(f"⚠️  {name} - Responded with {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} - Not Running")
        return False
    except Exception as e:
        print(f"❌ {name} - Error: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("  Testing Microservices Health")
    print("=" * 50)
    print()
    
    results = {}
    for name, url in SERVICES.items():
        results[name] = test_service(name, url)
        time.sleep(0.5)
    
    print()
    print("=" * 50)
    print("  Summary")
    print("=" * 50)
    
    running = sum(results.values())
    total = len(results)
    
    print(f"Services Running: {running}/{total}")
    
    if running == total:
        print("✅ All services are healthy!")
    else:
        print("⚠️  Some services are not running")
        print("\nTo start services, run: start_all.bat")

if __name__ == "__main__":
    main()
