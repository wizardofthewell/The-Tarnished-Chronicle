import requests
import os

# Test download from GitHub release
url = "https://github.com/RysanekDavid/The-Tarnished-Chronicle/releases/download/v1.0.4/ER_Boss_Checklist_Setup.exe"

print(f"Testing download from: {url}")
print("=" * 50)

try:
    # First, try to get headers
    print("Getting file information...")
    response = requests.head(url, allow_redirects=True, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Final URL: {response.url}")
    print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
    print(f"Content-Length: {response.headers.get('content-length', 'Unknown')} bytes")
    
    if response.status_code == 200:
        print("\n✅ URL is accessible!")
        
        # Try to download first 1KB
        print("\nTrying to download first 1KB...")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        chunk = next(response.iter_content(1024))
        print(f"Downloaded {len(chunk)} bytes successfully")
        print("✅ Download test successful!")
        
    else:
        print(f"\n❌ URL returned status code: {response.status_code}")
        
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")