"""Baseline text classifier using scikit-learn (TF-IDF + Logistic Regression).

Implements BaseClassifier without requiring an external LLM or API.
Trained on bootstrap domain concept data derived strictly from the knowledge base.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .classifier import BaseClassifier
from .config import CANONICAL_DOMAINS
from .data.bootstrap_data import BOOTSTRAP_TRAINING_EXAMPLES
from .intent import resolve_intent_name
from .schemas import ClassificationResult

logger = logging.getLogger(__name__)


class BaselineClassifier(BaseClassifier):
    """Local scikit-learn classifier providing baseline domain predictions and calibrated probabilities.
    
    Serves as the default reference classifier during development and evaluation,
    and shares the exact same contract as future LLM classifiers (such as GeminiClassifier).
    """

    def __init__(self, training_data: Optional[List[tuple]] = None) -> None:
        self._name = "BaselineClassifier(TF-IDF + LogisticRegression)"
        data = training_data or BOOTSTRAP_TRAINING_EXAMPLES
        self._texts = [item[0] for item in data]
        self._labels = [item[1] for item in data]

        self._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents="unicode",
            lowercase=True,
            token_pattern=r"(?u)\b[a-zA-Z0-9_-]+\b",
        )
        self._clf = LogisticRegression(
            C=3.0,
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
            solver="lbfgs",
        )

        self._pipeline = Pipeline([
            ("tfidf", self._vectorizer),
            ("clf", self._clf),
        ])
        self._fit()

    def _fit(self) -> None:
        """Fit the pipeline on training data."""
        self._pipeline.fit(self._texts, self._labels)
        self._classes = list(self._pipeline.classes_)

    @property
    def name(self) -> str:
        return self._name

    def classify(self, query: str) -> ClassificationResult:
        """Classify a query string into domain, intent, and confidence score."""
        clean_query = query.strip()
        if not clean_query:
            return ClassificationResult(
                domain=None,
                intent=None,
                confidence=0.0,
                domain_probabilities={d: 0.0 for d in CANONICAL_DOMAINS},
            )

        # Check vocabulary overlap to safely catch out-of-domain / zero-match queries
        tfidf_vec = self._vectorizer.transform([clean_query])
        nnz = tfidf_vec.nnz
        num_terms = len(clean_query.split())

        # Predict probability distribution
        probas = self._pipeline.predict_proba([clean_query])[0]
        prob_dict: Dict[str, float] = {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(self._classes, probas)
        }
        for d in CANONICAL_DOMAINS:
            if d not in prob_dict:
                prob_dict[d] = 0.0

        top_domain = max(prob_dict, key=prob_dict.get)  # type: ignore
        top_prob = prob_dict[top_domain]

        # Penalize confidence if very few terms matched the vocabulary
        if nnz == 0:
            top_prob = 0.05
            prob_dict = {d: 0.05 for d in CANONICAL_DOMAINS}
        elif nnz == 1 and num_terms >= 4:
            # Only one stray word matched in a multi-word query
            top_prob = round(top_prob * 0.5, 4)

        intent = resolve_intent_name(top_domain, clean_query) if top_prob > 0.1 else "unknown"

        return ClassificationResult(
            domain=top_domain if top_prob >= 0.15 else None,
            intent=intent,
            confidence=top_prob,
            domain_probabilities=prob_dict,
            raw_response={"nnz_features": nnz, "word_count": num_terms},
        )
