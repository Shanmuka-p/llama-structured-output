Purchase Order (PO) JSON Schema

Required keys (every PO object must include all keys; absent/unknown fields use null):

- buyer (string): The purchasing organisation name exactly as shown on the document. If absent or illegible, set to null.
- supplier (string): The supplier or vendor name. If absent, set to null.
- po_number (string): The purchase order identifier (e.g., "PO-2024-102"). If absent, set to null.
- date (string, YYYY-MM-DD): The PO issue date in ISO format; if not available, use null.
- delivery_date (string, YYYY-MM-DD or null): Expected delivery date; if unspecified, use null.
- currency (string, 3-letter ISO): Three-letter currency code (e.g., "GBP"). If not present, use null.
- total (number): Numeric total amount for the PO. If absent, set to null.
- items (array of objects): Array of ordered items; must be present (may be empty). Each item object must have:
  - item_name (string): Name or short description of the item; if missing, use an empty string.
  - quantity (integer): Quantity ordered; default to 1 if not specified.
  - unit_price (number): Unit price as a number; if not present, set to null.

Formatting notes and missing values:
- Dates must follow YYYY-MM-DD exactly. If a full date cannot be determined, use null.
- Numeric fields must be JSON numbers without currency symbols or thousands separators.
- For absent string values across top-level keys, use null consistently rather than empty strings (except `item_name` which may be empty string).
- Every example must include all top-level keys to ensure consistent schema learning during training.

Example valid PO JSON object:

{
  "buyer": "Acme Manufacturing",
  "supplier": "Global Plastics Ltd",
  "po_number": "PO-2024-778",
  "date": "2024-05-01",
  "delivery_date": null,
  "currency": "USD",
  "total": 5280.00,
  "items": [
    {"item_name": "Molding resin A", "quantity": 40, "unit_price": 120.00}
  ]
}