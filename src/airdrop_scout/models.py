from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class Target:
    name: str
    url: str | None = None
    notes: str | None = None


@dataclass
class ScoutSignals:
    normalized_name: str
    url: str | None
    tags: list[str]
    positive_signals: list[str]
    caution_signals: list[str]


@dataclass
class RiskScore:
    score: int
    level: str
    red_flags: list[str]
    mitigations: list[str]


@dataclass
class Strategy:
    verdict: str
    priority_score: int
    effort: str
    suggested_actions: list[str]


@dataclass
class Report:
    target: Target
    signals: ScoutSignals
    risk: RiskScore
    strategy: Strategy
    generated_at: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def now(cls, target: Target, signals: ScoutSignals, risk: RiskScore, strategy: Strategy, summary: str) -> "Report":
        return cls(
            target=target,
            signals=signals,
            risk=risk,
            strategy=strategy,
            generated_at=datetime.now(timezone.utc).isoformat(),
            summary=summary,
        )
