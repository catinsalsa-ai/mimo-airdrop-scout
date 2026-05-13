# Contributing

Thanks for checking out MiMo Airdrop Scout.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
pytest -q
```

## Guidelines

- Keep the default workflow runnable without API keys.
- Never add code that asks for seed phrases, private keys, OTP, or KYC documents.
- Prefer small, testable agents over one large function.
- Add tests when changing scoring or verdict logic.
