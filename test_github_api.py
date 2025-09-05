import requests
import json

# GitHub API to get release info
api_url = "https://api.github.com/repos/RysanekDavid/The-Tarnished-Chronicle/releases/tags/v1.0.4"

print("Fetching release info from GitHub API...")
print("=" * 50)

try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    print(f"Release Name: {data.get('name', 'N/A')}")
    print(f"Tag: {data.get('tag_name', 'N/A')}")
    print(f"Published: {data.get('published_at', 'N/A')}")
    print(f"\nAssets ({len(data.get('assets', []))}):")
    
    for asset in data.get('assets', []):
        print(f"\n  - Name: {asset.get('name')}")
        print(f"    Size: {asset.get('size', 0) / 1024 / 1024:.2f} MB")
        print(f"    Download URL: {asset.get('browser_download_url')}")
        print(f"    Download Count: {asset.get('download_count', 0)}")
    
    if not data.get('assets'):
        print("\n  No assets found! The installer file needs to be uploaded to the release.")
        
except requests.exceptions.RequestException as e:
    print(f"Error fetching release info: {e}")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")