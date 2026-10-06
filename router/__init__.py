"""OmniDesk-AI AI Router package.

Public interface for domain and multi-intent classification, confidence policy,
and routing result generation.
"""
from __future__ import annotations

from .baseline_classifier import BaselineClassifier
from .classifier import BaseClassifier
from .config import CANONICAL_DOMAINS, DOMAIN_ALIASES, RouterSettings, get_router_settings
from .router import Router, get_router, route_query
from .schemas import (
    ClassificationResult,
    HealthResponse,
    RouteIntent,
    RouteRequest,
    RoutingResult,
)

__all__ = [
    "Router",
    "route_query",
    "get_router",
    "BaseClassifier",
    "BaselineClassifier",
    "RouteIntent",
    "RoutingResult",
    "ClassificationResult",
    "RouteRequest",
    "HealthResponse",
    "CANONICAL_DOMAINS",
    "DOMAIN_ALIASES",
    "RouterSettings",
    "get_router_settings",
]
