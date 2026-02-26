from __future__ import annotations
import argparse
import subprocess
import sys

def main() -> None:
    p = argparse.ArgumentParser(prog="wise", description="WISE v3: One CLI for integrity + governance.")
    sub = p.add_subparsers(dest="mode", required=True)

    # Integrity
    sp = sub.add_parser("prove", help="Create proof for a file")
    sp.add_argument("file")
    sp.add_argument("--out", required=True)

    sp = sub.add_parser("verify", help="Verify file against proof")
    sp.add_argument("file")
    sp.add_argument("--proof", required=True)

    # Governance
    sp = sub.add_parser("gate", help="Governance gate on input text")
    sp.add_argument("--in", dest="infile", required=True)
    sp.add_argument("--out", required=True)
    sp.add_argument("--proof-out", dest="proof_out")

    sp = sub.add_parser("seal", help="Seal any file with proof")
    sp.add_argument("--file", required=True)
    sp.add_argument("--out", required=True)

    sp = sub.add_parser("run", help="Gate -> execute -> seal")
    sp.add_argument("--in", dest="infile", required=True)
    sp.add_argument("--out", dest="outfile", required=True)
    sp.add_argument("--artifacts", default=".truthlock/artifacts")
    sp.add_argument("--exec", nargs=argparse.REMAINDER, help="Command to run (reads stdin, writes stdout)")

    args = p.parse_args()

    if args.mode == "prove":
        raise SystemExit(subprocess.call(["winstack", "prove", args.file, "--out", args.out]))

    if args.mode == "verify":
        raise SystemExit(subprocess.call(["winstack", "verify", args.file, "--proof", args.proof]))

    if args.mode == "gate":
        cmd = ["truthlock", "gate", "--in", args.infile, "--out", args.out]
        if args.proof_out:
            cmd += ["--proof-out", args.proof_out]
        raise SystemExit(subprocess.call(cmd))

    if args.mode == "seal":
        raise SystemExit(subprocess.call(["truthlock", "seal", "--file", args.file, "--out", args.out]))

    if args.mode == "run":
        cmd = ["truthlock", "run", "--in", args.infile, "--out", args.outfile, "--artifacts", args.artifacts]
        if args.exec:
            cmd += ["--cmd"] + args.exec
        raise SystemExit(subprocess.call(cmd))

    raise SystemExit(1)
