from __future__ import annotations

from backend.app.mcp_server import analyze_customer_request, get_audit_summary, get_request_status


def test_mcp_analysis_tool_returns_structured_result() -> None:
    result = analyze_customer_request(
        request_text="I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",
        customer_id="CUST-101",
        order_id="ORD-1001",
        transaction_id="TXN-1001-1",
        amount=1499,
        currency="INR",
    )
    assert isinstance(result, dict)
    assert result.get("decision") in {"AUTO_REFUND", "HUMAN_APPROVAL", "INFORMATION_NEEDED", "ERROR"}


def test_mcp_status_and_audit_helpers() -> None:
    assert isinstance(get_request_status("missing-request"), dict)
    summary = get_audit_summary()
    assert isinstance(summary, dict)
    assert "count" in summary
