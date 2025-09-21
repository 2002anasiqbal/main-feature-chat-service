import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..src.main import app
from ..src.database.database import Base, get_db
from ..src.models.chat_models import Conversation, Message, Participant

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_conversation():
    response = client.post("/api/v1/chats/conversations", json={"participant_id": 2})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert len(data["participants"]) == 2

def test_get_conversations():
    client.post("/api/v1/chats/conversations", json={"participant_id": 2})
    response = client.get("/api/v1/chats/conversations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_conversation():
    conversation_response = client.post("/api/v1/chats/conversations", json={"participant_id": 2})
    conversation_id = conversation_response.json()["id"]
    response = client.get(f"/api/v1/chats/conversations/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id

def test_create_message():
    conversation_response = client.post("/api/v1/chats/conversations", json={"participant_id": 2})
    conversation_id = conversation_response.json()["id"]
    response = client.post(
        f"/api/v1/chats/conversations/{conversation_id}/messages",
        json={"content": "Hello, world!"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello, world!"

def test_get_messages():
    conversation_response = client.post("/api/v1/chats/conversations", json={"participant_id": 2})
    conversation_id = conversation_response.json()["id"]
    client.post(
        f"/api/v1/chats/conversations/{conversation_id}/messages",
        json={"content": "Hello, world!"},
    )
    response = client.get(f"/api/v1/chats/conversations/{conversation_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"] == "Hello, world!"
