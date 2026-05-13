from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agents import AirdropScoutWorkflow
from .models import Report, Target


def render_markdown(report: Report) -> str:
    lines = [
        f"# Airdrop Scout Report: {report.target.name}",
        "",
        f"Generated: `{report.generated_at}`",
        f"URL: {report.target.url or 'not provided'}",
        "",
        "## Verdict",
        f"- Verdict: **{report.strategy.verdict}**",
        f"- Priority score: **{report.strategy.priority_score}/100**",
        f"- Risk: **{report.risk.level} ({report.risk.score}/100)**",
        f"- Effort note: {report.strategy.effort}",
        "",
        "## Summary",
        report.summary,
        "",
        "## Positive signals",
        *[f"- {x}" for x in report.signals.positive_signals],
        "",
        "## Caution / red flags",
        *[f"- {x}" for x in report.risk.red_flags],
        "",
        "## Suggested actions",
        *[f"- {x}" for x in report.strategy.suggested_actions],
        "",
        "## Safety note",
        "Never share seed phrases/private keys/OTP/KYC documents. Use burner wallets for first interactions.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentic airdrop/testnet due-diligence scout.")
    parser.add_argument("name", help="Project/campaign name")
    parser.add_argument("--url", help="Official or candidate URL", default=None)
    parser.add_argument("--notes", help="Extra notes such as chain/tasks/status", default=None)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument("--output", "-o", help="Write report to file")
    args = parser.parse_args(argv)

    report = AirdropScoutWorkflow().run(Target(args.name, args.url, args.notes))
    output = json.dumps(report.to_dict(), indent=2) if args.json else render_markdown(report)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(f"Wrote report to {path}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
