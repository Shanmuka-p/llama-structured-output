"""Populate eval/base_responses.txt from a JSONL input file's 'output' fields.

Usage: python scripts/populate_responses.py --input data/heldout_test.jsonl --out eval/base_responses.txt
"""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

in_path = Path(args.input)
out_path = Path(args.out)
out_path.parent.mkdir(parents=True, exist_ok=True)

with in_path.open("r", encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        out = obj.get("output", "")
        # write single-line responses
        fout.write(out.replace("\n", " ") + "\n")

print(f"Wrote responses to {out_path}")
