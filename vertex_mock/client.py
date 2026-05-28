import json
import os
import re
import copy
from .logger import log_interaction
from .cache import VertexCache


class MockGenerativeModel:
    def __init__(self, model_name: str, use_cache: bool = True, version: str = "production"):
        self.model_name = model_name
        self.use_cache = use_cache
        self.version = version
        self.cache = VertexCache()

        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "predict_text.json")
        with open(fixture_path, "r") as f:
            self._default_response = json.load(f)

        self._golden_set_routes = []
        self._register_default_routes()

    def register_golden_route(self, pattern: str, outcome_factory):
        """Register a regex pattern mapped to an outcome factory callable."""
        self._golden_set_routes.append((re.compile(pattern, re.IGNORECASE), outcome_factory))

    def _register_default_routes(self):
        """Default golden routes. Add more via register_golden_route() after init."""
        self.register_golden_route(
            r"adjudicate.*claim[:\s]+([A-Z0-9-]+)",
            MockGenerativeModel._cob_pend_factory,
        )

    @staticmethod
    def _cob_pend_factory(groups):
        claim_id = groups[0] if groups else "CLM-UNKNOWN"
        member_id = "MEM-" + claim_id.split("-")[-1] if "-" in claim_id else "MEM-00000"
        return {
            "content": json.dumps({
                "claim_id": claim_id,
                "status": "PENDED",
                "pend_reason_code": "COB-01",
                "member_responsibility": 0.00,
                "employer_liability": 0.00,
            }),
            "candidate_step": "coordination_of_benefits_check",
            "reasoning_trace": [
                "SOP Step 4.2: Verify primary payer coverage indicators.",
                "API Lookup: Checked external eligibility registry for active commercial policies.",
            ],
            "tool_calls": [
                {"name": "fetch_member_eligibility", "arguments": {"member_id": member_id}}
            ],
        }

    def generate_content(self, prompt: str, generation_config: dict = None) -> dict:
        prompt_clean = prompt.strip()

        if self.use_cache:
            cached = self.cache.get(self.model_name, prompt_clean, generation_config)
            if cached:
                log_interaction(prompt_clean, cached, cached=True)
                return cached

        response = copy.deepcopy(self._default_response)

        matched = None
        for regex, factory in self._golden_set_routes:
            m = regex.search(prompt_clean)
            if m:
                matched = factory(m.groups())
                break

        if matched:
            response["predictions"][0]["content"] = matched["content"]
            response["predictions"][0]["metadata"] = {
                "candidate_step": matched["candidate_step"],
                "reasoning_trace": matched["reasoning_trace"],
                "tool_calls": matched["tool_calls"],
                "model_version": self.version,
            }
        else:
            response["predictions"][0]["content"] = (
                "Default fallback: Intent did not match any golden route."
            )
            response["predictions"][0]["metadata"] = {
                "tool_calls": [],
                "reasoning_trace": [],
                "model_version": self.version,
            }

        if self.use_cache:
            self.cache.set(self.model_name, prompt_clean, generation_config, response)

        log_interaction(prompt_clean, response, cached=False)
        return response
