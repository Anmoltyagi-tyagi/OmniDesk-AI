"""Ingestion CLI for the RAG module.

    python -m rag.ingest                    # load + chunk the KB, print per-domain counts
    python -m rag.ingest --export out.jsonl # also write every chunk as JSON lines
    python -m rag.ingest --demo             # run existing eval prompts through retrieve()
    python -m rag.ingest --domain IT --query "How do I reset my password?"

The eval/demo prompts are read from the repository's evaluation file
(`knowledgebase/06_evaluation_dataset_and_rag_notes.md`); they are *not* indexed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .chunker import chunk_documents
from .config import get_settings
from .loader import load_documents
from .models import Chunk
from .retriever import retrieve

_CASE_ID = re.compile(r"^(IT|HR|FIN|FAC)-\d+$")
_OOD_ID = re.compile(r"^OOD-\d+$")
_SECTION_REF = re.compile(r"§\s*(\d+(?:\.\d+)*)")
_DOC_REF = re.compile(r"\b((?:IT|HR|FIN|FAC)-KB-001)\b")


@dataclass(frozen=True)
class EvalCase:
    case_id: str  # "IT-01"
    query: str
    domain: str  # as written in the eval file: IT / HR / Finance / Facilities
    document_id: str  # "IT-KB-001"
    sections: tuple  # acceptable section numbers, e.g. ("5.6", "7.1")


def _table_rows(path: Path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def load_eval_cases(path: Optional[Path] = None) -> list[EvalCase]:
    """Single-domain eval queries (IT-xx, HR-xx, FIN-xx, FAC-xx) with expected sections."""
    path = Path(path) if path else get_settings().eval_file
    cases = []
    for cells in _table_rows(path):
        if len(cells) >= 4 and _CASE_ID.match(cells[0]):
            doc = _DOC_REF.search(cells[3])
            cases.append(
                EvalCase(
                    case_id=cells[0],
                    query=cells[1],
                    domain=cells[2],
                    document_id=doc.group(1) if doc else "",
                    sections=tuple(_SECTION_REF.findall(cells[3])),
                )
            )
    return cases


def load_ood_queries(path: Optional[Path] = None) -> list[tuple[str, str]]:
    """Out-of-domain queries (OOD-xx) that should retrieve nothing."""
    path = Path(path) if path else get_settings().eval_file
    return [(c[0], c[1]) for c in _table_rows(path) if len(c) >= 2 and _OOD_ID.match(c[0])]


def hit_rank(results, case: EvalCase) -> Optional[int]:
    """1-based rank of the first result matching the expected section, else None."""
    for i, r in enumerate(results, 1):
        if r.document_id == case.document_id and r.section_number in case.sections:
            return i
    return None


def is_hit(results, case: EvalCase) -> bool:
    return hit_rank(results, case) is not None


def build_chunks() -> list[Chunk]:
    return chunk_documents(load_documents())


def _print_stats(chunks: list[Chunk]) -> None:
    docs = Counter(c.document_id for c in chunks)
    per_domain = Counter(c.domain for c in chunks)
    print(f"Loaded {len(docs)} KB documents -> {len(chunks)} chunks")
    for domain in sorted(per_domain):
        ids = sorted({c.document_id for c in chunks if c.domain == domain})
        words = [c.word_count for c in chunks if c.domain == domain]
        print(f"  {domain:<11} {per_domain[domain]:>3} chunks  ({', '.join(ids)}; words/chunk {min(words)}-{max(words)})")


def _show(label: str, domain: str, query: str, results, expected: Optional[EvalCase] = None, show: int = 3) -> None:
    print(f"\n{label} [{domain}] {query}")
    if expected is not None:
        rank = hit_rank(results, expected)
        verdict = f"HIT at rank {rank}" if rank else "MISS (not in top results)"
        print(f"   expected {expected.document_id} §{' / §'.join(expected.sections)} -> {verdict}")
    if not results:
        print("   (no sufficiently relevant chunks - returned [])")
    for i, r in enumerate(results[:show], 1):
        print(f"   {i}. score={r.score:.3f}  {r.document_id} §{r.section_number} {r.section_title}  [{r.chunk_id}]")


def run_demo(per_domain: int = 2) -> None:
    cases = load_eval_cases()
    print("=== Single-domain prompts from the evaluation set ===")
    seen: Counter = Counter()
    for case in cases:
        if seen[case.domain] >= per_domain:
            continue
        seen[case.domain] += 1
        _show(case.case_id, case.domain, case.query, retrieve(case.domain, case.query, 5), case)
    print("\n=== Out-of-domain prompts (expected: no results) ===")
    for case_id, query in load_ood_queries()[:3]:
        _show(case_id, "IT", query, retrieve("IT", query, 3))
    print("\n=== Domain filtering: same query, different domain ===")
    q = "My laptop was lost or stolen"
    for domain in ("IT", "Finance", "Facilities"):
        _show("filter", domain, q, retrieve(domain, q, 2))


def main(argv: Optional[list[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="python -m rag.ingest", description=__doc__.split("\n")[0])
    ap.add_argument("--demo", action="store_true", help="run existing eval prompts through retrieve()")
    ap.add_argument("--export", metavar="PATH", help="write chunks as JSON lines")
    ap.add_argument("--domain", help="domain for --query")
    ap.add_argument("--query", help="run one ad-hoc query")
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args(argv)

    chunks = build_chunks()
    _print_stats(chunks)
    if args.export:
        with open(args.export, "w", encoding="utf-8") as fh:
            for c in chunks:
                fh.write(json.dumps(c.to_dict(), ensure_ascii=False) + "\n")
        print(f"Wrote {len(chunks)} chunks to {args.export}")
    if args.query:
        if not args.domain:
            ap.error("--query requires --domain")
        _show("query", args.domain, args.query, retrieve(args.domain, args.query, args.top_k))
    if args.demo:
        run_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
