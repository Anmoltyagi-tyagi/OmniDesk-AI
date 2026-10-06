"""Pydantic data models for OmniDesk-AI Router.

Strictly defines the contracts for:
- Classification result
- Route intents
- Overall routing result
- FastAPI request / response payloads
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from .config import CANONICAL_DOMAINS, DOMAIN_ALIASES

CanonicalDomainType = Literal["IT", "HR", "Finance", "Facilities"]


class RouteIntent(BaseModel):
    """A single routed sub-intent ready to be consumed by the RAG layer."""

    domain: str = Field(..., description="Canonical enterprise domain (IT, HR, Finance, Facilities)")
    intent: str = Field(..., min_length=1, description="Specific intent identifier or label")
    query: str = Field(..., min_length=1, description="The decomposed or original user sub-query")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Routing confidence score between 0.0 and 1.0")

    @field_validator("domain")
    @classmethod
    def validate_canonical_domain(cls, v: str) -> str:
        trimmed = (v or "").strip()
        if trimmed in CANONICAL_DOMAINS:
            return trimmed
        lower = trimmed.lower()
        if lower in DOMAIN_ALIASES:
            return DOMAIN_ALIASES[lower]
        raise ValueError(
            f"Invalid domain '{v}'. Must be one of canonical domains: {list(CANONICAL_DOMAINS)}"
        )

    @field_validator("query")
    @classmethod
    def validate_non_empty_query(cls, v: str) -> str:
        trimmed = (v or "").strip()
        if not trimmed:
            raise ValueError("Query string must not be empty or whitespace.")
        return trimmed

    @field_validator("confidence")
    @classmethod
    def validate_confidence_range(cls, v: float) -> float:
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Confidence score {v} must be between 0.0 and 1.0 inclusive.")
        return round(float(v), 4)


class RoutingResult(BaseModel):
    """The complete result of routing an employee query."""

    original_query: str = Field(..., description="Original user prompt before decomposition")
    intents: List[RouteIntent] = Field(default_factory=list, description="List of detected routes")
    needs_clarification: bool = Field(default=False, description="Whether user clarification is required")
    clarification_question: Optional[str] = Field(
        default=None, description="Deterministic question to present when ambiguous or low-confidence"
    )
    is_out_of_domain: bool = Field(
        default=False, description="Whether the query belongs outside supported enterprise domains"
    )
    explanation: Optional[str] = Field(
        default=None, description="Optional diagnostic or routing explanation"
    )

    @field_validator("original_query")
    @classmethod
    def validate_original_query(cls, v: str) -> str:
        trimmed = (v or "").strip()
        if not trimmed:
            raise ValueError("Original query must not be empty.")
        return trimmed

    @model_validator(mode="after")
    def validate_clarification_consistency(self) -> RoutingResult:
        if self.needs_clarification:
            if not self.clarification_question or not self.clarification_question.strip():
                raise ValueError("When needs_clarification is True, clarification_question must be provided.")
        else:
            if self.clarification_question is not None and not self.is_out_of_domain:
                raise ValueError("When needs_clarification is False, clarification_question must be None.")
        return self


class ClassificationResult(BaseModel):
    """Low-level output from any BaseClassifier implementation."""

    domain: Optional[str] = None
    intent: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    domain_probabilities: Dict[str, float] = Field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None

    @field_validator("domain")
    @classmethod
    def validate_domain_if_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        trimmed = v.strip()
        if trimmed in CANONICAL_DOMAINS:
            return trimmed
        lower = trimmed.lower()
        if lower in DOMAIN_ALIASES:
            return DOMAIN_ALIASES[lower]
        raise ValueError(f"Invalid domain '{v}'. Must be one of: {list(CANONICAL_DOMAINS)}")


class RouteRequest(BaseModel):
    """FastAPI payload for POST /route."""

    query: str = Field(..., min_length=1, description="Employee natural-language query")

    @field_validator("query")
    @classmethod
    def check_not_blank(cls, v: str) -> str:
        trimmed = (v or "").strip()
        if not trimmed:
            raise ValueError("Query must not be empty or blank.")
        return trimmed


class HealthResponse(BaseModel):
    """FastAPI payload for GET /health."""

    status: str = "healthy"
    service: str = "OmniDesk-AI Router"
    classifier: str
    version: str = "1.0.0"
