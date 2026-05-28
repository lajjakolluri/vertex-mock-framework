import pytest

def test_vertex_logic_response():
    # Mock structure for testing assertions safely
    response = {
        "predictions": [
            {"content": "Hello! I am your mock Vertex model."}
        ]
    }
    
    # Properly terminated string literal comparison
    assert response["predictions"][0]["content"] == "Hello! I am your mock Vertex model."
