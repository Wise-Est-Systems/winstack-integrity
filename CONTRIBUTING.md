# Contributing

This project is intentionally minimal and deterministic.

## Rules
- No feature creep.
- Preserve deterministic behavior.
- Keep outputs stable:
  - Winstack: VERIFIED / TAMPERED
  - Truthlock: ALLOW / FLAG / HALT

## Dev
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
