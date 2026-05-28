from app.vertex_client import call_vertex

def test_known_prompt():
    assert call_vertex("hello") == "Hi! How can I help you?"

def test_unknown_prompt():
    assert call_vertex("random") == "UNKNOWN_PROMPT"

def test_case_insensitive():
    assert call_vertex("HeLLo") == "Hi! How can I help you?"
