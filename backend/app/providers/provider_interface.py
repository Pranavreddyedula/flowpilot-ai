from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ProviderError(RuntimeError):
    pass


class BaseAIProvider(ABC):
    @abstractmethod
    async def analyze(self, *, request_text: str, customer_id: str | None = None, order_id: str | None = None, transaction_id: str | None = None, amount: Any = None, currency: str | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError
