from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.storage.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RequestRecord(Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    order_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    transaction_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    request_text: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(16), default="INR")
    source: Mapped[str] = mapped_column(String(32), default="api")
    provider: Mapped[str] = mapped_column(String(32), default="offline")
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    decision: Mapped[str] = mapped_column(String(32), default="INFORMATION_NEEDED")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class DecisionResult(Base):
    __tablename__ = "decision_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    provider: Mapped[str] = mapped_column(String(32), default="offline")
    model_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    proposed_decision: Mapped[str] = mapped_column(String(32), default="HUMAN_APPROVAL")
    final_decision: Mapped[str] = mapped_column(String(32), default="HUMAN_APPROVAL")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    reasons: Mapped[str] = mapped_column(Text, default="[]")
    missing_evidence: Mapped[str] = mapped_column(Text, default="[]")
    next_action: Mapped[str | None] = mapped_column(String(128), nullable=True)
    audit_reference: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class ApprovalTask(Base):
    __tablename__ = "approval_tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), default="OPEN")
    decision: Mapped[str] = mapped_column(String(32), default="HUMAN_APPROVAL")
    reviewer: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MockRefundRecord(Base):
    __tablename__ = "mock_refunds"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    refund_amount: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(16), default="INR")
    status: Mapped[str] = mapped_column(String(32), default="CREATED")
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    details: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class DemoEvidenceRecord(Base):
    __tablename__ = "demo_evidence"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), index=True)
    transaction_id: Mapped[str] = mapped_column(String(128), index=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(16), default="INR")
    status: Mapped[str] = mapped_column(String(32), default="VERIFIED")
    duplicate_count: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
