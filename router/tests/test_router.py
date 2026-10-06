"""End-to-end tests for OmniDesk-AI Router engine and FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient

from router.main import app
from router.router import get_router, route_query
from router.schemas import RoutingResult

client = TestClient(app)


# --------------------------------------------------------------------------- #
# Core Router Engine Tests
# --------------------------------------------------------------------------- #

def test_concrete_prompt_vpn_and_reimbursement():
    """Prompt from spec: 'My VPN isn't working and I need the travel reimbursement limit.'"""
    q = "My VPN isn't working and I need the travel reimbursement limit."
    result = route_query(q)

    assert isinstance(result, RoutingResult)
    assert not result.needs_clarification
    domains = [r.domain for r in result.intents]
    assert "IT" in domains
    assert "Finance" in domains


def test_concrete_prompt_leave_policy():
    """Prompt from spec: 'What is the leave policy?'"""
    q = "What is the leave policy?"
    result = route_query(q)

    assert isinstance(result, RoutingResult)
    assert not result.needs_clarification
    assert len(result.intents) == 1
    assert result.intents[0].domain == "HR"


def test_concrete_prompt_ambiguous_policy():
    """Prompt from spec: 'Tell me about the policy.' -> needs_clarification=True"""
    q = "Tell me about the policy."
    result = route_query(q)

    assert isinstance(result, RoutingResult)
    assert result.needs_clarification
    assert result.clarification_question is not None
    assert len(result.intents) == 0


def test_cross_domain_laptop_and_leave():
    """Prompt from spec: 'My laptop is broken and how many casual leaves do I have?'"""
    q = "My laptop is broken and how many casual leaves do I have?"
    result = route_query(q)

    assert not result.needs_clarification
    domains = [r.domain for r in result.intents]
    assert "IT" in domains
    assert "HR" in domains


def test_same_domain_multi_intent():
    q = "How do I reset my password and unlock my account?"
    result = route_query(q)

    assert not result.needs_clarification
    assert len(result.intents) == 2
    assert all(r.domain == "IT" for r in result.intents)
    intents = {r.intent for r in result.intents}
    assert "password_reset" in intents
    assert "account_unlock" in intents


def test_empty_query_raises_value_error():
    with pytest.raises(ValueError):
        route_query("   ")


def test_out_of_domain_queries():
    ood_queries = [
        "What is the weather in Delhi?",
        "What is the capital of France?",
        "I want a recipe for pasta.",
    ]
    for q in ood_queries:
        res = route_query(q)
        assert res.is_out_of_domain
        assert not res.needs_clarification
        assert len(res.intents) == 0


# --------------------------------------------------------------------------- #
# FastAPI Endpoint Tests
# --------------------------------------------------------------------------- #

def test_api_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "OmniDesk-AI Router"
    assert "BaselineClassifier" in data["classifier"]


def test_api_route_endpoint_success():
    payload = {"query": "My VPN isn't working and I need the travel reimbursement limit."}
    response = client.post("/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert not data["needs_clarification"]
    domains = [r["domain"] for r in data["intents"]]
    assert "IT" in domains
    assert "Finance" in domains


def test_api_route_endpoint_ambiguous():
    payload = {"query": "Tell me about the policy."}
    response = client.post("/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["needs_clarification"]
    assert "Which policy are you asking about" in data["clarification_question"]


def test_api_route_endpoint_empty_query():
    payload = {"query": "   "}
    response = client.post("/route", json=payload)
    assert response.status_code in (400, 422)


def test_api_route_endpoint_invalid_body():
    response = client.post("/route", json={})
    assert response.status_code == 422
