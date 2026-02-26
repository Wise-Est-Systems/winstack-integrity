from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from truthlock import __version__ as TL_VERSION
from truthlock.core import evaluate_text
from winstack_integrity import __version__ as WS_VERSION
from winstack_integrity.core import make_proof

EXIT_ALLOW = 0
EXIT_FLAG = 3
EXIT_HALT = 4
EXIT_ERROR = 1

def _die(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(EXIT_ERROR)

def _write_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, indent=2)

def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _ensure_dir(p: str) -> None:
    Path(p).mkdir(parents=True, exist_ok=True)

def cmd_gate(args: argparse.Namespace) -> int:
    if not os.path.exists(args.infile):
        _die(f"ERROR: input not found: {args.infile}")

    text = _read_text(args.infile)
    decision = evaluate_text(text, tool="truthlock", version=TL_VERSION).to_dict()
    _write_json(args.out, decision)

    if args.proof_out:
        _write_json(args.proof_out, make_proof(args.infile, tool="winstack", version=WS_VERSION).to_dict())

    d = decision["decision"]
    print(d)
    return EXIT_ALLOW if d == "ALLOW" else (EXIT_FLAG if d == "FLAG" else EXIT_HALT)

def cmd_seal(args: argparse.Namespace) -> int:
    if not os.path.exists(args.file):
        _die(f"ERROR: file not found: {args.file}")
    _write_json(args.out, make_proof(args.file, tool="winstack", version=WS_VERSION).to_dict())
    print("SEALED")
    return 0

def cmd_run(args: argparse.Namespace) -> int:
    if not os.path.exists(args.infile):
        _die(f"ERROR: input not found: {args.infile}")

    _ensure_dir(args.artifacts)

    gate_out = os.path.join(args.artifacts, "decision.json")
    in_proof = os.path.join(args.artifacts, "input.proof.json")
    out_proof = os.path.join(args.artifacts, "output.proof.json")
    out_file = args.outfile

    text = _read_text(args.infile)
    decision = evaluate_text(text, tool="truthlock", version=TL_VERSION).to_dict()
    _write_json(gate_out, decision)
    _write_json(in_proof, make_proof(args.infile, tool="winstack", version=WS_VERSION).to_dict())

    if decision["decision"] == "HALT":
        print("HALT")
        return EXIT_HALT

    if args.cmd:
        with open(args.infile, "rb") as fin, open(out_file, "wb") as fout:
            proc = subprocess.run(args.cmd, stdin=fin, stdout=fout, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
            return EXIT_ERROR
    else:
        with open(args.infile, "rb") as fin, open(out_file, "wb") as fout:
            fout.write(fin.read())

    _write_json(out_proof, make_proof(out_file, tool="winstack", version=WS_VERSION).to_dict())
    print(decision["decision"])
    return EXIT_ALLOW if decision["decision"] == "ALLOW" else EXIT_FLAG

def main() -> None:
    p = argparse.ArgumentParser(prog="truthlock", description="Truthlock Governance Runtime")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("gate", help="Pre-exec governance gate")
    sp.add_argument("--in", dest="infile", required=True)
    sp.add_argument("--out", required=True)
    sp.add_argument("--proof-out", dest="proof_out")
    sp.set_defaults(fn=cmd_gate)

    sp = sub.add_parser("seal", help="Seal any file with a Winstack proof")
    sp.add_argument("--file", required=True)
    sp.add_argument("--out", required=True)
    sp.set_defaults(fn=cmd_seal)

    sp = sub.add_parser("run", help="Gate -> execute -> seal")
    sp.add_argument("--in", dest="infile", required=True)
    sp.add_argument("--out", dest="outfile", required=True)
    sp.add_argument("--artifacts", default=".truthlock/artifacts")
    sp.add_argument("--cmd", nargs=argparse.REMAINDER)
    sp.set_defaults(fn=cmd_run)

    args = p.parse_args()
    rc = args.fn(args)
    raise SystemExit(rc)
