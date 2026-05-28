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
