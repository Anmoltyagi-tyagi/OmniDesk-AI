"""Interactive CLI for OmniDesk-AI Router.

Allows quick manual testing of single queries or interactive query loops:
    python -m router.cli "my vpn isnt working and i want my travel reimbursement"
    python -m router.cli  # interactive mode
"""
from __future__ import annotations

import json
import sys
from .router import route_query


def format_result(res) -> str:
    lines = []
    lines.append("-" * 60)
    lines.append(f"Query: \"{res.original_query}\"")
    lines.append(f"Needs Clarification: {res.needs_clarification}")
    if res.needs_clarification:
        lines.append(f"Clarification Question: {res.clarification_question}")
    if res.is_out_of_domain:
        lines.append(f"Out of Domain: True ({res.explanation})")
    if res.intents:
        lines.append(f"Detected Routes ({len(res.intents)}):")
        for i, route in enumerate(res.intents, 1):
            lines.append(
                f"  [{i}] Domain: {route.domain:<11} "
                f"Intent: {route.intent:<22} "
                f"Score: {route.confidence:.2f} "
                f"| Subquery: \"{route.query}\""
            )
    lines.append("-" * 60)
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = route_query(query)
        print(format_result(result))
        return

    print("=" * 60)
    print("OmniDesk-AI Interactive Router CLI")
    print("Type any employee query to test routing (or 'exit' to quit).")
    print("=" * 60)

    while True:
        try:
            query = input("\nEnter query > ").strip()
            if not query or query.lower() in ("exit", "quit", "q"):
                print("Exiting.")
                break
            result = route_query(query)
            print(format_result(result))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as ex:
            print(f"Error: {ex}")


if __name__ == "__main__":
    main()
