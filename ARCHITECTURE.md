# FlowPilot AI Architecture

Webhook → Normalize → Transaction/Policy Context → AI Decision Engine → Output Validation → Guardrail

### Safe branch
Guardrail passes → Mock Refund Action → JSON Audit Response

### Exception branch
Guardrail fails → Human Review / More Information → JSON Audit Response

### Guardrail
Automatic refund requires:
- duplicate payment verified
- amount <= ₹5,000
- AI confidence >= 0.85
- decision explicitly equals AUTO_REFUND

The architecture follows the supplied presentation's core pattern: capture, understand, decide, validate, act/route, notify and log. The supplied deck explicitly emphasizes human approval for risky exceptions. 
