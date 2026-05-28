import pytest

def test_vertex_logic_response():
    response = {
        "predictions": [
            {"content": "Hello! I am your mock Vertex model."}
        ]
    }
    assert response["predictions"][0]["content"] == "Hello! I am your mock Vertex model."
