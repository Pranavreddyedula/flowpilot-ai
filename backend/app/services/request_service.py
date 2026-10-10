from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.models import ApprovalTask, AuditEvent, DecisionResult, MockRefundRecord, RequestRecord
from backend.app.policy.engine import evaluate_policy
from backend.app.providers.bedrock_provider import BedrockProvider
from backend.app.providers.offline_provider import OfflineProvider
from backend.app.providers.provider_interface import BaseAIProvider, ProviderError


class RequestService:
    def __init__(self, session: Session):
        self.session = session
        self.provider = self._build_provider()

    def _build_provider(self) -> BaseAIProvider:
        provider_name = (settings.PROVIDER or "offline").lower()
        if provider_name == "bedrock":
            return BedrockProvider(model_id=settings.BEDROCK_MODEL_ID, region_name=settings.AWS_REGION)
        return OfflineProvider()

    def _build_idempotency_key(self, *, customer_id: str, request_text: str, order_id: str | None, transaction_id: str | None) -> str:
        raw = "|".join(
            [
                (customer_id or "").strip().lower(),
                (request_text or "").strip().lower(),
                (order_id or "").strip().lower(),
                (transaction_id or "").strip().lower(),
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _get_request_by_idempotency(self, key: str) -> RequestRecord | None:
        return self.session.query(RequestRecord).filter(RequestRecord.idempotency_key == key).first()

    def _create_audit_event(self, *, request_id: str | None, event_type: str, details: dict[str, Any]) -> AuditEvent:
        event = AuditEvent(
            id=str(uuid.uuid4()),
            request_id=request_id,
            event_type=event_type,
            details=json.dumps(details, default=str),
        )
        self.session.add(event)
        return event

    def _insert_refund(self, *, request_id: str, refund_amount: float, currency: str, idempotency_key: str) -> MockRefundRecord:
        refund = MockRefundRecord(
            id=str(uuid.uuid4()),
            request_id=request_id,
            refund_amount=float(refund_amount),
            currency=currency,
            status="CREATED",
            idempotency_key=idempotency_key,
        )
        self.session.add(refund)
        return refund

    def _serialize_request(self, record: RequestRecord) -> dict[str, Any]:
        decision_result = self.session.query(DecisionResult).filter(DecisionResult.request_id == record.id).order_by(DecisionResult.created_at.desc()).first()
        approval_task = self.session.query(ApprovalTask).filter(ApprovalTask.request_id == record.id, ApprovalTask.status == "OPEN").first()
        refund_record = self.session.query(MockRefundRecord).filter(MockRefundRecord.request_id == record.id).first()
        return {
            "request_id": record.id,
            "customer_id": record.customer_id,
            "order_id": record.order_id,
            "transaction_id": record.transaction_id,
            "request": record.request_text,
            "amount": record.amount,
            "currency": record.currency,
            "status": record.status,
            "decision": record.decision,
            "confidence": record.confidence,
            "provider": record.provider,
            "source": record.source,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "approval_task_id": approval_task.id if approval_task else None,
            "mock_refund_id": refund_record.id if refund_record else None,
            "decision_result": {
                "provider": decision_result.provider if decision_result else record.provider,
                "final_decision": decision_result.final_decision if decision_result else record.decision,
                "proposed_decision": decision_result.proposed_decision if decision_result else record.decision,
                "confidence": decision_result.confidence if decision_result else record.confidence,
                "status": decision_result.status if decision_result else record.status,
                "reason": decision_result.reasons if decision_result else "",
                "audit_reference": decision_result.audit_reference if decision_result else None,
            },
        }

    async def analyze_request(self, *, payload: dict[str, Any]) -> dict[str, Any]:
        customer_id = (payload.get("customer_id") or "CUST-DEMO").strip()
        request_text = (payload.get("request") or "").strip()
        order_id = (payload.get("order_id") or "").strip() or None
        transaction_id = (payload.get("transaction_id") or "").strip() or None
        amount = payload.get("amount")
        currency = (payload.get("currency") or "INR").upper()

        if not request_text:
            raise ValueError("Request text is required.")

        idempotency_key = self._build_idempotency_key(
            customer_id=customer_id,
            request_text=request_text,
            order_id=order_id,
            transaction_id=transaction_id,
        )
        existing = self._get_request_by_idempotency(idempotency_key)
        if existing:
            return {"idempotent": True, **self._serialize_request(existing)}

        request_record = RequestRecord(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            order_id=order_id,
            transaction_id=transaction_id,
            request_text=request_text,
            amount=float(amount) if amount is not None else None,
            currency=currency,
            source=payload.get("source", "api"),
            provider=self.provider.provider_name,
            status="PENDING",
            decision="INFORMATION_NEEDED",
            idempotency_key=idempotency_key,
        )
        self.session.add(request_record)
        self.session.flush()
        self._create_audit_event(request_id=request_record.id, event_type="request_received", details={"customer_id": customer_id, "order_id": order_id, "source": request_record.source})

        try:
            ai_result = await self.provider.analyze(
                request_text=request_text,
                customer_id=customer_id,
                order_id=order_id,
                transaction_id=transaction_id,
                amount=amount,
                currency=currency,
            )
        except ProviderError as exc:
            request_record.status = "ERROR"
            request_record.decision = "ERROR"
            request_record.provider = self.provider.provider_name
            self._create_audit_event(request_id=request_record.id, event_type="provider_error", details={"error": str(exc), "provider": self.provider.provider_name})
            self.session.commit()
            return {
                "request_id": request_record.id,
                "status": "ERROR",
                "decision": "ERROR",
                "message": "The AI provider is unavailable. The request has been queued for human review.",
                "provider": self.provider.provider_name,
                "idempotent": False,
            }

        self._create_audit_event(request_id=request_record.id, event_type="ai_proposal", details={"proposal": ai_result})

        policy_result = evaluate_policy(
            request_text=request_text,
            order_id=order_id,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            ai_decision=ai_result.get("decision"),
            confidence=ai_result.get("confidence"),
            provider=self.provider.provider_name,
            model_id=ai_result.get("model_id"),
        )
        self._create_audit_event(request_id=request_record.id, event_type="policy_guardrail", details={"policy_result": policy_result})

        final_decision = policy_result["decision"]
        request_record.status = policy_result["status"]
        request_record.decision = final_decision
        request_record.confidence = float(ai_result.get("confidence") or 0.0)
        request_record.provider = self.provider.provider_name

        decision_result = DecisionResult(
            id=str(uuid.uuid4()),
            request_id=request_record.id,
            provider=self.provider.provider_name,
            model_id=ai_result.get("model_id"),
            proposed_decision=str(ai_result.get("decision") or "HUMAN_APPROVAL").upper(),
            final_decision=final_decision,
            confidence=float(ai_result.get("confidence") or 0.0),
            status=policy_result["status"],
            reasons=json.dumps(policy_result.get("reasons", []), default=str),
            missing_evidence=json.dumps(policy_result.get("missing_evidence", []), default=str),
            next_action=policy_result.get("next_action"),
            audit_reference=str(uuid.uuid4()),
        )
        self.session.add(decision_result)
        request_record.status = policy_result["status"]
        request_record.decision = final_decision
        self.session.flush()

        if policy_result["status"] == "AUTO_RESOLVED":
            refund_key = self._build_idempotency_key(
                customer_id=customer_id,
                request_text=request_text + "|refund",
                order_id=order_id,
                transaction_id=transaction_id,
            )
            refund = self.session.query(MockRefundRecord).filter(MockRefundRecord.idempotency_key == refund_key).first()
            if refund is None:
                refund = self._insert_refund(
                    request_id=request_record.id,
                    refund_amount=float(amount or 0),
                    currency=currency,
                    idempotency_key=refund_key,
                )
                self._create_audit_event(request_id=request_record.id, event_type="mock_refund_created", details={"refund_id": refund.id, "amount": refund.refund_amount, "currency": refund.currency})
            else:
                self._create_audit_event(request_id=request_record.id, event_type="mock_refund_reused", details={"refund_id": refund.id, "amount": refund.refund_amount})
            policy_result["mock_refund_id"] = refund.id
            decision_result.audit_reference = refund.id
            request_record.status = "AUTO_RESOLVED"
        elif policy_result["status"] in {"HUMAN_REVIEW", "INFORMATION_NEEDED"}:
            task = ApprovalTask(
                id=str(uuid.uuid4()),
                request_id=request_record.id,
                status="OPEN",
                decision=final_decision,
                reviewer=None,
            )
            self.session.add(task)
            policy_result["approval_task_id"] = task.id
            self._create_audit_event(request_id=request_record.id, event_type="approval_needed", details={"approval_task_id": task.id, "decision": final_decision})

        self._create_audit_event(request_id=request_record.id, event_type="request_completed", details={"final_status": request_record.status, "decision": final_decision})
        self.session.commit()

        response = {
            "request_id": request_record.id,
            "status": request_record.status,
            "decision": final_decision,
            "action": policy_result.get("action"),
            "reason": policy_result.get("reason"),
            "reasons": policy_result.get("reasons"),
            "next_action": policy_result.get("next_action"),
            "provider": self.provider.provider_name,
            "model_id": ai_result.get("model_id"),
            "confidence": float(ai_result.get("confidence") or 0.0),
            "mock_refund_id": policy_result.get("mock_refund_id"),
            "approval_task_id": policy_result.get("approval_task_id"),
            "audit_reference": decision_result.audit_reference,
            "idempotent": False,
        }
        return response

    def get_request(self, request_id: str) -> dict[str, Any] | None:
        record = self.session.query(RequestRecord).filter(RequestRecord.id == request_id).first()
        if not record:
            return None
        return self._serialize_request(record)

    def get_approval_queue(self) -> list[dict[str, Any]]:
        rows = self.session.query(ApprovalTask).filter(ApprovalTask.status == "OPEN").all()
        result = []
        for task in rows:
            request = self.session.query(RequestRecord).filter(RequestRecord.id == task.request_id).first()
            if request is not None:
                result.append({
                    "approval_task_id": task.id,
                    "request_id": request.id,
                    "customer_id": request.customer_id,
                    "order_id": request.order_id,
                    "status": task.status,
                    "decision": task.decision,
                })
        return result

    def resolve_approval(self, *, task_id: str, action: str, reviewer: str, notes: str | None = None) -> dict[str, Any]:
        task = self.session.query(ApprovalTask).filter(ApprovalTask.id == task_id).first()
        if not task:
            raise ValueError("Approval task not found.")
        if task.status != "OPEN":
            raise ValueError("Approval task is already closed.")

        action_value = action.upper()
        if action_value not in {"APPROVE", "REJECT"}:
            raise ValueError("Action must be APPROVE or REJECT.")

        task.status = "RESOLVED"
        task.reviewer = reviewer or "demo-reviewer"
        task.notes = notes or ""
        task.resolved_at = func.now()

        request = self.session.query(RequestRecord).filter(RequestRecord.id == task.request_id).first()
        if request is None:
            raise ValueError("Linked request not found.")

        decision = "APPROVED" if action_value == "APPROVE" else "REJECTED"
        request.status = "APPROVED" if action_value == "APPROVE" else "REJECTED"
        request.decision = request.decision if action_value == "APPROVE" else "REJECTED"
        self._create_audit_event(request_id=request.id, event_type="approval_decision", details={"task_id": task_id, "action": decision, "reviewer": task.reviewer, "notes": notes})
        self.session.commit()
        return {"approval_task_id": task.id, "request_id": request.id, "status": request.status, "decision": request.decision, "action": decision}

    def get_audit_summary(self, *, status: str | None = None, result: str | None = None, date_from: str | None = None, date_to: str | None = None) -> dict[str, Any]:
        query = self.session.query(RequestRecord)
        if status:
            query = query.filter(RequestRecord.status == status)
        if result:
            query = query.filter(RequestRecord.decision == result)
        if date_from:
            query = query.filter(RequestRecord.created_at >= date_from)
        if date_to:
            query = query.filter(RequestRecord.created_at <= date_to)
        records = query.all()
        grouped = {"AUTO_RESOLVED": 0, "HUMAN_REVIEW": 0, "INFORMATION_NEEDED": 0, "REJECTED": 0, "ERROR": 0}
        for row in records:
            key = row.status
            grouped.setdefault(key, 0)
            grouped[key] += 1
        return {"count": len(records), "status_counts": grouped, "requests": [self._serialize_request(row) for row in records]}

    def provider_status(self) -> dict[str, Any]:
        return {
            "provider": self.provider.provider_name,
            "name": settings.APP_NAME,
            "configured": True,
            "offline_mode": self.provider.provider_name == "offline",
        }
