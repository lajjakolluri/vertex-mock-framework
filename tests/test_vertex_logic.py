import os
import pytest
import logging
from vertex_mock.client import MockGenerativeModel

def ask_my_ai_app(prompt: str):
    model = MockGenerativeModel("gemini-1.5-pro")
    return model.generate_content(prompt)

def test_vertex_prediction_flow():
    response = ask_my_app("Hello, vertex!")
    assert "predictions" in response
    assert response["predictions"][0]["content"] == "Hello! I am your 
mocked Vertex AI assistant."
    
def test_vertex_caching_mechanism(caplog):
    with caplog.at_level(logging.INFO):
        ask_my_ai_app("Cache testing prompt")
        assert '"cached": false' in caplog.text
        
        caplog.clear()
        
        ask_my_ai_app("Cache testing prompt")
        assert '"cached": true' in caplog.text
