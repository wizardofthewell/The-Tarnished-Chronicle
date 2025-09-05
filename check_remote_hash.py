import requests
import hashlib

url = "https://github.com/RysanekDavid/The-Tarnished-Chronicle/releases/download/v1.0.4/The_Tarnished_Chronicle_Setup.exe"

print("Downloading file to calculate SHA256...")
print("This may take a moment...")

try:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    
    sha256_hash = hashlib.sha256()
    downloaded = 0
    total_size = int(response.headers.get('content-length', 0))
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            sha256_hash.update(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                progress = (downloaded / total_size) * 100
                print(f"\rProgress: {progress:.1f}%", end='')
    
    print(f"\n\nSHA256: {sha256_hash.hexdigest()}")
    print(f"File size: {downloaded / 1024 / 1024:.2f} MB")
    
except Exception as e:
    print(f"Error: {e}")