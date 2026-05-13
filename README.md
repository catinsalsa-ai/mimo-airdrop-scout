# MiMo Airdrop Scout

**MiMo Airdrop Scout** is a small, runnable agentic workflow for crypto users who want to review a fresh airdrop or testnet opportunity before spending time, gas, or connecting a wallet.

It was built with **Hermes Agent** as the operator/development agent and includes a **MiMo-ready model adapter** for Xiaomi MiMo / OpenAI-compatible endpoints. The default mode is deterministic, so reviewers can run the project without API keys.

## Why this exists

Airdrop hunters often make decisions from hype threads, referral links, or incomplete alpha. This tool turns a project name/URL into a structured operator checklist:

- wallet-safety and scam signals
- task friction and gas risk
- stale, ended, or claim-stage campaign warnings
- final verdict: `SKIP`, `WATCH`, or `PRIORITY`
- Telegram-ready summary for quick sharing

## Agent workflow

The workflow is split into four small agents:

1. **Scout Agent** — normalizes the target and extracts early ecosystem/campaign signals.
2. **Risk Agent** — scores wallet, token, website, and campaign red flags.
3. **Strategy Agent** — estimates whether the opportunity is worth time/gas.
4. **Reporter Agent** — turns the result into a compact operator-style report.

This mirrors a real Hermes workflow: scan → reason → summarize → act.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
airdrop-scout "Base Guild" --url https://guild.xyz/base --output reports/base-guild.md
```

No API key is required for the deterministic workflow.

## Optional MiMo-compatible mode

If you have a Xiaomi MiMo / OpenAI-compatible endpoint, copy `.env.example` and set:

```bash
export MIMO_API_KEY="..."
export MIMO_BASE_URL="https://api.example.com/v1"
export MIMO_MODEL="mimo-v2.5-pro"
```

When configured, the Reporter Agent can use the model to generate a richer summary. If the model call fails, the CLI falls back to deterministic output.

## Demo commands

```bash
python -m airdrop_scout.cli "Base Guild" --url https://guild.xyz/base
python -m airdrop_scout.cli "Free Urgent Wallet Claim Airdrop" --url http://claim-free-airdrop.example --json
pytest -q
```

## Example output

```text
Base Guild: PRIORITY (70/100 priority, LOW risk 10/100). Do the lowest-risk official quests first.
```

See:

- [`examples/base-guild-generated.md`](examples/base-guild-generated.md)
- [`proof/terminal-demo.log`](proof/terminal-demo.log)
- [`docs/index.html`](docs/index.html) for a lightweight demo/landing page

## Project structure

```text
src/airdrop_scout/
  agents.py      # Scout/Risk/Strategy/Reporter workflow
  cli.py         # CLI entrypoint and Markdown/JSON output
  llm.py         # Optional MiMo/OpenAI-compatible adapter
  models.py      # Dataclasses for reports and scores
examples/        # Generated reports
proof/           # Terminal demo logs for challenge submission
tests/           # Pytest coverage for workflow behavior
docs/            # Static demo page
```

## Safety

This project is educational due diligence, not financial advice. It never asks for seed phrases, private keys, OTP, KYC documents, or wallet signatures. Use burner wallets for first interactions and verify official sources manually.

## License

MIT
