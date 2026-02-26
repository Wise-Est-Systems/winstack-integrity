Winstack Integrity

Winstack Integrity is a deterministic CLI tool that answers one question:

Did this file change?

It generates a SHA-256 proof for any file and verifies that file against the recorded proof at any time.

Output is binary and final:
	•	VERIFIED — file matches the recorded proof
	•	TAMPERED — file does not match the recorded proof

No external services.
No trust in platforms.
No interpretation.

Just math.

⸻

Why This Exists

Digital files can be modified without obvious signs of change.

Winstack provides a simple, local-first way to:
	•	Fingerprint a file
	•	Generate a portable proof object
	•	Verify integrity later
	•	Script verification in CI or automation pipelines

Installation

pip install -e .

Usage

Create a proof

winstack prove <file> --out proof.json
This generates a SHA-256 proof and saves it to proof.json.

Verify a file
winstack verify <file> --proof proof.json

Returns:
VERIFIED
or
TAMPERED

Exit codes:
	•	0 = VERIFIED
	•	2 = TAMPERED

Design Principles
	•	Deterministic output
	•	Local-first execution
	•	Portable proof objects
	•	Scriptable CLI behavior
	•	Minimal surface area

⸻

Scope

Winstack Integrity v0.1.0 does one thing only:

Verify file integrity using SHA-256.

No feature creep.
No network dependency.
No storage layer.




