from pathlib import Path

import pytest

from rag.loader import load_documents

KB_DIR = Path(__file__).resolve().parent.parent / "knowledgebase"

META = """**Metadata**

| Field | Value |
|---|---|
| document_id | {doc_id} |
| domain | {domain} |
| document_title | {title} |

> Synthetic document notice.

# {title}

## 1. Purpose

Some text.
"""


def test_loads_the_four_domain_kbs():
    docs = load_documents(KB_DIR)
    assert {d.document_id for d in docs} == {"IT-KB-001", "HR-KB-001", "FIN-KB-001", "FAC-KB-001"}
    assert {d.domain for d in docs} == {"IT", "HR", "Finance", "Facilities"}


def test_project_docs_are_not_indexed():
    files = {d.source_file for d in load_documents(KB_DIR)}
    assert "knowledgebase/00_context_and_index.md" not in files
    assert "knowledgebase/06_evaluation_dataset_and_rag_notes.md" not in files
    assert all(f.endswith("-KB-001.md") for f in files)


def test_metadata_is_parsed_and_removed_from_body():
    doc = next(d for d in load_documents(KB_DIR) if d.document_id == "IT-KB-001")
    assert doc.title == "IT Knowledge Base — Technology Services and Support"
    assert doc.metadata["version"] == "1.0"
    assert doc.metadata["effective_date"] == "2026-10-01"
    assert "| document_id |" not in doc.text
    assert "## 1. Purpose" in doc.text


def test_loader_is_generic_new_domain_and_non_kb_files(tmp_path):
    (tmp_path / "LEG-KB-001.md").write_text(META.format(doc_id="LEG-KB-001", domain="Legal", title="Legal KB"))
    (tmp_path / "notes.md").write_text("# Project notes\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
    docs = load_documents(tmp_path)
    assert [(d.document_id, d.domain) for d in docs] == [("LEG-KB-001", "Legal")]


def test_duplicate_document_id_is_rejected(tmp_path):
    for name in ("a.md", "b.md"):
        (tmp_path / name).write_text(META.format(doc_id="X-KB-001", domain="X", title="X"))
    with pytest.raises(ValueError, match="Duplicate document_id"):
        load_documents(tmp_path)


def test_incomplete_metadata_is_rejected(tmp_path):
    (tmp_path / "bad.md").write_text("| Field | Value |\n|---|---|\n| document_id | X-KB-001 |\n\n## 1. A\n\ntext\n")
    with pytest.raises(ValueError, match="missing"):
        load_documents(tmp_path)


def test_missing_directory_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "nope")
