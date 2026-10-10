from __future__ import annotations

import json
from typing import Any

import boto3

from backend.app.providers.provider_interface import BaseAIProvider, ProviderError


class BedrockProvider(BaseAIProvider):
    provider_name = "bedrock"

    def __init__(self, model_id: str, region_name: str = "us-east-1") -> None:
        self.model_id = model_id
        self.region_name = region_name

    async def analyze(
        self,
        *,
        request_text: str,
        customer_id: str | None = None,
        order_id: str | None = None,
        transaction_id: str | None = None,
        amount: Any = None,
        currency: str | None = None,
    ) -> dict[str, Any]:
        try:
            client = boto3.client("bedrock-runtime", region_name=self.region_name)
        except Exception as exc:  # pragma: no cover - defensive for missing AWS config
            raise ProviderError(f"Bedrock client could not be created: {exc}") from exc

        prompt = (
            "You are FlowPilot AI in a strict customer-service refund safety workflow. "
            "Return a valid JSON object only. Keys: intent, urgency, decision, confidence, "
            "reasons, entities, missing_evidence, next_action. Use only approved values: "
            "AUTO_REFUND, HUMAN_APPROVAL, INFORMATION_NEEDED, NO_ACTION. "
            "Never authorize a real refund. The amount is always in INR. "
            "Return a confidence value between 0 and 1."
            f"\nCustomer request: {request_text}\nCustomer ID: {customer_id or 'unknown'}\n"
            f"Order ID: {order_id or 'unknown'}\nTransaction ID: {transaction_id or 'unknown'}\n"
            f"Amount: {amount if amount is not None else 'unknown'}\nCurrency: {currency or 'INR'}"
        )

        try:
            response = client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 600, "temperature": 0.1, "topP": 0.9},
                system=[{"text": "You are a safe refund decision assistant. Produce structured JSON only."}],
            )
        except Exception as exc:  # pragma: no cover - depends on AWS account setup
            raise ProviderError(f"Bedrock call failed: {exc}") from exc

        content = response.get("output", {}).get("message", {}).get("content", [])
        text_blocks = [block.get("text", "") for block in content if isinstance(block, dict) and "text" in block]
        model_text = "\n".join(text_blocks).strip()
        if not model_text:
            raise ProviderError("Bedrock returned no parseable text output.")

        parsed = self._parse_json_output(model_text)
        if not isinstance(parsed, dict):
            raise ProviderError("Bedrock output was not a JSON object.")

        normalized = {
            "intent": parsed.get("intent", "unknown"),
            "urgency": parsed.get("urgency", "normal"),
            "decision": parsed.get("decision", "HUMAN_APPROVAL"),
            "confidence": float(parsed.get("confidence", 0.0) or 0.0),
            "reasons": parsed.get("reasons", ["Bedrock reasoning not provided."]),
            "entities": parsed.get("entities", {}),
            "missing_evidence": parsed.get("missing_evidence", []),
            "next_action": parsed.get("next_action", "Manual review required."),
            "provider": self.provider_name,
            "model_id": self.model_id,
        }
        return normalized

    @staticmethod
    def _parse_json_output(raw_text: str) -> dict[str, Any]:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end > start:
                return json.loads(cleaned[start : end + 1])
            raise
