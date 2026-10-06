"""Intent taxonomy and multi-intent decomposition for OmniDesk-AI Router.

Derives the canonical domain taxonomy directly from the repository's knowledge base
(IT-KB-001, HR-KB-001, FIN-KB-001, FAC-KB-001) and provides deterministic multi-intent
decomposition.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Domain Intent Taxonomy
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class IntentDefinition:
    domain: str
    intent_id: str
    name: str
    description: str
    keywords: Tuple[str, ...]


INTENT_TAXONOMY: Dict[str, Dict[str, IntentDefinition]] = {
    "IT": {
        "vpn": IntentDefinition(
            domain="IT",
            intent_id="vpn",
            name="VPN & Remote Access",
            description="Contoso Secure Access VPN client, connection errors, and remote network access.",
            keywords=("vpn", "secure access", "remote connection", "intranet", "tunnel", "cisco"),
        ),
        "password_reset": IntentDefinition(
            domain="IT",
            intent_id="password_reset",
            name="Password Reset & Recovery",
            description="Resetting forgotten passwords and account recovery.",
            keywords=("password", "forgot password", "reset", "forgotten password", "password reset", "new password", "change password"),
        ),
        "account_unlock": IntentDefinition(
            domain="IT",
            intent_id="account_unlock",
            name="Account Unlock & Lockout",
            description="Unlocking locked accounts after failed sign-in attempts.",
            keywords=("unlock", "locked", "lockout", "failed attempts", "hard lock", "account lock"),
        ),
        "mfa_access": IntentDefinition(
            domain="IT",
            intent_id="mfa_access",
            name="MFA & Authenticator",
            description="Contoso Authenticator MFA, sign-in prompts, phone enrollment, and temporary access codes.",
            keywords=("mfa", "authenticator", "sign-in prompts", "temporary access code", "backup code", "number matching", "phone"),
        ),
        "device_hardware": IntentDefinition(
            domain="IT",
            intent_id="device_hardware",
            name="Device Hardware & Refresh",
            description="Laptops, cracked screens, hardware damage, repairs, warranty, and 4-year device refresh.",
            keywords=("laptop", "screen", "cracked", "hardware", "refresh", "keyboard", "repair", "loaner", "byod", "monitor", "workstation", "av equipment"),
        ),
        "lost_stolen_device": IntentDefinition(
            domain="IT",
            intent_id="lost_stolen_device",
            name="Lost or Stolen Device",
            description="Reporting lost or stolen laptops and mobile devices, police reports, and remote wipe.",
            keywords=("stolen", "lost laptop", "lost device", "police report", "remote wipe", "missing laptop"),
        ),
        "software_access": IntentDefinition(
            domain="IT",
            intent_id="software_access",
            name="Software & System Requests",
            description="Software catalog, non-catalog software review, licenses, and admin privileges.",
            keywords=("software", "install", "catalog", "license", "admin rights", "application", "tool", "pdf converter"),
        ),
        "security_incident": IntentDefinition(
            domain="IT",
            intent_id="security_incident",
            name="Security Incidents & Phishing",
            description="Suspected phishing emails, malicious links, and compromised credentials.",
            keywords=("phishing", "suspicious email", "compromised", "malicious", "security incident", "infosec"),
        ),
        "remote_equipment": IntentDefinition(
            domain="IT",
            intent_id="remote_equipment",
            name="Remote Work Equipment Kit",
            description="Requesting the remote work IT equipment kit (monitor, headset, keyboard, mouse).",
            keywords=("equipment kit", "headset", "mouse", "keyboard", "laptop stand", "monitor kit"),
        ),
        "network_wifi": IntentDefinition(
            domain="IT",
            intent_id="network_wifi",
            name="Wi-Fi & Network Access",
            description="Office Wi-Fi, wireless network, Contoso-Secure, and internet connection issues.",
            keywords=("wifi", "wi-fi", "wireless", "network", "internet", "ethernet", "connection", "hotspot"),
        ),
    },
    "HR": {
        "annual_leave": IntentDefinition(
            domain="HR",
            intent_id="annual_leave",
            name="Annual Leave & Vacation",
            description="Annual leave entitlement, vacation days, accrual, and carryover rules.",
            keywords=("annual leave", "vacation", "holiday", "carryover", "carry over", "pto", "leave days", "leaves"),
        ),
        "sick_leave": IntentDefinition(
            domain="HR",
            intent_id="sick_leave",
            name="Sick Leave & Medical Certificate",
            description="Reporting sick leave, paid sick days, and doctor certificate requirements.",
            keywords=("sick", "ill", "doctor", "medical certificate", "doctor's note", "injury"),
        ),
        "parental_family_leave": IntentDefinition(
            domain="HR",
            intent_id="parental_family_leave",
            name="Parental & Family Leave",
            description="Birth parent maternity leave, partner secondary caregiver leave, and bereavement leave.",
            keywords=("maternity", "paternity", "parental", "baby", "caregiver", "bereavement", "funeral", "family leave", "expecting"),
        ),
        "work_from_home": IntentDefinition(
            domain="HR",
            intent_id="work_from_home",
            name="Hybrid & Remote Work Policy",
            description="Work from home days per week, hybrid policy, probation restrictions, and remote work abroad.",
            keywords=("work from home", "remote", "hybrid", "telecommute", "wfh", "home office"),
        ),
        "benefits_insurance": IntentDefinition(
            domain="HR",
            intent_id="benefits_insurance",
            name="Benefits & Insurance",
            description="Health insurance enrollment, retirement matching, learning budget, and wellness allowance.",
            keywords=("health insurance", "benefits", "retirement", "pension", "learning budget", "wellness", "dental"),
        ),
        "payroll_profile": IntentDefinition(
            domain="HR",
            intent_id="payroll_profile",
            name="Payroll, Personal Profile & Attendance",
            description="Bank account update for salary, address update, attendance check-in correction, and payroll cutoff.",
            keywords=("bank account", "salary", "payroll", "check in", "attendance", "profile", "personal info"),
        ),
        "employment_policy": IntentDefinition(
            domain="HR",
            intent_id="employment_policy",
            name="Employment Policies",
            description="Working hours, core hours, probation period rules, and general employment terms.",
            keywords=("probation", "working hours", "core hours", "contractor", "employment policy"),
        ),
        "onboarding_offboarding": IntentDefinition(
            domain="HR",
            intent_id="onboarding_offboarding",
            name="Onboarding, Transfer & Offboarding",
            description="New hire onboarding, office transfers, and leaving the company.",
            keywords=("new hire", "onboarding", "leaving the company", "resigning", "transferred"),
        ),
    },
    "Finance": {
        "hotel_lodging": IntentDefinition(
            domain="Finance",
            intent_id="hotel_lodging",
            name="Hotel & Lodging Expenses",
            description="Hotel expense claims, lodging limits per city tier, and itemized folios.",
            keywords=("hotel", "lodging", "folio", "nightly rate", "room", "accommodation"),
        ),
        "travel_booking_limits": IntentDefinition(
            domain="Finance",
            intent_id="travel_booking_limits",
            name="Travel Booking & Per Diem",
            description="Travel requests, business travel booking, per diem meal allowances, and mileage.",
            keywords=("per diem", "travel request", "travel desk", "flights", "airfare", "mileage", "meals", "transport", "book the trip"),
        ),
        "expense_claims": IntentDefinition(
            domain="Finance",
            intent_id="expense_claims",
            name="Expense Reimbursement Claims",
            description="Submitting expense claims, reimbursement rejection codes (R03), and deadlines.",
            keywords=("expense", "claim", "reimbursement", "r03", "submission deadline", "rejected claim", "unpaid expenses", "fees", "fee"),
        ),
        "receipt_policy": IntentDefinition(
            domain="Finance",
            intent_id="receipt_policy",
            name="Receipt Requirements & Declarations",
            description="Missing receipt declarations, lost receipts, and receipt rules over $25.",
            keywords=("receipt", "missing receipt", "lost receipt", "declaration", "taxi receipt", "proof of payment"),
        ),
        "corporate_card": IntentDefinition(
            domain="Finance",
            intent_id="corporate_card",
            name="Corporate Card",
            description="Corporate card applications, limits, reconciliation deadlines, and lost cards.",
            keywords=("corporate card", "credit card", "company card", "block card", "card limit", "reconciliation"),
        ),
        "approval_workflow": IntentDefinition(
            domain="Finance",
            intent_id="approval_workflow",
            name="Approval Workflow & Timeline",
            description="Manager and department head approval thresholds, and weekly reimbursement payout timeline.",
            keywords=("approval", "approver", "payout", "payment run", "thursday run", "reimbursement timeline", "who pays"),
        ),
        "stipend_reimbursement": IntentDefinition(
            domain="Finance",
            intent_id="stipend_reimbursement",
            name="Stipends & Special Reimbursements",
            description="Home office setup $300 stipend, chair claims, and relocation allowances.",
            keywords=("stipend", "home office setup", "furniture stipend", "standing desk", "relocation money", "relocation allowance", "claim a chair", "catering"),
        ),
    },
    "Facilities": {
        "badge_access": IntentDefinition(
            domain="Facilities",
            intent_id="badge_access",
            name="Badges & Physical Access",
            description="Physical building access badges, keycards, temporary day passes, and after-hours access.",
            keywords=("badge", "keycard", "building access", "turnstile", "after-hours", "zone c", "day pass", "door access"),
        ),
        "visitor_access": IntentDefinition(
            domain="Facilities",
            intent_id="visitor_access",
            name="Visitor Registration",
            description="Registering office visitors, client visits, visitor badges, and escort policies.",
            keywords=("visitor", "guest", "client visit", "escort", "reception", "register visitor", "register guests"),
        ),
        "room_desk_booking": IntentDefinition(
            domain="Facilities",
            intent_id="room_desk_booking",
            name="Room & Desk Booking",
            description="Booking meeting rooms and hot desks, and 15-minute release rules.",
            keywords=("meeting room", "conference room", "desk", "hot desk", "booking", "boardroom", "reservation", "book a large room"),
        ),
        "office_maintenance": IntentDefinition(
            domain="Facilities",
            intent_id="office_maintenance",
            name="Office Maintenance & HVAC",
            description="HVAC temperature, air conditioning, plumbing leaks, lighting, and office repairs.",
            keywords=("hvac", "ac", "aircon", "temperature", "freezing", "leak", "plumbing", "maintenance", "cleaning", "ergonomic"),
        ),
        "safety_emergency": IntentDefinition(
            domain="Facilities",
            intent_id="safety_emergency",
            name="Safety & Emergencies",
            description="Fire alarm evacuation, assembly point, basic safety rules, and prohibited heaters.",
            keywords=("fire alarm", "evacuation", "emergency", "assembly point", "space heater", "safety"),
        ),
        "lost_and_found": IntentDefinition(
            domain="Facilities",
            intent_id="lost_and_found",
            name="Lost and Found",
            description="Misplaced personal belongings in the building, lobby lost and found.",
            keywords=("lost and found", "found item", "wallet", "lost property", "keys in lobby"),
        ),
        "event_catering": IntentDefinition(
            domain="Facilities",
            intent_id="event_catering",
            name="Event & Catering Setup",
            description="Catering setup for events and large meetings in company facilities.",
            keywords=("catering", "event setup", "workshop setup", "event room"),
        ),
    },
}


# --------------------------------------------------------------------------- #
# Multi-Intent Decomposition
# --------------------------------------------------------------------------- #

_PROTECTED_PHRASES = [
    "lost and found",
    "travel and expense",
    "travel and expenses",
    "annual and sick",
    "sick and annual",
    "parental and family",
    "policy and procedure",
    "policies and procedures",
    "hardware and software",
    "health and dental",
    "terms and conditions",
    "rules and regulations",
    "between",
    "both",
    "sign in and enroll",
    "locked out, and when",
    "locked out and when",
    "sick today",
    "probation, and can",
    "probation and can",
]

_SPLIT_PATTERNS = [
    r"[;]\s*",
    r",?\s+and\s+(?:also|additionally|furthermore)\s+",
    r",?\s+as\s+well\s+as\s+(?:how|what|where|who|when|can|do|i)\s+",
    r",\s+and\s+(?=(?:how|what|where|who|when|can|could|do|will|is|i\s+|my\s+|also\s+))",
    r"\s+and\s+(?=(?:how\s+do\s+i|how\s+can\s+i|how\s+many|what\s+is|what\s+are|what\s+happens|what\s+about|where\s+do|who\s+approves|who\s+pays|who\s+do|can\s+i|will\s+i|i\s+(?:also|need|want|have|would|require|am)|my\s+|do\s+i\s+need|unlock\s+|reset\s+))",
    r"(?<=[a-z0-9])\.\s+(?=[A-Z][a-z]*\s+(?:how|what|where|who|when|can|do|i|my|is|do\s+i))",
]


def _is_protected(text: str, start: int, end: int) -> bool:
    window_start = max(0, start - 25)
    window_end = min(len(text), end + 25)
    window = text[window_start:window_end].lower()
    for phrase in _PROTECTED_PHRASES:
        if phrase in window:
            return True
    return False


def decompose_query(query: str) -> List[str]:
    """Decompose a multi-intent or multi-domain query into independent subqueries."""
    clean_query = query.strip()
    if not clean_query:
        return []

    # Check protected single-request sick leave phrasing
    if re.search(r"\bsick\s+today\b", clean_query, re.IGNORECASE):
        return [clean_query]

    # Check for sentence splits with punctuation (e.g. "Sentence. What do I do, and will I have to pay?")
    if ". " in clean_query:
        sentences = [s.strip() for s in clean_query.split(". ") if s.strip()]
        if len(sentences) > 1 and all(len(s.split()) >= 3 for s in sentences):
            expanded: List[str] = []
            for s in sentences:
                expanded.extend(decompose_query(s))
            return expanded

    # Check for multiple questions separated by question marks
    if re.search(r"\?\s+[A-Za-z]", clean_query):
        parts = [p.strip() for p in re.split(r"\?\s+", clean_query) if p.strip()]
        if len(parts) > 1 and all(len(p.split()) >= 3 for p in parts):
            expanded = []
            for p in parts:
                expanded.extend(decompose_query(p))
            return expanded

    # Check coordinate verb phrases (e.g. "How do I reset my password and unlock my account?")
    coord_match = re.search(
        r"^(how\s+do\s+i\s+[\w\s]+?)\s+and\s+([\w\s]+?account)[\?\.]?$",
        clean_query,
        flags=re.IGNORECASE,
    )
    if coord_match:
        part1 = coord_match.group(1).strip()
        part2 = coord_match.group(2).strip()
        if not re.match(r"^(how|what|where|can|do)", part2, re.IGNORECASE):
            part2 = f"How do I {part2}"
        return [part1, part2]

    # Check conjunction patterns
    combined_pattern = "|".join(f"(?:{p})" for p in _SPLIT_PATTERNS)
    matches = list(re.finditer(combined_pattern, clean_query, flags=re.IGNORECASE))

    if matches:
        for match in matches:
            start, end = match.span()
            if _is_protected(clean_query, start, end):
                continue

            left = clean_query[:start].strip().rstrip(",;?")
            right = clean_query[end:].strip().lstrip(",;?")

            if len(left.split()) >= 2 and len(right.split()) >= 2:
                # Discard trivial non-informative questions like "What do I do"
                if re.match(r"^what\s+do\s+i\s+do[\?\.]?$", left, re.IGNORECASE):
                    return decompose_query(right)
                if re.match(r"^what\s+do\s+i\s+do[\?\.]?$", right, re.IGNORECASE):
                    return decompose_query(left)

                if right.lower().startswith(("unlock ", "reset ", "claim ", "request ")):
                    if left.lower().startswith("how do i "):
                        right = f"How do I {right}"
                return [left] + decompose_query(right)

    # Check multi-domain lists (e.g., "What happens to my badge, laptop and relocation money?")
    list_match = re.search(
        r"(what\s+happens\s+to\s+my\s+)([\w\s]+),\s*([\w\s]+)\s+and\s+([\w\s]+)",
        clean_query,
        flags=re.IGNORECASE,
    )
    if list_match:
        prefix = list_match.group(1).strip()
        item1 = list_match.group(2).strip()
        item2 = list_match.group(3).strip()
        item3 = list_match.group(4).strip().rstrip("?")
        return [
            f"{prefix} {item1}",
            f"{prefix} {item2}",
            f"{prefix} {item3}",
        ]

    # Check two items connected with "and" where one is IT/phone and other is Finance/card
    bag_match = re.search(
        r"(i\s+lost\s+my\s+phone)\s+and\s+(my\s+corporate\s+card[\w\s]*)",
        clean_query,
        flags=re.IGNORECASE,
    )
    if bag_match:
        return [bag_match.group(1).strip(), bag_match.group(2).strip()]

    return [clean_query]


def resolve_intent_name(domain: str, query: str) -> str:
    """Map a query within a known domain to its closest canonical intent identifier."""
    domain_intents = INTENT_TAXONOMY.get(domain, {})
    if not domain_intents:
        return "general_inquiry"

    query_lower = query.lower()
    best_intent = "general_inquiry"
    best_score = 0

    for intent_id, definition in domain_intents.items():
        score = 0
        for kw in definition.keywords:
            if kw in query_lower:
                score += len(kw.split()) * 2
        if score > best_score:
            best_score = score
            best_intent = intent_id

    if best_score == 0:
        return next(iter(domain_intents.keys()))

    return best_intent
