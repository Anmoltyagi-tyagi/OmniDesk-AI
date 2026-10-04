import re
from collections import Counter
from pathlib import Path

import pytest

from rag.chunker import chunk_document, chunk_documents
from rag.loader import load_documents
from rag.models import Document

KB_DIR = Path(__file__).resolve().parent.parent / "knowledgebase"


@pytest.fixture(scope="module")
def docs():
    return load_documents(KB_DIR)


@pytest.fixture(scope="module")
def chunks(docs):
    return chunk_documents(docs)


def by_id(chunks, chunk_id):
    return next(c for c in chunks if c.chunk_id == chunk_id)


def test_chunk_counts_per_domain(chunks):
    # ### sections + "##" sections without "###" children (Purpose, Scope, Support Channels, FNI, ...)
    assert Counter(c.domain for c in chunks) == {"IT": 41, "HR": 39, "Finance": 40, "Facilities": 43}


def test_every_h3_becomes_one_chunk(docs, chunks):
    for doc in docs:
        h3 = re.findall(r"(?m)^### (\d+\.\d+) ", doc.text)
        got = [c.section_number for c in chunks if c.document_id == doc.document_id and "." in c.section_number]
        assert got == h3


def test_chunk_ids_are_deterministic_and_unique(docs, chunks):
    again = chunk_documents(docs)
    assert [c.chunk_id for c in chunks] == [c.chunk_id for c in again]
    assert chunks == again
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    assert by_id(chunks, "IT-KB-001#5.9").section_title == "Reporting a Lost or Stolen Device"


def test_no_chunk_crosses_a_heading_boundary(chunks):
    for c in chunks:
        assert not re.search(r"(?m)^#{1,6} ", c.content), c.chunk_id


def test_tables_stay_with_their_section(chunks):
    limits = by_id(chunks, "FIN-KB-001#4.3")
    assert limits.content.count("\n| Hotel") == 3 and "Client hospitality" in limits.content
    leave = by_id(chunks, "HR-KB-001#3.1")
    assert "| 3 to under 7 years | 22 working days |" in leave.content
    fni = by_id(chunks, "FAC-KB-001#12")  # Frequently Needed Information is section 12 in FAC
    assert fni.section_title == "Frequently Needed Information" and "| Lost badge |" in fni.content


def test_metadata_and_breadcrumb(chunks):
    c = by_id(chunks, "IT-KB-001#5.9")
    assert (c.document_id, c.domain, c.version, c.effective_date) == ("IT-KB-001", "IT", "1.0", "2026-10-01")
    assert c.source_file == "knowledgebase/IT-KB-001.md" and c.page is None
    assert c.parent_section_number == "5" and c.parent_section_title == "Procedures"
    assert c.breadcrumb == "IT Knowledge Base — Technology Services and Support > 5 Procedures > 5.9 Reporting a Lost or Stolen Device"
    assert c.word_count == len(c.content.split()) > 0
    top = by_id(chunks, "IT-KB-001#1")
    assert top.parent_section_number == "" and top.breadcrumb.endswith("> 1 Purpose")


def test_cross_references_survive_inside_chunks(chunks):
    assert "FIN-KB-001 Section 6.6" in by_id(chunks, "IT-KB-001#5.9").content
    assert "USD 800" in by_id(chunks, "IT-KB-001#5.9").content


def test_synthetic_notice_and_metadata_are_not_chunk_content(chunks):
    assert not any("Synthetic document" in c.content or "document_id |" in c.content for c in chunks)


def _doc(text: str) -> Document:
    return Document("T-KB-001", "T", "Test KB", "kb/T.md", text, {"document_id": "T-KB-001"})


def test_intro_text_under_h2_becomes_its_own_chunk():
    chunks = chunk_document(_doc("## 5. Procedures\n\nIntro line.\n\n### 5.1 First\n\nA\n\n### 5.2 Second\n\nB\n"))
    assert [(c.chunk_id, c.content) for c in chunks] == [
        ("T-KB-001#5", "Intro line."), ("T-KB-001#5.1", "A"), ("T-KB-001#5.2", "B"),
    ]


def test_h2_without_body_is_skipped_and_no_merge_across_h2():
    chunks = chunk_document(_doc("## 1. A\n\n### 1.1 X\n\none\n\n## 2. B\n\n### 2.1 Y\n\ntwo\n"))
    assert [(c.chunk_id, c.content) for c in chunks] == [("T-KB-001#1.1", "one"), ("T-KB-001#2.1", "two")]


def test_duplicate_section_numbers_fail_loudly_and_unnumbered_get_slug():
    with pytest.raises(ValueError, match="Duplicate section number"):
        chunk_document(_doc("## 1. A\n\nx\n\n## 1. B\n\ny\n"))
    assert chunk_document(_doc("## Overview\n\nx\n"))[0].chunk_id == "T-KB-001#overview"


def test_headings_inside_code_fences_are_ignored():
    chunks = chunk_document(_doc("## 1. A\n\n```\n## not a heading\n```\n\ntext\n"))
    assert len(chunks) == 1 and "## not a heading" in chunks[0].content
