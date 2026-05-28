#!/bin/bash

echo "🚀 Building Vertex Mock SDK Testing Framework..."

# 1. Create the entire directory structure
mkdir -p vertex_mock/fixtures tests

# 2. Create the JSON Fixture file
cat << 'EOF' > vertex_mock/fixtures/predict_text.json
{
  "predictions": [
    {
      "content": "This is a mocked response from the Vertex SDK Testing 
Framework!",
      "safetyAttributes": {
        "blocked": false,
        "categories": [],
        "scores": []
      }
    }
  ],
  "metadata": {
    "tokenMetadata": {
      "inputTokenCount": 10,
      "outputTokenCount": 12
    }
  }
}
EOF

# 3. Create the blank __init__.py file
touch vertex_mock/__init__.py

# 4. Create the Logger middleware
cat << 'EOF' > vertex_mock/logger.py
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s 
[%(levelname)s] %(message)s")
logger = logging.getLogger("VertexMockSDK")

def log_interaction(prompt, response, cached=False):
    log_data = {
        "event": "vertex_api_call",
        "cached": cached,
        "prompt_preview": prompt[:50] + "..." if len(prompt) > 50 else 
prompt,
        "response_preview": response["predictions"][0]["content"][:50] + 
"..."
    }
    logger.info(json.dumps(log_data))
EOF

# 5. Create the Cache middleware
cat << 'EOF' > vertex_mock/cache.py
import hashlib

class VertexCache:
    def __init__(self):
        self._cache = {}

    def _generate_key(self, model, prompt, parameters):
        raw_key = f"{model}:{prompt}:{str(parameters)}"
        return hashlib.md5(raw_key.encode('utf-8')).hexdigest()

    def get(self, model, prompt, parameters):
        key = self._generate_key(model, prompt, parameters)
        return self._cache.get(key)

    def set(self, model, prompt, parameters, response):
        key = self._generate_key(model, prompt, parameters)
        self._cache[key] = response
EOF

# 6. Create the Mock SDK Client
cat << 'EOF' > vertex_mock/client.py
import json
import os
from .logger import log_interaction
from .cache import VertexCache

class MockGenerativeModel:
    def __init__(self, model_name: str, use_cache: bool = True):
        self.model_name = model_name
        self.use_cache = use_cache
        self.cache = VertexCache()
        
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 
'predict_text.json')
        with open(fixture_path, 'r') as f:
            self._default_response = json.load(f)

    def generate_content(self, prompt: str, generation_config: dict = 
None) -> dict:
        if self.use_cache:
            cached_res = self.cache.get(self.model_name, prompt, 
generation_config)
            if cached_res:
                log_interaction(prompt, cached_res, cached=True)
                return cached_res

        response = self._default_response.copy()
        
        if "hello" in prompt.lower():
            response["predictions"][0]["content"] = "Hello! I am your 
mocked Vertex AI assistant."

        if self.use_cache:
            self.cache.set(self.model_name, prompt, generation_config, 
response)

        log_interaction(prompt, response, cached=False)
        return response
EOF

# 7. Create the test suite environment gatekeeper (conftest.py)
cat << 'EOF' > tests/conftest.py
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
EOF

# 8. Create the unit tests file
cat << 'EOF' > tests/test_vertex_logic.py
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
EOF

echo "✅ Done! All folders and files have been beautifully generated."
echo "👉 Run your tests now using: MOCK_VERTEX=true PYTHONPATH=. pytest 
tests/ -v --log-cli-level=INFO"
