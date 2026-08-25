Invoice JSON Schema

Required keys (every invoice object must include all keys; absent/unknown fields use null):

- vendor (string): The vendor or supplier name exactly as it appears on the document (e.g., "Acme Corp"). If the vendor is not legible or absent, set to null.
- invoice_number (string): The invoice identifier present on the invoice (e.g., "INV-2024-001"). If absent, set to null.
- date (string, YYYY-MM-DD): The invoice issue date in ISO format. If a full date is not present, set to null.
- due_date (string, YYYY-MM-DD or null): The payment due date in ISO format; if absent, use null.
- currency (string, 3-letter ISO): The three-letter currency code (e.g., "USD", "EUR"). If not indicated, use null.
- subtotal (number): Numeric subtotal amount before tax and discounts. If not present, use null.
- tax (number or null): Numeric tax amount. If no tax is shown, set to null.
- total (number): Numeric total amount due. If not present, use null.
- line_items (array of objects): Array of line item objects; an empty array is allowed but must be present. Each line item object must have:
  - description (string): Description of the item/service. If missing, use an empty string.
  - quantity (integer): Quantity purchased; if quantity is not stated, use 1.
  - unit_price (number): Unit price as a number; if not stated, set to null.

Notes on formatting and missing values:
- Dates must follow the exact format YYYY-MM-DD. If the source document shows only a month or ambiguous date, convert to null rather than guessing.
- Numeric values must be JSON numbers (no currency symbols or commas). Use decimal form for floats (e.g., 142500.00).
- For string fields that are absent or illegible, use null, except `description` which may be an empty string and `quantity` which defaults to 1 when unspecified.
- Keys must appear in the exact order shown above when serialized by humans (ordering is not required by JSON but keep consistent in examples). Every example in the training dataset must include every top-level key exactly (no keys omitted).

Example valid invoice JSON object:

{
  "vendor": "Tata Steel",
  "invoice_number": "INV-2024-031",
  "date": "2024-03-15",
  "due_date": null,
  "currency": "INR",
  "subtotal": 135000.00,
  "tax": 7500.00,
  "total": 142500.00,
  "line_items": [
    {"description": "Steel sheets 2mm", "quantity": 10, "unit_price": 13500.00}
  ]
}