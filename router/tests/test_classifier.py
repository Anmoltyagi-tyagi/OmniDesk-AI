"""Tests for BaseClassifier abstraction and BaselineClassifier implementation."""
import pytest

from router.baseline_classifier import BaselineClassifier
from router.classifier import BaseClassifier
from router.config import CANONICAL_DOMAINS
from router.schemas import ClassificationResult


def test_base_classifier_inheritance():
    assert issubclass(BaselineClassifier, BaseClassifier)


def test_baseline_classifier_instantiation_and_name():
    clf = BaselineClassifier()
    assert "BaselineClassifier" in clf.name


def test_baseline_classifier_single_prediction():
    clf = BaselineClassifier()
    res = clf.classify("How do I connect to the corporate VPN?")
    assert isinstance(res, ClassificationResult)
    assert res.domain == "IT"
    assert res.intent == "vpn"
    assert 0.0 <= res.confidence <= 1.0
    for domain in CANONICAL_DOMAINS:
        assert domain in res.domain_probabilities
        assert 0.0 <= res.domain_probabilities[domain] <= 1.0


def test_baseline_classifier_batch_prediction():
    clf = BaselineClassifier()
    queries = [
        "How do I reset my password?",
        "Can I carry over my annual leave?",
        "What is the nightly hotel expense limit?",
        "How do I book a meeting room?",
    ]
    results = clf.classify_batch(queries)
    assert len(results) == 4
    assert [r.domain for r in results] == ["IT", "HR", "Finance", "Facilities"]


def test_blank_query_handling():
    clf = BaselineClassifier()
    res = clf.classify("   ")
    assert res.domain is None
    assert res.confidence == 0.0


def test_custom_training_data_support():
    custom_data = [
        ("Printer queue stuck in office", "IT", "device_hardware"),
        ("Overtime pay rules and compensation", "HR", "employment_policy"),
    ]
    clf = BaselineClassifier(training_data=custom_data)
    res = clf.classify("Printer queue is not working")
    assert res.domain == "IT"
