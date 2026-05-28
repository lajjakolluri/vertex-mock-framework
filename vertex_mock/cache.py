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
