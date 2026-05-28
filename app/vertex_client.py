from app.responses import mock_vertex_responses

class VertexClient:
    def call(self, prompt: str) -> str:
        prompt = prompt.lower().strip()
        return mock_vertex_responses.get(prompt, "UNKNOWN_PROMPT")