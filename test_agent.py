import requests
import json

url = "http://localhost:8080/ask"

# Ask a question relevant to your PDF
question = "What is the specific topic of this document?"

payload = {"query": question}

print(f"🤖 Asking Veritas: '{question}'...")
try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("\n" + "="*50)
        print("VERITAS ANSWER:")
        print("="*50)
        print(data["answer"])
        print("\n" + "="*50)
        print(f"Sources Used: {data['sources']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection Failed: {e}")