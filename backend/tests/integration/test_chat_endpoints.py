import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.chat import RAGChatRequest, ContextContent, ContextContentTypeEnum


client = TestClient(app)


def test_chat_endpoint_unauthenticated():
    """Test chat endpoint returns proper message for unauthenticated requests."""
    # Create a test request
    test_request = RAGChatRequest(
        question="What is artificial intelligence?",
        context=ContextContent(
            type=ContextContentTypeEnum.retrieved_excerpt,
            content="Artificial intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence.",
            source_document_id="test-doc-1"
        ),
        mode="rag-mode"
    )

    # Send request without authentication
    response = client.post("/api/v1/chat/rag", json=test_request.model_dump())

    # Should return the exact unauthenticated message
    assert response.status_code == 200  # The endpoint should return 200 but with unauth message
    assert response.json()["answer"] == "Please sign in or create an account to use the chatbot."
    assert response.json()["status"] == "unauthorized"


def test_auth_verify_endpoint():
    """Test authentication verification endpoint."""
    # Test with invalid token
    response = client.post("/api/v1/auth/verify", json={"token": "invalid_token"})

    assert response.status_code == 200
    assert response.json()["authenticated"] is False
    assert response.json()["message"] == "Invalid or expired token"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Textbook RAG API"
    assert response.json()["status"] == "running"