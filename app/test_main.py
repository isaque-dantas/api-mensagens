from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_connection():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"

def test_post_message__on_happy_path():
    response = client.post("/message", content={"content": "Hello"})
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {"id": 1, "content": "Hello"}
