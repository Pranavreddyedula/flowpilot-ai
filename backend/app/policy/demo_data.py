from __future__ import annotations

DEMO_EVIDENCE = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "transaction_id": "TXN-1001-1",
        "amount": 1499.0,
        "currency": "INR",
        "status": "VERIFIED_DUPLICATE",
        "duplicate_count": 2,
        "notes": "Demo dataset: duplicate payment explicitly verified for order ORD-1001.",
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "transaction_id": "TXN-1002-1",
        "amount": 12500.0,
        "currency": "INR",
        "status": "VERIFIED_DUPLICATE",
        "duplicate_count": 2,
        "notes": "Demo dataset: duplicate payment exists but exceeds safe refund ceiling.",
    },
    "ORD-1003": {
        "order_id": "ORD-1003",
        "transaction_id": "TXN-1003-1",
        "amount": 750.0,
        "currency": "INR",
        "status": "VERIFIED_SINGLE_PAYMENT",
        "duplicate_count": 1,
        "notes": "Demo dataset: single payment, no duplicate evidence.",
    },
}

ALLOWED_DECISIONS = {
    "AUTO_REFUND",
    "HUMAN_APPROVAL",
    "INFORMATION_NEEDED",
    "REJECTED",
    "NO_ACTION",
    "ERROR",
}
