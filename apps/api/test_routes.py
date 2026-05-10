from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_routes():
    # Check health
    response = client.get("/health")
    print(f"GET /health: {response.status_code}")
    
    # Check enhance (POST)
    response = client.post("/api/prompts/enhance", json={"raw_prompt": "test", "diagram_type": "auto"})
    print(f"POST /api/prompts/enhance: {response.status_code}")
    if response.status_code == 404:
        print("ERROR: /api/prompts/enhance is 404!")

if __name__ == "__main__":
    test_routes()
