from llm_agent.llm_interface import classify_invoice

invoice_text = """Invoice #: 12983
Vendor: Bob’s Plumbing
Date: 05/06/2025
Amount: $435.00
Service Address: 120 Main St, Boston, MA"""

known_llcs = [
    "Main Street Holdings LLC",
    "Grove Apartments LLC"
]

result = classify_invoice(invoice_text, known_llcs)
print(result)
