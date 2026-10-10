from __future__ import annotations

import math
from typing import Any

from backend.app.policy.demo_data import ALLOWED_DECISIONS, DEMO_EVIDENCE

MAX_AUTO_REFUND_INR = 5000.0
CONFIDENCE_THRESHOLD = 0.85
CURRENCY = "INR"


def parse_amount(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = float(text.replace(",", "").replace("₹", "").replace("Rs", ""))
        except ValueError:
            return None
    elif isinstance(value, (int, float)):
        parsed = float(value)
    else:
        return None
    if math.isnan(parsed) or math.isinf(parsed) or parsed < 0:
        return None
    return parsed


def get_verified_evidence(order_id: str | None, transaction_id: str | None) -> dict[str, Any] | None:
    if order_id:
        match = DEMO_EVIDENCE.get(order_id)
        if match:
            return match
    if transaction_id:
        for evidence in DEMO_EVIDENCE.values():
            if evidence.get("transaction_id") == transaction_id:
                return evidence
    return None


def evaluate_policy(
    *,
    request_text: str,
    order_id: str | None,
    transaction_id: str | None,
    amount: Any,
    currency: str | None,
    ai_decision: str | None,
    confidence: Any,
    provider: str,
    model_id: str | None = None,
) -> dict[str, Any]:
    parsed_amount = parse_amount(amount)
    if parsed_amount is None and amount not in (None, ""):
        return {
            "status": "ERROR",
            "decision": "REJECTED",
            "action": "REJECTED",
            "reason": "Invalid or missing amount value.",
            "reasons": ["Invalid or missing amount value."],
            "next_action": "Provide a valid non-negative numeric amount in INR.",
            "missing_evidence": ["valid amount"],
            "provider": provider,
            "model_id": model_id,
            "mock_refund_id": None,
            "approval_task_id": None,
            "audit_reference": None,
            "evidence": None,
        }

    evidence = get_verified_evidence(order_id, transaction_id)
    normalized_currency = (currency or CURRENCY).upper()
    confidence_value = float(confidence) if confidence is not None else 0.0
    ai_decision_value = (ai_decision or "").upper()

    if ai_decision_value not in ALLOWED_DECISIONS:
        ai_decision_value = "HUMAN_APPROVAL"

    reasons: list[str] = []
    missing_evidence: list[str] = []

    if normalized_currency != CURRENCY:
        reasons.append("Currency is not INR.")
        missing_evidence.append("INR currency")

    if parsed_amount is not None and parsed_amount > MAX_AUTO_REFUND_INR:
        reasons.append("Requested amount exceeds the ₹5,000 automatic refund ceiling.")

    if confidence_value < CONFIDENCE_THRESHOLD:
        reasons.append("AI confidence is below the required 0.85 threshold.")

    if not evidence:
        missing_evidence.append("verified duplicate-payment evidence")
        reasons.append("No verified duplicate-payment evidence exists for the supplied order or transaction.")

    if evidence and evidence.get("status") != "VERIFIED_DUPLICATE":
        reasons.append("The evidence lookup did not confirm a duplicate payment.")

    if not order_id and not transaction_id:
        missing_evidence.append("order or transaction reference")
        reasons.append("Missing order or transaction evidence prevents safe verification.")

    if parsed_amount is not None and parsed_amount > MAX_AUTO_REFUND_INR:
        final_decision = "HUMAN_APPROVAL"
        status = "HUMAN_REVIEW"
        action = "APPROVAL_REQUIRED"
        next_action = "Escalate for manual approval because the amount exceeds the automatic threshold."
    elif confidence_value < CONFIDENCE_THRESHOLD:
        final_decision = "HUMAN_APPROVAL"
        status = "HUMAN_REVIEW"
        action = "APPROVAL_REQUIRED"
        next_action = "Request human review because confidence is below the threshold."
    elif not evidence or normalized_currency != CURRENCY:
        final_decision = "INFORMATION_NEEDED"
        status = "INFORMATION_NEEDED"
        action = "NEEDS_MORE_EVIDENCE"
        next_action = "Collect verified order and transaction evidence before taking any refund action."
    elif ai_decision_value == "AUTO_REFUND" and evidence and confidence_value >= CONFIDENCE_THRESHOLD and parsed_amount is not None and parsed_amount <= MAX_AUTO_REFUND_INR and normalized_currency == CURRENCY:
        final_decision = "AUTO_REFUND"
        status = "AUTO_RESOLVED"
        action = "MOCK_REFUND_CREATED"
        next_action = "Create a simulated refund record and audit event after policy checks pass."
    elif ai_decision_value in {"HUMAN_APPROVAL", "NO_ACTION"}:
        final_decision = "HUMAN_APPROVAL"
        status = "HUMAN_REVIEW"
        action = "APPROVAL_REQUIRED"
        next_action = "Escalate to a human reviewer for a manual decision."
    else:
        final_decision = "INFORMATION_NEEDED"
        status = "INFORMATION_NEEDED"
        action = "NEEDS_MORE_EVIDENCE"
        next_action = "Request more information or a verified evidence record."

    if not request_text.strip():
        final_decision = "REJECTED"
        status = "ERROR"
        action = "INVALID_REQUEST"
        next_action = "Submit a clear customer request with order or transaction details."

    if not reasons:
        reasons = ["Policy checks passed for the provided evidence and threshold."]
    if not missing_evidence:
        missing_evidence = ["none"]

    return {
        "status": status,
        "decision": final_decision,
        "action": action,
        "reason": reasons[0],
        "reasons": reasons,
        "next_action": next_action,
        "missing_evidence": missing_evidence,
        "provider": provider,
        "model_id": model_id,
        "mock_refund_id": None,
        "approval_task_id": None,
        "audit_reference": None,
        "evidence": evidence,
    }
