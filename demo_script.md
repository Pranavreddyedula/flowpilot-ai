# 3-Minute Hackathon Demo Script

## 0:00 — Problem
“Customer-service teams receive repetitive requests from email, forms and chat. Humans repeatedly classify, verify policy, check customer context and decide what to do.”

## 0:30 — Solution
“FlowPilot AI converts a natural-language request into an autonomous decision loop: understand, retrieve context, reason, validate, act or escalate, and log.”

## 0:55 — Demo 1: Safe automatic resolution
Send:
“I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.”

Show:
- intent = duplicate payment
- confidence >= 0.85
- decision = AUTO_REFUND
- status = AUTO_RESOLVED
- refund ID + audit record

## 1:35 — Demo 2: Human approval
Send:
“I was charged twice for order ORD-1002. The duplicate amount is Rs 12500. Please refund it.”

Show:
- high-value case
- decision = HUMAN_APPROVAL
- status = HUMAN_REVIEW

Say:
“The AI does not get unrestricted control. Risky cases are routed to a human.”

## 2:10 — Demo 3: Ambiguous request
Send:
“I think I was charged twice but I don't have the order number.”

Show:
- missing evidence
- decision = INFORMATION_NEEDED

## 2:35 — Differentiator
“Traditional automation moves data. FlowPilot uses AI to understand context, choose a path within guardrails, execute approved actions and preserve an audit trail.”

## 2:55 — Close
“FlowPilot can be extended from refunds to HR, finance, sales, IT support and other repetitive business operations.”
