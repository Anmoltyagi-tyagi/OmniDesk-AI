"""Settings and constants for the RAG module.

Everything configurable comes from environment variables (see `.env.example`).
No secrets are stored in code. The local MVP backend needs no credentials; the
Azure variables listed in `.env.example` are reserved for the later Azure AI
Search backend.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB_DIR = REPO_ROOT / "knowledgebase"
EVAL_FILENAME = "06_evaluation_dataset_and_rag_notes.md"

DEFAULT_BACKEND = "local"
DEFAULT_MIN_SCORE = 0.12

# Lower-cased alias -> canonical domain name used in KB metadata.
# Canonical names themselves are matched case-insensitively against the KB,
# so a new domain added to the KB works without touching this table.
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


@dataclass(frozen=True)
class Settings:
    kb_dir: Path
    backend: str
    min_score: float
    eval_file: Path


def get_settings() -> Settings:
    """Read settings from the environment (re-read on every call)."""
    kb_dir = Path(os.getenv("RAG_KB_DIR") or DEFAULT_KB_DIR)
    eval_file = Path(os.getenv("RAG_EVAL_FILE") or (kb_dir / EVAL_FILENAME))
    return Settings(
        kb_dir=kb_dir,
        backend=(os.getenv("RAG_BACKEND") or DEFAULT_BACKEND).strip().lower(),
        min_score=float(os.getenv("RAG_MIN_SCORE") or DEFAULT_MIN_SCORE),
        eval_file=eval_file,
    )
