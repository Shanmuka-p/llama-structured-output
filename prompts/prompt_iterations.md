Prompt iterations for base model

Version 1 (strict single-shot):

"Extract all invoice fields and return ONLY a valid JSON object exactly matching the invoice schema. Do not include any explanation, markdown, or code fences. Use null for missing values."

Version 2 (few-shot example + constraint):

Provide two few-shot examples (one full invoice, one with missing tax) demonstrating exact JSON output, then the instruction: "Now extract the fields from the following document and return only the JSON object matching the schema."

Version 3 (explicit format enforcement):

"Return exactly one JSON object. If you add any text other than the JSON, your output will be discarded. Keys must be: vendor, invoice_number, date, due_date, currency, subtotal, tax, total, line_items."

Include equivalent variations for purchase orders (replace schema and keys accordingly).