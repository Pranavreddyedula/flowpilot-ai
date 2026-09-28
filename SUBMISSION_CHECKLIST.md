# FlowPilot AI — Final Hackathon Submission Checklist

## 1. Core submission
- [x] Problem statement: repetitive customer-service operations
- [x] AI-powered decision making
- [x] n8n orchestration
- [x] Human-in-the-loop guardrail
- [x] End-to-end demo workflow
- [x] Measurable impact/KPI framing
- [x] Presentation deck
- [x] Importable n8n workflow
- [x] Sample test cases
- [x] Setup instructions

## 2. Live demo order
1. Import `flowpilot_ai_n8n_workflow.json`.
2. Configure `OPENAI_API_KEY`.
3. Activate/test the webhook.
4. Run `sample_requests.json` in this order:
   - ORD-1001 → AUTO_RESOLVED
   - ORD-1002 → HUMAN_REVIEW
   - Missing order → INFORMATION_NEEDED
5. Show the final JSON audit response.

## 3. Judge talking points
**Problem:** Humans repeatedly classify, verify and route requests.

**Innovation:** The system interprets natural language and chooses an action path instead of merely moving data between systems.

**Safety:** AI cannot directly perform unrestricted actions. Automatic refund requires a verified duplicate, amount within the policy limit, and confidence >= 0.85. Otherwise the workflow routes the case away from automatic execution.

**Business value:** Reduced repetitive work, faster response, traceability and measurable automation/escalation metrics.

## 4. Do not claim during the demo
- Do not claim a real refund was processed.
- Do not claim real customer/payment data is connected.
- Do not claim production readiness.
- Call the transaction lookup and refund action a **demo/mock integration**.

## 5. Final files
- `flowpilot_ai_n8n_workflow.json`
- `policy.json`
- `sample_requests.json`
- `README.md`
- `demo_script.md`
- `SUBMISSION_CHECKLIST.md`
- `FlowPilot_AI_Hackathon_Presentation.pptx`
- `docker-compose.yml`
