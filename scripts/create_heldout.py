"""Create a held-out test file of N examples sampled from curated_train.jsonl.

Usage: python scripts/create_heldout.py --input data/curated_train.jsonl --out data/heldout_test.jsonl --n 20
"""
import argparse
import json
import random
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--n", type=int, default=20)
args = parser.parse_args()

in_path = Path(args.input)
out_path = Path(args.out)
out_path.parent.mkdir(parents=True, exist_ok=True)

with in_path.open("r", encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]

if args.n >= len(lines):
    sample = lines
else:
    sample = random.sample(lines, args.n)

with out_path.open("w", encoding="utf-8") as f:
    for l in sample:
        f.write(l + "\n")

print(f"Wrote {len(sample)} examples to {out_path}")
