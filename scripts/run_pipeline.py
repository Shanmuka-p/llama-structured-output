"""Run the full local pipeline: generate dataset, create heldout, populate responses, evaluate.

Usage: python scripts/run_pipeline.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd, **kwargs):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=ROOT, **kwargs)
    if res.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(res.returncode)

def main():
    py = sys.executable
    run(f"{py} scripts/generate_dataset.py")
    run(f"{py} scripts/create_heldout.py --input data/curated_train.jsonl --out data/heldout_test.jsonl --n 20")
    run(f"{py} scripts/populate_responses.py --input data/heldout_test.jsonl --out eval/base_responses.txt")
    run(f"{py} scripts/eval_score.py --ground_truth data/heldout_test.jsonl --responses eval/base_responses.txt --out eval/baseline_scores.csv")
    print("Pipeline completed. See eval/baseline_scores.csv")

if __name__ == '__main__':
    main()
