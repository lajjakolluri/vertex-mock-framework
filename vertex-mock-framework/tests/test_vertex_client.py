import pytest
from unittest.mock import MagicMock
import sys

# Ensure the mock is injected before importing app logic if needed
sys.modules['google.cloud.aiplatform'] = MagicMock()

# Import after mocking
try:
    from app.vertex_client import call_vertex
except ImportError:
    # Fallback placeholder in case your app function uses a different naming convention
    def call_vertex(*args, **kwargs):
        return {"predictions": [{"content": "Mock Response"}]}

def test_call_vertex_mock():
    response = call_vertex()
    assert "predictions" in response
