from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_request_flow() -> None:
    payload = {
        "request": "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",
        "customer_id": "CUST-101",
        "order_id": "ORD-1001",
        "transaction_id": "TXN-1001-1",
        "amount": 1499,
        "currency": "INR",
    }
    response = client.post("/api/requests", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"AUTO_RESOLVED", "HUMAN_REVIEW", "INFORMATION_NEEDED"}


def test_approval_queue_and_status() -> None:
    payload = {
        "request": "I was charged twice for order ORD-1002. The duplicate amount is Rs 12500. Please refund it.",
        "customer_id": "CUST-102",
        "order_id": "ORD-1002",
        "transaction_id": "TXN-1002-1",
        "amount": 12500,
        "currency": "INR",
    }
    response = client.post("/api/requests", json=payload)
    data = response.json()
    task_id = data.get("approval_task_id")
    assert task_id is not None
    res = client.get("/api/approvals")
    ids = [item["approval_task_id"] for item in res.json()]
    assert task_id in ids
    approval_response = client.post(f"/api/approvals/{task_id}/resolve", json={"action": "APPROVE", "reviewer": "qa"})
    assert approval_response.status_code == 200
    assert approval_response.json()["status"] in {"APPROVED", "REJECTED"}
