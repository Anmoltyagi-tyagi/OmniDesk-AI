"""Tests for multi-intent decomposition and conjunction handling in router/intent.py."""
import pytest

from router.intent import decompose_query, resolve_intent_name


def test_single_intent_remains_intact():
    query = "What is the leave policy?"
    subqueries = decompose_query(query)
    assert len(subqueries) == 1
    assert subqueries[0] == "What is the leave policy?"


def test_protected_conjunction_phrases_not_split():
    # 'travel and expense' is a single conceptual topic
    q1 = "What is the travel and expense policy?"
    assert len(decompose_query(q1)) == 1

    # 'lost and found' is a single facility function
    q2 = "Where is the lost and found?"
    assert len(decompose_query(q2)) == 1

    # 'annual and sick leave'
    q3 = "Can I combine annual and sick leave?"
    assert len(decompose_query(q3)) == 1

    # 'hardware and software'
    q4 = "Who approves hardware and software requests?"
    assert len(decompose_query(q4)) == 1


def test_cross_domain_multi_intent_decomposition():
    # IT + Finance
    q1 = "My VPN isn't working, and I also need to know the travel reimbursement limit."
    subs1 = decompose_query(q1)
    assert len(subs1) >= 2
    assert any("VPN" in s for s in subs1)
    assert any("reimbursement" in s for s in subs1)

    # IT + HR
    q2 = "My laptop is broken and how many casual leaves do I have?"
    subs2 = decompose_query(q2)
    assert len(subs2) >= 2
    assert any("laptop" in s for s in subs2)
    assert any("leaves" in s for s in subs2)


def test_same_domain_multi_intent_decomposition():
    # IT: password reset + IT: account unlock
    q = "How do I reset my password and unlock my account?"
    subs = decompose_query(q)
    assert len(subs) == 2
    assert "password" in subs[0].lower()
    assert "account" in subs[1].lower()


def test_multi_sentence_question_decomposition():
    q = "What is the leave policy? How do I reset my password?"
    subs = decompose_query(q)
    assert len(subs) == 2
    assert "leave" in subs[0].lower()
    assert "password" in subs[1].lower()


def test_multi_entity_list_decomposition():
    q = "What happens to my badge, laptop and relocation money?"
    subs = decompose_query(q)
    assert len(subs) == 3
    assert any("badge" in s for s in subs)
    assert any("laptop" in s for s in subs)
    assert any("relocation" in s for s in subs)


def test_resolve_intent_name():
    assert resolve_intent_name("IT", "My VPN authentication failed") == "vpn"
    assert resolve_intent_name("IT", "Reset forgotten password") == "password_reset"
    assert resolve_intent_name("HR", "Annual vacation carryover") == "annual_leave"
    assert resolve_intent_name("Finance", "Hotel folio expense claim") == "hotel_lodging"
    assert resolve_intent_name("Facilities", "Lost keycard or badge") == "badge_access"
