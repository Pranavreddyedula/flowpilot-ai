from __future__ import annotations

from typing import Any

from backend.app.providers.provider_interface import BaseAIProvider, ProviderError


class OfflineProvider(BaseAIProvider):
    provider_name = "offline"

    async def analyze(
        self,
        *,
        request_text: str,
        customer_id: str | None = None,
        order_id: str | None = None,
        transaction_id: str | None = None,
        amount: Any = None,
        currency: str | None = None,
    ) -> dict[str, Any]:
        text = (request_text or "").lower()
        decision = "HUMAN_APPROVAL"
        confidence = 0.9
        intent = "unknown"
        if "charged twice" in text or "duplicate payment" in text or "refund" in text:
            intent = "duplicate_payment"
            if order_id == "ORD-1001" or transaction_id == "TXN-1001-1":
                decision = "AUTO_REFUND"
                confidence = 0.96
            elif order_id and order_id.upper() == "ORD-1002":
                decision = "HUMAN_APPROVAL"
                confidence = 0.91
            else:
                decision = "INFORMATION_NEEDED"
                confidence = 0.82
        if amount is not None and float(amount) > 5000:
            decision = "HUMAN_APPROVAL"
            confidence = 0.92
        if not order_id and not transaction_id:
            decision = "INFORMATION_NEEDED"
            confidence = 0.78
        return {
            "intent": intent,
            "urgency": "high" if "urgent" in text or "immediately" in text else "normal",
            "decision": decision,
            "confidence": confidence,
            "reasons": ["Offline provider used for deterministic demo logic."],
            "entities": {
                "customer_id": customer_id,
                "order_id": order_id,
                "transaction_id": transaction_id,
                "amount": amount,
                "currency": currency or "INR",
            },
            "missing_evidence": [] if order_id or transaction_id else ["order or transaction reference"],
            "next_action": "Proceed only when policy checks pass.",
            "provider": self.provider_name,
            "model_id": "offline-demo-model",
        }
