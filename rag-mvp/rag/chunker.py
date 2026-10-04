"""Heading-aware chunking (pure Python, no Azure, no I/O).

Rules (from the KB's own "Recommended Chunking Boundaries"):
  * each `###` subsection is one chunk;
  * a `##` section with no `###` children (Purpose, Scope, Support Channels,
    Frequently Needed Information, ...) is one chunk;
  * text sitting directly under a `##` heading *before* its first `###` becomes
    its own chunk (only if there is any);
  * chunks never cross a `##` boundary; tables stay inside their section because
    we split on headings only;
  * chunk IDs are deterministic: `<document_id>#<section_number>`.
"""
from __future__ import annotations

import re
from typing import Iterable, Optional

from .models import Chunk, Document

_H1 = re.compile(r"^#\s+\S")
_H2 = re.compile(r"^##\s+(.+?)\s*$")
_H3 = re.compile(r"^###\s+(.+?)\s*$")
_NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")


def _parse_heading(raw: str) -> tuple[str, str]:
    """'5.9 Reporting a Lost Device' -> ('5.9', 'Reporting a Lost Device').

    Unnumbered headings fall back to a slug so they still get a stable ID.
    """
    m = _NUMBERED.match(raw)
    if m:
        return m.group(1), m.group(2).strip()
    return re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-"), raw.strip()


def _split_sections(body: str) -> list[dict]:
    """Walk the body once and return raw sections in document order."""
    sections: list[dict] = []
    h2: Optional[tuple[str, str]] = None
    cur: Optional[dict] = None
    in_fence = False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m2 = None if in_fence else _H2.match(line)
        m3 = None if in_fence else _H3.match(line)
        if not in_fence and _H1.match(line):
            cur, h2 = None, None  # document title / anything above the first ##
        elif m2:
            h2 = _parse_heading(m2.group(1))
            cur = {"number": h2[0], "title": h2[1], "parent": None, "lines": []}
            sections.append(cur)
        elif m3:
            num, title = _parse_heading(m3.group(1))
            cur = {"number": num, "title": title, "parent": h2, "lines": []}
            sections.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
        # else: preamble before the first "##" (e.g. synthetic-content notice) -> dropped
    return sections


def chunk_document(doc: Document) -> list[Chunk]:
    sections = _split_sections(doc.text)
    meta = doc.metadata
    chunks: list[Chunk] = []
    seen: set[str] = set()
    for s in sections:
        content = "\n".join(s["lines"]).strip()
        if not content:
            continue  # heading with no body (e.g. a "##" that only introduces "###"s)
        parent = s["parent"]
        if parent:
            crumb = f"{doc.title} > {parent[0]} {parent[1]} > {s['number']} {s['title']}"
        else:
            crumb = f"{doc.title} > {s['number']} {s['title']}"
        chunk_id = f"{doc.document_id}#{s['number']}"
        if chunk_id in seen:
            raise ValueError(f"Duplicate section number in {doc.document_id}: {s['number']}")
        seen.add(chunk_id)
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=doc.document_id,
                domain=doc.domain,
                document_title=doc.title,
                document_type=meta.get("document_type", ""),
                version=meta.get("version", ""),
                effective_date=meta.get("effective_date", ""),
                owner_department=meta.get("owner_department", ""),
                confidentiality=meta.get("confidentiality", ""),
                section_number=s["number"],
                section_title=s["title"],
                parent_section_number=parent[0] if parent else "",
                parent_section_title=parent[1] if parent else "",
                breadcrumb=crumb,
                content=content,
                source_file=doc.source_file,
                word_count=len(content.split()),
            )
        )
    return chunks


def chunk_documents(docs: Iterable[Document]) -> list[Chunk]:
    return [c for d in docs for c in chunk_document(d)]
