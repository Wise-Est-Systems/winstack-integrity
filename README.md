# Winstack Integrity + Truthlock

A dual-system verification pipeline for deterministic integrity and governed execution.

This repository provides two tightly scoped components:

---

## 1. Winstack (Integrity Layer)

A local-first CLI that answers one question:

**Did this file change?**

Winstack generates a SHA-256 proof object for any file and later verifies that file against the recorded proof.

Output is binary and deterministic:

- VERIFIED — file matches proof  
- TAMPERED — file does not match proof  

No network dependency.  
No external trust.  
Only byte-level verification.

---

## 2. Truthlock (Governance Layer)

A deterministic execution gate for text-based workflows.

Truthlock evaluates input before execution and returns one of:

- ALLOW — safe to proceed  
- FLAG — governance signals detected  
- HALT — execution blocked  

Signals include:
- Fabrication pressure (e.g. "make up", "pretend", "fake sources")
- Unsourced factual assertions (FACT: lines without [source: ...])
- High-risk domains (medical, legal, finance)

Truthlock produces structured decision artifacts and supports pre-execution and post-execution sealing.

---

## Combined Model

Together, Winstack + Truthlock form a dual verification system:

1. Integrity Gate — ensure inputs have not changed  
2. Governance Gate — ensure execution meets deterministic policy  
3. Output Seal — attach proof artifacts for auditability  

This enables:

- Tamper-evident pipelines  
- Scriptable CI verification  
- Governed AI execution workflows  
- Local-first, reproducible audits  

---

## Installation (Development)

python3 -m venv .venv  
source .venv/bin/activate  
pip install -e .

---

## Winstack Usage

Create proof:

winstack prove file.txt --out proof.json

Verify file:

winstack verify file.txt --proof proof.json

Exit codes:
0 → VERIFIED  
2 → TAMPERED  

---

## Truthlock Usage

Pre-execution gate:

truthlock gate --in prompt.txt --out decision.json --proof-out input.proof.json

Run governed pipeline:

truthlock run --in prompt.txt --out output.txt

Seal output:

truthlock seal --file output.txt --out output.proof.json

Exit codes:
0 → ALLOW  
3 → FLAG  
4 → HALT  

---

## Design Principles

- Deterministic outputs  
- Local-first execution  
- Portable proof artifacts  
- Minimal surface area  
- No hidden state  
- Scriptable behavior  

---

## Scope

This is infrastructure.

It does not:
- Train models  
- Modify weights  
- Provide hosted services  
- Store remote data  

It provides deterministic verification and governance primitives.
