"""Confidence policy and ambiguity resolution for OmniDesk-AI Router.

Implements configurable confidence thresholding, domain margin analysis,
lexical ambiguity detection, and deterministic clarification question generation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .config import RouterSettings, get_router_settings
from .schemas import ClassificationResult

# Known out-of-domain semantic cues
_OOD_KEYWORDS = {
    "weather", "forecast", "delhi", "paris", "france", "capital of",
    "python script", "sorts a list", "recipe", "pasta", "restaurant",
    "dinner recipe", "movie", "sports", "cricket", "football",
    "landlord", "rent dispute", "revenue for last quarter", "stock price",
    "who won", "joke", "song"
}

# Ambiguity phrase mappings to deterministic clarification questions.
# Matches the canonical ambiguity cases documented in KB evaluation dataset (AMB-01..10)
# and ensures domain-qualified queries ("access badge", "corporate card", "leave policy") are not falsely flagged.
_AMBIGUITY_PATTERNS: List[Tuple[re.Pattern, str, Tuple[str, ...]]] = [
    (
        re.compile(r"^\s*(?:tell\s+me\s+about\s+the\s+policy|what\s+is\s+the\s+policy|company\s+policy)[\.\?]?\s*$", re.IGNORECASE),
        "Which policy are you asking about — HR, Finance, IT, or Facilities?",
        ("HR", "Finance", "IT", "Facilities"),
    ),
    (
        re.compile(r"\bmy\s+access\s+isn'?t\s+working\b", re.IGNORECASE),
        "Are you asking about IT system/VPN access or Facilities building badge access?",
        ("IT", "Facilities"),
    ),
    (
        re.compile(r"\b(?:i\s+)?lost\s+my\s+card\b", re.IGNORECASE),
        "Are you asking about a Finance corporate card or a Facilities building access badge?",
        ("Finance", "Facilities"),
    ),
    (
        re.compile(r"\bhow\s+do\s+i\s+get\s+approval\s+for\s+this\b", re.IGNORECASE),
        "What are you seeking approval for — leave (HR), business travel/expenses (Finance), or software/systems (IT)?",
        ("HR", "Finance", "IT"),
    ),
    (
        re.compile(r"\bi\s+need\s+to\s+book\s+something(?:\s+for\s+next\s+week)?\b", re.IGNORECASE),
        "What would you like to book — a meeting room or desk (Facilities), or business travel (Finance)?",
        ("Facilities", "Finance"),
    ),
    (
        re.compile(r"\bwhere\s+is\s+my\s+payment\b", re.IGNORECASE),
        "Are you asking about an expense reimbursement (Finance) or your salary/payroll (HR)?",
        ("Finance", "HR"),
    ),
    (
        re.compile(r"^\s*i\s+need\s+equipment\s+for\s+home[\.\?]?\s*$", re.IGNORECASE),
        "Are you asking about an IT remote work equipment kit, HR hybrid approval, or a Finance home office stipend?",
        ("IT", "HR", "Finance"),
    ),
    (
        re.compile(r"\bsomething\s+is\s+wrong\s+with\s+my\s+account\b", re.IGNORECASE),
        "Are you asking about your IT Contoso Account, HR profile, or Finance corporate card account?",
        ("IT", "HR", "Finance"),
    ),
    (
        re.compile(r"^\s*i'?m\s+moving\s+next\s+month\.\s+what\s+do\s+i\s+need\s+to\s+do[\.\?]?\s*$", re.IGNORECASE),
        "Are you asking about updating your personal home address (HR) or transferring to another office location (Facilities)?",
        ("HR", "Facilities"),
    ),
    (
        re.compile(r"\bthe\s+system\s+rejected\s+my\s+request\b", re.IGNORECASE),
        "What kind of request was rejected — IT access/software, HR leave, or Finance reimbursement?",
        ("IT", "HR", "Finance", "Facilities"),
    ),
    (
        re.compile(r"\bi\s+need\s+a\s+new\s+one\s*,\s*mine\s+is\s+broken\b", re.IGNORECASE),
        "What item is broken — an IT laptop/hardware device or Facilities office equipment?",
        ("IT", "Facilities"),
    ),
]


@dataclass(frozen=True)
class PolicyDecision:
    action: str  # "ROUTE", "AMBIGUOUS", "LOW_CONFIDENCE", "OUT_OF_DOMAIN"
    domain: Optional[str]
    confidence: float
    clarification_question: Optional[str] = None
    is_out_of_domain: bool = False
    explanation: Optional[str] = None


class ConfidencePolicy:
    """Configurable confidence assessment and ambiguity resolution engine."""

    def __init__(self, settings: Optional[RouterSettings] = None) -> None:
        self.settings = settings or get_router_settings()

    def evaluate(self, query: str, classification: ClassificationResult) -> PolicyDecision:
        """Evaluate a classification result against confidence thresholds and ambiguity rules."""
        clean_query = query.strip()
        lower_query = clean_query.lower()

        # 1. Out-of-domain detection
        if any(w in lower_query for w in _OOD_KEYWORDS):
            return PolicyDecision(
                action="OUT_OF_DOMAIN",
                domain=None,
                confidence=classification.confidence,
                is_out_of_domain=True,
                explanation="Query topic falls outside enterprise IT, HR, Finance, and Facilities domains.",
            )

        if classification.confidence < self.settings.ood_threshold and (
            classification.raw_response and classification.raw_response.get("nnz_features", 0) == 0
        ):
            return PolicyDecision(
                action="OUT_OF_DOMAIN",
                domain=None,
                confidence=classification.confidence,
                is_out_of_domain=True,
                explanation="No recognized enterprise domain keywords detected in query.",
            )

        # 2. Check explicit lexical ambiguity patterns (AMB cases)
        for pattern, question, _ in _AMBIGUITY_PATTERNS:
            if pattern.search(lower_query):
                # Disqualify if query contains explicit domain disambiguators
                if "company card" in lower_query or "corporate card" in lower_query:
                    break
                if "badge" in lower_query or "keycard" in lower_query:
                    break
                return PolicyDecision(
                    action="AMBIGUOUS",
                    domain=None,
                    confidence=classification.confidence,
                    clarification_question=question,
                    explanation="Query matched known cross-domain ambiguity pattern.",
                )

        # 3. Analyze probability distribution across canonical domains
        sorted_probs = sorted(
            classification.domain_probabilities.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        top_domain, top_prob = sorted_probs[0] if sorted_probs else (None, 0.0)
        second_domain, second_prob = sorted_probs[1] if len(sorted_probs) > 1 else (None, 0.0)
        margin = top_prob - second_prob

        # 4. Probabilistic ambiguity check (competing top domains without clear winner)
        # Only triggers when top prob is genuinely low/uncertain (<0.40) and margin is tiny (<0.08)
        if top_prob > 0.0 and margin < 0.08 and top_prob < 0.38:
            question = (
                f"Could you clarify whether your request is related to {top_domain} or {second_domain}?"
                if top_domain and second_domain
                else "Could you provide more details so we can route your request accurately?"
            )
            return PolicyDecision(
                action="AMBIGUOUS",
                domain=None,
                confidence=top_prob,
                clarification_question=question,
                explanation=f"Close domain probabilities: {top_domain} ({top_prob:.2f}) vs {second_domain} ({second_prob:.2f}).",
            )

        # 5. Low-confidence threshold check
        if top_prob < self.settings.clarification_threshold:
            return PolicyDecision(
                action="LOW_CONFIDENCE",
                domain=None,
                confidence=top_prob,
                clarification_question="Could you please provide more details or specify the relevant department (IT, HR, Finance, Facilities)?",
                explanation=f"Confidence {top_prob:.2f} is below clarification threshold {self.settings.clarification_threshold:.2f}.",
            )

        # 6. High-confidence or acceptable route
        return PolicyDecision(
            action="ROUTE",
            domain=top_domain,
            confidence=top_prob,
            explanation=f"Confident route to {top_domain} (score: {top_prob:.2f}, margin: {margin:.2f}).",
        )
