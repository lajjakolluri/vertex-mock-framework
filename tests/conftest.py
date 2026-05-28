import pytest
import os
from unittest.mock import patch
from vertex_mock.client import MockGenerativeModel

@pytest.fixture(autouse=True)
def mock_vertex_environment():
    if os.getenv("ENVIRONMENT") == "CI" or os.getenv("MOCK_VERTEX") == 
"true":
        with patch('vertexai.generative_models.GenerativeModel', 
new=MockGenerativeModel):
            yield
    else:
        yield
