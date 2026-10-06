"""Evaluation harness for OmniDesk-AI Routing Layer.

Parses `knowledgebase/06_evaluation_dataset_and_rag_notes.md` without modifying it,
and runs the routing engine against:
- 40 single-domain queries (IT, HR, Finance, Facilities)
- 10 ambiguous queries
- 10 multi-domain queries
- 5 out-of-domain queries

Calculates domain accuracy, multi-intent detection accuracy, clarification accuracy,
and false-routing rate.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from .config import get_router_settings
from .router import Router, get_router
from .schemas import RoutingResult


@dataclass
class SingleDomainCase:
    case_id: str
    query: str
    expected_domain: str
    expected_section: str


@dataclass
class AmbiguousCase:
    case_id: str
    query: str
    possible_domains: List[str]
    expected_behavior: str


@dataclass
class MultiDomainCase:
    case_id: str
    query: str
    expected_domains: List[str]
    expected_intents: str


@dataclass
class OodCase:
    case_id: str
    query: str
    expected_behavior: str


def parse_eval_markdown(path: Path) -> Tuple[List[SingleDomainCase], List[AmbiguousCase], List[MultiDomainCase], List[OodCase]]:
    """Parse the four test suites from the markdown file."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    single_cases: List[SingleDomainCase] = []
    ambiguous_cases: List[AmbiguousCase] = []
    multi_cases: List[MultiDomainCase] = []
    ood_cases: List[OodCase] = []

    current_section = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## A.") or stripped.startswith("### A"):
            current_section = "A"
        elif stripped.startswith("## B."):
            current_section = "B"
        elif stripped.startswith("## C."):
            current_section = "C"
        elif stripped.startswith("## D."):
            current_section = "D"
        elif stripped.startswith("## ") and not any(k in stripped for k in ("A", "B", "C", "D")):
            current_section = None

        if not stripped.startswith("|"):
            continue

        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or cells[0] in ("#", "---"):
            continue

        cid = cells[0]

        # Section A: Single domain (IT-xx, HR-xx, FIN-xx, FAC-xx)
        if current_section == "A" and len(cells) >= 4 and re.match(r"^(?:IT|HR|FIN|FAC)-\d+$", cid):
            single_cases.append(
                SingleDomainCase(
                    case_id=cid,
                    query=cells[1],
                    expected_domain=cells[2],
                    expected_section=cells[3],
                )
            )

        # Section B: Ambiguous (AMB-xx)
        elif current_section == "B" and len(cells) >= 5 and re.match(r"^AMB-\d+$", cid):
            possible = [d.strip() for d in cells[2].split(",") if d.strip()]
            ambiguous_cases.append(
                AmbiguousCase(
                    case_id=cid,
                    query=cells[1],
                    possible_domains=possible,
                    expected_behavior=cells[4],
                )
            )

        # Section C: Multi domain (MD-xx)
        elif current_section == "C" and len(cells) >= 5 and re.match(r"^MD-\d+$", cid):
            expected_doms = [d.strip() for d in cells[2].split(",") if d.strip()]
            multi_cases.append(
                MultiDomainCase(
                    case_id=cid,
                    query=cells[1],
                    expected_domains=expected_doms,
                    expected_intents=cells[3],
                )
            )

        # Section D: Out of domain (OOD-xx)
        elif current_section == "D" and len(cells) >= 3 and re.match(r"^OOD-\d+$", cid):
            ood_cases.append(
                OodCase(
                    case_id=cid,
                    query=cells[1],
                    expected_behavior=cells[2],
                )
            )

    return single_cases, ambiguous_cases, multi_cases, ood_cases


def run_evaluation(router: Optional[Router] = None, verbose: bool = False) -> Dict[str, Any]:
    """Execute complete evaluation suite and return formatted metrics."""
    settings = get_router_settings()
    router = router or get_router()

    eval_path = settings.eval_file
    if not eval_path.exists():
        raise FileNotFoundError(f"Evaluation dataset file not found at: {eval_path}")

    single_cases, amb_cases, md_cases, ood_cases = parse_eval_markdown(eval_path)

    # 1. Single-domain evaluation
    single_correct = 0
    per_domain_stats: Dict[str, Dict[str, int]] = {
        d: {"total": 0, "correct": 0} for d in ("IT", "HR", "Finance", "Facilities")
    }

    single_results = []
    for c in single_cases:
        res = router.route_query(c.query)
        detected_domain = res.intents[0].domain if res.intents else None
        is_hit = detected_domain == c.expected_domain
        if is_hit:
            single_correct += 1
            per_domain_stats[c.expected_domain]["correct"] += 1
        per_domain_stats[c.expected_domain]["total"] += 1
        single_results.append((c.case_id, c.expected_domain, detected_domain, is_hit, c.query))

    single_acc = (single_correct / len(single_cases)) if single_cases else 0.0

    # 2. Ambiguity evaluation
    amb_correct = 0
    amb_results = []
    for c in amb_cases:
        res = router.route_query(c.query)
        is_clarified = res.needs_clarification and bool(res.clarification_question)
        if is_clarified:
            amb_correct += 1
        amb_results.append((c.case_id, is_clarified, res.clarification_question, c.query))

    amb_acc = (amb_correct / len(amb_cases)) if amb_cases else 0.0

    # 3. Multi-domain evaluation
    md_fully_detected = 0
    md_total_expected_domains = 0
    md_detected_expected_domains = 0
    md_results = []
    for c in md_cases:
        res = router.route_query(c.query)
        routed_domains = set(r.domain for r in res.intents)
        expected_set = set(c.expected_domains)
        is_full_match = expected_set.issubset(routed_domains)
        if is_full_match:
            md_fully_detected += 1
        matches = len(routed_domains.intersection(expected_set))
        md_detected_expected_domains += matches
        md_total_expected_domains += len(expected_set)
        md_results.append((c.case_id, c.expected_domains, list(routed_domains), is_full_match, c.query))

    md_full_acc = (md_fully_detected / len(md_cases)) if md_cases else 0.0
    md_domain_recall = (
        (md_detected_expected_domains / md_total_expected_domains)
        if md_total_expected_domains
        else 0.0
    )

    # 4. Out-of-domain evaluation
    ood_correct = 0
    ood_results = []
    for c in ood_cases:
        res = router.route_query(c.query)
        # OOD is correctly handled if it was identified as out of domain OR abstained / clarified
        # and NOT falsely routed into canonical domains with high confidence
        is_safe = res.is_out_of_domain or res.needs_clarification or len(res.intents) == 0
        if is_safe:
            ood_correct += 1
        ood_results.append((c.case_id, is_safe, res.is_out_of_domain, c.query))

    ood_acc = (ood_correct / len(ood_cases)) if ood_cases else 0.0

    # 5. Overall False-Routing Rate
    # False routing = single domain misrouted + ambiguous falsely routed + OOD falsely routed
    total_eval_queries = len(single_cases) + len(amb_cases) + len(ood_cases)
    false_single = len(single_cases) - single_correct
    false_amb = len(amb_cases) - amb_correct
    false_ood = len(ood_cases) - ood_correct
    total_false_routes = false_single + false_amb + false_ood
    false_routing_rate = (total_false_routes / total_eval_queries) if total_eval_queries else 0.0

    metrics = {
        "classifier": router.classifier.name,
        "single_domain_accuracy": single_acc,
        "single_domain_total": len(single_cases),
        "single_domain_correct": single_correct,
        "per_domain_stats": per_domain_stats,
        "ambiguity_clarification_accuracy": amb_acc,
        "ambiguity_total": len(amb_cases),
        "ambiguity_correct": amb_correct,
        "multi_domain_full_accuracy": md_full_acc,
        "multi_domain_domain_recall": md_domain_recall,
        "multi_domain_total": len(md_cases),
        "multi_domain_full_hits": md_fully_detected,
        "out_of_domain_abstention_accuracy": ood_acc,
        "out_of_domain_total": len(ood_cases),
        "false_routing_rate": false_routing_rate,
        "intent_accuracy_note": "Intent labels are not explicitly tagged in section A of evaluation dataset; domain accuracy measured directly.",
    }

    # Print summary report
    print("\n" + "=" * 70)
    print(f"OMNIDESK-AI ROUTER EVALUATION REPORT")
    print(f"Classifier: {router.classifier.name}")
    print("=" * 70)

    print(f"\n1. SINGLE-DOMAIN QUERIES (Target >= 85%):")
    print(f"   Accuracy: {single_acc * 100:.1f}% ({single_correct}/{len(single_cases)})")
    for d, st in per_domain_stats.items():
        pct = (st['correct'] / st['total']) * 100 if st['total'] else 0
        print(f"     - {d:<12}: {pct:5.1f}% ({st['correct']}/{st['total']})")

    print(f"\n2. AMBIGUOUS QUERIES CLARIFICATION (Target >= 80%):")
    print(f"   Clarification Rate: {amb_acc * 100:.1f}% ({amb_correct}/{len(amb_cases)})")

    print(f"\n3. MULTI-DOMAIN MULTI-INTENT DETECTION:")
    print(f"   Full Suite Accuracy: {md_full_acc * 100:.1f}% ({md_fully_detected}/{len(md_cases)})")
    print(f"   Domain-level Recall: {md_domain_recall * 100:.1f}% ({md_detected_expected_domains}/{md_total_expected_domains})")

    print(f"\n4. OUT-OF-DOMAIN ABSTENTION (Target 100%):")
    print(f"   Abstention Rate:    {ood_acc * 100:.1f}% ({ood_correct}/{len(ood_cases)})")

    print(f"\n5. OVERALL FALSE-ROUTING RATE:")
    print(f"   False-Routing Rate: {false_routing_rate * 100:.1f}% ({total_false_routes}/{total_eval_queries})")

    print(f"\n6. INTENT ACCURACY STATUS:")
    print(f"   {metrics['intent_accuracy_note']}")
    print("=" * 70 + "\n")

    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate OmniDesk-AI Routing Layer")
    parser.add_argument("--verbose", action="store_true", help="Print details for every test query")
    args = parser.parse_args()

    run_evaluation(verbose=args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
