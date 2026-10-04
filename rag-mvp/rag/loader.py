"""Knowledge-base loading and light cleaning.

A Markdown file is a *knowledge-base document* if its first table is a
metadata table containing at least `document_id` (see the `**Metadata**` block
in each KB file). Files without it - the context/index file and the
evaluation/RAG-notes file - are skipped, so project documentation never ends up
in the searchable index. No file names are hard-coded: dropping a new
`XYZ-KB-001.md` with a metadata block into the KB folder is enough.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Optional

from .config import get_settings
from .models import Document

log = logging.getLogger(__name__)

# "| document_id | IT-KB-001 |" -> ("document_id", "IT-KB-001"). Keys are snake_case,
# which excludes header rows ("| Field | Value |") and ordinary content tables.
_META_ROW = re.compile(r"^\|\s*([a-z][a-z0-9_]*)\s*\|\s*(.*?)\s*\|?\s*$")
_REQUIRED = ("document_id", "domain", "document_title")


def _clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _split_metadata(text: str) -> tuple[dict, str]:
    """Return (metadata from the first table, text after that table)."""
    lines = text.split("\n")
    meta: dict = {}
    start = end = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            if start is None:
                start = i
            m = _META_ROW.match(line.strip())
            if m:
                meta[m.group(1)] = m.group(2)
            end = i
        elif start is not None:
            break
    if start is None:
        return {}, text
    return meta, "\n".join(lines[end + 1 :]).strip()


def load_document(path: Path, kb_dir: Path) -> Optional[Document]:
    """Load one file; return None if it is not a knowledge-base document."""
    text = _clean(path.read_text(encoding="utf-8"))
    meta, body = _split_metadata(text)
    if "document_id" not in meta:
        return None
    missing = [k for k in _REQUIRED if not meta.get(k)]
    if missing:
        raise ValueError(f"{path.name}: metadata is missing {missing}")
    rel = path.relative_to(kb_dir).as_posix()
    return Document(
        document_id=meta["document_id"],
        domain=meta["domain"],
        title=meta["document_title"],
        source_file=f"{kb_dir.name}/{rel}",
        text=body,
        metadata=meta,
    )


def load_documents(kb_dir: Optional[Path] = None) -> list[Document]:
    """Load every knowledge-base document under `kb_dir` (default: settings)."""
    kb_dir = Path(kb_dir) if kb_dir else get_settings().kb_dir
    if not kb_dir.is_dir():
        raise FileNotFoundError(f"Knowledge-base directory not found: {kb_dir}")
    docs: dict[str, Document] = {}
    for path in sorted(kb_dir.rglob("*.md")):
        doc = load_document(path, kb_dir)
        if doc is None:
            log.info("Skipping non-KB file: %s", path.name)
            continue
        if doc.document_id in docs:
            raise ValueError(
                f"Duplicate document_id {doc.document_id}: "
                f"{docs[doc.document_id].source_file} and {doc.source_file}"
            )
        docs[doc.document_id] = doc
    return list(docs.values())
