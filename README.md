\# 🚀 FlowPilot AI — Autonomous Business Process Automation



> \*\*AI-powered customer-service automation using n8n, Google Gemini, policy guardrails, human-in-the-loop approval, Gmail notifications, and auditable JSON results.\*\*



\---



\## 🔗 Live Project Links



| Resource | Link |

|---|---|

| 📦 \*\*GitHub Repository\*\* | \[FlowPilot AI — GitHub](https://github.com/Pranavreddyedula/flowpilot-ai) |

| ⚙️ \*\*Live n8n Workflow\*\* | \[FlowPilot AI — n8n Cloud](https://pranav16.app.n8n.cloud/workflow/j0CcZaKNKzRACXLU) |

| 🧩 \*\*n8n Platform\*\* | \[n8n.io](https://n8n.io/) |

| 📚 \*\*n8n Documentation\*\* | \[n8n Docs](https://docs.n8n.io/) |

| 🤖 \*\*Google Gemini\*\* | \[Google AI Studio](https://aistudio.google.com/) |



\---



\# 📌 Project Overview



\*\*FlowPilot AI\*\* is an n8n-based AI decision and action agent designed to automate repetitive customer-service processes.



The system receives a natural-language customer request, uses \*\*Google Gemini\*\* to understand the request, applies decision and confidence guardrails, and then either:



\- Executes a safe \*\*mock refund action\*\*, or

\- Routes the request to \*\*human approval\*\* and sends a Gmail notification.



The complete concept is:



```text

Capture

&#x20;  ↓

Understand

&#x20;  ↓

Decide

&#x20;  ↓

Validate

&#x20;  ↓

Act / Escalate

&#x20;  ↓

Notify

&#x20;  ↓

Log



The primary hackathon demonstration is duplicate-payment and refund handling.



🎯 Problem Statement



Customer-service teams receive many repetitive requests every day.



Examples include:



Duplicate payment complaints

Refund requests

High-value refund requests

Requests requiring additional information

Requests that need human approval



Traditional automation often works with fixed rules:



IF X → DO Y



This becomes difficult when customers describe their problems using natural language.



For example:



"I was charged twice for my order. Please refund the extra payment."



The system needs to understand what the customer means before deciding what action should happen.



💡 Our Solution



FlowPilot AI adds an AI decision layer before automation executes an action.



The workflow:



Receives the customer request.

Normalizes the request.

Sends the request to Google Gemini.

Gemini identifies the intent, urgency, entities, decision, confidence, and reason.

The AI output is validated.

Guardrails check whether automatic execution is allowed.

Safe requests go to the mock refund action.

Risky requests go to human approval.

Gmail sends an approval notification.

The workflow returns an auditable JSON result.

🧠 What Makes FlowPilot More Than Simple Automation?



A normal automation may simply follow:



IF condition → ACTION



FlowPilot first understands the natural-language request.



The AI decision layer considers:



Intent

Urgency

Order ID

Amount

Currency

Requested action

Confidence

Reason for the decision



Then deterministic workflow guardrails decide whether the AI's decision can proceed to automatic execution.



This creates a combination of:



Natural Language

&#x20;      +

AI Decisioning

&#x20;      +

Guardrails

&#x20;      +

Automation

&#x20;      +

Human-in-the-Loop

&#x20;      +

Auditability

🏗️ Architecture

High-Level Architecture

&#x20;                   ┌─────────────────────┐

&#x20;                   │      Customer       │

&#x20;                   │ Natural Language    │

&#x20;                   │      Request        │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │    n8n Webhook      │

&#x20;                   │ Capture Request     │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │ Normalize Request   │

&#x20;                   │ Customer / Order    │

&#x20;                   │ Request / Source    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   Gemini AI Engine  │

&#x20;                   │ Intent              │

&#x20;                   │ Urgency             │

&#x20;                   │ Entities            │

&#x20;                   │ Decision            │

&#x20;                   │ Confidence          │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │ Validate AI Output  │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   Guardrail Check   │

&#x20;                   │ Decision +          │

&#x20;                   │ Confidence          │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                 ┌────────────┴────────────┐

&#x20;                 │                         │

&#x20;                 ▼                         ▼

&#x20;       ┌─────────────────┐       ┌────────────────────┐

&#x20;       │    SAFE CASE    │       │    RISKY CASE      │

&#x20;       │ AUTO\_REFUND     │       │ HUMAN\_APPROVAL     │

&#x20;       └────────┬────────┘       └──────────┬─────────┘

&#x20;                │                           │

&#x20;                ▼                           ▼

&#x20;       ┌─────────────────┐       ┌────────────────────┐

&#x20;       │ Mock Refund     │       │ Human Approval     │

&#x20;       │ Action          │       │ Queue              │

&#x20;       └────────┬────────┘       └──────────┬─────────┘

&#x20;                │                           │

&#x20;                │                           ▼

&#x20;                │                  ┌────────────────────┐

&#x20;                │                  │ Gmail Notification │

&#x20;                │                  └──────────┬─────────┘

&#x20;                │                             │

&#x20;                └──────────────┬──────────────┘

&#x20;                               │

&#x20;                               ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   Return Result     │

&#x20;                   │ JSON + Audit        │

&#x20;                   └─────────────────────┘

🔄 Complete Workflow



The current n8n workflow contains these main stages:



Incoming Customer Request

&#x20;           ↓

Normalize Request

&#x20;           ↓

AI Decision Engine

&#x20;           ↓

Validate AI Output

&#x20;           ↓

Guardrail Check

&#x20;       ↙        ↘

&#x20;    SAFE         RISKY

&#x20;      ↓            ↓

Execute Refund   Human Approval

&#x20;      ↓            ↓

&#x20;      │          Gmail

&#x20;      │            ↓

&#x20;      └──────┬─────┘

&#x20;             ↓

&#x20;       Return Result

&#x20;             ↓

&#x20;         JSON Audit

🧩 n8n Workflow Nodes

1\. Incoming Customer Request



The workflow begins with an n8n Webhook.



It receives:



Customer request

Customer ID

Order ID

Source



Example:



{

&#x20; "request": "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "source": "hackathon-demo"

}

2\. Normalize Request



The request is converted into a consistent structure.



The workflow prepares:



Request

Customer ID

Order ID

Timestamp

Source



This ensures that the AI receives clean and predictable input.



🤖 3. AI Decision Engine



The AI Decision Engine uses Google Gemini.



Current live demo model:



Gemini 3.5 Flash-Lite



Gemini analyzes the customer request and produces structured information.



The AI is expected to identify:



Intent

Urgency

Entities

Decision

Confidence

Reason

Customer Message

🧪 4. Validate AI Output



The workflow parses the AI response.



If the AI response cannot be safely parsed, the workflow falls back to a human-review decision rather than allowing an unsafe automatic action.



This is an important safety layer.



🛡️ 5. Guardrail Check



The Guardrail Check determines whether the request can proceed automatically.



The current automatic execution requirement is:



Decision = AUTO\_REFUND

AND

Confidence >= 0.85



If both conditions are satisfied:



AUTO\_REFUND

&#x20;     ↓

Execute Refund



Otherwise:



Human Approval

💰 6. Execute Refund — Mock Action



The Execute Refund node is intentionally a mock action for the hackathon.



It generates a simulated refund identifier such as:



RF-xxxxxxxx



and returns:



AUTO\_RESOLVED

Important



The refund action:



Does NOT connect to a real payment gateway.

Does NOT move real money.

Does NOT create a real banking transaction.



It demonstrates where a production refund API would be connected.



👤 7. Human Approval Queue



High-risk or uncertain requests are routed to the human approval path.



The workflow generates:



HUMAN\_REVIEW



and:



APPROVAL\_REQUIRED



The reviewer receives information such as:



Customer ID

Order ID

Decision

Confidence

Reason

Customer message

Status

Action

📧 8. Gmail Notification



The high-risk path uses Gmail to notify the human reviewer.



Example:



FlowPilot Human Approval Required



Customer ID: CUST-101

Order ID: ORD-1001

Decision: HUMAN\_APPROVAL

Confidence: 0.95



Reason:

High-value refund request requires manual verification.



Status:

HUMAN\_REVIEW



Action:

APPROVAL\_REQUIRED



This demonstrates the human-in-the-loop concept.



📦 9. Return Result



The final node returns a structured JSON response.



Example:



{

&#x20; "status": "AUTO\_RESOLVED",

&#x20; "action": "REFUND\_CREATED",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "confidence": 0.95

}



The response also contains audit information.



🛡️ Policy \& Guardrails



The project includes a policy.json file describing the intended refund decision policy.



Current demo policy:



Scenario	Decision

Duplicate payment ≤ ₹5,000	AUTO\_REFUND

Duplicate payment > ₹5,000	HUMAN\_APPROVAL

Missing order / transaction evidence	INFORMATION\_NEEDED

Suspicious or unclear case	HUMAN\_APPROVAL



Automatic execution also requires:



Confidence >= 0.85



This prevents every AI decision from automatically becoming an action.



🧪 Live Demo Scenario 1 — Safe Duplicate Payment

Customer Request

I was charged twice for order ORD-1001.

Please refund the duplicate payment of Rs 1499.

Request

{

&#x20; "request": "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "source": "hackathon-auto-refund-test"

}

Workflow

Customer Request

&#x20;      ↓

Webhook

&#x20;      ↓

Normalize

&#x20;      ↓

Gemini

&#x20;      ↓

AUTO\_REFUND

&#x20;      ↓

Confidence Check

&#x20;      ↓

Execute Refund Mock

&#x20;      ↓

AUTO\_RESOLVED

Example Output

status      : AUTO\_RESOLVED

action      : REFUND\_CREATED

customer\_id : CUST-101

order\_id    : ORD-1001

refund\_id   : RF-xxxxxxxx

confidence  : 0.95

Important



The refund\_id is only a simulated demo identifier.



No real money is transferred.



🚨 Live Demo Scenario 2 — High-Value Request

Customer Request

I want a refund of Rs 50000 for my order ORD-1001.

Please process it immediately.

Request

{

&#x20; "request": "I want a refund of Rs 50000 for my order ORD-1001. Please process it immediately.",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "source": "hackathon-high-risk-test"

}

Workflow

Customer Request

&#x20;      ↓

Webhook

&#x20;      ↓

Normalize

&#x20;      ↓

Gemini

&#x20;      ↓

HUMAN\_APPROVAL

&#x20;      ↓

Guardrail

&#x20;      ↓

Human Approval Queue

&#x20;      ↓

Gmail Notification

&#x20;      ↓

HUMAN\_REVIEW

Example Output

status      : HUMAN\_REVIEW

action      : APPROVAL\_REQUIRED

decision    : HUMAN\_APPROVAL

confidence  : 0.95



This demonstrates that the system does not automatically execute every request.



📊 Example AI Output



A typical structured AI response looks like:



{

&#x20; "intent": "duplicate\_charge",

&#x20; "urgency": "normal",

&#x20; "entities": {

&#x20;   "order\_id": "ORD-1001",

&#x20;   "amount": 1499,

&#x20;   "currency": "INR"

&#x20; },

&#x20; "decision": "AUTO\_REFUND",

&#x20; "confidence": 0.95,

&#x20; "reason": "Clear duplicate-charge request within the low-risk policy limit.",

&#x20; "customer\_message": "The refund workflow has been initiated for Rs 1499."

}



The exact confidence and generated customer message may vary between AI executions.



📋 Example Audit Output



The workflow returns audit information along with the result.



Example:



{

&#x20; "status": "AUTO\_RESOLVED",

&#x20; "action": "REFUND\_CREATED",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "reason": "Low-risk duplicate-charge request.",

&#x20; "audit": {

&#x20;   "agent\_decision": "AUTO\_REFUND",

&#x20;   "confidence": 0.95,

&#x20;   "timestamp": "2026-09-29T05:47:01.198Z"

&#x20; }

}



For human review:



{

&#x20; "status": "HUMAN\_REVIEW",

&#x20; "action": "APPROVAL\_REQUIRED",

&#x20; "decision": "HUMAN\_APPROVAL",

&#x20; "audit": {

&#x20;   "escalation": true

&#x20; }

}

🧰 Technology Stack

Core Technologies

Technology	Usage

n8n Cloud	Workflow orchestration

Google Gemini	AI understanding and decisioning

Gemini 3.5 Flash-Lite	Current live AI model

JavaScript	n8n Code nodes

REST / Webhooks	Request interface

Gmail	Human approval notification

JSON	Data exchange and audit output

PowerShell	Live webhook testing/demo

GitHub	Source code and documentation

Concepts Used

AI Decisioning

Natural Language Processing

Workflow Automation

Business Process Automation

Human-in-the-Loop

Policy Guardrails

Confidence Thresholds

Exception Handling

Webhooks

REST APIs

Structured JSON

Auditability

🖥️ PowerShell Live Demo



PowerShell is used only as the client that sends the test request.



The actual automation is performed by n8n.



Example:



$jsonBody = @{

&#x20;   request = "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499."

&#x20;   customer\_id = "CUST-101"

&#x20;   order\_id = "ORD-1001"

&#x20;   source = "hackathon-demo"

} | ConvertTo-Json -Compress



Invoke-RestMethod `

&#x20;   -Method POST `

&#x20;   -Uri "YOUR\_N8N\_WEBHOOK\_TEST\_URL" `

&#x20;   -ContentType "application/json" `

&#x20;   -Body $jsonBody

🎤 How To Demonstrate The Project

Step 1 — Open GitHub



Show the project repository:



👉 FlowPilot AI — GitHub



Explain:



"This repository contains our project documentation, n8n workflow, policy configuration, demo scripts, architecture, and presentation."



Step 2 — Open n8n



Open the live workflow:



👉 FlowPilot AI — n8n Cloud



Show the workflow canvas.



Explain:



"This is the live automation workflow. The request enters through the webhook, Gemini understands it, the output is validated, and guardrails decide whether the workflow can automatically act or needs human approval."



Step 3 — Run Low-Risk Request



Use PowerShell.



Send:



I was charged twice for order ORD-1001.

Please refund the duplicate payment of Rs 1499.



Show the workflow execution.



The safe path should look like:



Webhook

&#x20; ↓

Normalize

&#x20; ↓

Gemini

&#x20; ↓

Validate

&#x20; ↓

Guardrail

&#x20; ↓

Execute Refund

&#x20; ↓

Return Result



Then show:



AUTO\_RESOLVED

Step 4 — Run High-Risk Request



Send:



I want a refund of Rs 50000 for my order ORD-1001.

Please process it immediately.



Show that the workflow takes the other branch:



Guardrail

&#x20;   ↓

Human Approval

&#x20;   ↓

Gmail

&#x20;   ↓

Human Review



Then open Gmail and show the approval notification.



📦 Repository Structure

flowpilot-ai/

│

├── ARCHITECTURE.md

├── README.md

├── demo\_script.md

├── docker-compose.yml

├── FlowPilot\_AI\_Hackathon\_Presentation.pptx

├── flowpilot\_ai\_n8n\_workflow.json

├── policy.json

├── sample\_requests.json

└── SUBMISSION\_CHECKLIST.md

Important Files

README.md



Complete project documentation.



ARCHITECTURE.md



Architecture and system design.



flowpilot\_ai\_n8n\_workflow.json



Importable n8n workflow baseline.



policy.json



Policy rules and guardrails.



sample\_requests.json



Example requests for testing.



demo\_script.md



Hackathon demonstration script.



SUBMISSION\_CHECKLIST.md



Submission checklist.



docker-compose.yml



Local/self-hosted n8n configuration support.



FlowPilot\_AI\_Hackathon\_Presentation.pptx



Hackathon presentation.



⚙️ Setup

1\. Install / Open n8n



Use either:



n8n Cloud

Self-hosted n8n



Official website:



👉 https://n8n.io/



Documentation:



👉 https://docs.n8n.io/



2\. Import The Workflow



Import:



flowpilot\_ai\_n8n\_workflow.json



into n8n.



3\. Configure Google Gemini



The current live demo uses Google Gemini.



Configure the Gemini credential inside n8n.



The API key must remain private.



Never put API keys inside GitHub.



Do not commit:



API keys

Passwords

Tokens

Credentials

Secrets

4\. Configure Gmail



The high-risk human-review path uses Gmail.



Configure a Gmail credential in n8n and connect it to the approval notification node.



5\. Test The Webhook



Use the webhook test URL generated by n8n.



Send:



{

&#x20; "request": "I was charged twice for order ORD-1001. Please refund the duplicate payment of Rs 1499.",

&#x20; "customer\_id": "CUST-101",

&#x20; "order\_id": "ORD-1001",

&#x20; "source": "demo"

}

🔐 Security \& Safety



FlowPilot is currently a hackathon prototype.



The project includes several safety concepts:



AI Decision Constraints



The AI is expected to return approved decision values such as:



AUTO\_REFUND

HUMAN\_APPROVAL

INFORMATION\_NEEDED

NO\_ACTION

Confidence Guardrail



Automatic execution requires:



confidence >= 0.85

Human-in-the-Loop



Risky requests are routed to human approval.



Mock Financial Action



The refund action is simulated.



No real money is transferred.



Credential Safety



API credentials should be stored inside n8n credentials/environment variables and should never be committed to GitHub.



⚠️ Current Limitations



This is a hackathon prototype, not a production payment system.



The current version does not contain:



Real payment gateway integration

Real refund processing

Real banking transaction

Production transaction database lookup

Production customer database

Production authentication system

RAG/vector database

Enterprise approval system

Production fraud detection system



The current project focuses on demonstrating:



AI Understanding

&#x20;      +

Decisioning

&#x20;      +

Guardrails

&#x20;      +

Workflow Automation

&#x20;      +

Human Approval

&#x20;      +

Auditability

🚀 Future Improvements



The architecture can be extended with real production systems.



Database Integration



Possible future integrations:



PostgreSQL

Google Sheets

MySQL

Customer Database

Transaction Database



This would allow actual transaction verification before making decisions.



🧠 RAG / Knowledge Base



A future version could add:



Policy Documents

&#x20;     ↓

Vector Database

&#x20;     ↓

RAG Retrieval

&#x20;     ↓

Gemini

&#x20;     ↓

Policy-aware Decision



This would allow FlowPilot to retrieve company policies dynamically.



💳 Real Payment Integration



The mock refund node could eventually be replaced with a real authenticated payment API.



Example:



FlowPilot

&#x20;  ↓

Guardrail

&#x20;  ↓

Payment API

&#x20;  ↓

Refund

&#x20;  ↓

Transaction ID

&#x20;  ↓

Audit Log



The production version would require proper authentication, authorization, transaction verification, idempotency, monitoring, and security controls.



📧 More Notification Channels



Future notification integrations could include:



Slack

Microsoft Teams

Gmail

SMS

Internal support dashboards

📊 Future Dashboard



A dashboard could track:



Total requests

Auto-resolution rate

Human-review rate

Average resolution time

Approval rate

Error rate

Rework rate

Human intervention rate

🌐 Production Architecture



A future production architecture could look like:



Customer

&#x20;  ↓

API Gateway

&#x20;  ↓

Authentication

&#x20;  ↓

n8n Orchestration

&#x20;  ↓

AI Decision Engine

&#x20;  ↓

RAG / Policy Knowledge

&#x20;  ↓

Customer + Transaction Database

&#x20;  ↓

Policy / Risk Engine

&#x20;  ↓

Guardrails

&#x20;  ├───────────────┐

&#x20;  ↓               ↓

Safe Action     Human Review

&#x20;  ↓               ↓

Payment API      Gmail / Slack

&#x20;  ↓

Audit Log

&#x20;  ↓

Monitoring / Dashboard

📈 Current Project Status

Component	Status

GitHub Repository	✅ Working

n8n Cloud Workflow	✅ Working

Webhook	✅ Working

Request Normalization	✅ Working

Gemini AI Decision Engine	✅ Working

AI Output Validation	✅ Working

Confidence Guardrail	✅ Working

Low-Risk Auto Resolution	✅ Working

Mock Refund Action	✅ Working

Human Approval Routing	✅ Working

Gmail Notification	✅ Working

JSON Result	✅ Working

Audit Information	✅ Working

Real Payment Integration	🔜 Future

Real Database Verification	🔜 Future

RAG / Vector Database	🔜 Future

Production Dashboard	🔜 Future

🧪 Test Cases

Test Case 1 — Safe Duplicate

Request:

I was charged twice for order ORD-1001.

Please refund the duplicate payment of Rs 1499.



Expected:



AUTO\_RESOLVED

Test Case 2 — High-Value Request

Request:

I want a refund of Rs 50000 for order ORD-1001.



Expected:



HUMAN\_REVIEW

Test Case 3 — Incomplete Request

Request:

I want my money back.



Expected AI decision:



INFORMATION\_NEEDED



The current workflow is designed to prevent non-approved decisions from reaching the automatic refund path.

