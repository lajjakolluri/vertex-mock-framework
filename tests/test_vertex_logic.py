import json
import pytest
from vertex_mock.client import MockGenerativeModel


# TIER 1: OUTCOME EVALUATION
def test_claims_adjudication_outcome():
    model = MockGenerativeModel(
        "gemini-1.5-pro", use_cache=False
    )
    response = model.generate_content(
        "Adjudicate incoming clinical billing"
        " data for claim CLM-88902-X"
    )
    pred = response["predictions"][0]
    claim = json.loads(pred["content"])
    assert claim["claim_id"] == "CLM-88902-X"
    assert claim["status"] == "PENDED"
    assert claim["pend_reason_code"] == "COB-01"
    assert isinstance(
        claim["member_responsibility"], float
    )
    assert isinstance(
        claim["employer_liability"], float
    )


# TIER 2: TRAJECTORY EVALUATION
def test_agent_trajectory_and_tool_auditing():
    model = MockGenerativeModel(
        "gemini-1.5-pro", use_cache=False
    )
    response = model.generate_content(
        "Adjudicate incoming clinical billing"
        " data for claim CLM-77123"
    )
    meta = response["predictions"][0]["metadata"]
    assert len(meta["tool_calls"]) > 0
    tool = meta["tool_calls"][0]
    assert tool["name"] == "fetch_member_eligibility"
    assert "member_id" in tool["arguments"]
    assert tool["arguments"]["member_id"] == "MEM-77123"
    traces = meta["reasoning_trace"]
    assert any("SOP Step" in t for t in traces)
    assert any("API Lookup:" in t for t in traces)


# TIER 3: AUTO-SxS REGRESSION
def test_sxs_pairwise_regulatory_stability():
    prompt = (
        "Adjudicate incoming clinical billing"
        " data for claim CLM-11223"
    )
    prod = MockGenerativeModel(
        "gemini-1.5-pro",
        use_cache=False,
        version="production",
    )
    cand = MockGenerativeModel(
        "gemini-1.5-pro",
        use_cache=False,
        version="candidate-v2.4",
    )
    pr = prod.generate_content(prompt)
    cr = cand.generate_content(prompt)
    pc = json.loads(pr["predictions"][0]["content"])
    cc = json.loads(cr["predictions"][0]["content"])
    pv = pr["predictions"][0]["metadata"]["model_version"]
    cv = cr["predictions"][0]["metadata"]["model_version"]
    assert pc["status"] == cc["status"], (
        "Regression: status changed between versions"
    )
    assert pc["pend_reason_code"] == cc["pend_reason_code"], (
        "Regression: pend code drifted"
    )
    assert pc["member_responsibility"] == (
        cc["member_responsibility"]
    ), "Regression: member responsibility changed"
    assert pv != cv, (
        "SxS misconfigured: same version on both instances"
    )
