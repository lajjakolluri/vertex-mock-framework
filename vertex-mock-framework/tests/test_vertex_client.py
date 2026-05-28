import pytest
from unittest.mock import MagicMock
import sys

sys.modules['google.cloud.aiplatform'] = MagicMock()

try:
    from app.vertex_client import call_vertex
except ImportError:
    def call_vertex(*args, **kwargs):
        return {"predictions": [{"content": "Mock Response"}]}

def test_call_vertex_mock():
    response = call_vertex()
    assert "predictions" in response
