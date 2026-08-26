Training Configuration and Justification

Dataset: data/curated_train.jsonl (50 invoices, 30 purchase orders)
Fine-tuning method: LoRA (parameter-efficient, reduces GPU/CPU memory needs)

LoRA settings (recommended):
- Rank (r): 16 — tradeoff between expressive capacity and overfitting risk on a small dataset. Rank=8 may underfit JSON formatting behaviors; 32 increases overfit risk.
- Alpha: 32 — standard practice is alpha ≈ 2× rank; scales adapter outputs.
- Learning rate: 2e-4 — mid-range learning rate for LoRA on instructive format tasks; not too high to destabilize adapters, not too low to stall learning.
- Epochs: 3 — balances learning JSON-format behavior while limiting overfitting on 80 examples.
- Batch size: choose the largest batch size that fits in your machine's RAM/VRAM. On CPU-only or limited GPU, use batch_size=4 or use gradient accumulation to simulate larger batches.
- Weight decay: 0.0 — for LoRA adapters, weight decay is typically small or zero.
- Optimizer: AdamW or AdaFactor where supported.

Rationale summary:
- Dataset is small but diverse; the objective is format consistency rather than high semantic generalisation, so LoRA with moderate rank (16) enables learning the JSON pattern without modifying base weights excessively.
- Alpha at 2× rank scales gradients to stabilize training; LR at 2e-4 is a common starting point for LoRA on instruction-like tasks.
- 3 epochs should be enough to learn formatting patterns; monitor the loss curve to avoid an early drop indicative of overfitting.

Before training checklist:
- Verify every line in `data/curated_train.jsonl` parses as JSON and that each example's `output` field is itself a valid JSON string (or object) matching your schema.
- Ensure screenshots/ folder exists to save config and loss images.

Files to capture during the run:
- screenshots/training_config.png — capture the entire fine-tune panel before starting training.
- screenshots/loss_curve.png — capture the final loss curve after training completes.

Notes about LlamaFactory UI steps (brief):
1. Launch `llamafactory-cli webui` and open the Fine-Tune tab.
2. Upload `data/curated_train.jsonl` as the dataset.
3. Set method to LoRA and enter the parameters above; justify them in this file before training.
4. Click Train and monitor the curve.

If you have multiple runs (hyperparameter sweep), document each run in this file with its parameters and attach its loss curve and any changes to the dataset.