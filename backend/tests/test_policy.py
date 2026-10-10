from __future__ import annotations

from backend.app.policy.engine import evaluate_policy


def test_amount_ceiling_blocks_auto_refund() -> None:
    result = evaluate_policy(
        request_text="I was charged twice for ORD-1002. Please refund Rs 12500.",
        order_id="ORD-1002",
        transaction_id="TXN-1002-1",
        amount=12500,
        currency="INR",
        ai_decision="AUTO_REFUND",
        confidence=0.96,
        provider="offline",
    )
    assert result["decision"] == "HUMAN_APPROVAL"
    assert result["status"] == "HUMAN_REVIEW"


def test_confidence_threshold_requires_high_confidence() -> None:
    result = evaluate_policy(
        request_text="I was charged twice for ORD-1001.",
        order_id="ORD-1001",
        transaction_id="TXN-1001-1",
        amount=1499,
        currency="INR",
        ai_decision="AUTO_REFUND",
        confidence=0.84,
        provider="offline",
    )
    assert result["decision"] == "HUMAN_APPROVAL"


def test_verified_duplicate_evidence_allows_auto_refund() -> None:
    result = evaluate_policy(
        request_text="I was charged twice for ORD-1001. Please refund the duplicate payment.",
        order_id="ORD-1001",
        transaction_id="TXN-1001-1",
        amount=1499,
        currency="INR",
        ai_decision="AUTO_REFUND",
        confidence=0.95,
        provider="offline",
    )
    assert result["status"] == "AUTO_RESOLVED"
    assert result["decision"] == "AUTO_REFUND"


def test_missing_evidence_requires_information_needed() -> None:
    result = evaluate_policy(
        request_text="I think I was charged twice.",
        order_id=None,
        transaction_id=None,
        amount=299,
        currency="INR",
        ai_decision="AUTO_REFUND",
        confidence=0.9,
        provider="offline",
    )
    assert result["status"] == "INFORMATION_NEEDED"


def test_invalid_currency_is_rejected() -> None:
    result = evaluate_policy(
        request_text="Please refund duplicate payment.",
        order_id="ORD-1001",
        transaction_id="TXN-1001-1",
        amount=1499,
        currency="USD",
        ai_decision="AUTO_REFUND",
        confidence=0.95,
        provider="offline",
    )
    assert result["status"] == "INFORMATION_NEEDED"


def test_invalid_amount_is_rejected() -> None:
    result = evaluate_policy(
        request_text="Please refund duplicate payment.",
        order_id="ORD-1001",
        transaction_id="TXN-1001-1",
        amount="not-a-number",
        currency="INR",
        ai_decision="AUTO_REFUND",
        confidence=0.95,
        provider="offline",
    )
    assert result["status"] == "ERROR"
    assert result["decision"] == "REJECTED"
