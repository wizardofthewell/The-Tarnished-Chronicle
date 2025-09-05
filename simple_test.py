#!/usr/bin/env python3
"""
Simple test for auto-updater
"""
import os
import sys
import shutil
import hashlib
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

print("="*50)
print("SIMPLE AUTO-UPDATER TEST")
print("="*50)

# 1. Calculate hash of current installer
if os.path.exists("ER_Boss_Checklist_Setup.exe"):
    sha256_hash = hashlib.sha256()
    with open("ER_Boss_Checklist_Setup.exe", "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    hash_value = sha256_hash.hexdigest()
    print(f"Installer SHA256: {hash_value}")
    
    # Copy as test file
    shutil.copy("ER_Boss_Checklist_Setup.exe", "ER_Boss_Checklist_Setup_Test.exe")
    
    # Update test manifest
    manifest = {
        "version": "1.0.6",  # Higher than 1.0.5
        "url": "http://localhost:8000/ER_Boss_Checklist_Setup_Test.exe",
        "sha256": hash_value,
        "notes": "Test update",
        "force": False,
        "published_at": "2025-09-04T20:00:00Z"
    }
    
    with open("test_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("Created test_manifest.json")
else:
    print("ERROR: ER_Boss_Checklist_Setup.exe not found!")
    sys.exit(1)

# 2. Start local server
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[SERVER] {format}" % args)

server = HTTPServer(('localhost', 8000), Handler)
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True
thread.start()
print("\nServer started at http://localhost:8000")

# 3. Instructions
print("\n" + "="*50)
print("TEST INSTRUCTIONS:")
print("="*50)
print("1. Edit src/config/app_config.py:")
print('   MANIFEST_URL = "http://localhost:8000/test_manifest.json"')
print("2. Run: python src/main.py")
print("3. Should detect version 1.0.6 available")
print("4. Click Yes and watch for download progress")
print("\nPress Ctrl+C to stop server when done")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nTest stopped")