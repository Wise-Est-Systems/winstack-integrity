import argparse
import json
import os
import sys
from winstack_integrity import __version__
from winstack_integrity.core import make_proof, compare

def die(msg):
    print(msg)
    sys.exit(1)

def main():
    p = argparse.ArgumentParser(prog="winstack")
    sub = p.add_subparsers(dest="cmd", required=True)

    f1 = sub.add_parser("prove")
    f1.add_argument("file")
    f1.add_argument("--out", required=True)

    f2 = sub.add_parser("verify")
    f2.add_argument("file")
    f2.add_argument("--proof", required=True)

    args = p.parse_args()

    if args.cmd == "prove":
        if not os.path.exists(args.file):
            die("File not found")
        proof = make_proof(args.file, "winstack", __version__).to_dict()
        with open(args.out, "w") as f:
            json.dump(proof, f, indent=2)
        print("PROOF CREATED")

    if args.cmd == "verify":
        if not os.path.exists(args.file):
            die("File not found")
        with open(args.proof) as f:
            proof = json.load(f)
        ok, observed, expected = compare(args.file, proof)
        if ok:
            print("VERIFIED")
            sys.exit(0)
        else:
            print("TAMPERED")
            print("expected:", expected)
            print("observed:", observed)
            sys.exit(2)
