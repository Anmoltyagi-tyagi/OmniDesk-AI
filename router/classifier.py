"""Provider-agnostic classification abstraction for OmniDesk-AI.

Defines BaseClassifier which both BaselineClassifier (scikit-learn) and
future LLM classifiers (such as GeminiClassifier) implement.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from .schemas import ClassificationResult


class BaseClassifier(ABC):
    """Abstract base class for all router classifiers.
    
    Adhering strictly to this interface guarantees that the upstream Router,
    confidence policy engine, and downstream API endpoints remain 100% agnostic
    to whether classification is performed locally via scikit-learn or via an
    external LLM API (such as Gemini).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name or identifier of the classifier implementation."""
        pass

    @abstractmethod
    def classify(self, query: str) -> ClassificationResult:
        """Classify a single query into predicted domain, intent, and confidence score.

        Args:
            query: Natural language query string.

        Returns:
            ClassificationResult containing predicted domain, intent, confidence,
            and probability distribution across canonical domains.
        """
        pass

    def classify_batch(self, queries: List[str]) -> List[ClassificationResult]:
        """Classify a list of queries. Default implementation loops over classify.

        Can be overridden by sub-classes for optimized batching or vectorization.
        """
        return [self.classify(q) for q in queries]
