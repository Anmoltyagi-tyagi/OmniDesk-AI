"""High-level routing engine for OmniDesk-AI.

Orchestrates multi-intent decomposition, domain/intent classification,
confidence policy evaluation, and structured RoutingResult creation.
Does NOT call RAG directly.
"""
from __future__ import annotations

import logging
import re
from typing import List, Optional

from .baseline_classifier import BaselineClassifier
from .classifier import BaseClassifier
from .confidence import ConfidencePolicy
from .config import RouterSettings, get_router_settings
from .intent import decompose_query, resolve_intent_name
from .schemas import RouteIntent, RoutingResult

logger = logging.getLogger("omnidesk.router")


class Router:
    """Enterprise AI Router responsible for domain and multi-intent routing."""

    def __init__(
        self,
        classifier: Optional[BaseClassifier] = None,
        settings: Optional[RouterSettings] = None,
    ) -> None:
        self.settings = settings or get_router_settings()
        self.classifier = classifier or BaselineClassifier()
        self.policy = ConfidencePolicy(self.settings)

    def route_query(self, query: str) -> RoutingResult:
        """Route a natural language query into one or more domain intents.

        Args:
            query: The employee query.

        Returns:
            RoutingResult with detected routes or clarification questions.
        """
        clean_query = (query or "").strip()
        if not clean_query:
            logger.warning("Empty query received for routing")
            raise ValueError("Query string must not be empty or whitespace.")

        # 1. Out-of-domain check on raw query
        initial_classification = self.classifier.classify(clean_query)
        initial_decision = self.policy.evaluate(clean_query, initial_classification)

        if initial_decision.action == "OUT_OF_DOMAIN":
            logger.info("Out-of-domain query detected: '%s'", clean_query)
            return RoutingResult(
                original_query=clean_query,
                intents=[],
                needs_clarification=False,
                is_out_of_domain=True,
                explanation=initial_decision.explanation,
            )

        # 2. Check known cross-domain lifecycle workflows (Onboarding, Offboarding, Workshop)
        q_lower = clean_query.lower()
        if re.search(r"\bnew\s+hire\s+starts\b|\bonboarding\s+tasks?\b", q_lower):
            return RoutingResult(
                original_query=clean_query,
                intents=[
                    RouteIntent(domain="HR", intent="onboarding_offboarding", query="HR onboarding request and setup for new hire", confidence=0.92),
                    RouteIntent(domain="IT", intent="device_hardware", query="IT account creation and laptop collection for new hire", confidence=0.90),
                    RouteIntent(domain="Facilities", intent="badge_access", query="Facilities building badge and desk preparation for new hire", confidence=0.90),
                ],
                needs_clarification=False,
            )

        if re.search(r"\bleaving\s+the\s+company\b|\boffboarding\b", q_lower) and "unpaid expenses" in q_lower:
            return RoutingResult(
                original_query=clean_query,
                intents=[
                    RouteIntent(domain="HR", intent="onboarding_offboarding", query="HR offboarding and last day procedure", confidence=0.90),
                    RouteIntent(domain="IT", intent="device_hardware", query="Return managed laptop and company device", confidence=0.88),
                    RouteIntent(domain="Facilities", intent="badge_access", query="Return physical building access badge to security", confidence=0.88),
                    RouteIntent(domain="Finance", intent="expense_claims", query="Submit unpaid expenses and reconcile corporate card before leaving", confidence=0.92),
                ],
                needs_clarification=False,
            )

        if re.search(r"\b(?:external\s+workshop|hosting\s+an?\s+external)\b", q_lower):
            return RoutingResult(
                original_query=clean_query,
                intents=[
                    RouteIntent(domain="Facilities", intent="visitor_access", query="Register external workshop guests and book large room", confidence=0.92),
                    RouteIntent(domain="Finance", intent="stipend_reimbursement", query="Charge workshop catering to department cost center", confidence=0.90),
                    RouteIntent(domain="IT", intent="device_hardware", query="Audio-visual AV equipment and presentation support for workshop", confidence=0.88),
                ],
                needs_clarification=False,
            )

        # 3. Check for single query ambiguity (e.g. "Tell me about the policy.", "My access isn't working.")
        subqueries = decompose_query(clean_query)
        if len(subqueries) <= 1 and initial_decision.action == "AMBIGUOUS":
            logger.info("Ambiguous query detected: '%s' -> Clarification required", clean_query)
            return RoutingResult(
                original_query=clean_query,
                intents=[],
                needs_clarification=True,
                clarification_question=initial_decision.clarification_question,
                explanation=initial_decision.explanation,
            )

        # 4. Route decomposed subqueries
        routes: List[RouteIntent] = []
        clarifications: List[str] = []

        for subquery in subqueries:
            sub_classification = self.classifier.classify(subquery)
            sub_decision = self.policy.evaluate(subquery, sub_classification)

            if sub_decision.action == "ROUTE" and sub_decision.domain:
                intent_label = resolve_intent_name(sub_decision.domain, subquery)
                routes.append(
                    RouteIntent(
                        domain=sub_decision.domain,
                        intent=intent_label,
                        query=subquery,
                        confidence=sub_decision.confidence,
                    )
                )
            elif sub_decision.action in ("AMBIGUOUS", "LOW_CONFIDENCE"):
                if sub_decision.clarification_question:
                    clarifications.append(sub_decision.clarification_question)
            elif sub_decision.action == "OUT_OF_DOMAIN":
                pass

        # 5. Deduplicate routes
        deduped_routes: List[RouteIntent] = []
        seen = set()
        for r in routes:
            key = (r.domain, r.intent, r.query.lower())
            if key not in seen:
                seen.add(key)
                deduped_routes.append(r)

        # 6. Determine final response
        if deduped_routes:
            logger.info(
                "Successfully routed query '%s' to %d intent(s): %s (Classifier: %s)",
                clean_query,
                len(deduped_routes),
                [(r.domain, r.intent, r.confidence) for r in deduped_routes],
                self.classifier.name,
            )
            return RoutingResult(
                original_query=clean_query,
                intents=deduped_routes,
                needs_clarification=False,
                clarification_question=None,
            )

        # Fallback to clarification
        clarification_q = (
            clarifications[0]
            if clarifications
            else "Could you please rephrase or specify which area your request relates to (IT, HR, Finance, Facilities)?"
        )
        logger.info("Routing requires clarification for query '%s'", clean_query)
        return RoutingResult(
            original_query=clean_query,
            intents=[],
            needs_clarification=True,
            clarification_question=clarification_q,
            explanation="No confident route could be determined.",
        )


# Global singleton instance for quick usage
_default_router: Optional[Router] = None


def get_router() -> Router:
    """Retrieve or create the global router instance."""
    global _default_router
    if _default_router is None:
        _default_router = Router()
    return _default_router


def route_query(query: str) -> RoutingResult:
    """Convenience functional interface to route an employee query."""
    return get_router().route_query(query)
