import requests
import json
import os

try:
    with open("debug_brd.txt", "r", encoding="utf-8") as f:
        brd_text = f.read()

    print(f"Sending BRD of size: {len(brd_text)}")
    
    url = "http://127.0.0.1:8000/api/analyze/requirements"
    headers = {"Content-Type": "application/json"}
    payload = {"text": brd_text}

    print("POST ...")
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}") # Print first 500 chars

except Exception as e:
    print(f"FAILED: {e}")
