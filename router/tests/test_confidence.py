"""Tests for confidence policy, margin analysis, and ambiguity resolution."""
import pytest

from router.confidence import ConfidencePolicy
from router.config import get_router_settings
from router.schemas import ClassificationResult


def test_high_confidence_route():
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain="IT",
        intent="vpn",
        confidence=0.88,
        domain_probabilities={"IT": 0.88, "HR": 0.04, "Finance": 0.04, "Facilities": 0.04},
    )
    decision = policy.evaluate("My VPN is completely blocked", cr)
    assert decision.action == "ROUTE"
    assert decision.domain == "IT"
    assert decision.confidence == 0.88


def test_low_confidence_clarification():
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain="Finance",
        intent="unknown",
        confidence=0.25,
        domain_probabilities={"Finance": 0.25, "IT": 0.24, "HR": 0.26, "Facilities": 0.25},
    )
    decision = policy.evaluate("some vague inquiry", cr)
    assert decision.action in ("LOW_CONFIDENCE", "AMBIGUOUS")
    assert decision.domain is None
    assert decision.clarification_question is not None


def test_ambiguous_policy_query_triggers_clarification():
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain="HR",
        intent="employment_policy",
        confidence=0.45,
        domain_probabilities={"HR": 0.45, "IT": 0.20, "Finance": 0.20, "Facilities": 0.15},
    )
    decision = policy.evaluate("Tell me about the policy.", cr)
    assert decision.action == "AMBIGUOUS"
    assert "Which policy are you asking about" in decision.clarification_question


def test_ambiguous_access_query():
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain="IT",
        confidence=0.40,
        domain_probabilities={"IT": 0.40, "Facilities": 0.35, "HR": 0.15, "Finance": 0.10},
    )
    decision = policy.evaluate("My access isn't working.", cr)
    assert decision.action == "AMBIGUOUS"
    assert "IT system/VPN access or Facilities" in decision.clarification_question


def test_ambiguous_card_query():
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain="Finance",
        confidence=0.40,
        domain_probabilities={"Finance": 0.40, "Facilities": 0.35, "HR": 0.15, "IT": 0.10},
    )
    decision = policy.evaluate("I lost my card.", cr)
    assert decision.action == "AMBIGUOUS"
    assert "Finance corporate card or a Facilities" in decision.clarification_question


@pytest.mark.parametrize("ood_query", [
    "What is the weather in Delhi?",
    "What is the capital of France?",
    "Can you write a Python script that sorts a list of numbers?",
    "I want a recipe for pasta.",
    "Can you recommend a good restaurant near the office?",
])
def test_out_of_domain_detection(ood_query):
    policy = ConfidencePolicy()
    cr = ClassificationResult(
        domain=None,
        confidence=0.10,
        domain_probabilities={"IT": 0.10, "HR": 0.10, "Finance": 0.10, "Facilities": 0.10},
        raw_response={"nnz_features": 0},
    )
    decision = policy.evaluate(ood_query, cr)
    assert decision.action == "OUT_OF_DOMAIN"
    assert decision.is_out_of_domain
    assert decision.domain is None
