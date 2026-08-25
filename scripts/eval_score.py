"""Evaluation helper: given a responses file and a ground-truth mapping, compute parse success rate and CSV rows.

Usage:
python scripts/eval_score.py --ground_truth ground_truth.jsonl --responses responses.txt --out eval/baseline_scores.csv

This script expects the responses file to contain one response per line aligned to ground-truth lines.
"""
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ground_truth", required=True)
parser.add_argument("--responses", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

with open(args.ground_truth, encoding="utf-8") as f:
    gt = [json.loads(l) for l in f]
with open(args.responses, encoding="utf-8") as f:
    responses = [line.rstrip("\n") for line in f]

rows = []
valid_count = 0
for i,(g,r) in enumerate(zip(gt,responses)):
    filename = g.get("id", f"doc_{i+1}")
    raw50 = r[:50].replace('\n',' ')
    is_valid = True
    has_all = False
    key_acc = 0.0
    val_acc = 0.0
    try:
        parsed = json.loads(r)
    except Exception:
        is_valid = False
        parsed = None
    if is_valid:
        # assume ground-truth output is in g['output'] as JSON string
        try:
            truth = json.loads(g['output']) if isinstance(g.get('output'), str) else g.get('output')
            required_keys = truth.keys()
            present_keys = parsed.keys() if isinstance(parsed, dict) else []
            has_all = all(k in present_keys for k in required_keys)
            key_acc = sum(1 for k in required_keys if k in present_keys)/len(required_keys)
            # value accuracy: simple equality check on present keys
            matches = 0
            total = 0
            for k in required_keys:
                if k in present_keys:
                    total += 1
                    if parsed[k] == truth[k]:
                        matches += 1
            val_acc = matches/total if total>0 else 0.0
        except Exception:
            has_all = False
    if is_valid and has_all:
        valid_count += 1
    rows.append({
        'filename': filename,
        'raw_output_first_50_chars': raw50,
        'is_valid_json': is_valid,
        'has_all_required_keys': has_all,
        'key_accuracy': round(key_acc,3),
        'value_accuracy': round(val_acc,3),
        'notes': ''
    })

with open(args.out, 'w', encoding='utf-8') as f:
    f.write('filename,raw_output_first_50_chars,is_valid_json,has_all_required_keys,key_accuracy,value_accuracy,notes\n')
    for r in rows:
        f.write(f"{r['filename']},{r['raw_output_first_50_chars']},{r['is_valid_json']},{r['has_all_required_keys']},{r['key_accuracy']},{r['value_accuracy']},{r['notes']}\n")

print(f"Parse-success count: {valid_count} / {len(rows)}")
