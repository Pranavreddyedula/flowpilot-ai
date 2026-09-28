# FlowPilot AI — Autonomous Business Process Automation

## Project
**FlowPilot AI** is an n8n-based AI decision and action agent for customer-service requests.

It follows the same concept as the supplied hackathon presentation:

**Capture → Understand → Decide → Validate → Act/Escalate → Notify → Log**

The demo use case is duplicate-payment/refund handling.

## What makes it more than simple automation
A normal automation follows fixed rules such as `IF X → DO Y`.
FlowPilot first interprets a natural-language request, identifies intent/urgency/entities, makes a policy-aware decision, checks confidence, and then either executes an approved action or sends the case to human approval.

## Architecture
1. Webhook receives customer request.
2. Request is normalized.
3. LLM extracts intent, urgency, entities and decision.
4. Guardrails validate the AI decision and confidence.
5. Approved low-risk requests go to the refund action.
6. High-risk/uncertain requests go to the human approval queue.
7. The workflow returns an auditable JSON result.

## What is actually automated
- Natural-language request intake
- Transaction/policy context lookup (demo dataset)
- AI classification and decisioning
- Confidence and policy guardrails
- Automatic refund mock action for safe cases
- Human-review routing for risky cases
- Information-needed routing for incomplete cases
- JSON audit output

**Important:** the refund execution is a mock action for the hackathon demo. It does not move real money.

## Setup
### 1. Install n8n
Use n8n Cloud or self-hosted n8n.

### 2. Import workflow
Import `flowpilot_ai_n8n_workflow.json` into n8n.

### 3. Configure API key
Set an environment variable:
`OPENAI_API_KEY=YOUR_KEY`

Or replace the HTTP Request authentication with your preferred credential method.

### 4. Activate and test
Use the webhook test URL and POST a request such as:

```json
{
  "request": "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",
  "customer_id": "CUST-101",
  "order_id": "ORD-1001",
  "source": "demo"
}
```

## Demo outcomes
- Small verified duplicate → `AUTO_RESOLVED`
- High-value duplicate → `HUMAN_REVIEW`
- Missing evidence → AI should choose `INFORMATION_NEEDED`, which remains outside automatic execution

## Important hackathon note
The refund node is intentionally a **safe demo/mock action**. For production, replace it with an authenticated payment/refund API and add database-backed transaction verification.

## Suggested extensions
- Gmail trigger
- Google Sheets/PostgreSQL customer lookup
- Vector database/RAG policy retrieval
- Slack approval notification
- Real payment gateway API
- Dashboard for resolution time, auto-resolution rate, escalation rate and error/rework rate

## Submission story
Problem: customer requests are fragmented and repetitive.
Solution: AI understands the request and n8n executes only policy-approved actions.
Differentiator: context + reasoning + guardrails + human-in-the-loop + auditability.
