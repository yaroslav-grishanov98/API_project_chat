import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Chat API Service!"}

def test_simple_create_chat(client: TestClient):
    """Проверяет базовое создание чата с минимальными данными."""
    response = client.post("/v1/chats/", json={"title": "My Simple Chat"})
    assert response.status_code == 201
    created_chat = response.json()
    assert created_chat["title"] == "My Simple Chat"
    assert "id" in created_chat
    assert "created_at" in created_chat

@pytest.mark.parametrize("title, status_code", [
    ("", 422),
    ("a" * 201, 422),
    ("   My Chat   ", 201),
    ("Valid Title", 201),
])
def test_create_chat_validation(client: TestClient, title: str, status_code: int):
    if status_code == 201:
        response = client.post("/v1/chats/", json={"title": title})
        assert response.status_code == 201
        assert response.json()["title"] == title.strip()
        assert "id" in response.json()
        assert "created_at" in response.json()
    else:
        response = client.post("/v1/chats/", json={"title": title})
        assert response.status_code == status_code


def test_create_and_get_chat(client: TestClient, session: Session):
    response = client.post("/v1/chats/", json={"title": "Test Chat"})
    assert response.status_code == 201
    created_chat = response.json()
    assert created_chat["title"] == "Test Chat"

    chat_id = created_chat["id"]

    response = client.get(f"/v1/chats/{chat_id}")
    assert response.status_code == 200
    retrieved_chat = response.json()
    assert retrieved_chat["id"] == chat_id
    assert retrieved_chat["title"] == "Test Chat"
    assert "messages" in retrieved_chat
    assert retrieved_chat["messages"] == []


def test_send_message_to_existing_chat(client: TestClient, session: Session):
    create_chat_res = client.post("/v1/chats/", json={"title": "Chat with messages"})
    assert create_chat_res.status_code == 201
    chat_id = create_chat_res.json()["id"]

    message_text = "Hello from test!"
    send_message_res = client.post(f"/v1/chats/{chat_id}/messages/", json={"text": message_text})
    assert send_message_res.status_code == 201
    sent_message = send_message_res.json()
    assert sent_message["text"] == message_text
    assert sent_message["chat_id"] == chat_id
    assert "id" in sent_message
    assert "created_at" in sent_message


def test_send_message_to_non_existent_chat(client: TestClient, session: Session):
    response = client.post("/v1/chats/999/messages/", json={"text": "This should fail"})
    assert response.status_code == 404
    assert "Chat with id 999 not found" in response.json()["detail"]


@pytest.mark.parametrize("text, status_code", [
    ("", 422),
    ("a" * 5001, 422),
    ("Short text", 201),
])
def test_send_message_validation(client: TestClient, session: Session, text: str, status_code: int):
    create_chat_res = client.post("/v1/chats/", json={"title": "Val Chat"})
    assert create_chat_res.status_code == 201
    chat_id = create_chat_res.json()["id"]

    response = client.post(f"/v1/chats/{chat_id}/messages/", json={"text": text})
    assert response.status_code == status_code


def test_get_chat_with_limited_messages(client: TestClient, session: Session):
    create_chat_res = client.post("/v1/chats/", json={"title": "Limited Messages Chat"})
    assert create_chat_res.status_code == 201
    chat_id = create_chat_res.json()["id"]

    for i in range(5):
        client.post(f"/v1/chats/{chat_id}/messages/", json={"text": f"Message {i+1}"})

    response = client.get(f"/v1/chats/{chat_id}?limit=3")
    assert response.status_code == 200
    chat_with_messages = response.json()
    assert len(chat_with_messages["messages"]) == 3
    assert chat_with_messages["messages"][0]["text"] == "Message 5"
    assert chat_with_messages["messages"][1]["text"] == "Message 4"
    assert chat_with_messages["messages"][2]["text"] == "Message 3"

    response = client.get(f"/v1/chats/{chat_id}?limit=100")
    assert response.status_code == 200
    chat_with_messages = response.json()
    assert len(chat_with_messages["messages"]) == 5


def test_delete_chat(client: TestClient, session: Session):
    create_chat_res = client.post("/v1/chats/", json={"title": "Chat to Delete"})
    assert create_chat_res.status_code == 201
    chat_id = create_chat_res.json()["id"]

    client.post(f"/v1/chats/{chat_id}/messages/", json={"text": "Msg 1"})
    client.post(f"/v1/chats/{chat_id}/messages/", json={"text": "Msg 2"})

    response = client.delete(f"/v1/chats/{chat_id}")
    assert response.status_code == 204

    response = client.get(f"/v1/chats/{chat_id}")
    assert response.status_code == 404

    response = client.post(f"/v1/chats/{chat_id}/messages/", json={"text": "Should not work"})
    assert response.status_code == 404

def test_delete_non_existent_chat(client: TestClient, session: Session):
    response = client.delete("/v1/chats/999")
    assert response.status_code == 404
    assert "Chat with id 999 not found" in response.json()["detail"]


def test_get_non_existent_chat(client: TestClient, session: Session):
    response = client.get("/v1/chats/999")
    assert response.status_code == 404
    assert "Chat with id 999 not found" in response.json()["detail"]
