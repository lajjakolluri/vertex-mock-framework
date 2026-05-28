import os
import pytest
from unittest.mock import MagicMock
import sys

# Force mock mode if explicitly set via environment variables
if os.getenv("ENVIRONMENT") == "CI" or os.getenv("MOCK_VERTEX") == "true":
    sys.modules['google.cloud.aiplatform'] = MagicMock()
