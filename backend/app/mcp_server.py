from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from sqlalchemy.orm import Session

if __package__ in {None, ""}:
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from backend.app.config import settings
from backend.app.services.request_service import RequestService
from backend.app.storage.db import SessionLocal, init_db

init_db()

mcp = FastMCP(
    "FlowPilotMCP",
    host=settings.MCP_HOST,
    port=settings.MCP_PORT,
)


def resolve_service() -> RequestService:
    db = SessionLocal()
    try:
        return RequestService(db)
    finally:
        db.close()


@mcp.tool()
def analyze_customer_request(
    request_text: str,
    customer_id: str | None = None,
    order_id: str | None = None,
    transaction_id: str | None = None,
    amount: float | None = None,
    currency: str | None = "INR",
) -> dict[str, Any]:
    """Analyze a customer request, extract intent and business context, and return a structured AI proposal."""
    service = resolve_service()
    try:
        return asyncio.run(
            service.provider.analyze(
                request_text=request_text,
                customer_id=customer_id,
                order_id=order_id,
                transaction_id=transaction_id,
                amount=amount,
                currency=currency,
            )
        )
    except Exception as exc:  # pragma: no cover - defensive server failure path
        return {"error": str(exc), "provider": service.provider.provider_name, "decision": "ERROR"}


@mcp.tool()
async def process_customer_request(
    request_text: str,
    customer_id: str | None = None,
    order_id: str | None = None,
    transaction_id: str | None = None,
    amount: float | None = None,
    currency: str | None = "INR",
) -> dict[str, Any]:
    """Process a request through the deterministic policy engine and produce a safe mock decision or approval task."""
    db = SessionLocal()
    service = RequestService(db)
    try:
        return await service.analyze_request(
            payload={
                "request": request_text,
                "customer_id": customer_id or "CUST-DEMO",
                "order_id": order_id,
                "transaction_id": transaction_id,
                "amount": amount,
                "currency": currency or "INR",
                "source": "mcp",
            }
        )
    finally:
        db.close()


@mcp.tool()
def get_request_status(request_id: str) -> dict[str, Any]:
    """Look up a request and its latest decision status."""
    db = SessionLocal()
    service = RequestService(db)
    try:
        result = service.get_request(request_id)
        return result or {"request_id": request_id, "status": "NOT_FOUND"}
    finally:
        db.close()


@mcp.tool()
def get_audit_summary(status: str | None = None, result: str | None = None) -> dict[str, Any]:
    """Return summary counts and filtered audit records without revealing secrets."""
    db = SessionLocal()
    service = RequestService(db)
    try:
        return service.get_audit_summary(status=status, result=result)
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
