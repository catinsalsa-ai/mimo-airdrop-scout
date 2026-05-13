# 100T Submission Copy

## Q1 Email
khasbimln@gmail.com

## Q2 Agent tool used most
Hermes Agent

## Q3 Primary model series
MiMo

## Q4 Describe what you built with agents or AI-driven workflows
I built MiMo Airdrop Scout, an agentic due-diligence workflow for crypto airdrop/testnet hunters. The project solves a practical problem I hit often: deciding whether a new airdrop/testnet is worth my time, gas, and wallet risk before connecting anything.

The workflow is split into four small agents: a Scout Agent that normalizes the target and extracts basic signals, a Risk Agent that checks wallet-safety and campaign red flags, a Strategy Agent that decides SKIP/WATCH/PRIORITY based on risk and effort, and a Reporter Agent that turns the result into a concise Telegram-ready report. I built and iterated the project through Hermes Agent from Telegram/terminal, and the code includes a MiMo-ready OpenAI-compatible adapter so the deterministic report can be upgraded with MiMo reasoning when an API key is configured.

The current MVP runs as a Python CLI, includes tests, sample reports, a lightweight docs/demo page, and proof logs. It is designed to be safe by default: it never asks for seed phrases, private keys, OTP, KYC documents, or wallet signatures.

## Q5 Proof of usage and impact
- Terminal demo log: proof/terminal-demo.log
- Tests: pytest -q passes
- Demo docs page: docs/index.html
- GitHub repo / live demo URL: add after pushing repo
