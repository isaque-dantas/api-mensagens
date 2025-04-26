from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app

from app.models import engine
from app.models.message import Message

client = TestClient(app, headers={"content-type": "application/json"})
session = Session(engine)


def test_connection():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_post_message():
    message = {"content": "Hello"}

    response = client.post(
        "/message",
        json={"content": "Hello"}
    )

    assert response.status_code == 201
    assert response.json()["content"] == message["content"]


def test_get_messages():
    response = client.get("/message")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_message_by_id():
    session.add(
        Message(content="My message")
    )
    session.commit()

    response = client.get("/message/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_message_by_id__non_existent():
    response = client.get("/message/999999999")
    assert response.status_code == 404


def test_update_message():
    message = Message(content="Old message")
    session.add(message)
    session.commit()
    session.refresh(message)

    response = client.put(
        f"/message/{message.id}", 
        json={"content": "New message"}
    )
    
    session.refresh(message)

    assert response.status_code == 200
    assert message.content == "New message"


def test_delete_message():
    message = Message(content="My message")
    session.add(message)
    session.commit()
    session.refresh(message)

    response = client.delete(f"/message/{message.id}")

    assert response.status_code == 204


def test_delete_message__non_existent():
    response = client.delete("/message/999999999")
    assert response.status_code == 404
