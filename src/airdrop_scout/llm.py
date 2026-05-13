from __future__ import annotations

import os
from typing import Any

import httpx


class MiMoClient:
    """Tiny OpenAI-compatible client for optional Xiaomi MiMo reasoning.

    The project works without API keys. This adapter is intentionally small so
    reviewers can inspect how model calls would be wired in production.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("MIMO_API_KEY") or os.getenv("XIAOMI_API_KEY")
        self.base_url = (base_url or os.getenv("MIMO_BASE_URL") or "").rstrip("/")
        self.model = model or os.getenv("MIMO_MODEL", "mimo-v2.5-pro")

    @property
    def available(self) -> bool:
        return bool(self.api_key and self.base_url)

    def complete(self, system: str, user: str, timeout: float = 30.0) -> str:
        if not self.available:
            raise RuntimeError("MiMo API env not configured; use deterministic mode.")
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        with httpx.Client(timeout=timeout) as client:
            r = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return data["choices"][0]["message"]["content"]
