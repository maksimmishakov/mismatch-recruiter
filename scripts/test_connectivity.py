import socket
import requests

print("Testing connectivity...")
print(f"Hostname: {socket.gethostname()}")

urls = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://mismatch-recruiter-backend-1:5000",
    "http://backend:5000"
]

for url in urls:
    try:
        print(f"\nTrying {url}...")
        response = requests.get(url, timeout=2)
        print(f"  Status: {response.status_code}")
        print(f"  Response length: {len(response.content)}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {str(e)[:100]}")
