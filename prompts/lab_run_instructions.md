Runbook: Baseline & Fine-Tuned Evaluation Prompts and Screenshot Checklist

This file contains copy-paste prompts to use in LlamaFactory or Open WebUI for baseline (base model) and fine-tuned evaluations, few-shot examples, inference settings, and an exact screenshot checklist. Use these to ensure reproducible runs and to produce the artifacts required for the deliverables.

1) Global instructions (use for all prompts)
- Temperature: `0.0`
- Top-p: `1.0`
- Max tokens: `512` (adjust if needed)
- Stop sequences: none (let model finish); prefer deterministic temperature.
- Output requirement: ALWAYS return exactly one JSON object matching the schema. No markdown, no code fences, no extra commentary. Use `null` for missing top-level fields, dates in `YYYY-MM-DD`, numbers as JSON numbers (no currency symbols).

2) Strict single-shot prompt (Invoice)

Extract all invoice fields and return ONLY a single valid JSON object exactly matching the invoice schema. Do not include any explanation, markdown, or code fences. Use `null` for missing values and dates in `YYYY-MM-DD`. Keys required (exact names): `vendor`, `invoice_number`, `date`, `due_date`, `currency`, `subtotal`, `tax`, `total`, `line_items`. Each `line_items` element must be an object with `description`, `quantity`, `unit_price`.

Document:
<paste raw invoice text here>

Return:

(Expect single JSON object only)

3) Strict single-shot prompt (Purchase Order)

Extract all purchase order fields and return ONLY a single valid JSON object exactly matching the PO schema. Do not include any explanation, markdown, or code fences. Use `null` for missing values and dates in `YYYY-MM-DD`. Keys required (exact names): `buyer`, `supplier`, `po_number`, `date`, `delivery_date`, `currency`, `total`, `items`. Each `items` element must be an object with `item_name`, `quantity`, `unit_price`.

Document:
<paste raw PO text here>

Return:

(Expect single JSON object only)

4) Few-shot prompt (Invoice) — copy-paste both examples followed by the query

Example 1 (complete):

Input:
Vendor: Acme Corp
Invoice: INV-2024-001
Date: 2024-01-15
Due: 2024-02-14
Currency: USD
Items:
 - Widget A | Qty: 2 | Unit: 10.00
Subtotal: USD 20.00
Tax: USD 2.00
Total: USD 22.00

Output:
{"vendor": "Acme Corp", "invoice_number": "INV-2024-001", "date": "2024-01-15", "due_date": "2024-02-14", "currency": "USD", "subtotal": 20.0, "tax": 2.0, "total": 22.0, "line_items": [{"description": "Widget A", "quantity": 2, "unit_price": 10.0}]}

Example 2 (missing tax):

Input:
Vendor: Small Farm
Invoice: SF-10
Date: 2024-03-01
Items:
 - Eggs | Qty: 30 | Unit: 0.50
Subtotal: USD 15.00
Total: USD 15.00

Output:
{"vendor": "Small Farm", "invoice_number": "SF-10", "date": "2024-03-01", "due_date": null, "currency": "USD", "subtotal": 15.0, "tax": null, "total": 15.0, "line_items": [{"description": "Eggs", "quantity": 30, "unit_price": 0.5}]}

Now extract fields from the following document and return only the JSON object:

<paste raw invoice text here>

5) Few-shot prompt (Purchase Order) — two examples then query

Example 1 (complete):

Input:
Buyer: RetailCo Ltd
Supplier: Global Plastics Ltd
PO Number: PO-2024-900
Date: 2024-09-10
Delivery Date: 2024-09-20
Items:
 - Part-101 | Qty: 10 | Unit: 12.50
Total: USD 125.00

Output:
{"buyer": "RetailCo Ltd", "supplier": "Global Plastics Ltd", "po_number": "PO-2024-900", "date": "2024-09-10", "delivery_date": "2024-09-20", "currency": "USD", "total": 125.0, "items": [{"item_name": "Part-101", "quantity": 10, "unit_price": 12.5}]}

Example 2 (missing delivery_date):

Input:
Buyer: Greenfield Foods
Supplier: Sunrise Foods
PO Number: PO-2024-602
Date: 2024-04-18
Items:
 - Fresh Fruit | Qty: 200 | Unit: 0.50
Total: USD 100.00

Output:
{"buyer": "Greenfield Foods", "supplier": "Sunrise Foods", "po_number": "PO-2024-602", "date": "2024-04-18", "delivery_date": null, "currency": "USD", "total": 100.0, "items": [{"item_name": "Fresh Fruit", "quantity": 200, "unit_price": 0.5}]}

Now extract fields from the following document and return only the JSON object:

<paste raw PO text here>

6) Format-enforcement prompt (short strict form)

Return exactly one JSON object with these keys in this order: [list keys]. If you output anything else (markdown, commentary, code fences), the response will be treated as invalid. Use `null` for missing values and `YYYY-MM-DD` for dates. Example: `vendor, invoice_number, date, due_date, currency, subtotal, tax, total, line_items`.

7) Recommended inference settings (repeat)
- Temperature: `0.0` (deterministic)
- Top-p: `1.0`
- Max tokens: `512`
- Best of / n: 1
- Stop sequences: none

8) Screenshot checklist (exact filenames and what to capture)
- `screenshots/training_config.png`: Capture the full LlamaFactory Fine-Tune panel before clicking Train. Include dataset name, method (LoRA), and all hyperparameters (rank, alpha, lr, epochs, batch size).
- `screenshots/training_start.png`: Capture the screen showing training started (job list or progress indicator).
- `screenshots/loss_curve.png`: After training completes, capture the final loss curve (entire plot).
- `screenshots/model_loaded_inference.png`: Capture the inference UI with the selected model name (base or fine-tuned) and inference settings visible.
- `screenshots/base_inference_response_doc01.png` ... `screenshots/base_inference_response_doc20.png`: For each held-out document, capture the inference result screen (raw model output visible) when running the base model. Save each screenshot with the matching doc index.
- `screenshots/finetuned_inference_response_doc01.png` ... `screenshots/finetuned_inference_response_doc20.png`: Same for the fine-tuned model.
- `eval/baseline_responses.md` and `eval/finetuned_responses.md`: Copy verbatim the raw outputs from each screenshot (or the inference text box) into these files. Keep exact ordering (doc01 .. doc20).
- `eval/base_responses.txt` and `eval/finetuned_responses.txt`: Also paste each raw response as a single line aligned to `data/heldout_test.jsonl` order; these files are used by `scripts/eval_score.py`.

9) Exact step-by-step checklist (baseline)
1. Open LlamaFactory/Open WebUI, select `Llama-3.2-3B-Instruct` (or the base model you want to test). Set inference parameters to the recommended values.
2. Load the held-out document (first entry from `data/heldout_test.jsonl`) into the inference input box.
3. Paste the appropriate prompt (invoice or PO) above the document (or use the strict single-shot prompt with the document pasted inline).
4. Run. Wait for the model output to appear. Screenshot the entire page and save to `screenshots/base_inference_response_doc01.png`.
5. Copy the raw output (exact text) into the next empty line of `eval/base_responses.txt` and also paste with header into `eval/baseline_responses.md`.
6. Repeat steps 2–5 for all 20 held-out examples.

10) Exact step-by-step checklist (fine-tuned)
1. Load your fine-tuned LoRA model in LlamaFactory's inference tab (select checkpoint or adapter config). Confirm model name is visible; screenshot as `screenshots/model_loaded_inference.png`.
2. Repeat the same 20 document runs using the exact same prompts and inference settings.
3. For each run save screenshots to `screenshots/finetuned_inference_response_docXX.png` and copy verbatim outputs into `eval/finetuned_responses.txt` and `eval/finetuned_responses.md` aligned with their doc index.

11) After collecting responses — scoring
- Ensure `eval/base_responses.txt` and `eval/finetuned_responses.txt` each contain exactly 20 lines aligned to `data/heldout_test.jsonl`.
- Run the evaluation helper to compute CSVs:

```powershell
python scripts/eval_score.py --ground_truth data/heldout_test.jsonl --responses eval/base_responses.txt --out eval/baseline_scores.csv
python scripts/eval_score.py --ground_truth data/heldout_test.jsonl --responses eval/finetuned_responses.txt --out eval/finetuned_scores.csv
```

- Update `eval/summary.md` with the baseline parse success rate and the post-fine-tuning parse success rate computed from the CSV files.
- Populate `eval/before_vs_after.md` with the aggregate numbers.

12) Notes & common failure modes to watch for during runs
- If outputs are wrapped in markdown fences (```json), paste the inner JSON only for the CSV generation OR prefer to re-run with stricter prompt enforcing "no markdown".
- If the model returns additional keys, record this as a wrong-schema-key error in your notes and in `eval/baseline_scores.csv` notes column.
- If dates are not in YYYY-MM-DD, count as a value_accuracy penalty.

13) If you want, I can:
- Generate a one-click clipboard-ready prompt file containing the exact prompt for each held-out doc (I can produce that now). 
- Or produce a PowerShell script to automate opening the heldout docs and saving prompts/responses locally (browser automation would be required for screenshots).


End of runbook.