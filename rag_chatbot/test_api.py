import requests
import sys

BASE_URL = "http://localhost:8000"

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        sys.exit(1)

def test_upload(file_path):
    print(f"\nUploading {file_path}...")
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            print(f"Upload status: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Upload failed: {e}")

def test_ask(query):
    print(f"\nAsking: {query}")
    try:
        response = requests.post(f"{BASE_URL}/ask", json={"query": query})
        print(f"Ask status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data['answer']}")
            print("Sources:")
            for source in data['sources']:
                print(f"- {source['source']} (Page {source['page']})")
        else:
            print(response.text)
    except Exception as e:
        print(f"Ask failed: {e}")

if __name__ == "__main__":
    # Ensure server is running before executing this
    test_root()
    
    # Create a dummy PDF for testing if needed, or use an existing one
    # test_upload("sample.pdf")
    # test_ask("What is the summary of the document?")
