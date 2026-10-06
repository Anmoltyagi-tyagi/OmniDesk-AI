"""Configuration and settings for the OmniDesk-AI Router.

Centralizes canonical domain definitions, confidence thresholds, file paths,
and provider-agnostic classifier configuration points.
No secrets are stored here.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB_DIR = REPO_ROOT / "knowledgebase"
EVAL_FILENAME = "06_evaluation_dataset_and_rag_notes.md"

# Canonical domains recognized by the enterprise architecture
CANONICAL_DOMAINS = ("IT", "HR", "Finance", "Facilities")

# Normalized alias mappings matching the existing RAG contract
DOMAIN_ALIASES = {
    "it": "IT",
    "information technology": "IT",
    "hr": "HR",
    "human resources": "HR",
    "finance": "Finance",
    "fin": "Finance",
    "fees": "Finance",
    "finance / fees": "Finance",
    "finance/fees": "Finance",
    "facilities": "Facilities",
    "facility": "Facilities",
    "fac": "Facilities",
}

# Default confidence thresholds (configurable via environment variables)
DEFAULT_HIGH_CONFIDENCE_THRESHOLD = 0.65
DEFAULT_CLARIFICATION_THRESHOLD = 0.35
DEFAULT_AMBIGUITY_MARGIN_THRESHOLD = 0.15
DEFAULT_OOD_THRESHOLD = 0.30


@dataclass(frozen=True)
class RouterSettings:
    """Settings for the routing and classification layer."""

    kb_dir: Path
    eval_file: Path
    high_confidence_threshold: float
    clarification_threshold: float
    ambiguity_margin_threshold: float
    ood_threshold: float
    classifier_type: str

    # Future external model provider integration points (e.g. Azure OpenAI / Gemini)
    # (Leave None until external classifier is configured)
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_openai_api_version: Optional[str] = None


def get_router_settings() -> RouterSettings:
    """Load settings from environment variables with sensible defaults."""
    kb_dir = Path(os.getenv("ROUTER_KB_DIR") or DEFAULT_KB_DIR)
    eval_file = Path(os.getenv("ROUTER_EVAL_FILE") or (kb_dir / EVAL_FILENAME))

    return RouterSettings(
        kb_dir=kb_dir,
        eval_file=eval_file,
        high_confidence_threshold=float(
            os.getenv("ROUTER_HIGH_CONFIDENCE_THRESHOLD") or DEFAULT_HIGH_CONFIDENCE_THRESHOLD
        ),
        clarification_threshold=float(
            os.getenv("ROUTER_CLARIFICATION_THRESHOLD") or DEFAULT_CLARIFICATION_THRESHOLD
        ),
        ambiguity_margin_threshold=float(
            os.getenv("ROUTER_AMBIGUITY_MARGIN_THRESHOLD") or DEFAULT_AMBIGUITY_MARGIN_THRESHOLD
        ),
        ood_threshold=float(
            os.getenv("ROUTER_OOD_THRESHOLD") or DEFAULT_OOD_THRESHOLD
        ),
        classifier_type=(os.getenv("ROUTER_CLASSIFIER_TYPE") or "baseline").strip().lower(),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )
