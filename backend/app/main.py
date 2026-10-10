from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.services.request_service import RequestService
from backend.app.storage.db import SessionLocal, init_db


class RequestSubmission(BaseModel):
    request: str = Field(..., min_length=5)
    customer_id: str = Field(default="CUST-DEMO")
    order_id: str | None = None
    transaction_id: str | None = None
    amount: float | None = None
    currency: str = "INR"
    source: str = "api"


class ApprovalAction(BaseModel):
    action: str = Field(...)
    reviewer: str = Field(default="demo-reviewer")
    notes: str | None = None


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()
app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "service": settings.APP_NAME, "provider": settings.PROVIDER}


@app.get("/ready")
async def ready() -> dict[str, Any]:
    return {"status": "ready", "database": "sqlite", "provider": settings.PROVIDER}


@app.get("/api/provider-status")
async def provider_status(db: Session = Depends(get_db)) -> dict[str, Any]:
    service = RequestService(db)
    return service.provider_status()


@app.post("/api/requests")
async def submit_request(payload: RequestSubmission, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = RequestService(db)
    try:
        result = await service.analyze_request(payload=payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - safe failure path
        raise HTTPException(status_code=500, detail="Request processing failed.") from exc
    return result


@app.get("/api/requests/{request_id}")
async def get_request(request_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = RequestService(db)
    request = service.get_request(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found.")
    return request


@app.get("/api/approvals")
async def approvals(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = RequestService(db)
    return service.get_approval_queue()


@app.post("/api/approvals/{task_id}/resolve")
async def resolve_approval(task_id: str, payload: ApprovalAction, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = RequestService(db)
    try:
        return service.resolve_approval(task_id=task_id, action=payload.action, reviewer=payload.reviewer, notes=payload.notes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/audit")
async def audit_summary(
    status: str | None = Query(default=None),
    result: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    service = RequestService(db)
    return service.get_audit_summary(status=status, result=result, date_from=date_from, date_to=date_to)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "FlowPilot AI API is running."}
