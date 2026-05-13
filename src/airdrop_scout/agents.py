from __future__ import annotations

import re
from urllib.parse import urlparse

from .llm import MiMoClient
from .models import Report, RiskScore, ScoutSignals, Strategy, Target

SCAM_WORDS = {"claim", "free", "airdrop", "bonus", "connect", "wallet", "urgent", "limited"}
TRUST_WORDS = {"base", "guild", "docs", "github", "testnet", "devnet", "faucet", "quest"}
ENDED_WORDS = {"tge", "ended", "closed", "snapshot done", "claim live"}


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class ScoutAgent:
    def run(self, target: Target) -> ScoutSignals:
        text = " ".join([target.name, target.url or "", target.notes or ""])
        words = _words(text)
        tags: list[str] = []
        positives: list[str] = []
        cautions: list[str] = []

        if words & TRUST_WORDS:
            tags.append("ecosystem-signal")
            positives.append("Target contains ecosystem/testnet/dev tooling keywords worth checking.")
        if target.url:
            host = urlparse(target.url).netloc.lower()
            if host:
                positives.append(f"Public URL provided: {host}")
            if any(part in host for part in ["example", "free", "claim"]):
                cautions.append("Domain pattern looks generic or claim-oriented; verify official links manually.")
        else:
            cautions.append("No URL provided; official source verification is missing.")
        if words & ENDED_WORDS:
            cautions.append("Text hints the campaign may be ended, TGE'd, or already in claim stage.")
        if not positives:
            positives.append("Enough input to start manual due-diligence checklist.")
        return ScoutSignals(target.name.strip(), target.url, sorted(tags), positives, cautions)


class RiskAgent:
    def run(self, target: Target, signals: ScoutSignals) -> RiskScore:
        text = " ".join([target.name, target.url or "", target.notes or ""])
        words = _words(text)
        red_flags = list(signals.caution_signals)
        score = 20

        scam_hits = sorted(words & SCAM_WORDS)
        if len(scam_hits) >= 3:
            score += 35
            red_flags.append(f"Multiple claim/hype keywords detected: {', '.join(scam_hits)}")
        elif scam_hits:
            score += 15
            red_flags.append(f"Contains claim/hype keywords: {', '.join(scam_hits)}")

        if target.url and not target.url.startswith("https://"):
            score += 20
            red_flags.append("URL is not HTTPS.")
        if words & ENDED_WORDS:
            score += 25
        if "ecosystem-signal" in signals.tags:
            score -= 10
        score = max(0, min(100, score))

        level = "LOW" if score < 35 else "MEDIUM" if score < 70 else "HIGH"
        mitigations = [
            "Use a fresh burner wallet for first interaction.",
            "Check official X/Discord/GitHub/docs before connecting wallet.",
            "Avoid signatures that request token approvals or unknown permissions.",
        ]
        return RiskScore(score, level, red_flags or ["No strong automated red flag detected."], mitigations)


class StrategyAgent:
    def run(self, signals: ScoutSignals, risk: RiskScore) -> Strategy:
        priority = 50
        if "ecosystem-signal" in signals.tags:
            priority += 20
        if risk.level == "HIGH":
            priority -= 35
        elif risk.level == "MEDIUM":
            priority -= 10
        if any("ended" in x.lower() or "tge" in x.lower() for x in signals.caution_signals):
            priority -= 25
        priority = max(0, min(100, priority))

        if priority >= 65 and risk.level != "HIGH":
            verdict = "PRIORITY"
            effort = "Do the lowest-risk official quests first."
        elif priority >= 35:
            verdict = "WATCH"
            effort = "Track updates; only interact after official source verification."
        else:
            verdict = "SKIP"
            effort = "Not worth wallet/time risk right now."
        actions = [
            "Verify official website from X/GitHub/docs, not from random referral threads.",
            "Record task cost, gas chain, and required signatures before doing quests.",
            "Re-run this scout after new funding/testnet/mainnet news appears.",
        ]
        return Strategy(verdict, priority, effort, actions)


class ReporterAgent:
    def __init__(self, mimo: MiMoClient | None = None) -> None:
        self.mimo = mimo or MiMoClient()

    def run(self, target: Target, signals: ScoutSignals, risk: RiskScore, strategy: Strategy) -> str:
        deterministic = (
            f"{target.name}: {strategy.verdict} ({strategy.priority_score}/100 priority, "
            f"{risk.level} risk {risk.score}/100). {strategy.effort} "
            f"Main caution: {risk.red_flags[0]}"
        )
        if not self.mimo.available:
            return deterministic
        prompt = f"""Create a concise Telegram-ready crypto airdrop due-diligence summary.
Target: {target}
Signals: {signals}
Risk: {risk}
Strategy: {strategy}
Keep it practical and do not give financial advice."""
        try:
            return self.mimo.complete("You are a cautious crypto security analyst.", prompt)
        except Exception as exc:  # fallback keeps CLI reliable
            return deterministic + f" (MiMo fallback used: {exc.__class__.__name__})"


class AirdropScoutWorkflow:
    def __init__(self) -> None:
        self.scout = ScoutAgent()
        self.risk = RiskAgent()
        self.strategy = StrategyAgent()
        self.reporter = ReporterAgent()

    def run(self, target: Target) -> Report:
        signals = self.scout.run(target)
        risk = self.risk.run(target, signals)
        strategy = self.strategy.run(signals, risk)
        summary = self.reporter.run(target, signals, risk, strategy)
        return Report.now(target, signals, risk, strategy, summary)
