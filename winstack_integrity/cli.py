from __future__ import annotations
import argparse
import json
import os
import sys
from winstack_integrity import __version__
from winstack_integrity.core import make_proof, compare

EXIT_VERIFIED = 0
EXIT_TAMPERED = 2
EXIT_ERROR = 1

def _die(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(EXIT_ERROR)

def main() -> None:
    p = argparse.ArgumentParser(prog="winstack", description="Winstack Integrity: did this file change?")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("prove", help="Create a proof JSON for a file")
    sp.add_argument("file")
    sp.add_argument("--out", required=True)

    sp = sub.add_parser("verify", help="Verify a file against a proof JSON")
    sp.add_argument("file")
    sp.add_argument("--proof", required=True)

    args = p.parse_args()

    if args.cmd == "prove":
        if not os.path.exists(args.file):
            _die(f"ERROR: file not found: {args.file}")
        proof = make_proof(args.file, tool="winstack", version=__version__).to_dict()
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(proof, f, sort_keys=True, indent=2)
        print("OK: PROOF CREATED")
        raise SystemExit(0)

    if args.cmd == "verify":
        if not os.path.exists(args.file):
            _die(f"ERROR: file not found: {args.file}")
        if not os.path.exists(args.proof):
            _die(f"ERROR: proof not found: {args.proof}")

        with open(args.proof, "r", encoding="utf-8") as f:
            proof = json.load(f)

        ok, observed, expected = compare(args.file, proof)
        if ok:
            print("VERIFIED")
            raise SystemExit(EXIT_VERIFIED)
        else:
            print("TAMPERED")
            print("expected:", expected)
            print("observed:", observed)
            raise SystemExit(EXIT_TAMPERED)
