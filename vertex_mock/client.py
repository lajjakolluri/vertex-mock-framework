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
            response["predictions"][0]["content"] = "Hello! I am your mocked Vertex AI assistant."

        if self.use_cache:
            self.cache.set(self.model_name, prompt, generation_config, 
response)

        log_interaction(prompt, response, cached=False)
        return response
