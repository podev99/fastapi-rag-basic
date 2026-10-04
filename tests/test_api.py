# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Initialize a TestClient to bypass running the actual Uvicorn server during tests
client = TestClient(app)

def test_health_check():
    """Test the /health endpoint to ensure the API is running correctly."""
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok", 
        "message": "System is running smoothly."
    }

@patch("app.api.routes.process_and_store_document")
def test_upload_pdf_success(mock_process):
    """
    Test the /upload endpoint with a valid PDF file.
    Uses @patch to mock the 'process_and_store_document' function,
    preventing actual calls to LangChain and Google Generative AI APIs.
    """
    # Mock the return value to simulate 5 chunks being created
    mock_process.return_value = 5
    
    # Create a dummy PDF file in memory
    file_data = {
        "file": ("dummy_test.pdf", b"This is a fake PDF content", "application/pdf")
    }
    
    response = client.post("/api/v1/upload", files=file_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "dummy_test.pdf"
    assert data["chunks_created"] == 5
    assert "successfully" in data["message"]
    
    # Verify that the mocked LangChain function was called exactly once
    mock_process.assert_called_once()

def test_upload_invalid_file_type():
    """Test that the /upload endpoint correctly rejects non-PDF files."""
    file_data = {
        "file": ("wrong_file.txt", b"Some text content", "text/plain")
    }
    
    response = client.post("/api/v1/upload", files=file_data)
    
    assert response.status_code == 400
    assert "only PDF files are supported" in response.json()["detail"]

@patch("app.api.routes.ask_question")
def test_chat_success(mock_ask):
    """
    Test the /chat endpoint with a valid user query.
    Mocks the LLM response to ensure deterministic testing without incurring API costs.
    """
    mock_ask.return_value = "This is a mocked answer from the LLM."
    
    payload = {"query": "What is FastAPI?"}
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is FastAPI?"
    assert data["answer"] == "This is a mocked answer from the LLM."
    
    # Verify the mocked function was called with the correct query
    mock_ask.assert_called_once_with("What is FastAPI?")

def test_chat_empty_query():
    """Test that the /chat endpoint rejects empty or whitespace-only queries."""
    payload = {"query": "   "}
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]