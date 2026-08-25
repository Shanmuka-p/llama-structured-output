"""Generate a synthetic curated_train.jsonl dataset (50 invoices, 30 purchase orders)
and a matching curation log. This script creates data/curated_train.jsonl and data/curation_log.md.

Run: python scripts/generate_dataset.py
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# templates removed; examples constructed directly as Python dicts below

vendors = ["Acme Corp","Tata Steel","Global Plastics Ltd","Sunrise Foods","Atlas Logistics","Mercury Tech","Northwind Traders","Velvet Furnishings","Oceanic Imports","BrightHealth Services"]
buyers = ["Acme Corp","RetailCo Ltd","FinTrade LLC","HealthFirst","LogiTrans","Prime Retailers","Cornerstone Inc","Devon Enterprises","Metro Supplies","Greenfield Foods"]
currencies = ["USD","EUR","GBP","INR","JPY"]

examples = []
curation_rows = []

# Helper generators
import random
from datetime import date, timedelta

def rand_date(start_year=2023, end_year=2025):
    start = date(start_year,1,1)
    delta = (date(end_year,12,31) - start).days
    d = start + timedelta(days=random.randint(0, delta))
    return d.isoformat()

# Generate 50 invoices
for i in range(1,51):
    vendor = random.choice(vendors)
    inv = f"INV-{2024}-{100+i}"
    d = rand_date()
    # randomly omit due_date or tax
    if random.random() < 0.2:
        due = None
    else:
        due = (date.fromisoformat(d) + timedelta(days=30)).isoformat()
    currency = random.choice(currencies)
    num_items = random.choice([1,1,2,3,4])
    line_items = []
    subtotal = 0.0
    for j in range(num_items):
        desc = f"Item {j+1} description"
        qty = random.choice([1,1,2,3])
        unit = round(random.uniform(10,5000),2)
        line_items.append({"description":desc,"quantity":qty,"unit_price":unit})
        subtotal += qty*unit
    # 20% missing tax
    if random.random() < 0.2:
        tax = None
    else:
        tax = round(subtotal * 0.10,2)
    total = round((subtotal + (tax or 0.0)),2)
    subtotal = round(subtotal,2)
    invoice_obj = {
        "vendor": vendor,
        "invoice_number": inv,
        "date": d,
        "due_date": due,
        "currency": currency,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "line_items": line_items
    }
    # synthetic raw text (simple)
    raw = f"Vendor: {vendor}\nInvoice: {inv}\nDate: {d}\nTotal: {currency} {total}\nItems:\n"
    for li in line_items:
        raw += f" - {li['description']} | Qty: {li['quantity']} | Unit: {li['unit_price']}\n"
    example = {
        "instruction": "Extract invoice fields as JSON. Return ONLY a valid JSON object exactly matching the invoice schema. No explanations, no markdown.",
        "input": raw,
        "output": json.dumps(invoice_obj, ensure_ascii=False)
    }
    examples.append(example)
    curation_rows.append((f"inv_{i:03d}", "invoice", "synthetic", "kept", "synthetic example, varied items, tax present/missing per rule"))

# Generate 30 purchase orders
for i in range(1,31):
    buyer = random.choice(buyers)
    supplier = random.choice(vendors)
    po = f"PO-{2024}-{200+i}"
    d = rand_date()
    if random.random() < 0.25:
        delivery = None
    else:
        delivery = (date.fromisoformat(d) + timedelta(days=random.choice([7,14,21,30]))).isoformat()
    currency = random.choice(currencies)
    num_items = random.choice([1,1,2,3,4])
    items = []
    total = 0.0
    for j in range(num_items):
        name = f"Part-{j+1}-{random.randint(100,999)}"
        qty = random.choice([1,5,10,2,3])
        unit = round(random.uniform(5,2000),2)
        items.append({"item_name":name,"quantity":qty,"unit_price":unit})
        total += qty*unit
    total = round(total,2)
    po_obj = {
        "buyer": buyer,
        "supplier": supplier,
        "po_number": po,
        "date": d,
        "delivery_date": delivery,
        "currency": currency,
        "total": total,
        "items": items
    }
    raw = f"Buyer: {buyer}\nSupplier: {supplier}\nPO: {po}\nDate: {d}\nTotal: {currency} {total}\nItems:\n"
    for it in items:
        raw += f" - {it['item_name']} | Qty: {it['quantity']} | Unit: {it['unit_price']}\n"
    example = {
        "instruction": "Extract purchase order fields as JSON. Return ONLY a valid JSON object exactly matching the PO schema. No explanations, no markdown.",
        "input": raw,
        "output": json.dumps(po_obj, ensure_ascii=False)
    }
    examples.append(example)
    curation_rows.append((f"po_{i:03d}", "purchase_order", "synthetic", "kept", "synthetic example, varied items, delivery present/missing per rule"))

# Write JSONL
out_file = OUT_DIR / "curated_train.jsonl"
with out_file.open("w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

# Write curation log (simple table)
log_file = OUT_DIR / "curation_log.md"
with log_file.open("w", encoding="utf-8") as f:
    f.write("# Curation Log\n\n")
    f.write("example_id | document_type | source | kept_or_rejected | reason\n")
    f.write("--- | --- | --- | --- | ---\n")
    for row in curation_rows:
        f.write(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n")

print(f"Wrote {len(examples)} examples to {out_file}")
print(f"Wrote curation log to {log_file}")
