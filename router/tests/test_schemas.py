"""Tests for Pydantic schemas and validation rules in router/schemas.py."""
import pytest
from pydantic import ValidationError

from router.schemas import (
    ClassificationResult,
    HealthResponse,
    RouteIntent,
    RouteRequest,
    RoutingResult,
)


def test_valid_route_intent():
    intent = RouteIntent(
        domain="IT",
        intent="vpn",
        query="My VPN is not connecting",
        confidence=0.95,
    )
    assert intent.domain == "IT"
    assert intent.intent == "vpn"
    assert intent.query == "My VPN is not connecting"
    assert intent.confidence == 0.95


def test_canonical_domain_normalization():
    # Lowercase alias should normalize to canonical name
    it_intent = RouteIntent(domain="it", intent="vpn", query="vpn down", confidence=0.8)
    assert it_intent.domain == "IT"

    fin_intent = RouteIntent(domain="finance / fees", intent="expenses", query="claim hotel", confidence=0.9)
    assert fin_intent.domain == "Finance"

    fac_intent = RouteIntent(domain="fac", intent="badge", query="lost badge", confidence=0.85)
    assert fac_intent.domain == "Facilities"

    hr_intent = RouteIntent(domain="human resources", intent="leave", query="vacation", confidence=0.7)
    assert hr_intent.domain == "HR"


def test_invalid_domain_raises_validation_error():
    with pytest.raises(ValidationError):
        RouteIntent(
            domain="Marketing",
            intent="ads",
            query="run campaign",
            confidence=0.8,
        )


def test_invalid_confidence_bounds():
    with pytest.raises(ValidationError):
        RouteIntent(domain="IT", intent="vpn", query="vpn test", confidence=1.5)

    with pytest.raises(ValidationError):
        RouteIntent(domain="IT", intent="vpn", query="vpn test", confidence=-0.1)


def test_empty_query_rejected():
    with pytest.raises(ValidationError):
        RouteIntent(domain="IT", intent="vpn", query="   ", confidence=0.8)


def test_valid_routing_result_without_clarification():
    res = RoutingResult(
        original_query="What is the annual leave policy?",
        intents=[
            RouteIntent(domain="HR", intent="annual_leave", query="What is the annual leave policy?", confidence=0.9)
        ],
        needs_clarification=False,
        clarification_question=None,
    )
    assert not res.needs_clarification
    assert res.clarification_question is None
    assert len(res.intents) == 1


def test_valid_routing_result_with_clarification():
    res = RoutingResult(
        original_query="Tell me about the policy.",
        intents=[],
        needs_clarification=True,
        clarification_question="Which policy are you asking about — HR, Finance, IT, or Facilities?",
    )
    assert res.needs_clarification
    assert res.clarification_question is not None


def test_clarification_inconsistency_validation():
    # needs_clarification=True requires clarification_question
    with pytest.raises(ValidationError):
        RoutingResult(
            original_query="ambiguous prompt",
            intents=[],
            needs_clarification=True,
            clarification_question=None,
        )

    # needs_clarification=False requires clarification_question to be None
    with pytest.raises(ValidationError):
        RoutingResult(
            original_query="clear prompt",
            intents=[],
            needs_clarification=False,
            clarification_question="Did you mean something else?",
        )


def test_route_request_validation():
    req = RouteRequest(query="My laptop screen is broken")
    assert req.query == "My laptop screen is broken"

    with pytest.raises(ValidationError):
        RouteRequest(query="   ")


def test_classification_result_defaults():
    cr = ClassificationResult()
    assert cr.domain is None
    assert cr.confidence == 0.0
    assert cr.domain_probabilities == {}
