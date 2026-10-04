"""Plain data containers shared by the RAG modules.

`RetrievedChunk` is the public output contract of `rag.retrieve()`. Callers
(router / orchestrator) depend on its fields, so treat them as a stable API.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class Document:
    """One knowledge-base file after loading and cleaning."""

    document_id: str
    domain: str
    title: str
    source_file: str  # e.g. "knowledgebase/IT-KB-001.md"
    text: str  # cleaned body, metadata table removed
    metadata: dict


@dataclass(frozen=True)
class Chunk:
    """One indexable unit: a `###` section (or a `##` section with no children)."""

    chunk_id: str  # deterministic, e.g. "IT-KB-001#5.9"
    document_id: str
    domain: str
    document_title: str
    document_type: str
    version: str
    effective_date: str
    owner_department: str
    confidentiality: str
    section_number: str  # "5.9"
    section_title: str  # "Reporting a Lost or Stolen Device"
    parent_section_number: str  # "5" ("" for top-level chunks)
    parent_section_title: str  # "Procedures" ("" for top-level chunks)
    breadcrumb: str  # "IT Knowledge Base ... > 5 Procedures > 5.9 Reporting ..."
    content: str  # clean section body (tables included, heading excluded)
    source_file: str
    word_count: int
    page: Optional[int] = None  # always None for Markdown sources

    @property
    def search_text(self) -> str:
        """Text that is embedded / keyword-indexed: breadcrumb + content."""
        return f"{self.breadcrumb}\n{self.content}"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class RetrievedChunk:
    """Result item returned by `retrieve()`. Backend-independent."""

    content: str
    score: float
    domain: str
    document_id: str
    section_number: str
    section_title: str
    source_file: str
    chunk_id: str
    page: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)
